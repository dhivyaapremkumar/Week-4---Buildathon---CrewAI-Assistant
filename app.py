import os
from datetime import datetime
import time
from dotenv import load_dotenv
import re
import streamlit as st

from crewai import Agent, Task, Crew, Process, LLM

from crewai_tools import SerperDevTool
# -------------------------------------------------------
# Load Environment Variables
# -------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in .env")
    st.stop()

if not SERPER_API_KEY:
    st.error("SERPER_API_KEY not found in .env")
    st.stop()
# -------------------------------------------------------
# LLM
# -------------------------------------------------------

llm = LLM(
    provider="openai", model="gpt-4.1-mini", api_key=OPENAI_API_KEY, temperature=0.3
)
# -------------------------------------------------------
# Search Tool
# -------------------------------------------------------

search_tool = SerperDevTool()
st.set_page_config(
    page_title="Multi-Agent Customer Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.stApp{

background:#0f172a;
color:white;

}

/* ==========================================================
HERO BANNER
========================================================== */

.hero{

background:linear-gradient(
135deg,
#2563eb,
#4f46e5,
#7c3aed,
#2563eb);

background-size:300% 300%;

animation:gradientMove 8s ease infinite;

padding:22px 30px;

border-radius:24px;

margin-bottom:25px;

box-shadow:0 20px 45px rgba(0,0,0,.35);

position:relative;

overflow:hidden;

}

.hero::before{

content:"";

position:absolute;

top:-40%;

right:-10%;

width:280px;

height:280px;

background:rgba(255,255,255,.08);

border-radius:50%;

}

.hero-title{

font-size:32px;

font-weight:800;

color:white;

margin-bottom:10px;

}

.hero-sub{

font-size:16px;

margin-bottom:18px;

color:#E2E8F0;

margin-bottom:25px;

}

.badge{

display:inline-block;

padding:8px 18px;

border-radius:30px;

background:rgba(255,255,255,.15);

backdrop-filter:blur(12px);

margin-right:10px;

color:white;

font-size:15px;

font-weight:600;

}

.online{

background:#22c55e;

color:white;

}

@keyframes gradientMove{

0%{

background-position:0% 50%;

}

50%{

background-position:100% 50%;

}

100%{

background-position:0% 50%;

}

}

.card{

background:#1e293b;

padding:20px;

border-radius:18px;

border:1px solid rgba(255,255,255,.08);

margin-bottom:15px;

}

/* =======================================================
LIVE TERMINAL
======================================================= */

.log{

background:#030712;

border:1px solid #334155;

border-radius:18px;

padding:18px;

height:340px;

overflow-y:auto;

font-family:"Consolas";

font-size:15px;

line-height:1.8;

box-shadow:0 12px 30px rgba(0,0,0,.35);

}

.answer{

background:#111827;

padding:20px;

border-left:5px solid #3b82f6;

border-radius:12px;

}
/* ==========================================================
TEXT AREA
========================================================== */

.stTextArea textarea{

    background:#1e293b !important;

    color:white !important;

    border:1px solid #334155 !important;

    border-radius:12px !important;

    font-size:17px !important;

}

.stTextArea textarea::placeholder{

    color:#94a3b8 !important;

}

/* Label */

.stTextArea label{

    color:white !important;

    font-weight:600;

}

/* ==========================================================
BUTTON
========================================================== */

.stButton>button{

    width:100%;
    height:58px;
    border:none;
    border-radius:14px;
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    color:white !important;
    font-size:19px;
    font-weight:bold;
    letter-spacing:.5px;
    transition:.3s;

}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:0 10px 25px rgba(37,99,235,.35);

}
/* =======================================================
PIPELINE
======================================================= */

.pipeline{

display:flex;

justify-content:space-between;

align-items:center;

margin-top:25px;

margin-bottom:25px;

padding:20px;

background:#111827;

border-radius:18px;

border:1px solid rgba(255,255,255,.08);

box-shadow:0 12px 30px rgba(0,0,0,.35);

}

.node{

display:flex;

flex-direction:column;

align-items:center;

width:120px;

}

.circle{

width:74px;

height:74px;

border-radius:50%;

display:flex;

justify-content:center;

align-items:center;

font-size:34px;

font-weight:bold;

transition:.4s;

}

