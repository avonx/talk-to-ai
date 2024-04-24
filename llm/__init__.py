from .groq import Groq
from .anthropic import Anthropic


class LanguageModel:
    def __init__(self, llm_type):
        if llm_type == "groq":
            self.llm = Groq()
        elif llm_type == "anthropic":
            self.llm = Anthropic()
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

    def generate_response(self, user_message):
        return self.llm.generate_response(user_message)
