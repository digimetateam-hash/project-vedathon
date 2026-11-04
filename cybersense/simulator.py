"""
CPT-IoT telemetry simulator for the CyberSense x Black Door testbed.

This module does NOT perform any real exploitation. It emits *labelled
telemetry* — a stream of normalized events representing what each layer
(browser, API, MQTT, syslog, actuator) would log during benign operation
and during the six controlled scenarios A-F. Each event carries a ground
truth stage label STAGE_0..STAGE_5 so detectors can be scored.

Event schema (GAP #4, #5): e = (t, layer, actor, session, action, evidence, stage)
  t        float   synchronized timestamp (seconds), with bounded clock skew
  layer    str     one of: browser, api, mqtt, syslog, sensor
  actor    str     source identity (client ip / service)
  session  str     identity token carried across HTTP and MQTT, or None
  action   str     short action verb
  evidence dict    raw fields (confidence, dst, topic, state, ...)
  stage    int     0..5 ground-truth transition stage of the attack
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field, asdict
from typing import Optional

# Transition stages (GAP #2, #15): the ordered cyber-to-physical progression.
STAGE_BENIGN = 0        # normal traffic
STAGE_HOOK = 1          # browser hooked (read local context)
STAGE_SESSION = 2       # session token hijacked (act as victim)
STAGE_GATEWAY = 3       # internal API reached via gateway
STAGE_COMMAND = 4       # MQTT command capability (publish to command topic)
STAGE_IMPACT = 5        # actuator state changed (physical impact)

STAGE_NAMES = {
    0: "STAGE_0", 1: "STAGE_1", 2: "STAGE_2",
    3: "STAGE_3", 4: "STAGE_4", 5: "STAGE_5",
}

# Network topology mirrored from the repo (demo/index.html, docs).
CLIENT_IP = "172.28.0.2"
GATEWAY_IP = "172.28.0.3"
BROKER_IP = "172.28.0.4"
CMD_TOPIC = "home/security/door"


@dataclass
class Event:
    t: float
    layer: str
    actor: str
    session: Optional[str]
    action: str
    evidence: dict = field(default_factory=dict)
    stage: int = 0

    def as_dict(self):
        return asdict(self)


class ScenarioSimulator:
    """Generates one labelled telemetry trace for a given scenario."""

    def __init__(self, rng: random.Random, clock_skew_ms: float = 40.0):
        self.rng = rng
        # Max absolute per-component clock skew; correlation must tolerate it.
        self.clock_skew_ms = clock_skew_ms

    # --- helpers ----------------------------------------------------------
    def _skew(self) -> float:
        return self.rng.uniform(-self.clock_skew_ms, self.clock_skew_ms) / 1000.0

    def _jit(self, base: float, frac: float = 0.25) -> float:
        """Positive timing jitter around a nominal inter-stage delay."""
        return max(0.05, self.rng.gauss(base, base * frac))

    def _benign_background(self, start: float, dur: float, actors) -> list[Event]:
        """Benign web browsing + periodic sensor telemetry (Scenario A texture).

        Some benign events deliberately *look* suspicious (a benign fetch to
        the gateway, a benign MQTT read) so detectors can incur false
        positives — otherwise precision would be trivially 1.0.
        """
        evs: list[Event] = []
        t = start
        while t < start + dur:
            t += self.rng.expovariate(1.5)  # ~1.5 events/sec
            if t >= start + dur:
                break
            actor = self.rng.choice(actors)
            r = self.rng.random()
            if r < 0.55:
                evs.append(Event(t + self._skew(), "api", actor, None,
                                 "GET", {"uri": "/portal", "confidence": 0.02}, 0))
            elif r < 0.75:
                evs.append(Event(t + self._skew(), "sensor", "temp-01", None,
                                 "reading", {"state": "closed", "confidence": 0.0}, 0))
            elif r < 0.90:
                # benign browser telemetry (no hook payload)
                evs.append(Event(t + self._skew(), "browser", actor, None,
                                 "dom_load", {"confidence": 0.05}, 0))
            elif r < 0.94:
                # benign fetch that happens to hit the gateway subnet
                evs.append(Event(t + self._skew(), "api", actor, None,
                                 "GET", {"uri": "/status", "dst": GATEWAY_IP,
                                         "confidence": 0.18}, 0))
            elif r < 0.97:
                # benign periodic MQTT telemetry read (not a command)
                evs.append(Event(t + self._skew(), "mqtt", "dashboard", None,
                                 "subscribe", {"topic": "home/telemetry",
                                               "confidence": 0.12}, 0))
            else:
                # Confusable benign event: a legitimate admin action that, to a
                # single-layer or capability-blind detector, looks like an
                # attack capability. It carries a benign session with NO prior
                # chain, so a capability-aware + identity engine rejects it,
                # while blind detectors raise a false positive.
                benign_sess = f"#S{self.rng.randint(10,99)}-{self.rng.randint(1000,9999)}"
                choice = self.rng.random()
                if choice < 0.5:
                    evs.append(Event(t + self._skew(), "api", actor, benign_sess,
                                     "POST", {"uri": "/api/lock", "dst": GATEWAY_IP,
                                              "confidence": 0.58,
                                              "capability": "access_internal_api"}, 0))
                else:
                    evs.append(Event(t + self._skew(), "mqtt", "dashboard", benign_sess,
                                     "publish", {"topic": "home/config",
                                                 "confidence": 0.57,
                                                 "capability": "publish_command"}, 0))
        return evs

    def _attack_stage(self, t: float, stage: int, session: str) -> list[Event]:
        """Emit the observable evidence produced when the attack reaches `stage`."""
        s = self._skew()
        if stage == STAGE_HOOK:
            return [Event(t + s, "browser", CLIENT_IP, session, "hook",
                          {"payload": "hook.js", "confidence": 0.86,
                           "capability": "read_local_context"}, STAGE_HOOK)]
        if stage == STAGE_SESSION:
            return [Event(t + s, "syslog", CLIENT_IP, session, "token_reuse",
                          {"confidence": 0.74, "capability": "act_as_session"}, STAGE_SESSION)]
        if stage == STAGE_GATEWAY:
            return [Event(t + s, "api", CLIENT_IP, session, "POST",
                          {"uri": "/api/lock", "dst": GATEWAY_IP, "confidence": 0.69,
                           "capability": "access_internal_api"}, STAGE_GATEWAY)]
        if stage == STAGE_COMMAND:
            return [Event(t + s, "mqtt", GATEWAY_IP, session, "publish",
                          {"topic": CMD_TOPIC, "confidence": 0.81,
                           "capability": "publish_command"}, STAGE_COMMAND)]
        if stage == STAGE_IMPACT:
            return [Event(t + s, "sensor", BROKER_IP, session, "state_change",
                          {"state": "open", "confidence": 0.99,
                           "capability": "physical_impact"}, STAGE_IMPACT)]
        return []

    # --- public API -------------------------------------------------------
    def run(self, scenario: str) -> dict:
        """Return {'events': [...], 'highest_stage': int, 't_impact': float|None,
        'stage_times': {stage: t}, 'scenario': str}.
        """
        actors = [f"172.28.0.{i}" for i in range(20, 30)]
        warmup = self.rng.uniform(4.0, 8.0)
        events = self._benign_background(0.0, warmup, actors)
        session = f"#A{self.rng.randint(10,99)}-{self.rng.randint(1000,9999)}"

        # Map scenario letter -> highest stage actually reached.
        highest = {
            "A": STAGE_BENIGN, "B": STAGE_HOOK, "C": STAGE_GATEWAY,
            "D": STAGE_COMMAND, "E": STAGE_IMPACT, "F": STAGE_IMPACT,
        }[scenario]

        # Scenario C reaches the gateway via discovery but through a hijacked
        # session, so it still traverses hook->session->gateway.
        chain = [STAGE_HOOK, STAGE_SESSION, STAGE_GATEWAY, STAGE_COMMAND, STAGE_IMPACT]
        # nominal inter-stage delays (s), loosely following the demo edges
        delays = {STAGE_HOOK: 2.1, STAGE_SESSION: 1.4, STAGE_GATEWAY: 3.2,
                  STAGE_COMMAND: 1.1, STAGE_IMPACT: 1.6}

        stage_times: dict[int, float] = {}
        t = warmup + self.rng.uniform(0.5, 1.5)
        t_impact = None
        intervention_stage = None
        if scenario == "F":
            # Counterfactual intervention fires at the command stage (drop the
            # MQTT publish) before physical impact — the defensive case.
            intervention_stage = STAGE_COMMAND

        for st in chain:
            if st > highest:
                break
            t += self._jit(delays[st])
            # background noise continues to interleave
            events += self._benign_background(t - self._jit(delays[st]), self._jit(delays[st]), actors)
            evs = self._attack_stage(t, st, session)
            stage_times[st] = t
            if st == STAGE_IMPACT:
                if intervention_stage is not None:
                    # intervention already broke the chain; impact never happens
                    break
                t_impact = t
            # In scenario F, stop emitting the attack chain after the command
            # stage: the publish is dropped, so no impact event is produced.
            if intervention_stage is not None and st == intervention_stage:
                events += evs  # the command attempt is still observed...
                # ...but it is the last attack event; chain severed here.
                stage_times.pop(STAGE_IMPACT, None)
                break
            events += evs

        # tail of benign traffic
        events += self._benign_background(t + 0.5, self.rng.uniform(3.0, 6.0), actors)
        events.sort(key=lambda e: e.t)
        return {
            "scenario": scenario,
            "events": events,
            "highest_stage": highest if scenario != "F" else STAGE_COMMAND,
            "t_impact": t_impact,
            "stage_times": stage_times,
            "intervention_stage": intervention_stage,
            "session": session,
        }
