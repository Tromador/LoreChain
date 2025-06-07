# lc_core/chain_manager.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from .memory_manager import VectorStoreMemory
from .config import DEFAULT_SESSION_ID, OPENAI_API_KEY


class ChainManager:
    def __init__(self, memory: VectorStoreMemory):
        self.memory = memory
        self.session_id = DEFAULT_SESSION_ID

        self.llm = ChatOpenAI(api_key=OPENAI_API_KEY)

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""
You are a helpful assistant.
Use the following context to answer the question.
If the context is irrelevant or unhelpful, answer from general knowledge.

Context:
{context}

Question:
{question}
""".strip(),
        )

        self.chain = (
            {"context": self.retrieve_context, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )

    def retrieve_context(self, question: str) -> str:
        results = self.memory.search(question, k=5, session_id=self.session_id)
        return "\n\n".join([doc.page_content for doc in results])

    def run(self, user_input: str) -> str:
        response = self.chain.invoke(user_input)
        return response.content if hasattr(response, "content") else str(response)
