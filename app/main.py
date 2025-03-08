from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends

from app.dependencies import get_player_state
from app.models.blackjack_models import BlackjackTurn
from app.player_state import PlayerState
from app.startup import start_up_connect


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Starting Blackjack-Player")

    start_up_connect(
        game_url="http://127.0.0.1:5000",
        own_url="http://127.0.0.1:5001",
        player_state=get_player_state(),
    )

    yield

    print("Shutting down player")


app = FastAPI(title="Blackjack-Battle-Player", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello from blackjack player"}


@app.get("/connection-check")
async def connection_check(player_state: PlayerState = Depends(get_player_state)):
    print("Received connection check")
    return {"player_id": player_state.player_id}


@app.post("/turn")
async def turn(blackjack_turn: BlackjackTurn):
    print("Received turn data")
    return {"message": "Received turn data!"}


def start():
    """
    Start a uvicorn server using the FastAPI app
    :return:
    """
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)


def start_dev():
    uvicorn.run("app.main:app", host="127.0.0.1", port=5001, reload=True)
