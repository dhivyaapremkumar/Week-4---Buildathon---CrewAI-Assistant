import os
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from crew import run_crew

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="CrewAI Agentic Search Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "execution_time" not in st.session_state:
    st.session_state.execution_time = 0

if "result" not in st.session_state:
    st.session_state.result = None

# -------------------------------------------------
# PREMIUM CSS
# -------------------------------------------------

st.markdown(
    """
<style>

html,body,[class*="css"]{
    font-family: 'Segoe UI';
}

.stApp{
    background:#09111f;
}

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #334155;
}

section[data-testid="stSidebar"] *{
    color:#F8FAFC !important;
}

section[data-testid="stSidebar"] p{
    color:#CBD5E1 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:white !important;
    font-weight:700;
}
/* All markdown text */
.stMarkdown{
    color:#F8FAFC !important;
}

/* Paragraphs */
p{
    color:#E2E8F0 !important;
}

/* Labels */
label{
    color:#F8FAFC !important;
}

/* Expanders */
details{
    color:white;
}

/* Text inside expanders */
div[data-testid="stExpander"]{
    color:white;
}

/* Code blocks */
pre{
    color:#F8FAFC !important;
}

/* Lists */
li{
    color:#E2E8F0 !important;
}
/* Header */

.title{
font-size:40px;
font-weight:700;
color:white;
}

.subtitle{
font-size:17px;
color:#94a3b8;
}

/* Glass Cards */

.glass{
background:rgba(255,255,255,.05);
padding:22px;
border-radius:20px;
border:1px solid rgba(255,255,255,.10);
backdrop-filter:blur(18px);
margin-bottom:15px;
}

/* Status Cards */

.status-card{
background:#111827;
padding:18px;
border-radius:18px;
text-align:center;
border:1px solid #263244;
color:white;
}

.metric-card{
background:#111827;
padding:18px;
border-radius:15px;
border:1px solid #263244;
text-align:center;
}

.metric-title{
font-size:14px;
color:#94a3b8;
}

.metric-value{
font-size:28px;
font-weight:bold;
color:white;
}

.green{
color:#22c55e;
font-weight:bold;
}

.orange{
color:#f59e0b;
font-weight:bold;
}

.red{
color:#ef4444;
font-weight:bold;
}

.workflow{

background:#111827;

padding:20px;

border-radius:20px;

border:1px solid #334155;

color:white;

}

footer{
visibility:hidden;
}

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:
    st.title("🤖 CrewAI Assistant")

    st.sidebar.markdown(
        """
<span style='color:#CBD5E1;font-size:16px;'>
🚀 Buildathon Edition
</span>
""",
        unsafe_allow_html=True,
    )
    st.sidebar.divider()
    if OPENAI_API_KEY:
        st.sidebar.subheader("System Health")

        st.sidebar.success("🟢 CrewAI")

        st.sidebar.success("🟢 Logger")

        st.sidebar.success("🟢 Streamlit")
        st.success("✅ OpenAI Connected")
    else:
        st.error("❌ OpenAI Missing")

    if SERPAPI_API_KEY:
        st.success("✅ SerpAPI Connected")
    else:
        st.error("❌ SerpAPI Missing")

    st.divider()

    st.markdown("### Project")

    st.write("🏢 Fourth Axis Designers")

    st.write("🤖 CrewAI")

    st.write("🌐 SerpAPI")

    st.write("🧠 GPT-4.1 Mini")

    st.divider()

    st.markdown("### Search History")

    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.write("•", item)

    else:
        st.caption("No searches yet.")
    with st.expander("ℹ About"):
        st.write("CrewAI Agentic Search Assistant")

        st.write("Version 1.0")

        st.write("OpenAI")

        st.write("CrewAI")

        st.write("SerpAPI")

        st.write("Streamlit")

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    """
<div class="title">
🤖 CrewAI Agentic Search Assistant
</div>

<div class="subtitle">
Powered by OpenAI • CrewAI • SerpAPI
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# -------------------------------------------------
# METRICS
# -------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
<div class="metric-card">
<div class="metric-title">
Agents
</div>

<div class="metric-value">
3
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        """
<div class="metric-card">
<div class="metric-title">
Tool Calls
</div>

<div class="metric-value">
1
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
<div class="metric-card">
<div class="metric-title">
Execution Time
</div>

<div class="metric-value">
{st.session_state.execution_time}
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        """
<div class="metric-card">
<div class="metric-title">
Status
</div>

<div class="metric-value green">
ONLINE
</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.write("")

# -------------------------------------------------
# QUERY
# -------------------------------------------------

st.markdown("## 🔍 Ask Your Question")

with st.container(border=True):

    query = st.text_input(
        "Enter your query",
        placeholder="Latest AI News..."
    )

    col1, col2 = st.columns([3, 1])

    with col2:
        run = st.button(
            "🚀 Run Crew",
            use_container_width=True
        )

# -------------------------------------------------
# WORKFLOW
# -------------------------------------------------

st.markdown("## ⚙️ Agent Workflow")

flow = st.columns(4)

with flow[0]:
    st.success("👤 User")

with flow[1]:
    st.info("👋 Greeting")

with flow[2]:
    st.warning("🌐 Search")

with flow[3]:
    st.error("📝 Logger")

st.write("")

# -------------------------------------------------
# LIVE STATUS
# -------------------------------------------------

st.markdown("## ⚡ Live Agent Status")

c1, c2, c3 = st.columns(3)

greeting_status = c1.empty()

search_status = c2.empty()

logger_status = c3.empty()

greeting_status.success("👋 Waiting")

search_status.info("🌐 Waiting")

logger_status.warning("📝 Waiting")

st.divider()

# -------------------------------------------------
# TIMELINE PLACEHOLDER
# -------------------------------------------------

timeline = st.empty()

progress_bar = st.progress(0)

st.divider()

# -------------------------------------------------
# OUTPUT AREA
# -------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

m1.metric("🤖 Agents", "3")

m2.metric("🛠 Tool Calls", "1")

m3.metric("⏱ Time", f"{st.session_state.execution_time}s")

m4.metric("✅ Status", "SUCCESS")

left, right = st.columns([2, 1])

output_area = left.container(border=True)

log_area = right.container(border=True)

# -------------------------------------------------
# RUN CREW
# -------------------------------------------------

if run:
    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    start_time = time.time()

    st.session_state.history.append(query)

    timeline.info("🚀 Initializing Crew...")

    progress_bar.progress(5)

    greeting_status.warning("🟡 Greeting Agent Running")

    time.sleep(0.4)

    progress_bar.progress(20)

    search_status.info("⏳ Waiting")

    logger_status.info("⏳ Waiting")

    try:
        thinking = st.empty()

        thinking.info("🤖 Initializing Crew...")
        time.sleep(0.5)

        thinking.info("👋 Greeting Agent is thinking...")
        time.sleep(0.5)

        thinking.info("🌐 Search Agent is searching Google...")
        time.sleep(0.5)

        thinking.info("📝 Logger Agent is preparing the report...")
        result = run_crew(query)
        thinking.success("✅ Crew Execution Completed")

        execution_time = round(time.time() - start_time, 2)

        st.session_state.execution_time = execution_time

        st.session_state.result = result

        progress_bar.progress(40)

        greeting_status.success("🟢 Greeting Completed")

        timeline.info("👋 Greeting Agent Finished")

        time.sleep(0.4)

        progress_bar.progress(70)

        search_status.success("🟢 Search Completed")

        timeline.info("🌐 Search Agent Finished")

        time.sleep(0.4)

        progress_bar.progress(90)

        logger_status.success("🟢 Logger Completed")

        timeline.info("📝 Logger Agent Finished")

        progress_bar.progress(100)

    except Exception as e:
        st.error(e)

        st.stop()
if st.session_state.result:
    result = st.session_state.result

    with output_area:
        with st.expander("👋 Greeting Agent", expanded=True):
            st.markdown(result["greeting_output"])

        with st.expander("🌐 Search Agent", expanded=True):
            st.markdown(result["search_output"])

        with st.expander("📝 Logger Agent", expanded=False):
            st.code(result["logger_output"])

    log_text = f"""
Timestamp:
{datetime.now()}

Execution Time:
{st.session_state.execution_time}

Query:
{query}

-----------------------------------

Greeting

{result["greeting_output"]}

-----------------------------------

Search

{result["search_output"]}

-----------------------------------

Logger

{result["logger_output"]}
"""

    os.makedirs("logs", exist_ok=True)

    with open("logs/execution_log.txt", "w", encoding="utf-8") as f:
        f.write(log_text)

    with log_area:
        st.subheader("📄 Execution Log")

        st.markdown(
            """
<style>
.scroll-box{
    height:450px;
    overflow-y:auto;
    background:#111827;
    border:1px solid #334155;
    border-radius:12px;
    padding:15px;
    color:#F8FAFC;
    font-family:Consolas, monospace;
    white-space:pre-wrap;
}
</style>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
<div class="scroll-box">
<pre>{log_text}</pre>
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("### 📊 Execution Summary")

        st.write(f"**Query:** {query}")

        st.write(f"**Timestamp:** {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

        st.write("**Agents Executed:** 3")

        st.write("**Model:** GPT-4.1 Mini")

        st.write("**Search Engine:** Google (SerpAPI)")
        st.download_button(
            "📥 Download Log",
            data=log_text,
            file_name="execution_log.txt",
            mime="text/plain",
        )

        st.metric("Execution Time", f"{st.session_state.execution_time} sec")

        st.success("Execution Successful")
st.divider()

st.markdown(
    """
<div style="text-align:center;color:#94A3B8;padding:20px;">
Developed by <b>Fourth Axis Designers Pvt. Ltd.</b><br>
CrewAI • OpenAI • SerpAPI • Streamlit
</div>
""",
    unsafe_allow_html=True,
)
