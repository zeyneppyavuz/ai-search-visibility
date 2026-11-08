from pathlib import Path

import yaml
from sqlalchemy import JSON, Column
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


class BrandDB(SQLModel, table=True):
    __tablename__ = "brands"

    id: str = Field(primary_key=True)
    name: str
    aliases: list[str] = Field(sa_column=Column(JSON))
    domain: str


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def _seed(model, yaml_file, key):
    with open(DATA_DIR / yaml_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    added = 0
    with Session(engine) as session:
        for item in data[key]:
            if session.get(model, item["id"]) is None:
                session.add(model(**item))
                added += 1
        session.commit()
    return added


def seed_prompts():
    return _seed(PromptDB, "prompts.yaml", "prompts")


def seed_brands():
    return _seed(BrandDB, "brands.yaml", "brands")