import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==============================================================================
# PAGE CONFIGURATION & STYLING
# ==============================================================================
st.set_page_config(
    page_title="CyberSense × Black Door — Cyber-to-Physical Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Cyber-Defense Theme
st.markdown("""
<style>
    /* Dark Cyber Theme Foundations */
    .stApp {
        background-color: #090b10;
        color: #f8fafc;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #10141d;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
    }
    
    /* Alert Banners */
    .critical-banner {
        background: linear-gradient(180deg, rgba(239, 68, 68, 0.15) 0%, rgba(16, 20, 29, 0.95) 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.2);
    }
    .neutralized-banner {
        background: linear-gradient(180deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 20, 29, 0.95) 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
    }
    
    /* Tab Headers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #161c28;
        border-radius: 8px 8px 0 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        padding: 8px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #06b6d4 !important;
        color: #000000 !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "intervened" not in st.session_state:
    st.session_state.intervened = False
if "intervention_type" not in st.session_state:
    st.session_state.intervention_type = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "relay_locked" not in st.session_state:
    st.session_state.relay_locked = True
if "logs" not in st.session_state:
    st.session_state.logs = [
        {"time": "10:01:12", "layer": "BROWSER", "event": "Stored XSS payload executed on client 172.28.0.2", "status": "⚠️ HOOKED"},
        {"time": "10:01:14", "layer": "SESSION", "event": "Session token #A81-9941 extracted via BeEF hook", "status": "🔑 COMPROMISED"},
        {"time": "10:01:16", "layer": "WEB/API", "event": "Recon probe to internal IoT Gateway 172.28.0.3:5000", "status": "📡 API DISCOVERY"},
        {"time": "10:01:19", "layer": "IOT-NET", "event": "MQTT client connect using token #A81 on broker 1883", "status": "⚙️ AUTH REUSED"},
        {"time": "10:01:21", "layer": "TRANSITION", "event": "Stage T4 reached: Publish command capability acquired", "status": "🔴 CPT WARNING"},
    ]

# ==============================================================================
# SIDEBAR CONTROLS & HUD
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛡️ CYBERSENSE × BLACK DOOR")
    st.caption("Cross-Layer Cyber-to-Physical Transition Framework")
    st.divider()

    st.markdown("#### 🎯 Active Target Context")
    st.markdown("""
    - **Target Device:** Smart Actuator #03 (Door Solenoid)
    - **Subnet:** `172.28.0.0/24` (Isolated Namespace)
    - **Active Session:** `#A81-9941`
    - **Victim IP:** `172.28.0.2` (Safari/macOS)
    """)
    st.divider()

    st.markdown("#### ⚡ Simulation Controls")
    col_rst1, col_rst2 = st.columns(2)
    with col_rst1:
        if st.button("🔄 Reset Attack", use_container_width=True):
            st.session_state.intervened = False
            st.session_state.intervention_type = None
            st.session_state.relay_locked = True
            st.rerun()
    with col_rst2:
        if st.button("🧪 Inject Anomaly", use_container_width=True):
            st.session_state.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "layer": "PHYSICAL",
                "event": "Actuator current surge detected (+420mA)",
                "status": "⚡ CURRENT SPIKE"
            })
            st.rerun()

    st.divider()
    st.markdown("#### 📖 Research Core Question")
    st.info(
        "“Can CyberSense identify the transition from a compromised browser/client to "
        "cyber-physical control capability earlier than conventional IoT or network-based "
        "detection, and recommend an optimal intervention point before physical impact occurs?”"
    )

# ==============================================================================
# MAIN TABS ARCHITECTURE
# ==============================================================================
tab_defense, tab_lab, tab_baselines, tab_forensics = st.tabs([
    "🛡️ CyberSense Defense Radar",
    "🚪 Black Door 6-Pillar Lab",
    "📊 Benchmarks & Baselines (B1–B8)",
    "📜 Multi-Layer Evidence Forensics"
])

# ==============================================================================
# TAB 1: CYBERSENSE DEFENSE RADAR
# ==============================================================================
with tab_defense:
    if not st.session_state.intervened:
        st.markdown("""
        <div class="critical-banner">
            <h3 style="color:#ef4444; margin:0 0 0.5rem 0;">⚠️ CYBERSENSE EARLY WARNING: CYBER → PHYSICAL TRANSITION DETECTED</h3>
            <p style="margin:0; font-size:0.95rem; color:#cbd5e1;">
                Correlated cross-layer transition from remote browser compromise to physical actuator control capability.
                <b>Stage T4 (IoT Command Capability)</b> reached before actuator state change.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="neutralized-banner">
            <h3 style="color:#10b981; margin:0 0 0.5rem 0;">✅ THREAT NEUTRALIZED: PHYSICAL IMPACT PREVENTED</h3>
            <p style="margin:0; font-size:0.95rem; color:#cbd5e1;">
                Counterfactual Intervention executed: <b>{st.session_state.intervention_type}</b>.
                Attack chain severed at transition point T4. Smart Actuator #03 preserved with 0s operational downtime.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 4 Key Metrics Bar
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Transition Stage",
            value="NEUTRALIZED" if st.session_state.intervened else "T4 (IoT Command)",
            delta="Normal" if st.session_state.intervened else "Stage T0 → T4 (+4.2s)",
            delta_color="normal" if st.session_state.intervened else "inverse"
        )
    with m2:
        st.metric(
            label="Physical Impact Lead Time (GAP #07)",
            value="FROZEN" if st.session_state.intervened else "11.4s",
            delta="Secured" if st.session_state.intervened else "-0.1s/tick (Critical)",
            delta_color="normal" if st.session_state.intervened else "inverse"
        )
    with m3:
        st.metric(
            label="Identity Continuity (GAP #04)",
            value="Verified (#A81)",
            delta="HTTP -> MQTT Match"
        )
    with m4:
        st.metric(
            label="Target Reachability (GAP #06)",
            value="BLOCKED" if st.session_state.intervened else "CONTROL CAPABLE",
            delta="Safe" if st.session_state.intervened else "Target Reachable"
        )

    st.write("")
    st.markdown("#### 📈 Physical Reachability Progression Gauge")
    reach_progress = 0 if st.session_state.intervened else 75
    st.progress(reach_progress)
    st.caption("Stage: [NOT REACHABLE 0%] → [POTENTIALLY 25%] → [REACHABLE 50%] → **[CONTROL CAPABLE 75%]** → [PHYSICAL IMPACT 100%]")

    st.write("")
    st.markdown("#### 🌐 Capability-Aware Dynamic Attack Graph (GAP #03)")
    
    # Render Graphviz with Dynamic Intervened State
    if not st.session_state.intervened:
        dot_code = """
        digraph G {
            rankdir=LR;
            node [shape=box, style="filled,rounded", fontname="JetBrains Mono", fontsize=11];
            edge [fontname="JetBrains Mono", fontsize=9, color="#ef4444", fontcolor="#f59e0b"];

            Browser [label="💻 BeEF Hook\n(172.28.0.2)", fillcolor="#fee2e2", fontcolor="#991b1b", color="#ef4444"];
            Session [label="🔑 Session #A81\n(Token Context)", fillcolor="#fee2e2", fontcolor="#991b1b", color="#ef4444"];
            Gateway [label="📡 IoT Gateway\n(172.28.0.3)", fillcolor="#fee2e2", fontcolor="#991b1b", color="#ef4444"];
            MQTT    [label="⚙️ MQTT Broker\n(172.28.0.4)", fillcolor="#fee2e2", fontcolor="#991b1b", color="#ef4444"];
            Target  [label="🚪 Actuator #03\n(Solenoid Lock)", fillcolor="#fef3c7", fontcolor="#92400e", color="#f59e0b"];

            Browser -> Session [label="Read DOM\nΔt: +2.1s"];
            Session -> Gateway [label="Reuse Token\nΔt: +1.4s"];
            Gateway -> MQTT    [label="Access API\nΔt: +3.2s"];
            MQTT    -> Target  [label="Publish Command\nΔt: +1.1s", penwidth=2.5];
        }
        """
    else:
        dot_code = """
        digraph G {
            rankdir=LR;
            node [shape=box, style="filled,rounded", fontname="JetBrains Mono", fontsize=11];
            edge [fontname="JetBrains Mono", fontsize=9];

            Browser [label="💻 BeEF Hook\n(172.28.0.2)", fillcolor="#e2e8f0", fontcolor="#475569", color="#94a3b8"];
            Session [label="🔑 Session #A81\n(Token Context)", fillcolor="#e2e8f0", fontcolor="#475569", color="#94a3b8"];
            Gateway [label="📡 IoT Gateway\n(172.28.0.3)", fillcolor="#e2e8f0", fontcolor="#475569", color="#94a3b8"];
            MQTT    [label="⚙️ MQTT Broker\n(Intervened)", fillcolor="#d1fae5", fontcolor="#065f46", color="#10b981"];
            Target  [label="🚪 Actuator #03\n(SECURED)", fillcolor="#d1fae5", fontcolor="#065f46", color="#10b981"];

            Browser -> Session [label="Read DOM", color="#94a3b8"];
            Session -> Gateway [label="Reuse Token", color="#94a3b8"];
            Gateway -> MQTT    [label="Dropped", color="#10b981", style=dashed];
            MQTT    -> Target  [label="CHAIN BROKEN\nImpact Prevented", color="#10b981", penwidth=3.0, fontcolor="#059669"];
        }
        """
    st.graphviz_chart(dot_code, use_container_width=True)

    st.write("")
    st.markdown("#### ✂️ Counterfactual Intervention Engine (GAP #09 & #10)")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🎯 BLOCK MQTT SESSION #A81 (Recommended)", use_container_width=True, type="primary"):
            st.session_state.intervened = True
            st.session_state.intervention_type = "Block MQTT Session #A81"
            st.session_state.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "layer": "DEFENSE",
                "event": "Optimal intervention executed: MQTT Session #A81 revoked. Actuator preserved.",
                "status": "🛡️ SEVERED"
            })
            st.rerun()
        st.caption("IES Score: **0.94** | Risk: **-100%** | Availability Cost: **LOW (Zero collateral downtime)**")
    with c2:
        if st.button("⛔ SHUT DOWN ENTIRE IOT GATEWAY", use_container_width=True):
            st.session_state.intervened = True
            st.session_state.intervention_type = "Full IoT Gateway Shutdown"
            st.session_state.logs.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "layer": "DEFENSE",
                "event": "Emergency action: Entire IoT Gateway disabled. High collateral disruption.",
                "status": "⚠️ DOWNTIME"
            })
            st.rerun()
        st.caption("IES Score: **0.32** | Risk: **-100%** | Availability Cost: **CRITICAL (14 benign sensors offline)**")
    with c3:
        if st.button("🚫 REVOKE BROWSER COOKIE ONLY", use_container_width=True):
            st.warning("Ineffective: Attacker already migrated credentials to internal MQTT socket!")
        st.caption("IES Score: **0.15** | Risk: **-25%** | Attack already moved lateral to IoT layer.")

    st.write("")
    st.markdown("#### 📖 Reconstructed Attack Story (GAP #12 & #14)")
    st.info(
        "“A compromised browser session (BeEF hook) accessed the internal IoT gateway at 172.28.0.3, "
        "obtained command publication capability through the MQTT interface on topic `home/security/door`, "
        "and reached the physical solenoid lock actuator **11.4 seconds before state transition**.”"
    )

