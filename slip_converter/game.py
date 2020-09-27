import sys
sys.path.append("..")
from abc import ABC, abstractmethod
from datetime import datetime

from slip_converter.prediction.market import Market


class FootBallGame():
    def __init__(self, home: str, away: str, prediction: str, market:Market, dateTime: datetime = None):
        self._home = home
        self._away = away
        self._dateTime = dateTime
        self._prediction = prediction
        self._market = market

    @property
    def home(self)->str:
        return self._home 
    
    @property
    def away(self)->str:
        return self._away

    @property
    def dateTime(self)->datetime:
        return self._dateTime

    @property
    def prediction(self)->str:
        pass

    def makePrediction(self)->None:
        self._market.predict(self._prediction)
