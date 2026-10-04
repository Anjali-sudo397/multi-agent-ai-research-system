import streamlit as st
import time
from pathlib import Path

from pipeline import run_research_pipeline


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');


/* ───────────────── GLOBAL ───────────────── */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(
            ellipse 80% 50% at 20% -10%,
            rgba(255,140,50,0.12) 0%,
            transparent 60%
        ),
        radial-gradient(
            ellipse 60% 40% at 80% 110%,
            rgba(255,80,30,0.08) 0%,
            transparent 55%
        );
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1200px;
}


/* ───────────────── HERO ───────────────── */

.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    opacity: 0.9;
}

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1rem;
}

.hero h1 span {
    color: #ff8c32;
}

.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #b5afa7;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}


/* ───────────────── DIVIDER ───────────────── */

.divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,140,50,0.3),
        transparent
    );
    margin: 2rem 0;
}


/* ───────────────── INPUT CARD ───────────────── */

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
}


/* ───────────────── TEXT INPUT ───────────────── */

.stTextInput > div > div > input {
    background-color: #17171f !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    border: 1px solid rgba(255,140,50,0.35) !important;
    border-radius: 10px !important;

    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;

    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    background-color: #17171f !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #8f8a84 !important;
    -webkit-text-fill-color: #8f8a84 !important;
    opacity: 1 !important;
}


/* ───────────────── FILE UPLOADER ───────────────── */

/* Main uploader */
.stFileUploader {
    color: #ffffff !important;
}

.stFileUploader > section {
    background-color: #17171f !important;
    border: 1px solid rgba(255,140,50,0.35) !important;
    border-radius: 10px !important;
}