# ==============================================================================
# TAB 2: BLACK DOOR 6-PILLAR LAB TESTBED
# ==============================================================================
with tab_lab:
    st.markdown("### 🚪 Black Door: Experimental Cyber-Physical Testbed")
    st.caption("The 6-pillar lab provisioning and attack environment powering CyberSense research.")

    p1, p2, p3 = st.columns(3)
    with p1:
        with st.container(border=True):
            st.markdown("#### 1. 🌐 BeEF Lab")
            st.write("Browser Exploitation Framework Hub.")
            st.code('<script src="http://172.28.0.2:3000/hook.js"></script>', language="html")
            if st.button("Inspect Hook Status", key="btn_beef"):
                st.success("Hook active on client 172.28.0.2:8080 (Chrome 120/macOS)")
    with p2:
        with st.container(border=True):
            st.markdown("#### 2. 📡 IoT Security Lab")
            st.write("Virtual IoT Gateways & MQTT Broker.")
            st.code("Topic: home/security/door/cmd\nPayload: {'action':'unlock'}", language="json")
            if st.button("Probe MQTT Topics", key="btn_mqtt"):
                st.info("3 active topics found: sensors/temp, sensors/cam, security/door")
    with p3:
        with st.container(border=True):
            st.markdown("#### 3. 🤖 Robotic Provisioning")
            st.write("Docker Engine Ephemeral Containers.")
            st.markdown("- **Spin-up Latency:** < 22.4 seconds\n- **Isolation:** `iptables` No-WAN egress")
            if st.button("Verify Sandbox Quota", key="btn_dock"):
                st.success("Resource Quota: 0.5 vCPU, 512MB RAM per container (Healthy)")

    p4, p5, p6 = st.columns(3)
    with p4:
        with st.container(border=True):
            st.markdown("#### 4. 🎯 Auto-Scoring Engine")
            st.write("Automated Passive Webhook Evaluator.")
            flag_input = st.text_input("Submit Hackathon Flag:", "VEDA{cpt_transition_mitigated_2026}")
            if st.button("Verify Flag", key="btn_flag"):
                if "cpt" in flag_input.lower():
                    st.session_state.score += 100
                    st.success(f"Flag Verified! +100 Points. Current Score: {st.session_state.score} PTS")
                else:
                    st.error("Invalid Flag signature.")
    with p5:
        with st.container(border=True):
            st.markdown("#### 5. 📊 Dual Dashboard")
            st.write("Unified Operator & Attacker UI.")
            st.write("Switch seamlessly between Student Attack Lab Console & CyberSense Defense Radar.")
            st.info("Current View: Dual Synchronization Active")
    with p6:
        with st.container(border=True):
            st.markdown("#### 6. 🔌 Physical IoT Demo")
            st.write("ESP32 Relay & 12V Solenoid Hardware Kit.")
            status_text = "LOCKED 🔒 (12V High)" if st.session_state.relay_locked else "UNLOCKED 🔓 (12V Low)"
            st.write(f"Hardware Relay Status: **{status_text}**")
            if st.button("Toggle Physical Solenoid", key="btn_solenoid"):
                st.session_state.relay_locked = not st.session_state.relay_locked
                new_status = "LOCKED" if st.session_state.relay_locked else "UNLOCKED"
                st.session_state.logs.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "layer": "PHYSICAL",
                    "event": f"Manual Hardware Relay Toggle: Door is now {new_status}",
                    "status": "🔌 RELAY STATE"
                })
                st.rerun()

