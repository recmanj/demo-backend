from sqlalchemy.orm import Session
from demo_backend.models import Note

SAMPLE_NOTES = [
    {"title": "Welcome to Notes", "content": "This is a simple notes application. Create, edit, and delete notes as you like."},
    {"title": "Meeting Notes", "content": "Discuss project timeline\nReview sprint goals\nAssign action items"},
    {"title": "Shopping List", "content": "Milk\nBread\nEggs\nCoffee"},
]


def run_seed(db: Session) -> int:
    inserted = 0
    for note_data in SAMPLE_NOTES:
        exists = db.query(Note).filter(Note.title == note_data["title"]).first()
        if not exists:
            db.add(Note(**note_data))
            inserted += 1
    db.commit()
    return inserted
