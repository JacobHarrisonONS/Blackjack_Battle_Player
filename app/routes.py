from fastapi import APIRouter, Depends

from app.dependencies import get_player_state
from app.logic import take_turn
from app.models.blackjack_models import ManualConnect, BlackjackTurn
from app.player_state import PlayerState

router = APIRouter()


@router.get("/")
async def root():
    """
    root endpoint
    :return:
    """
    return {"message": "Hello from blackjack player"}


@router.get("/connect")
async def connect(
    manual_connect: ManualConnect, player_state: PlayerState = Depends(get_player_state)
):
    """
    Manual connect endpoint, request received from blackjack controller
    :param manual_connect:
    :param player_state:
    :return:
    """
    player_state.set_player_id(manual_connect.player_id)
    return {"nickname": player_state.nickname, "player_id": manual_connect.player_id}


@router.get("/connection-check")
async def connection_check(player_state: PlayerState = Depends(get_player_state)):
    """
    Used by blackjack service to ensure this player is still connected.
    :param player_state:
    :return:
    """
    print("Received connection check")
    return {"player_id": player_state.player_id}


@router.post("/turn")
async def turn(blackjack_turn: BlackjackTurn):
    """
    Primary endpoint for blackjack player, receive game and player state, return either Stand or Hit
    :param blackjack_turn:
    :return:
    """
    choice = take_turn(blackjack_turn)
    return {"action": choice}
