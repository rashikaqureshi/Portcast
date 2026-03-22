from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .services import (
    fetch_and_store_paragraph,
    search_paragraphs,
    compute_top_words,
    get_word_definition,
    get_all_paragraphs,
)

router = APIRouter()


@router.get("/fetch")
def fetch_paragraph(db: Session = Depends(get_db)):
    paragraph = fetch_and_store_paragraph(db)

    if not paragraph or not paragraph.content:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch paragraph",
        )

    return {
        "id": paragraph.id,
        "content": paragraph.content,
    }


@router.get("/search")
def search(words: str, operator: str, db: Session = Depends(get_db)):

    if not words:
        raise HTTPException(status_code=400, detail="words required")

    if operator not in ["and", "or"]:
        raise HTTPException(status_code=400, detail="invalid operator")

    words_list = [w.strip().lower() for w in words.split(",")]

    results = search_paragraphs(db, words_list, operator)

    return [
        {"id": p.id, "content": p.content}
        for p in results
    ]


@router.get("/dictionary")
def dictionary(db: Session = Depends(get_db)):

    paragraphs = get_all_paragraphs(db)

    if not paragraphs:
        return []

    top_words = compute_top_words(paragraphs)

    results = []

    for word, count in top_words:
        definition = get_word_definition(word)

        results.append(
            {
                "word": word,
                "count": count,
                "definition": definition,
            }
        )

    return results