/* Upload area text */
.stFileUploader > section p,
.stFileUploader > section span,
.stFileUploader > section small {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Upload label */
.stFileUploader label {
    color: #ffb06a !important;
}

/* 200MB helper text */
.stFileUploader small {
    color: #b8b1a8 !important;
    -webkit-text-fill-color: #b8b1a8 !important;
}

/* Browse button */
.stFileUploader button {
    background-color: #17171f !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    border: 1px solid rgba(255,140,50,0.5) !important;
    border-radius: 8px !important;

    font-weight: 600 !important;
}

/* Browse hover */
.stFileUploader button:hover {
    background-color: #24242d !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;

    border-color: #ff8c32 !important;
}


/* ───────────────── AFTER FILE UPLOAD ───────────────── */

/* Selected file container */
[data-testid="stFileUploaderFile"] {
    background-color: #17171f !important;
    border: 1px solid rgba(255,140,50,0.3) !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
}

/* Everything inside selected file */
[data-testid="stFileUploaderFile"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* File name */
[data-testid="stFileUploaderFile"] span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* File size / metadata */
[data-testid="stFileUploaderFile"] small {
    color: #b8b1a8 !important;
    -webkit-text-fill-color: #b8b1a8 !important;
}

/* Remove / X button */
[data-testid="stFileUploaderFile"] button {
    background: transparent !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
}

/* Uploaded file icons */
[data-testid="stFileUploaderFile"] svg {
    color: #ff8c32 !important;
    fill: #ff8c32 !important;
}


/* ───────────────── SUCCESS MESSAGE ───────────────── */

.stAlert {
    background-color: #17171f !important;
    border: 1px solid rgba(80,200,120,0.3) !important;
}

.stAlert p,
.stAlert span {
    color: #f0ebe0 !important;
}


/* ───────────────── BUTTON ───────────────── */

.stButton > button {
    background: linear-gradient(
        135deg,
        #ff8c32 0%,
        #ff5a1a 100%
    ) !important;

    color: #0a0a0f !important;

    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;

    border: none !important;
    border-radius: 10px !important;

    padding: 0.7rem 2.2rem !important;

    cursor: pointer !important;

    box-shadow:
        0 4px 20px rgba(255,140,50,0.3) !important;

    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;

    box-shadow:
        0 8px 28px rgba(255,140,50,0.4) !important;
}


/* ───────────────── PIPELINE CARDS ───────────────── */

.step-card {
    background: rgba(255,255,255,0.03);

    border: 1px solid rgba(255,255,255,0.07);

    border-radius: 14px;

    padding: 1.5rem 1.8rem;

    margin-bottom: 1.2rem;

    position: relative;

    overflow: hidden;
}

.step-card.active {
    border-color: rgba(255,140,50,0.4);
    background: rgba(255,140,50,0.04);
}

.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}

.step-card::before {
    content: '';

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 3px;

    border-radius: 14px 0 0 14px;

    background: rgba(255,255,255,0.05);
}

.step-card.active::before {
    background: #ff8c32;
}

.step-card.done::before {
    background: #50c878;
}

.step-header {
    display: flex;
    align-items: center;

    gap: 0.8rem;

    margin-bottom: 0.3rem;
}

.step-num {
    font-family: 'DM Mono', monospace;

    font-size: 0.68rem;

    font-weight: 500;

    letter-spacing: 0.15em;

    color: #ff8c32;

    opacity: 0.7;
}

.step-title {
    font-family: 'Syne', sans-serif;

    font-size: 0.95rem;

    font-weight: 700;

    color: #f0ebe0;
}

.step-status {
    margin-left: auto;

    font-family: 'DM Mono', monospace;

    font-size: 0.68rem;

    letter-spacing: 0.1em;
}

.status-waiting {
    color: #8a8580;
}

.status-running {
    color: #ff8c32;
}

.status-done {
    color: #50c878;
}


/* ───────────────── RESULT PANELS ───────────────── */

.result-panel {
    background: rgba(255,255,255,0.025);

    border: 1px solid rgba(255,255,255,0.07);

    border-radius: 14px;

    padding: 1.8rem 2rem;

    margin-top: 1rem;

    margin-bottom: 1.5rem;
}

.result-panel-title {
    font-family: 'DM Mono', monospace;

    font-size: 0.7rem;

    font-weight: 500;

    letter-spacing: 0.2em;

    text-transform: uppercase;

    color: #ff8c32;

    margin-bottom: 1rem;

    padding-bottom: 0.7rem;

    border-bottom:
        1px solid rgba(255,140,50,0.15);
}

.result-content {
    font-size: 0.92rem;

    line-height: 1.8;

    color: #e0dbd2 !important;

    white-space: pre-wrap;

    font-family: 'DM Sans', sans-serif;
}


/* ───────────────── REPORT ───────────────── */

.report-panel {
    background: rgba(255,255,255,0.025);

    border:
        1px solid rgba(255,140,50,0.2);

    border-radius: 16px;

    padding: 2rem 2.5rem;

    margin-top: 1rem;
}


/* ───────────────── FEEDBACK ───────────────── */

.feedback-panel {
    background: rgba(255,255,255,0.025);

    border:
        1px solid rgba(80,200,120,0.2);

    border-radius: 16px;

    padding: 2rem 2.5rem;

    margin-top: 1rem;
}

.panel-label {
    font-family: 'DM Mono', monospace;

    font-size: 0.7rem;

    letter-spacing: 0.2em;

    text-transform: uppercase;

    margin-bottom: 1.2rem;

    padding-bottom: 0.7rem;
}

.panel-label.orange {
    color: #ff8c32;

    border-bottom:
        1px solid rgba(255,140,50,0.15);
}

.panel-label.green {
    color: #50c878;

    border-bottom:
        1px solid rgba(80,200,120,0.15);
}


/* ───────────────── SPINNER ───────────────── */

.stSpinner > div {
    color: #ff8c32 !important;
}


/* ───────────────── EXPANDER ───────────────── */

details summary {
    font-family: 'DM Mono', monospace !important;

    font-size: 0.75rem !important;

    color: #d5d0c8 !important;

    letter-spacing: 0.1em !important;

    cursor: pointer;
}


/* ───────────────── SECTION HEADING ───────────────── */

.section-heading {
    font-family: 'Syne', sans-serif;

    font-size: 1.3rem;

    font-weight: 700;

    color: #f0ebe0 !important;

    margin: 2rem 0 1rem;
}


/* ───────────────── GENERAL TEXT ───────────────── */

.stApp p,
.stApp span,
.stApp label,
.stApp li {
    color: #e8e4dc;
}

.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown span {
    color: #e8e4dc !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #f5f0e8 !important;
}


/* ───────────────── ALERTS ───────────────── */

.stAlert,
.stAlert p,
.stAlert span {
    color: #f0ebe0 !important;
}


/* ───────────────── DOWNLOAD ───────────────── */

.stDownloadButton button {
    color: #ffffff !important;

    background: #1c1c25 !important;

    border:
        1px solid rgba(255,140,50,0.4) !important;
}


/* ───────────────── NOTICE ───────────────── */

.notice {
    font-family: 'DM Mono', monospace;

    font-size: 0.72rem;

    color: #a09890 !important;

    text-align: center;

    margin-top: 3rem;

    letter-spacing: 0.08em;
}


/* ───────────────── RESEARCH TOPIC INPUT TEXT ───────────────── */

.stTextInput input,
.stTextInput textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ff8c32 !important;
}

