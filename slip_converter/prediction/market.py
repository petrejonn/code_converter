from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd


from abc import ABC, abstractmethod

class Market(ABC):
    def __init__(self,  prediction: str, driver: WebElement, game: tuple, action, matchsFilePath: str):
        self._prediction = prediction
        self._driver = driver
        self._action = action
        self._game = game
        _c,_t = self._getCatNTour(game, matchsFilePath)
        self._matchCategory = _c
        self._matchTournament = _t
        self._openMatch()

    def _getCatNTour(self, game: tuple, filePath: str)->tuple:
        df = pd.read_csv("slip_converter/"+filePath, sep="\t")
        idx = df['match'].str.contains(game[0]) & df['match'].str.contains(game[1])
        nprow =  df.loc[idx].values
        assert(nprow.size > 0)
        self._game = tuple(nprow[0][2].split("--v--"))
        return (nprow[0][0],nprow[0][1])
    
    @abstractmethod
    def _openMatch(self)->None:
        pass

    @property
    @abstractmethod
    def shortCode(self)->str:
        pass

    @abstractmethod
    def predict(self, prediction: str)->None:
        pass

class OneXTwo(Market):
    pass

class DoubleChance(Market):
    pass

class GGNG(Market):
    pass

class FirstGoal(Market):
    pass

class LastGoal(Market):
    pass

class DNB(Market):
    pass
    
class HNB(Market):
    pass

class ANB(Market):
    pass

class Handicap01(Market):
    pass

class Handicap02(Market):
    pass

class Handicap10(Market):
    pass

class Handicap20(Market):
    pass

class WinMargin(Market):
    pass

class OU05(Market):
    pass

class OU15(Market):
    pass

class OU25(Market):
    pass

class OU35(Market):
    pass

class OU45(Market):
    pass

class OU55(Market):
    pass

class OU65(Market):
    pass

class OU75(Market):
    pass

class HomeOU05(Market):
    pass

class HomeOU15(Market):
    pass

class HomeOU25(Market):
    pass

class HomeOU35(Market):
    pass

class HomeOU45(Market):
    pass

class HomeOU55(Market):
    pass

class AwayOU05(Market):
    pass

class AwayOU15(Market):
    pass

class AwayOU25(Market):
    pass

class AwayOU35(Market):
    pass

class AwayOU45(Market):
    pass

class AwayOU55(Market):
    pass

class TotalGoals(Market):
    pass