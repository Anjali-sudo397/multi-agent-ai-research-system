from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_urls


# ============================================================
# MODEL SETUP
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ============================================================
# SEARCH AGENT
# ============================================================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


# ============================================================
# READER AGENT
# ============================================================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_urls]
    )


# ============================================================
# WRITER CHAIN
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a rigorous research writer.

Your job is to write a factual research report using ONLY the information
contained in the provided research.

Strict rules:
- Do NOT invent facts, statistics, dates, studies, companies, or sources.
- Do NOT use outside knowledge.
- Do NOT attribute a claim to a source unless that source appears in the provided research.
- Use numerical claims only when they are explicitly present in the research.
- If evidence is insufficient, say that the available sources do not establish the claim.
- Keep source URLs exactly as provided.
- Clearly distinguish reported facts from observations or conclusions.
"""
    ),
    (
        "human",
        """Write a detailed research report on:

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

## Executive Summary
## Key Findings
## Benefits / Applications
## Risks and Limitations
## Conclusion
## Sources

Important:
Every factual claim must be supported by the provided research.
Do not manufacture statistics or citations.
In the Sources section, list ONLY URLs that actually appear in the provided research.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ============================================================
# CRITIC CHAIN
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a sharp and constructive research critic.
Be honest and specific."""
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()


# ============================================================
# REVISION CHAIN
# ============================================================

revision_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert research editor.

Revise the report using the critic feedback and fact-check results.

STRICT RULES:
- Use ONLY information supported by the provided research sources.
- REMOVE unsupported statistics, percentages, dates, study results,
  company claims, or citations.
- If a claim is marked NOT SUPPORTED, remove it or rewrite it
  without the unsupported claim.
- Do NOT invent replacement facts or numbers.
- Do NOT create new sources or references.
- Preserve only claims that are VERIFIED or reasonably supported.
- Keep the report factual and evidence-based.
"""
    ),
    (
        "human",
        """Topic:
{topic}

Current Report:
{report}

Critic + Fact Check Feedback:
{feedback}

Return only the revised research report."""
    ),
])

revision_chain = revision_prompt | llm | StrOutputParser()


# ============================================================
# FACT CHECKER CHAIN
# ============================================================

fact_checker_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict research fact checker.

Verify every important claim ONLY against the provided research sources.

Rules:
- VERIFIED = clearly supported by the research.
- PARTIALLY VERIFIED = only partly supported.
- NOT SUPPORTED = no evidence in the research.
- Do NOT use outside knowledge.
- Do NOT invent facts, numbers, dates, studies, or sources.
- Pay special attention to statistics and percentages."""
    ),
    (
        "human",
        """Fact-check the research report below using the provided research.

Topic:
{topic}

Research Sources:
{research}

Report:
{report}

For each important claim, classify it as:
- VERIFIED
- PARTIALLY VERIFIED
- NOT SUPPORTED

Then provide:

1. Claims that need correction
2. Claims that are well supported
3. Missing or weak sources

Be concise and evidence-based.
"""
    ),
])

fact_checker_chain = fact_checker_prompt | llm | StrOutputParser()


# ============================================================
# QUALITY CHECK CHAIN
# ============================================================

quality_check_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict research quality controller.

Evaluate the report using the critic feedback and fact-check results.

Return ONLY one of these two decisions:

PASS
REVISE

Choose REVISE if there are significant unsupported claims,
factual issues, missing evidence, or major quality problems.

Choose PASS only when the report is sufficiently accurate,
well-supported and complete."""
    ),
    (
        "human",
        """Topic:
{topic}

Report:
{report}

Critic Feedback:
{feedback}

Fact Check:
{fact_check}

Decision:"""
    ),
])

quality_check_chain = quality_check_prompt | llm | StrOutputParser()


print("Research chains loaded successfully.")