.stTextInput input::placeholder,
.stTextInput textarea::placeholder {
    color: #aaa39b !important;
    -webkit-text-fill-color: #aaa39b !important;
    opacity: 1 !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────────────────────
# STEP CARD
# ─────────────────────────────────────────────────────────────────────────────

def step_card(
    num: str,
    title: str,
    state: str,
    desc: str = ""
):

    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }

    label, cls = status_map.get(
        state,
        ("", "")
    )

    card_cls = {
        "running": "active",
        "done": "done"
    }.get(
        state,
        ""
    )

    description = ""

    if desc:
        description = (
            f"""
            <div class="step-description">
                {desc}
            </div>
            """
        )

    st.html(
        f"""
        <div class="step-card {card_cls}">

            <div class="step-header">

                <span class="step-num">
                    {num}
                </span>

                <span class="step-title">
                    {title}
                </span>

                <span class="step-status {cls}">
                    {label}
                </span>

            </div>

            {description}

        </div>
        """
    )


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False

if "done" not in st.session_state:
    st.session_state.done = False


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────

st.html(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            Multi-Agent AI System
        </div>

        <h1>
            Research<span>Mind</span>
        </h1>

        <p class="hero-sub">
            Four specialized AI agents collaborate —
            searching, scraping, writing, and critiquing —
            to deliver a polished research report on any topic.
        </p>

    </div>

    <div class="divider"></div>
    """
)


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────────────────

col_input, col_spacer, col_pipeline = st.columns(
    [5, 0.5, 4]
)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────────────────────────────────────

with col_input:

    st.html(
        """
        <div class="input-card">
        """
    )

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )

    uploaded_file = st.file_uploader(
        "📄 Upload a research document",
        type=["pdf", "txt"],
        help="Maximum file size: 200MB"
    )

    if uploaded_file is not None:

        documents_dir = Path("documents")

        documents_dir.mkdir(
            exist_ok=True
        )

        file_path = (
            documents_dir /
            uploaded_file.name
        )

        file_path.write_bytes(
            uploaded_file.getbuffer()
        )

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

    run_btn = st.button(
        "⚡  Run Research Pipeline",
        use_container_width=True
    )

    st.html(
        """
        </div>
        """
    )


    # ───────────────── EXAMPLE CHIPS ─────────────────

    st.html(
        """
        <div style="
            display:flex;
            gap:0.5rem;
            flex-wrap:wrap;
            align-items:center;
            margin-bottom:1.5rem;
        ">

            <span style="
                font-family:'DM Mono',monospace;
                font-size:0.68rem;
                color:#9b948c;
                letter-spacing:0.1em;
            ">
                TRY →
            </span>

            <span style="
                background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08);
                border-radius:6px;
                padding:0.25rem 0.7rem;
                font-size:0.75rem;
                color:#c5beb5;
            ">
                LLM agents 2025
            </span>

            <span style="
                background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08);
                border-radius:6px;
                padding:0.25rem 0.7rem;
                font-size:0.75rem;
                color:#c5beb5;
            ">
                CRISPR gene editing
            </span>

            <span style="
                background:rgba(255,255,255,0.04);
                border:1px solid rgba(255,255,255,0.08);
                border-radius:6px;
                padding:0.25rem 0.7rem;
                font-size:0.75rem;
                color:#c5beb5;
            ">
                Fusion energy progress
            </span>

        </div>
        """
    )


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE SECTION
# ─────────────────────────────────────────────────────────────────────────────

with col_pipeline:

    st.html(
        """
        <div class="section-heading">
            Pipeline
        </div>
        """
    )

    r = st.session_state.results

    def get_step_state(step):

        if not r:
            return "waiting"

        steps = [
            "search",
            "reader",
            "writer",
            "critic"
        ]

        if step in r:
            return "done"

        if st.session_state.running:

            for current_step in steps:

                if current_step not in r:

                    if current_step == step:
                        return "running"

                    return "waiting"

        return "waiting"


    step_card(
        "01",
        "Search Agent",
        get_step_state("search"),
        "Gathers recent web information"
    )

    step_card(
        "02",
        "Reader Agent",
        get_step_state("reader"),
        "Scrapes & extracts deep content"
    )

    step_card(
        "03",
        "Writer Chain",
        get_step_state("writer"),
        "Drafts the full research report"
    )

    step_card(
        "04",
        "Critic Chain",
        get_step_state("critic"),
        "Reviews & scores the report"
    )


# ─────────────────────────────────────────────────────────────────────────────
# RUN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

if run_btn:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

    else:

        st.session_state.running = True

        with st.spinner(
            "🤖 ResearchMind is running the multi-agent pipeline..."
        ):

            try:

                result = run_research_pipeline(
                    topic.strip()
                )

                st.session_state.results = result

                st.session_state.done = True

            except Exception as e:

                st.error(
                    f"Pipeline failed: {e}"
                )

            finally:

                st.session_state.running = False


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────

r = st.session_state.results


if r:

    st.html(
        """
        <div class="divider"></div>

        <div class="section-heading">
            Results
        </div>
        """
    )


    # ───────────────── SEARCH RESULTS ─────────────────

    if "search_results" in r:

        with st.expander(
            "🔍 Search Results",
            expanded=False
        ):

            st.html(
                f"""
                <div class="result-panel">

                    <div class="result-panel-title">
                        Web Research
                    </div>

                    <div class="result-content">
                        {r["search_results"]}
                    </div>

                </div>
                """
            )


    # ───────────────── DOCUMENT RESEARCH ─────────────────

    if "document_research" in r:

        with st.expander(
            "📚 Uploaded Document Research",
            expanded=False
        ):

            st.html(
                f"""
                <div class="result-panel">

                    <div class="result-panel-title">
                        RAG Research
                    </div>

                    <div class="result-content">
                        {r["document_research"]}
                    </div>

                </div>
                """
            )


    # ───────────────── FINAL REPORT ─────────────────

    if "revised_report" in r:

        st.html(
            """
            <div class="report-panel">

                <div class="panel-label orange">
                    📝 Final Research Report
                </div>
            """
        )

        st.markdown(
            r["revised_report"]
        )

        st.html(
            """
            </div>
            """
        )

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["revised_report"],
            file_name=(
                f"research_report_"
                f"{int(time.time())}.md"
            ),
            mime="text/markdown",
        )


    # ───────────────── CRITIC FEEDBACK ─────────────────

    if "feedback" in r:

        st.html(
            """
            <div class="feedback-panel">

                <div class="panel-label green">
                    🧐 Critic Feedback
                </div>
            """
        )

        st.markdown(
            r["feedback"]
        )

        st.html(
            """
            </div>
            """
        )


    # ───────────────── FACT CHECK ─────────────────

    if "fact_check" in r:

        with st.expander(
            "✅ Fact Check",
            expanded=False
        ):

            st.markdown(
                r["fact_check"]
            )


    # ───────────────── QUALITY DECISION ─────────────────

    if "quality_decision" in r:

        st.html(
            f"""
            <div class="notice">

                <strong>Quality Decision:</strong>
                {r["quality_decision"]}

                &nbsp; | &nbsp;

                <strong>Revisions:</strong>
                {r.get("revision_count", 0)}

            </div>
            """
        )


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.html(
    """
    <div class="notice">
        ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
    </div>
    """
)
