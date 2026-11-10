
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logger = logging.getLogger(__name__)

# Model configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e2b")


# Primary LLM: Groq
groq_llm = None

if GROQ_API_KEY:
    groq_llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,
        max_retries=0,
    )


# Fallback LLM: Local Ollama
local_llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0,
    num_ctx=16384,
    keep_alive="10m",
)


class FallbackLLM:
    """Try Groq first. Automatically switch to Ollama on failure."""

    def __init__(self, primary, fallback):
        self.primary = primary
        self.fallback = fallback

    def invoke(self, input, config=None, **kwargs):

        if self.primary is not None:
            try:
                logger.info("Using primary LLM: Groq")

                response = self.primary.invoke(
                    input,
                    config=config,
                    **kwargs
                )

                logger.info("Groq response received successfully")
                return response

            except Exception as exc:
                logger.warning(
                    "Groq failed: %s. Switching to Ollama.",
                    exc
                )

        logger.warning(
            "Using fallback LLM: Ollama (%s)",
            OLLAMA_MODEL
        )

        try:
            response = self.fallback.invoke(
                input,
                config=config,
                **kwargs
            )

            logger.info("Ollama response received successfully")
            return response

        except Exception as fallback_error:
            logger.exception("Both LLM providers failed")

            raise RuntimeError(
                f"Groq and Ollama both failed. "
                f"Fallback error: {fallback_error}"
            ) from fallback_error


# Shared LLM instance used throughout backend.py
llm = FallbackLLM(
    primary=groq_llm,
    fallback=local_llm
)

logger.info(
    "LLM failover configured: Groq -> Ollama (%s)",
    OLLAMA_MODEL
)
