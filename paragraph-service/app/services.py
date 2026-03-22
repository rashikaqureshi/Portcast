import requests
from collections import Counter
from requests.exceptions import RequestException

from sqlalchemy import or_, and_

from .models import Paragraph
from .utils import extract_words, definition_cache
from .config import STOP_WORDS, METAPHOR_API_URL, DICTIONARY_API_BASE_URL


def fetch_and_store_paragraph(db):
    try:
        response = requests.get(METAPHOR_API_URL)

        if response.status_code != 200:
            raise Exception("Failed API call")

        text = response.text

        if not text:
            raise Exception("Empty response")

    except RequestException:
        raise Exception("External API failed")

    paragraph = Paragraph(content=text)
    db.add(paragraph)
    db.commit()
    db.refresh(paragraph)

    return paragraph


def search_paragraphs(db, words_list, operator):
    query = db.query(Paragraph)

    conditions = [
        Paragraph.content.ilike(f"%{word}%")
        for word in words_list
    ]

    if operator == "or":
        query = query.filter(or_(*conditions))
    else:
        query = query.filter(and_(*conditions))

    return query.all()


def get_all_paragraphs(db):
    return db.query(Paragraph).all()


def compute_top_words(paragraphs, n=10):
    all_words = []

    for p in paragraphs:
        words = extract_words(p.content)
        words = [w for w in words if w not in STOP_WORDS]
        all_words.extend(words)

    return Counter(all_words).most_common(n)


def get_word_definition(word):
    if word in definition_cache:
        return definition_cache[word]

    try:
        url = f"{DICTIONARY_API_BASE_URL}/{word}"
        response = requests.get(url)
        data = response.json()

        if not data:
            raise ValueError("Empty response")

        definition = data[0]["meanings"][0]["definitions"][0]["definition"]

    except (RequestException, KeyError, IndexError, ValueError):
        definition = "No definition found"

    definition_cache[word] = definition
    return definition