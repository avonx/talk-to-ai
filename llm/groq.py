from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import os
import time

from dotenv import load_dotenv

load_dotenv()

with open(os.environ.get("PROMPT_PATH"), "r") as file:
    template = file.read().strip()

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)


class Groq:
    def __init__(self):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.model_name = os.environ.get("GROQ_MODEL_NAME")
        self.memory_length = 100
        self.groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name,
            temperature=os.environ.get("GROQ_TEMPERATURE"),
        )
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.groq_chat, memory=self.memory, prompt=PROMPT, verbose=True
        )

    def generate_response(self, user_message):
        start_time = time.time()
        response = self.conversation.predict(input=user_message)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"LLM elapsed time: {elapsed_time:.2f} seconds")
        return response
