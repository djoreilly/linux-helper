import os

MODEL = os.getenv("GOOGLE_GENAI_MODEL")
if not MODEL:
    MODEL = "gemini-2.5-flash"

# MODEL needs to be defined before this import
from . import agent  # pylint: disable=wrong-import-position
