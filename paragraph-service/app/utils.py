import re
from collections import Counter
from .config import STOP_WORDS

definition_cache = {}
def extract_words(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())