.wait{

background:#475569;

}

.run{

background:#f59e0b;

box-shadow:0 0 30px rgba(245,158,11,.65);

animation:pulse 1.2s infinite;

}

.done{

background:#22c55e;

box-shadow:0 0 30px rgba(34,197,94,.65);

}

.line{

height:6px;

flex:1;

background:#334155;

border-radius:30px;

margin:0 10px;

}

.line-active{

background:linear-gradient(90deg,#2563eb,#7c3aed);

}

@keyframes pulse{

0%{

transform:scale(1);

}

50%{

transform:scale(1.08);

}

100%{

transform:scale(1);

}

}
/* ==========================================================
RESPONSE CARDS
========================================================== */

.response-card{

background:rgba(30,41,59,.95);

border:1px solid rgba(255,255,255,.08);

border-radius:18px;

padding:20px;

margin-top:10px;

margin-bottom:15px;

box-shadow:0 10px 25px rgba(0,0,0,.35);

transition:.35s;

}

.response-card:hover{

transform:translateY(-4px);

box-shadow:0 20px 45px rgba(0,0,0,.45);

}

.response-title{

font-size:22px;

font-weight:700;

margin-bottom:15px;

padding-bottom:10px;

border-bottom:1px solid rgba(255,255,255,.08);

}

.assistant{

border-left:6px solid #22c55e;

}

.search{

border-left:6px solid #3b82f6;

}

.report{

border-left:6px solid #f59e0b;

}

.response-content{

font-size:16px;

line-height:1.6;

color:#e2e8f0;

white-space:pre-wrap;

margin:0;

padding:0;

}
/* ==========================================================
DOWNLOAD BUTTON
========================================================== */

.stDownloadButton > button{

    width:100%;

    height:52px;

    border:none;

    border-radius:14px;

    background:linear-gradient(135deg,#16a34a,#22c55e) !important;

    color:white !important;

    font-size:17px;

    font-weight:700;

    transition:.3s;

    box-shadow:0 10px 25px rgba(34,197,94,.35);

}

.stDownloadButton > button:hover{

    transform:translateY(-2px);

    box-shadow:0 18px 35px rgba(34,197,94,.45);

}

/* Fix white text */

.stDownloadButton button p{

    color:white !important;

}
/* =======================================================
KPI CARDS
======================================================= */

.kpi{

background:#1e293b;

padding:18px;

border-radius:18px;

border:1px solid rgba(255,255,255,.08);

transition:.35s;

box-shadow:0 10px 25px rgba(0,0,0,.25);

height:115px;

}

.kpi:hover{

transform:translateY(-4px);

box-shadow:0 20px 40px rgba(0,0,0,.35);

}

.kpi-icon{

font-size:28px;

margin-bottom:6px;

}

.kpi-value{

font-size:22px;

font-weight:700;

color:white;

}

.kpi-label{

color:#94a3b8;

font-size:15px;

margin-top:5px;

}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="hero">
<div style="display:flex;
justify-content:space-between;
align-items:center;">
<div>
<div class="hero-title">
🤖 Multi-Agent Customer Support
</div>

<div class="hero-sub">
AI Powered Customer Support using CrewAI, Streamlit & OpenAI
</div>

<div>
<span class="badge">⚡ 3 AI Agents</span><span class="badge">🌐 Live Search</span><span class="badge">📄 Report Generator</span>
</div>

</div>

<div>
<span class="badge online">🟢 ONLINE</span>
</div>

</div>

</div>
""",
    unsafe_allow_html=True,
)
c1, c2, c3, c4 = st.columns(4)

cards = [
    ("🤖", "3", "AI Agents"),
    ("⚙️", "Sequential", "Execution"),
    ("🌐", "Enabled", "Live Search"),
    ("🟢", "Ready", "System Status"),
]

for col, (icon, value, label) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(
            f"""
   <div class="kpi"><div class="kpi-icon">{icon}</div>
   <div class="kpi-value">{value}
   </div>
   <div class="kpi-label">
   
   {label}
   
   </div>

   </div>""",
            unsafe_allow_html=True,
        )
with st.sidebar:

    st.markdown("# 🚀 AI Control Center")

    st.success("🟢 SYSTEM ONLINE")

    st.markdown("---")

    st.markdown("### ⚙ AI Services")

    st.markdown("""
✅ Assistant Agent

✅ Web Search Agent

✅ Entry Agent
""")

    st.markdown("---")

    st.markdown("### 📊 System Status")

    st.markdown("""
🧠 OpenAI &nbsp;&nbsp;&nbsp;&nbsp;🟢 Connected

🌐 Serper &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;🟢 Connected

🤖 CrewAI &nbsp;&nbsp;&nbsp;&nbsp;🟢 Ready
""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📈 Execution")

    st.metric("Agents", "3")

    st.metric("Process", "Sequential")

    st.metric("Search", "Live")

    st.markdown("---")

    st.caption("⚡ Powered by")

    st.caption("CrewAI")

    st.caption("OpenAI")

    st.caption("Streamlit")


def workflow(step):

    states = ["wait"] * 4
    lines = ["line"] * 3

    if step == 1:
        states[0] = "run"

    elif step == 2:
        states[0] = "done"
        states[1] = "run"
        lines[0] = "line line-active"

    elif step == 3:
        states[0] = "done"
        states[1] = "done"
        states[2] = "run"
        lines[0] = "line line-active"
        lines[1] = "line line-active"

    elif step == 4:
        states = ["done"] * 4
        lines = ["line line-active"] * 3

    workflow_placeholder.markdown(
        f"""

<div class="pipeline">

<div class="node">

<div class="circle {states[0]}">

🤖

</div>

Assistant

</div>

<div class="{lines[0]}"></div>

<div class="node">

<div class="circle {states[1]}">

🌐

</div>

Search

</div>

<div class="{lines[1]}"></div>

<div class="node">

<div class="circle {states[2]}">

📝

</div>

Entry

</div>

<div class="{lines[2]}"></div>

<div class="node">

<div class="circle {states[3]}">

📄

</div>

Report

</div>

</div>

""",
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)
query_container = st.container()

with query_container:
    st.markdown("### 💬 Enter Your Customer Support Question")
    query = st.text_area(
        "", height=140, placeholder="Example : How do I reset my password?"
    )

    run = st.button("🚀 Run Crew", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
# =========================================================
# DASHBOARD
# =========================================================

progress = st.progress(0)

workflow_placeholder = st.empty()

st.markdown("---")

left, right = st.columns([3, 1])

with left:
    logs = st.empty()

with right:
    stats_box = st.empty()
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    assistant_box = st.empty()

with col2:
    web_box = st.empty()

st.divider()
st.markdown("---")
entry_box = st.empty()

download_box = st.empty()

terminal_logs = []


def log(message):

    icons = {
        "Assistant": "🤖",
        "Search": "🌐",
        "Entry": "📝",
        "Crew": "🚀",
        "Report": "📄",
        "Finished": "✅",
    }

    icon = "📌"

    for key in icons:
        if key.lower() in message.lower():
            icon = icons[key]

    terminal_logs.append(
        f"""
<div style="padding:8px 0;
border-bottom:1px solid #1e293b;">

<span style="color:#22c55e;">
{icon}
</span>

<span style="color:#94a3b8;">
{datetime.now().strftime("%H:%M:%S")}
</span>

<span style="color:white;">
{message}
</span>

</div>

"""
    )

    html = """

<div class="log">

<h4 style="color:#60a5fa;">
🖥 LIVE EXECUTION TERMINAL
</h4>

"""

    for item in terminal_logs:
        html += item

    html += "</div>"

    logs.markdown(html, unsafe_allow_html=True)


# ============================================================
# AGENT 1 - ASSISTANT
# ============================================================

assistant_agent = Agent(
    role="Assistant",
    goal="Answer the user's question using your own knowledge without using the internet.",
    backstory="""
You are an experienced AI customer support representative.
Provide professional, concise and accurate responses.
""",
    llm=llm,
    verbose=True,
)

# ============================================================
# AGENT 2 - WEB SEARCH ASSISTANT
# ============================================================

web_search_agent = Agent(
    role="Web Search Assistant",
    goal="Search the web and provide the latest answer.",
    backstory="""
You are an expert web researcher.
Always use the search tool before answering.
Use reliable sources.
""",
    llm=llm,
    tools=[search_tool],
    verbose=True,
)

# ============================================================
# AGENT 3 - ENTRY AGENT
# ============================================================

entry_agent = Agent(
    role="Entry Agent",
    goal="Generate a structured report of the previous responses.",
    backstory="""
You document every customer interaction.
Your reports are neat, professional and easy to read.
""",
    llm=llm,
    verbose=True,
)
assistant_task = Task(
    description="""
Answer the following customer question.

Question:
{query}

Do NOT search the web.
Use only your own knowledge.
""",
    expected_output="""
A clear professional answer.
""",
    agent=assistant_agent,
)
web_task = Task(
    description="""
You are REQUIRED to use the Serper search tool.

DO NOT answer from memory.

User Question:
{query}

Instructions:

1. Call the Serper search tool.
2. Read the search results.
3. Create your answer ONLY from those search results.
4. Mention the sources if available.

If you answer without calling the tool, your task has failed.
""",
    expected_output="A response generated from live search results.",
    agent=web_search_agent,
    context=[assistant_task],
)
entry_task = Task(
    description="""
Create a customer support report using the previous task outputs.

The report should contain:

Customer Question

Assistant Answer

Web Search Answer

Write the report in a clean readable format.
""",
    expected_output="""
A formatted report.
""",
    agent=entry_agent,
    context=[assistant_task, web_task],
    output_file="answers.txt",
)
crew = Crew(
    agents=[assistant_agent, web_search_agent, entry_agent],
    tasks=[assistant_task, web_task, entry_task],
    process=Process.sequential,
    verbose=True,
)


# ============================================================
# RUN CREW
# ============================================================
def animate_progress(start, end):
    for i in range(start, end + 1):
        progress.progress(i)
        time.sleep(0.06)


if run:
    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        animate_progress(0,25)
        workflow(1)
        log("🤖 Assistant Agent Started")
        time.sleep(0.4)

        # Execute the Crew
        result = crew.kickoff(inputs={"query": query})

        animate_progress(25,50)
        workflow(2)
        log("🌐 Web Search Started")
        time.sleep(0.4)

        animate_progress(50,75)
        workflow(3)
        log("📝 Entry Agent Started")

        # ---------------------------------------------------
        # READ TASK OUTPUTS
        # ---------------------------------------------------

        assistant_answer = ""
        web_answer = ""
        report = ""

        try:
            outputs = crew.tasks

            if len(outputs) > 0 and outputs[0].output:
                assistant_answer = str(outputs[0].output)

            if len(outputs) > 1 and outputs[1].output:
                web_answer = str(outputs[1].output)

            if len(outputs) > 2 and outputs[2].output:
                report = str(outputs[2].output)

        except Exception as e:
            report = str(result)

        animate_progress(75,100)
        workflow(4)

        log("Crew Finished Successfully")

        log("Report Generated")
        stats_box.success("""
### 📊 Execution Summary

✅ Assistant

✅ Web Search

✅ Entry Agent

📄 Report Saved
""")

        # ---------------------------------------------------
        # DISPLAY ANSWERS
        # ---------------------------------------------------

        assistant_box.markdown(
            f"""
<div class="response-card assistant">

<div class="response-title">
🤖 Assistant Agent
</div>

<div class="response-content">

{assistant_answer}

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        web_box.markdown(
            f"""
<div class="response-card search">

<div class="response-title">
🌐 Web Search Agent
</div>

<div class="response-content">

{web_answer}

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        # Remove excessive blank lines
        report = re.sub(r"\n{3,}", "\n\n", report)

        # Remove leading/trailing whitespace
        report = report.strip()
        entry_box.markdown(
            f"""
<div class="response-card report">

<div class="response-title">
📝 Customer Support Report
</div>

<div class="response-content">{report}</div>

</div>
""",
            unsafe_allow_html=True,
        )

        # ---------------------------------------------------
        # DOWNLOAD
        # ---------------------------------------------------

        if os.path.exists("answers.txt"):
            with open("answers.txt", "r", encoding="utf-8") as f:
                download_box.download_button(
                    label="📥Download Customer Report",
                    data=f.read(),
                    file_name="answers.txt",
                    mime="text/plain",
                )

    except Exception as e:
        st.exception(e)
