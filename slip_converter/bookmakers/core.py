from abc import ABC, abstractmethod

from selenium.webdriver.remote.webelement import WebElement


class BookMaker(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _bookGame(self, game: tuple) -> None:
        pass

    @abstractmethod
    def bookGames(self, games: tuple) -> None:
        pass

    @abstractmethod
    def getBookingCode(self) -> str:
        """
        @return: BetSlip Code
        """
        pass

    @classmethod
    @abstractmethod
    def loadCode(cls, code: str) -> tuple:
        """
        @return: tuple of games
        """
        pass

    @abstractmethod
    def _insertCode(self, code: str) -> None:
        """
        @Desc: Insert code into betslip input field of Site
        """
        pass

    @abstractmethod
    def getBookingGames(self) -> tuple:
        """
        @return: A tuple of all the games in the betslip
        """
        pass

    @abstractmethod
    def _reloadBaseUrl(self,) -> None:
        """
        @Desc: re-initialize content of base page
        """
        pass

    @abstractmethod
    def _serializeBetslipGames(self) -> None:
        """
        @Desc: create a Game Object of all games in betslip
        """
        pass

    @abstractmethod
    def _getBetslipHomeTeam(self, webElement: WebElement) -> str:
        pass

    @abstractmethod
    def _getBetslipAwayTeam(self, webElement: WebElement) -> str:
        pass

    @abstractmethod
    def _getBetslipPrediction(self, webElement: WebElement) -> str:
        pass

    @abstractmethod
    def _getBetslipOdds(self, webElement: WebElement) -> str:
        pass

    @abstractmethod
    def _getBetslipMarket(self, webElement: WebElement) -> str:
        pass