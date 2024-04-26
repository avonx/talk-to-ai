from .groq import Groq
from .anthropic import Anthropic


class LanguageModel:
    def __init__(self, llm_type, config, character_config):
        if llm_type == "groq":
            self.llm = Groq(config, character_config)
        elif llm_type == "anthropic":
            self.llm = Anthropic(config, character_config)
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")

    def generate_response(self, user_message):
        return self.llm.generate_response(user_message)
