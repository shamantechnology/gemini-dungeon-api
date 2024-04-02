"""
NPC AI Agent
Used for storing unique NPCs created by the DM
Stores conversations for player to continue with
Can be another type of LLM
"""
import os
import uuid

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

import logging
logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("npcagent")

class NPCAgent:
    def __init__(
        self,
        npc_name: str,
        location_name: str,
        npc_class: str,
        npc_race: str,
        npc_gender: str,
        npc_id: str="",
        llm: str="openai"
    ):
        self.npc_name = npc_name
        self.location_name = location_name
        self.npc_id = npc_id if npc_id else str(uuid.uuid4()).replace("-", "")
        
        self.conversation = None
        self.chain_recorder = None
        self.session_id = None
        self.history = None
        self.hkey_prefix = None
        self.memory = None
        self.embedding = None
        
        self.user_session = None

        # setup llm
        if llm == "google":
            self.llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro")
            self.embedding = VertexAIEmbeddings(model_name="textembedding-gecko@001")
        elif llm == "openai":
            self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
            self.embedding = OpenAIEmbeddings(model="text-embedding-ada-002")

    def chat(self, user_msg: str, session_id: str) -> str:
        """
        Initialize conversation and memory per session and npc_id
        """
        self.user_session = session_id

        # setup redis chat history
        self.hkey_prefix = f"npc_{self.session_id}_{self.npc_id}"
        self.history = RedisChatMessageHistory(
            url=os.environ["REDIS_URL"], 
            session_id=self.session_id, 
            key_prefix=self.hkey_prefix
        )

        # check if redis is online
        try:
            self.history.redis_client.ping()
        except Exception as err:
            logging.error(f"Redis is not online: {err}")
            raise

        # setup memory
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=10,
            chat_memory=self.history
        )



        
