from typing import List, Any

from sqlalchemy.orm import Session

from account.domain.entity.account import Account
from board.domain.entity.board import Board
from board.repository.board_repository_impl import BoardRepositoryImpl
from account.repository.account_repository_impl import AccountRepositoryImpl
from board.service.board_service import BoardService
from config.mysql_config import MySQLConfig


class BoardServiceImpl(BoardService):

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

    def __init__(self):
        self.board_repository = BoardRepositoryImpl.get_instance()
        self.account_repository = AccountRepositoryImpl.get_instance()

    def create_board(self, account_id: int, title: str, content: str) -> Board:

        session: Session = MySQLConfig().get_session()

        try:
            account = session.get(Account, account_id)

            if not account:
                raise ValueError("Account not found")

            board = Board.create(account_id, title, content)

            self.board_repository.save(session, board)

            session.commit()

            return board

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def list_boards(self, page: int = 1, page_size: int = 10) -> list[Board]:
        if page < 1:
            page = 1

        offset = (page - 1) * page_size
        session = MySQLConfig().get_session()
        try:
            boards = self.board_repository.find_all(session, offset=offset, limit=page_size)
            return boards
        finally:
            session.close()

