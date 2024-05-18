"""
Gemini DM

Gemini AI based dungeon master
"""
import logging

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

import os
import random
import uuid
from pathlib import Path
import re

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from player import Player
# from models.player import PlayerSession

import logging
logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("gdm_server")

class GeminiDM:
    def __init__(self, agent=False):
        self.dm_id = str(uuid.uuid4()).replace("-", "")
        self.instruction_prompt_path = Path("prompts/dmstart.txt") if not agent else Path("prompts/dmagent.txt")
        self.story_path = Path("data/story.txt")
        self.player = None
        
        self.conversation = None
        self.chain_recorder = None
        self.session_id = None
        self.history = None
        self.hkey_prefix = None
        self.memory = None
        self.embedding = None
        self.campaign_file = Path(f"data/campaign{random.randint(1,8)}.txt")

        # setup llm
        self.use_llm = os.environ["LLM_MODEL"]
        llm_provider = os.environ["LLM_PROVIDER"]
        llm_model = os.environ["LLM_MODEL"]
        llm_embedding_model = os.environ["LLM_EMBEDDING_MODEL"]
        if llm_provider == "google":
            self.llm = ChatGoogleGenerativeAI(temperature=0.7, model=llm_model)
            self.embedding = VertexAIEmbeddings(model_name=llm_embedding_model)
        elif llm_provider == "openai":
            self.llm = ChatOpenAI(temperature=0.3, model=llm_model)
            self.embedding = OpenAIEmbeddings(model=llm_embedding_model)

    def chat(self, user_msg: str, session_id: str = None, player: Player=None, use_llm: str=os.environ["LLM_MODEL"]) -> str:
        """
        Initialize conversation and memory per session
        Initialize player information, if needed
        """
        if not session_id:
            self.session_id = str(uuid.uuid4()).replace("-", "")

            # redo: add database lookup for player generation
            # connect player or player character to session
            logger.info(f"Creating new player [session: {self.session_id}]")
            self.player = Player()
        else:
            self.session_id = session_id
            self.player = player

        # setup redis chat history
        logger.info(f"Loading redis history @ main_{self.session_id}")
        self.hkey_prefix = f"main_{self.session_id}"
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
        logger.info(f"Loading conversation history")
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=10,
            chat_memory=self.history
        )
        
        # randomly pick campaign
        campaign_txt = ""
        with open(self.campaign_file) as ctf:
            for cline in ctf.readlines():
                campaign_txt += cline

        # setup instruction prompt
        prompt_txt = ""
        with open(self.instruction_prompt_path) as txtfile:
            for tline in txtfile.readlines():
                if re.findall(r"Synopsis\:$", tline):
                    prompt_txt += tline
                    prompt_txt += f"\n{campaign_txt}\n"
                else:
                    prompt_txt += tline

        # build prompt with player information and 
        # for the chat buffer
        # have to reformat dict as conversationchain will mistake
        # it as a template variable
        prompt_txt += f"""
        Player Stats:
        {{{self.player.player_info()}}}
        Player Items:
        {", ".join(self.player.inventory)}"""

        logger.info(prompt_txt)

        prompt_txt += """
        Current Conversation:
        {history}
        
        Human: {input}
        AI:"""

        # print(f"prompt_txt: {prompt_txt}")

        self.instruction_prompt_template = PromptTemplate(
            input_variables=["history", "input"], template=prompt_txt
        )

        try:
            logger.info("Creating conversation chain and invoking")
            # creating llm chain
            self.conversation = ConversationChain(
                llm=self.llm,
                prompt=self.instruction_prompt_template,
                memory=self.memory,
                verbose=True,
            )

            resp = self.conversation.invoke(user_msg)
            logger.info(f"ai raw response: {resp['response']}")
        except Exception as err:
            logger.error(f"chaining and invoking failed: {err}")
            raise
            
        return resp["response"]
