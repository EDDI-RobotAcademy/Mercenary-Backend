from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from board.domain.entity.board import Board


class BoardRepository(ABC):

    @abstractmethod
    def save(self, session: Session, board: Board) -> Board:
        pass
