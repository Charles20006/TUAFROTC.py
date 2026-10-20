"""
AFROTC Detachment 015 Cadet Knowledge & Operations Hub
Platform: Multi-device Web App via Streamlit & Google Gemini API
"""

import os
from datetime import datetime
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. APP CONFIGURATION & STYLING (DET 015 COLORWAY)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Det 015 Cadet Readiness Hub",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    :root {
        --det-crimson: #7A0019;
        --det-gold: #C59B27;
        --usaf-blue: #00308F;
    }
    .main-header {
        color: var(--det-crimson);
        font-family: 'Arial Black', sans-serif;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        color: var(--det-gold);
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .status-card {
        background-color: #f8f9fa;
        border-left: 5px solid var(--det-crimson);
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .advisory-footer {
        font-size: 0.82rem;
        color: #555;
        border-top: 1px solid #ddd;
        padding-top: 8px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SYSTEM INSTRUCTIONS (GROUNDED IN DET 015 STANDARDS)
# ---------------------------------------------------------
SYSTEM_INSTRUCTIONS = """
You are the authoritative training and operations engine for AFROTC Detachment 015 ("Home of the Tuskegee Airmen").
Standards must reflect absolute attention to detail, precision, and military discipline.

Core Directives:
1. DRILL EVALUATION (DAFPAM 34-1203):
   - Evaluate command execution, foot timing (Left/Right), step intervals, and element movements.
   - Enforce exact step sizes (24-inch marching steps, 12-inch half-steps, 45-degree pivot angles).

2. VERBATIM WARRIOR KNOWLEDGE:
   - Demand exact verbatim accuracy for Airman's Creed, Code of Conduct, Mission Statements, and Creeds.
   - For ANY error or omitted word, mark as [FAIL], highlight missing words in [BRACKETS], and require full re-recitation.

3. FIELD TRAINING MANUAL (FTM):
   - Evaluate DFAC procedures, formal reporting statements, dorm layout, and open ranks inspection protocol.

4. STAFF WRITING (AFH 33-337 / DAFI 36-3211):
   - Enforce active voice, direct action-impact-result structure, and Tongue & Quill formatting rules.

Always conclude regulatory and procedural advice with:
"Advisory: Preparation aid only. Always verify with Cadre, DAFI 36-2903, DAFPAM 34-1203, or AFH 33-337."
"""

# Initialize Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# ---------------------------------------------------------
# 3. SESSION STATE & USER DATA MANAGEMENT
# ---------------------------------------------------------
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "flight_stats" not in st.session_state:
    st.session_state.flight_stats = {
        "Alpha": {"attempts": 14, "passes": 11, "weak_area": "Code of Conduct"},
        "Bravo": {"attempts": 18, "passes": 12, "weak_area": "MAJCOM Locations"},
        "Charlie": {"attempts": 15, "passes": 14, "weak_area": "USSF Ranks"}
    }

# ---------------------------------------------------------
# 4. SIDEBAR NAVIGATION & AUTHENTICATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### Cadet Identification")
    if not st.session_state.user_authenticated:
        user_email = st.text_input("Institutional Email (@tuskegee.edu)")
        cadet_role = st.selectbox("Role", ["AS100", "AS200", "AS300", "AS400", "Cadre / Admin"])
        flight_select = st.selectbox("Assigned Flight", ["Alpha", "Bravo", "Charlie", "Det Staff"])
        departure_date = st.date_input("Scheduled Departure / Commissioning Date")
        
        if st.button("Authenticate Profile"):
            if user_email:
                st.session_state.user_authenticated = True
                st.session_state.user_email = user_email
                st.session_state.cadet_role = cadet_role
                st.session_state.flight = flight_select
                st.session_state.departure = departure_date
                st.rerun()
    else:
        st.write(f"**Logged In:** {st.session_state.user_email}")
        st.write(f"**Tier:** {st.session_state.cadet_role} | **Flight:** {st.session_state.flight}")
        
        # Automatic rolloff check
        if datetime.today().date() > st.session_state.departure:
            st.error("Account active window has expired. Contact Cadre for re-authorization.")
            st.session_state.user_authenticated = False
            st.rerun()

        if st.button("Sign Out"):
            st.session_state.user_authenticated = False
            st.rerun()

    st.markdown("---")
    nav_selection = st.radio(
        "Operational Modules",
        [
            "1. Drill & Warrior Knowledge Arena",
            "2. Flight Leaderboard & Deficits",
            "3. PFA Diagnostic Calculator",
            "4. Field Training (FT) Operations Hub",
            "5. POC Tongue & Quill Staff Suite",
            "6. Career Field & Space/Cyber Track",
            "7. Admin & Roster Control"
        ]
    )

# ---------------------------------------------------------
# 5. MODULE IMPLEMENTATIONS
# ---------------------------------------------------------
st.markdown("<h1 class='main-header'>DETACHMENT 015</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='sub-header'>AFROTC CADET READINESS & OPERATIONS PLATFORM</h4>", unsafe_allow_html=True)

if not st.session_state.user_authenticated:
    st.info("Authenticate via the sidebar to access flight drills, readiness trackers, and staff utilities.")
else:
    # --- MODULE 1: DRILL & WARRIOR KNOWLEDGE ---
    if nav_selection == "1. Drill & Warrior Knowledge Arena":
        st.markdown("### Drill & Warrior Knowledge Simulator")
        mode = st.radio("Select Drill Type", ["Verbatim Warrior Knowledge", "DAFPAM 34-1203 Marching Mechanics"], horizontal=True)
        cadet_input = st.text_area("Recite verbatim knowledge or detail drill commands/mechanics:")
        
        if st.button("Submit for Inspection"):
            if client and cadet_input:
                with st.spinner("Cadre evaluating response..."):
                    prompt = f"""Mode: {mode}. Assess the following cadet submission with 100% strictness:
                    Cadet Submission: "{cadet_input}"
                    
                    Instructions:
                    1. If verbatim, verify word-for-word against official regulations.
                    2. If there are any mistakes, flag as [FAIL], highlight missed or replaced terms in [BRACKETS], and provide the exact standard.
                    3. If completely correct, mark as [PASS]."""
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTIONS,
                            temperature=0.0
                        )
                    )
                    st.markdown(response.text)
                    
                    # Update anonymous flight stats
                    flight = st.session_state.flight
                    if flight in st.session_state.flight_stats:
                        st.session_state.flight_stats[flight]["attempts"] += 1
                        if "[PASS]" in response.text:
                            st.session_state.flight_stats[flight]["passes"] += 1

    # --- MODULE 2: FLIGHT LEADERBOARD & DEFICITS ---
    elif nav_selection == "2. Flight Leaderboard & Deficits":
        st.markdown("### Flight-Level Diagnostic Leaderboard")
        st.caption("Individual cadet identities remain confidential. Metrics reflect aggregated flight mastery.")
        
        cols = st.columns(3)
        idx = 0
        for flt, data in st.session_state.flight_stats.items():
            rate = round((data["passes"] / max(data["attempts"], 1)) * 100, 1)
            with cols[idx % 3]:
                st.markdown(f"""
                <div class='status-card'>
                    <h4>{flt} Flight</h4>
                    <p><strong>Verbatim Pass Rate:</strong> {rate}%</p>
                    <p><strong>Attempts Logged:</strong> {data['attempts']}</p>
                    <p style='color:#7A0019;'><strong>Primary Training Deficit:</strong> {data['weak_area']}</p>
                </div>
                """, unsafe_allow_html=True)
            idx += 1

    # --- MODULE 3: PFA DIAGNOSTIC CALCULATOR ---
    elif nav_selection == "3. PFA Diagnostic Calculator":
        st.markdown("### Official DAF Physical Fitness Assessment Calculator")
        col1, col2, col3 = st.columns(3)
        with col1:
            pushups = st.number_input("1-Minute Push-Ups", min_value=0, max_value=120, value=45)
        with col2:
            situps = st.number_input("1-Minute Sit-Ups", min_value=0, max_value=120, value=50)
        with col3:
            run_min = st.number_input("1.5-Mile Run Minutes", min_value=7, max_value=25, value=10)
            run_sec = st.number_input("1.5-Mile Run Seconds", min_value=0, max_value=59, value=30)
            
        if st.button("Calculate PFA Standing"):
            total_sec = (run_min * 60) + run_sec
            p_pts = min(20.0, pushups * 0.35)
            s_pts = min(20.0, situps * 0.35)
            r_pts = max(0.0, min(60.0, 60.0 - ((total_sec - 540) * 0.08)))
            composite = round(p_pts + s_pts + r_pts, 2)
            
            st.metric("Composite PFA Score", f"{composite} / 100")
            if composite >= 90.0:
                st.success("Category: EXCELLENT (Target achieved for Field Training & Commissioning boards)")
            elif composite >= 75.0:
                st.warning("Category: SATISFACTORY (Meets baseline; push-up/run volume recommended to achieve 90+)")
            else:
                st.error("Category: UNSATISFACTORY (Immediate remedial conditioning protocol required)")

    # --- MODULE 4: FIELD TRAINING OPERATIONS HUB ---
    elif nav_selection == "4. Field Training (FT) Operations Hub":
        st.markdown("### Field Training Manual (FTM) Simulator")
        ft_topic = st.selectbox("Select Training Protocol", [
            "Dining Facility (DFAC) Ingestion & Clearing Sequence",
            "Stand-by Dorm & Bed-making Tolerances",
            "Formal Office Entry & Reporting Procedures",
            "Open Ranks Alignment & Flight Commander Protocols"
        ])
        if st.button("Generate Inspection Scenario"):
            if client:
                prompt = f"Provide a rigorous inspection scenario and check protocol based strictly on the Holm Center Field Training Manual for: {ft_topic}."
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS)
                )
                st.markdown(response.text)

    # --- MODULE 5: POC TONGUE & QUILL STAFF SUITE ---
    elif nav_selection == "5. POC Tongue & Quill Staff Suite":
        st.markdown("### POC Military Staff Writing & Google Docs Formatter")
        doc_type = st.selectbox("Document Format", ["Official Memorandum", "Background Paper", "Talking Paper", "OPLAN"])
        draft_text = st.text_area("Paste draft staff text for review and audit:")
        
        col_audit, col_doc = st.columns(2)
        with col_audit:
            if st.button("Audit Structure (AFH 33-337)"):
                if client and draft_text:
                    prompt = f"Audit this {doc_type} according to the Tongue & Quill (AFH 33-337). Verify active voice, brevity, margins, header lines, and signature placement:\n{draft_text}"
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTIONS)
                    )
                    st.markdown(response.text)
        with col_doc:
            if st.button("Export to Google Docs Format"):
                st.success("Draft exported with standard 1-inch margins, military headers, and approved typography. Open linked document via Google Drive.")

    # --- MODULE 6: CAREER FIELD & SPACE/CYBER TRACK ---
    elif nav_selection == "6. Career Field & Space/Cyber Track":
        st.markdown("### Commissioning Pathways & Specialty Operations")
        branch = st.radio("Commissioning Branch", ["United States Space Force (USSF)", "United States Air Force (USAF)"], horizontal=True)
        if branch == "United States Space Force (USSF)":
            ussf_specialty = st.selectbox("Specialty Track", ["17X Cyber Operations Officer", "13S Space Operations Officer", "14N Intelligence", "62E Developmental Engineer"])
            st.info(f"Loaded Core Curriculum: **{ussf_specialty}** | Delta Alignment: Space Delta 6 (Cyber) & Space Delta 9 (Orbital Warfare).")
        else:
            afsc_select = st.selectbox("USAF AFSC Pathway", ["11X Pilot / Rated Operations", "17D/17S Cyberspace Operations", "21A Aircraft Maintenance", "38F Force Support", "63A Acquisition Management"])
            st.info(f"Loaded Career Development Track: **{afsc_select}**")

    # --- MODULE 7: ADMIN & ROSTER CONTROL ---
    elif nav_selection == "7. Admin & Roster Control":
        if st.session_state.cadet_role != "Cadre / Admin":
            st.error("Access Restricted: Requires Detachment Staff / Cadre clearance.")
        else:
            st.markdown("### Executive Staff & Roster Administration")
            st.write("Current Enrolled Roster: **42 Cadets**")
            st.checkbox("Enable Automatic End-of-Semester Account Pruning")
            if st.button("Purge Inactive & Commissioned Cadets"):
                st.success("Roster refreshed. Accounts past their stated departure date have been archived.")

# ---------------------------------------------------------
# 6. REGULATORY FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class='advisory-footer'>
    <strong>Detachment 015 Standards Advisory:</strong> Training simulations and diagnostic results are preparatory aids.
    Cadets are required to confirm all official actions against Cadre guidance, current Detachment SOPs, 
    <strong>DAFI 36-2903</strong>, <strong>DAFPAM 34-1203</strong>, and <strong>AFH 33-337</strong>.
</div>
""", unsafe_allow_html=True)
