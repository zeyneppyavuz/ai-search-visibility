import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from minipeec.api.main import app
from minipeec.db import BrandDB, PromptDB, get_session


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([
            PromptDB(id="t1", text="Best bank for expats?", intent="commercial", language="en"),
            PromptDB(id="t2", text="Revolut vs N26?", intent="comparison", language="en"),
            BrandDB(id="n26", name="N26", aliases=["N26", "N26 Bank"], domain="n26.com"),
            BrandDB(id="revolut", name="Revolut", aliases=["Revolut"], domain="revolut.com"),
        ])
        session.commit()
        yield session


@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()