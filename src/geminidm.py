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
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.chains import ConversationChain

from player import Player
# from models.player import PlayerSession


class GeminiDM:
    def __init__(self):
        self.dm_id = str(uuid.uuid4()).replace("-", "")
        self.instruction_prompt_path = Path("prompts/dmstart.txt")
        self.story_path = Path("data/story.txt")
        self.player = None
        self.player_sessions = {} # replace with database
        self.llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro")
        self.conversation = None
        self.chain_recorder = None
        self.session_id = None
        self.history = None
        self.hkey_prefix = None
        self.memory = None
        self.embedding = None
        self.campaign_file = Path(f"data/campaign{random.randint(1,8)}.txt")

        # setup logging
        self.class_logger = logging.getLogger(__name__)
        self.class_logger.setLevel(logging.DEBUG)

    def chat(self, user_msg: str, session_id: str = None, player: Player=None) -> str:
        """
        Initialize conversation and memory per session
        Initialize player information, if needed
        """
        if not session_id:
            self.session_id = str(uuid.uuid4()).replace("-", "")

            # redo: add database lookup for player generation
            # connect player or player character to session
            self.class_logger.info(f"Creating new player [session: {self.session_id}]")
            self.player = Player()

            self.player_sessions[self.session_id] = self.player
        else:
            self.session_id = session_id
            self.player = player

        # setup redis chat history
        self.hkey_prefix = f"message_store_{self.session_id}"
        self.history = RedisChatMessageHistory(
            url=os.environ["REDIS_URL"], 
            session_id=self.session_id, 
            key_prefix=self.hkey_prefix
        )
        # setup memory
        self.memory = ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=10, chat_memory=self.history)
        self.embedding = VertexAIEmbeddings(model_name="textembedding-gecko@001") # make changable
        
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
        Player Info:
        {{{self.player.player_info()}}}\n"""

        prompt_txt += """
        Current Conversation:
        {history}
        
        Human: {input}
        AI:"""

        self.instruction_prompt_template = PromptTemplate(
            input_variables=["history", "input"], template=prompt_txt
        )

        # creating llm chain
        self.conversation = ConversationChain(
            llm=self.llm,
            prompt=self.instruction_prompt_template,
            memory=self.memory,
            verbose=True,
        )

        resp = self.conversation.invoke(user_msg)
        self.class_logger.info(f"ai raw response: {resp['response']}")
        
        return resp["response"]


    # def chat(self, user_msg: str) -> str:
    #     """
    #     String input to gemini chat from user
    #     Record chat interaction and test for conciseness with TruLens
    #     """
    #     resp = self.conversation.invoke(user_msg)
    #     self.class_logger.info(f"ai raw response: {resp['response']}")
    #     return resp["response"]
