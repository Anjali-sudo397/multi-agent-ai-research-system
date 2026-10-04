from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag_retrieve import retrieve

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a document question-answering assistant.

Answer the user's question using ONLY the provided document context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not present in the context, say:
  "The answer is not available in the provided documents."
- Keep the answer clear and concise.
"""
    ),
    (
        "human",
        """Question:
{question}

Document Context:
{context}

Answer:"""
    )
])


qa_chain = prompt | llm | StrOutputParser()


def answer_question(question):
    results = retrieve(question)

    context = "\n\n".join(
        f"Source: {result['source']}\n{result['text']}"
        for result in results
    )

    answer = qa_chain.invoke({
        "question": question,
        "context": context
    })

    return answer


if __name__ == "__main__":
    question = input("Ask a question about the documents: ")

    answer = answer_question(question)

    print("\nAnswer:\n")
    print(answer)