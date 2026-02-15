from abc import abstractmethod, ABC

from board.domain.entity.board import Board


class BoardService(ABC):

    @abstractmethod
    def create_board(self, account_id: int, title: str, content: str) -> Board:
        pass
