from sqlalchemy.orm import Session
from board.domain.entity.board import Board
from board.repository.board_repository import BoardRepository


class BoardRepositoryImpl(BoardRepository):

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, session: Session, board: Board) -> Board:
        session.add(board)
        return board
