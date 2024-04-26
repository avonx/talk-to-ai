from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import os
import time


class Groq:
    def __init__(self, config, character_config):
        self.groq_api_key = config["groq_api_key"]
        self.model_name = config["groq_model_name"]
        self.memory_length = config["memory_length"]

        with open(character_config["prompt_path"], "r") as file:
            template = file.read().strip()

        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

        self.groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name,
            temperature=config["temperature"],
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
