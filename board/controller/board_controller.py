from fastapi import Cookie
from authentication.service.authentication_service_impl import AuthenticationServiceImpl

from fastapi import APIRouter, Depends, HTTPException

from board.controller.request.create_board_request import CreateBoardRequest
from board.service.board_service_impl import BoardServiceImpl


board_router = APIRouter(prefix="/board")

def inject_board_service() -> BoardServiceImpl:
    return BoardServiceImpl.get_instance()

def inject_auth_service() -> AuthenticationServiceImpl:
    return AuthenticationServiceImpl.get_instance()


def get_authenticated_account_id(
    userToken: str = Cookie(None),
    auth_service: AuthenticationServiceImpl = Depends(inject_auth_service),
) -> int:

    if not userToken:
        raise HTTPException(status_code=401, detail="Authentication required")

    account_id = auth_service.validate_session(userToken)

    if not account_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    return account_id

@board_router.post("/create")
def create_board(
    request: CreateBoardRequest,
    account_id: int = Depends(get_authenticated_account_id),
    board_service: BoardServiceImpl = Depends(inject_board_service),
):
    try:
        board = board_service.create_board(
            account_id=account_id,
            title=request.title,
            content=request.content,
        )

        return {
            "id": board.id,
            "title": board.title,
            "content": board.content,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))