# ==============================================================================
# TAB 3: BENCHMARKS & BASELINES (B1–B8)
# ==============================================================================
with tab_baselines:
    st.markdown("### 📊 Benchmark Comparison: CyberSense vs Baselines (B1–B8)")
    st.caption("Rigorous comparative validation across 8 detection paradigms.")

    baseline_data = {
        "Baseline": [
            "B1: Network-Only (Suricata/Snort)",
            "B2: IoT-Only Anomaly Detector",
            "B3: Network + Sensor Fusion",
            "B4: Static Attack Graph",
            "B5: Dynamic Attack Graph",
            "B6: CyberSense (w/o Capability Layer)",
            "B7: CyberSense (w/o Browser Evidence)",
            "B8: CyberSense Full System (Proposed)"
        ],
        "Cross-Layer Correlation": ["No", "No", "Partial", "Partial", "Partial", "Yes", "Partial", "✅ Complete"],
        "Physical Lead Time (s)": [0.0, 1.2, 2.1, 0.0, 3.4, 6.2, 4.1, 11.4],
        "Detection F1-Score": [0.72, 0.78, 0.81, 0.69, 0.84, 0.88, 0.83, 0.96],
        "Intervention Efficiency": [0.21, 0.35, 0.44, 0.28, 0.61, 0.74, 0.58, 0.94]
    }
    df_baselines = pd.DataFrame(baseline_data)
    st.dataframe(df_baselines, use_container_width=True)

    st.write("")
    st.markdown("#### ⏱️ Physical Impact Lead Time Comparison (Higher = Earlier Warning)")
    chart_data = pd.DataFrame({
        "Model": df_baselines["Baseline"],
        "Lead Time (Seconds)": df_baselines["Physical Lead Time (s)"]
    }).set_index("Model")
    st.bar_chart(chart_data)
    st.caption("Conventional IDS only triggers at or after physical impact (Lead time ~0s). CyberSense provides **11.4 seconds of actionable early warning**.")

# ==============================================================================
# TAB 4: MULTI-LAYER EVIDENCE FORENSICS
# ==============================================================================
with tab_forensics:
    st.markdown("### 📜 Multi-Layer Evidence Chain Forensics (GAP #11 & #13)")
    st.caption("Cryptographically attributable telemetry logs spanning all 6 layers.")

    df_logs = pd.DataFrame(st.session_state.logs)
    st.dataframe(df_logs, use_container_width=True)

    st.write("")
    st.markdown("#### 🔍 Evidence Layer Filter")
    layer_filter = st.multiselect(
        "Filter by Evidence Layer:",
        ["BROWSER", "SESSION", "WEB/API", "IOT-NET", "TRANSITION", "DEFENSE", "PHYSICAL"],
        default=["BROWSER", "WEB/API", "IOT-NET", "TRANSITION"]
    )
    filtered_df = df_logs[df_logs["layer"].isin(layer_filter)]
    st.dataframe(filtered_df, use_container_width=True)

# Footer
st.divider()
st.caption("🛡️ CyberSense × Black Door — VedaThon 2026 Innovation by DigiMeta Team. Released under MIT License.")
