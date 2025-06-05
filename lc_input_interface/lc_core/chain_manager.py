# lc_core/chain_manager.py

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from .memory_manager import VectorStoreMemory
from .config import DEFAULT_SESSION_ID
from .config import OPENAI_API_KEY

class ChainManager:
    def __init__(self, memory: VectorStoreMemory):
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(api_key=OPENAI_API_KEY),
            retriever=memory.vectorstore.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=False,
        )

    def run(self, user_input: str) -> str:
        return self.qa_chain.run(user_input)
