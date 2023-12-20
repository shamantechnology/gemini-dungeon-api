"""
Gemini DM

Gemini AI based dungeon master
"""
import logging

logging.basicConfig(format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

from pathlib import Path
from concurrent.futures import as_completed

import faiss

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import VertexAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
from langchain.memory import VectorStoreRetrieverMemory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from trulens_eval import Feedback, LiteLLM, TruChain

from player import Player


class GeminiDM:
    def __init__(self, player: any = None):
        self.instruction_prompt_path = Path("prompts/dmstart.txt")
        self.story_path = Path("data/story.txt")
        self.player = player if player else Player()
        self.llm = ChatGoogleGenerativeAI(temperature=0.1, model="gemini-pro")
        self.conversation = None
        self.chain_recorder = None

        # setup logging
        self.class_logger = logging.getLogger(__name__)
        self.class_logger.setLevel(logging.DEBUG)

        # get story
        story_txt = ""
        with open(self.story_path) as txtfile:
            for tline in txtfile.readlines():
                story_txt += tline

        # setup instruction prompt
        prompt_txt = ""
        with open(self.instruction_prompt_path) as txtfile:
            for tline in txtfile.readlines():
                prompt_txt += tline

        self.instruction_prompt_template = PromptTemplate(
            input_variables=["history", "input"], template=prompt_txt
        )

        # self.memory = ConversationBufferMemory()

        # print(self.instruction_prompt_template)

        # self.instruction_prompt = self.instruction_prompt_template.format(
        #     player=self.player.player_sheet(), history=""
        # )

        # setup chat vectorstore
        # this is using faiss-cpu
        embedding_size = 768
        self.vectorstore = FAISS(
            VertexAIEmbeddings().embed_query,
            # HuggingFaceEmbeddings().embed_query,
            faiss.IndexFlatL2(embedding_size),
            InMemoryDocstore({}),
            {},
        )

        # setup memory
        retriever = self.vectorstore.as_retriever(search_kwargs=dict(k=1))
        self.memory = VectorStoreRetrieverMemory(
            retriever=retriever
        )

        self.memory.save_context(
            {"System": f"Player Information\n{self.player.player_sheet()}"}, {"AI": ""}
        )


        self.memory.save_context(
            {"System": f"The story\n{story_txt}"}, {"AI": ""}
        )

        # creating llm chain
        self.conversation = ConversationChain(
            llm=self.llm,
            prompt=self.instruction_prompt_template,
            memory=self.memory,
            verbose=True,
        )

        # setup trulens
        feedbacks = []

        # use conciseness feedback
        litellm_provider = LiteLLM(model_engine="chat-bison")
        feedbacks.append(Feedback(litellm_provider.conciseness).on_output())

        # self.chain_recorder = TruChain(
        #     self.conversation,
        #     app_id="med-coder-llm",
        #     feedbacks=feedbacks
        # )

    def chat(self, user_msg: str) -> str:
        """
        String input to gemini chat from user
        Record chat interaction and test for conciseness with TruLens
        """
        # tru_record = None
        # with self.chain_recorder as recorder:
        resp = self.conversation.invoke(user_msg)
        #     tru_record = recorder.get()

        # conciseness_val = 1.0
        # if tru_record:
        #     for feedback_future in as_completed(tru_record.feedback_results):
        #         feedback, feedback_result = feedback_future.result()

        #         if feedback.name == "conciseness":
        #             conciseness_val = (
        #                 float(feedback_result.result) if feedback_result.result else 1.0
        #             )

        # if conciseness_val < 0.5:
        #     return "I don't not understand...."
        # else:
        return resp["response"]
