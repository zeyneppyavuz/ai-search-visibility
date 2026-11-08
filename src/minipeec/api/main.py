from enum import Enum
from pathlib import Path

import yaml
from fastapi import FastAPI
from pydantic import BaseModel

DATA_DIR = Path(__file__).resolve().parents[3] / "data"


class Intent(str, Enum):
    commercial = "commercial"
    comparison = "comparison"
    informational = "informational"


class Prompt(BaseModel):
    id: str
    text: str
    intent: Intent
    language: str


class Brand(BaseModel):
    id: str
    name: str
    aliases: list[str]
    domain: str


class Health(BaseModel):
    status: str


def load_prompts() -> list[Prompt]:
    with open(DATA_DIR / "prompts.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [Prompt(**p) for p in data["prompts"]]


def load_brands() -> list[Brand]:
    with open(DATA_DIR / "brands.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [Brand(**b) for b in data["brands"]]


app = FastAPI(title="mini Peec")


@app.get("/health", response_model=Health)
def health():
    return {"status": "ok"}


@app.get("/prompts", response_model=list[Prompt])
def list_prompts():
    return load_prompts()


@app.get("/brands", response_model=list[Brand])
def list_brands():
    return load_brands()