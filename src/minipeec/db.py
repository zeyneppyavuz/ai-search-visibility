from pathlib import Path

import yaml
from sqlmodel import Field, Session, SQLModel, create_engine

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DB_PATH = DATA_DIR / "minipeec.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


class PromptDB(SQLModel, table=True):
    __tablename__ = "prompts"

    id: str = Field(primary_key=True)
    text: str
    intent: str
    language: str


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def seed_prompts():
    with open(DATA_DIR / "prompts.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    added = 0
    with Session(engine) as session:
        for p in data["prompts"]:
            if session.get(PromptDB, p["id"]) is None:
                session.add(PromptDB(**p))
                added += 1
        session.commit()
    return added