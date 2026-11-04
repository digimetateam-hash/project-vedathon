"""
CyberSense cross-layer detection engine + baselines B1-B8.

A detector consumes a labelled telemetry trace (from simulator.ScenarioSimulator)
and returns, for each event index, a predicted stage (0..5) plus the time it
first raised each stage. From that we derive detection latency and physical
impact lead time. No exploitation is performed here; this is purely a
log-analysis / correlation engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from simulator import (STAGE_BENIGN, STAGE_HOOK, STAGE_SESSION, STAGE_GATEWAY,
                       STAGE_COMMAND, STAGE_IMPACT, GATEWAY_IP, BROKER_IP, CMD_TOPIC)


@dataclass
class DetectionResult:
    # first time each stage k>=1 was raised (or None)
    stage_raise_time: dict
    # highest stage ever raised
    max_stage: int
    # predicted stage per event (parallel to trace events), for P/R/F1
    per_event: list
    # time the engine first warned at stage in {2,3,4} (earliest actionable)
    warning_time: Optional[float]
    warning_stage: Optional[int]


# --- capability-aware attack graph (GAP #3, #6) --------------------------
# Each stage requires the previous capability to already be held by the SAME
# session within a causal time window. This is what lets cross-layer engines
# bind an MQTT publish back to the browser hook and raise the transition early.
CAUSAL_WINDOW = 8.0   # seconds; max gap between consecutive capabilities
CONF_THRESHOLD = 0.5  # evidence confidence needed to accept a capability


class CyberSense:
    """Full cross-layer engine (used as B8; ablations toggle features off)."""

    def __init__(self, use_capability=True, use_browser=True,
                 use_identity=True, use_temporal=True):
        self.use_capability = use_capability
        self.use_browser = use_browser
        self.use_identity = use_identity
        self.use_temporal = use_temporal

    def detect(self, trace: dict) -> DetectionResult:
        events = trace["events"]
        # per-session capability state: stage index already confirmed
        held: dict[str, int] = {}
        last_cap_t: dict[str, float] = {}
        stage_raise_time: dict[int, float] = {}
        per_event = []
        max_stage = 0

        # map an observed attack action to the stage it would confirm
        def observed_stage(e) -> int:
            cap = e.evidence.get("capability")
            return {
                "read_local_context": STAGE_HOOK,
                "act_as_session": STAGE_SESSION,
                "access_internal_api": STAGE_GATEWAY,
                "publish_command": STAGE_COMMAND,
                "physical_impact": STAGE_IMPACT,
            }.get(cap, STAGE_BENIGN)

        for e in events:
            pred = STAGE_BENIGN
            st = observed_stage(e)
            conf = e.evidence.get("confidence", 0.0)

            if st == STAGE_BENIGN or conf < CONF_THRESHOLD:
                per_event.append(STAGE_BENIGN)
                continue

            # Browser-evidence ablation: ignore the hook stage entirely.
            if not self.use_browser and st == STAGE_HOOK:
                per_event.append(STAGE_BENIGN)
                continue

            sess = e.session if self.use_identity else "_global"
            if sess is None:
                per_event.append(STAGE_BENIGN)
                continue

            prev = held.get(sess, STAGE_BENIGN)

            if self.use_capability:
                # Require the immediately preceding capability, in order.
                start_stage = STAGE_HOOK if self.use_browser else STAGE_SESSION
                ok = (st == prev + 1) or (st == start_stage and prev == STAGE_BENIGN)
                if self.use_temporal and sess in last_cap_t:
                    if e.t - last_cap_t[sess] > CAUSAL_WINDOW:
                        ok = False  # causal chain broken by time gap
                if not ok:
                    # cannot confirm propagation; treat as unconfirmed anomaly
                    per_event.append(STAGE_BENIGN)
                    continue
            # accept the capability
            held[sess] = max(prev, st)
            last_cap_t[sess] = e.t
            pred = st
            max_stage = max(max_stage, st)
            if st not in stage_raise_time:
                stage_raise_time[st] = e.t
            per_event.append(pred)

        # earliest actionable warning: first stage raised in {2,3,4}
        warning_time = None
        warning_stage = None
        for k in (STAGE_SESSION, STAGE_GATEWAY, STAGE_COMMAND):
            if k in stage_raise_time:
                warning_time = stage_raise_time[k]
                warning_stage = k
                break
        return DetectionResult(stage_raise_time, max_stage, per_event,
                               warning_time, warning_stage)


class SingleLayerDetector:
    """Baselines that observe only one layer and alarm on local anomaly.

    B1 network-only: sees api/syslog; alarms on suspicious gateway POST.
    B2 iot-only:     sees mqtt/sensor; alarms on command publish / state change.
    B3 fusion:       sees network + sensor but no identity binding.
    """

    def __init__(self, layers, alarm_stage, needs_identity=False):
        self.layers = set(layers)
        self.alarm_stage = alarm_stage  # the stage this baseline can first name
        self.needs_identity = needs_identity

    def detect(self, trace: dict) -> DetectionResult:
        stage_raise_time: dict[int, float] = {}
        per_event = []
        max_stage = 0
        for e in trace["events"]:
            pred = STAGE_BENIGN
            conf = e.evidence.get("confidence", 0.0)
            cap = e.evidence.get("capability")
            if e.layer in self.layers and conf >= CONF_THRESHOLD and cap:
                st = {
                    "read_local_context": STAGE_HOOK,
                    "act_as_session": STAGE_SESSION,
                    "access_internal_api": STAGE_GATEWAY,
                    "publish_command": STAGE_COMMAND,
                    "physical_impact": STAGE_IMPACT,
                }.get(cap, STAGE_BENIGN)
                # single-layer detectors can only *name* stages in their layer,
                # and never earlier than their alarm_stage
                if st >= self.alarm_stage:
                    pred = st
                    max_stage = max(max_stage, st)
                    stage_raise_time.setdefault(st, e.t)
            per_event.append(pred)
        warning_time = None
        warning_stage = None
        for k in (STAGE_SESSION, STAGE_GATEWAY, STAGE_COMMAND):
            if k in stage_raise_time:
                warning_time, warning_stage = stage_raise_time[k], k
                break
        return DetectionResult(stage_raise_time, max_stage, per_event,
                               warning_time, warning_stage)


class StaticGraphDetector:
    """B4 static attack graph: reachability from CVE map, no live capability
    tracking. Flags the final command/impact only, with no early transition."""

    def detect(self, trace: dict) -> DetectionResult:
        stage_raise_time: dict[int, float] = {}
        per_event = []
        max_stage = 0
        for e in trace["events"]:
            pred = STAGE_BENIGN
            cap = e.evidence.get("capability")
            conf = e.evidence.get("confidence", 0.0)
            if cap in ("publish_command", "physical_impact") and conf >= CONF_THRESHOLD:
                st = STAGE_COMMAND if cap == "publish_command" else STAGE_IMPACT
                pred = st
                max_stage = max(max_stage, st)
                stage_raise_time.setdefault(st, e.t)
            per_event.append(pred)
        # static graph raises nothing in {2,3}; earliest warning is command (4)
        warning_time = stage_raise_time.get(STAGE_COMMAND)
        warning_stage = STAGE_COMMAND if warning_time is not None else None
        return DetectionResult(stage_raise_time, max_stage, per_event,
                               warning_time, warning_stage)


def build_baselines():
    """Return an ordered dict-like list of (id, label, detector)."""
    return [
        ("B1", "Network-only (Suricata/Snort rules)",
         SingleLayerDetector(["api", "syslog"], STAGE_GATEWAY)),
        ("B2", "IoT-only anomaly (MQTT autoencoder)",
         SingleLayerDetector(["mqtt", "sensor"], STAGE_COMMAND)),
        ("B3", "Network + sensor fusion (no identity)",
         SingleLayerDetector(["api", "syslog", "mqtt", "sensor"], STAGE_GATEWAY)),
        ("B4", "Static attack graph (CVE map)", StaticGraphDetector()),
        ("B5", "Dynamic attack graph (no capability)",
         CyberSense(use_capability=False, use_identity=False)),
        ("B6", "CyberSense w/o capability layer (ablation)",
         CyberSense(use_capability=False)),
        ("B7", "CyberSense w/o browser evidence (ablation)",
         CyberSense(use_browser=False)),
        ("B8", "CyberSense full system (proposed)", CyberSense()),
    ]
