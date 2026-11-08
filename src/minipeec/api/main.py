from contextlib import asynccontextmanager
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from minipeec.db import BrandDB, PromptDB, create_db, get_session


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(title="mini Peec", lifespan=lifespan)


@app.get("/health", response_model=Health)
def health():
    return {"status": "ok"}


# ---------- Prompts ----------

@app.get("/prompts", response_model=list[Prompt])
def list_prompts(session: Session = Depends(get_session)):
    return session.exec(select(PromptDB)).all()


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str, session: Session = Depends(get_session)):
    prompt = session.get(PromptDB, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt: Prompt, session: Session = Depends(get_session)):
    if session.get(PromptDB, prompt.id) is not None:
        raise HTTPException(status_code=409, detail="Prompt id already exists")
    db_prompt = PromptDB(**prompt.model_dump(mode="json"))
    session.add(db_prompt)
    session.commit()
    session.refresh(db_prompt)
    return db_prompt


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str, session: Session = Depends(get_session)):
    prompt = session.get(PromptDB, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    session.delete(prompt)
    session.commit()


# ---------- Brands ----------

@app.get("/brands", response_model=list[Brand])
def list_brands(session: Session = Depends(get_session)):
    return session.exec(select(BrandDB)).all()


@app.get("/brands/{brand_id}", response_model=Brand)
def get_brand(brand_id: str, session: Session = Depends(get_session)):
    brand = session.get(BrandDB, brand_id)
    if brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand