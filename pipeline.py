import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from rag_retrieve import retrieve

from agents import (
    build_search_agent,
    writer_chain,
    critic_chain,
    revision_chain,
    fact_checker_chain,
    quality_check_chain,
)

from tools import scrape_urls


# -----------------------------
# LangGraph State
# -----------------------------

class ResearchState(TypedDict, total=False):
    topic: str
    search_results: str
    document_research: str
    scraped_content: str
    research: str
    report: str
    feedback: str
    fact_check: str
    revised_report: str
    quality_decision: str
    revision_count: int


# -----------------------------
# Node 1 - Search
# -----------------------------
def document_researcher_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("DOCUMENT RESEARCHER")
    print("=" * 50)

    results = retrieve(state["topic"], k=3)

    if not results:
        return {
            "document_research": "No relevant information found in uploaded documents."
        }

    document_research = "\n\n".join(
        f"Source: {result['source']}\n{result['text']}"
        for result in results
    )

    return {
        "document_research": document_research
    }

def search_node(state: ResearchState):

    print("\n" + "=" * 50)
    print("STEP 1 - SEARCH AGENT")
    print("=" * 50)

    search_agent = build_search_agent()

    result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {state['topic']}"
            )
        ]
    })

    search_results = result["messages"][-1].content

    print("\nSearch completed.")

    return {
        "search_results": search_results
    }


# -----------------------------
# Node 2 - Multi-source Reader
# -----------------------------

def reader_node(state: ResearchState):

    print("\n" + "=" * 50)
    print("STEP 2 - MULTI-SOURCE READER")
    print("=" * 50)

    urls = re.findall(
        r'https?://[^\s\]\)>"\']+',
        state["search_results"]
    )

    urls = list(dict.fromkeys(urls))[:5]

    print("\nURLs selected:")

    for url in urls:
        print(url)

    if urls:
        scraped_content = scrape_urls.invoke(
            "\n".join(urls)
        )
    else:
        scraped_content = "No valid URLs were found."

    return {
        "scraped_content": scraped_content
    }


# -----------------------------
# Node 3 - Writer
# -----------------------------

def writer_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("STEP 3 - WRITER")
    print("=" * 50)

    research = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}\n\n"
        f"UPLOADED DOCUMENT RESEARCH:\n{state['document_research']}"
    )

    report = writer_chain.invoke({
        "topic": state["topic"],
        "research": research
    })

    return {
        "research": research,
        "report": report,
        "revision_count": 0
    }

 

# -----------------------------
# Node 4 - Critic
# -----------------------------

def critic_node(state: ResearchState):

    print("\n" + "=" * 50)
    print("STEP 4 - CRITIC")
    print("=" * 50)

    feedback = critic_chain.invoke({
        "report": state["report"]
    })

    return {
        "feedback": feedback
    }


# -----------------------------
# Node 5 - Fact Checker
# -----------------------------

def fact_checker_node(state: ResearchState):

    print("\n" + "=" * 50)
    print("STEP 5 - FACT CHECKER")
    print("=" * 50)

    fact_check = fact_checker_chain.invoke({
        "topic": state["topic"],
        "research": state["research"][:2500],
        "report": state["report"][:2500]
    })

    return {
        "fact_check": fact_check
    }


# -----------------------------
# Node 6 - Revision
# -----------------------------

def revision_node(state: ResearchState):

    print("\n" + "=" * 50)
    print("STEP 6 - REVISION")
    print("=" * 50)

    revision_count = state.get("revision_count", 0) + 1

    combined_feedback = (
        f"CRITIC FEEDBACK:\n{state['feedback'][:1500]}\n\n"
        f"FACT CHECK:\n{state['fact_check'][:2000]}"
    )

    revised_report = revision_chain.invoke({
        "topic": state["topic"],
        "report": state["report"][:3500],
        "feedback": combined_feedback
    })

    print(f"\nRevision attempt: {revision_count}")

    return {
        "revised_report": revised_report,
        "revision_count": revision_count
    }


# -----------------------------
# Node 7 - Quality Check
# -----------------------------

def quality_check_node(state: ResearchState):

    print("\n" + "=" * 50)
    print("STEP 7 - QUALITY CHECK")
    print("=" * 50)

    decision = quality_check_chain.invoke({
        "topic": state["topic"],
        "report": state["revised_report"][:3000],
        "feedback": state["feedback"],
        "fact_check": state["fact_check"][:1500]
    })

    decision = decision.strip().upper()

    print("\nQuality decision:", decision)

    return {
        "quality_decision": decision
    }


# -----------------------------
# Conditional Router
# -----------------------------

def quality_router(state: ResearchState):

    revision_count = state.get("revision_count", 0)

    if "PASS" in state["quality_decision"]:
        return "end"

    if revision_count >= 2:
        print("\nMaximum revision limit reached.")
        return "end"

    return "revise"


# -----------------------------
# Build LangGraph
# -----------------------------

graph = StateGraph(ResearchState)

graph.add_node("search", search_node)
graph.add_node("document_researcher", document_researcher_node)
graph.add_node("reader", reader_node)
graph.add_node("writer", writer_node)
graph.add_node("critic", critic_node)
graph.add_node("fact_checker", fact_checker_node)
graph.add_node("revision", revision_node)
graph.add_node("quality_check", quality_check_node)


# Main flow

graph.add_edge(START, "search")

graph.add_edge("search", "reader")

graph.add_edge("reader", "document_researcher")

graph.add_edge("document_researcher", "writer")


graph.add_edge("writer", "critic")

graph.add_edge("critic", "fact_checker")

graph.add_edge("fact_checker", "revision")

graph.add_edge("revision", "quality_check")


# Conditional loop

graph.add_conditional_edges(
    "quality_check",
    quality_router,
    {
        "revise": "revision",
        "end": END
    }
)


# Compile graph

research_graph = graph.compile()


# -----------------------------
# Run Pipeline
# -----------------------------

def run_research_pipeline(topic: str) -> dict:

    result = research_graph.invoke({
        "topic": topic,
        "revision_count": 0
    })

    print("\n" + "=" * 50)
    print("RESEARCH PIPELINE COMPLETED")
    print("=" * 50)

    print("\nTotal revisions:", result.get("revision_count", 0))

    print("\nFinal quality decision:")
    print(result.get("quality_decision", "N/A"))

    print("\nFINAL REVISED REPORT:\n")
    print(result["revised_report"])

    return result


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)