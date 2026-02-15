from abc import abstractmethod, ABC
from typing import List

from board.domain.entity.board import Board


class BoardService(ABC):

    @abstractmethod
    def create_board(self, account_id: int, title: str, content: str) -> Board:
        pass

    @abstractmethod
    def list_boards(self, page: int = 1, page_size: int = 10) -> list[Board]:
        pass
