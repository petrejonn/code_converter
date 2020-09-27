from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import market
from exceptions import PredictionNoFoundException, MarketNotFoundException


class SportybetMarketMixin(object):
    def _openMatch(self)->None:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sport-list"))
            )
        finally:
            games_list = self._driver.find_element_by_class_name("sport-list")
        categories_list = games_list.find_elements_by_class_name("category-list-item")
        category: WebElement
        for cat in categories_list:
            category_item = cat.find_element_by_class_name("category-item")
            category_span = category_item.find_elements_by_tag_name("span")[0]
            if self._matchCategory in category_span.text:
                category = cat
                break
        self._action.move_to_element(category).perform()
        tournament_list = category.find_elements_by_class_name("tournament-list-item")
        for tournament in tournament_list:
            if self._matchTournament == tournament.find_element_by_class_name("tournament-name").text.strip():
                tournament.click()
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "teams"))
            )
        finally:
            games = self._driver.find_elements_by_class_name("teams")
            for game in games:
                home = game.find_element_by_class_name("home-team").text.strip()
                away = game.find_element_by_class_name("away-team").text.strip()
                if self._game[0] in home and self._game[1] in away:
                    game.click()
                    break

    def predict(self, prediction: str)->None:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m-table__wrapper"))
            )
        finally:
            market_found = False
            prediction_found = False
            pred_types = self._driver.find_elements_by_class_name("m-table__wrapper")
            for pred_type in pred_types:
                if pred_type.find_element_by_class_name("m-table-header-title").text.strip().lower() == self.shortCode.lower():
                    market_found = True
                    outcomes = pred_type.find_element_by_class_name("m-outcome").find_elements_by_class_name("m-table-cell")
                    for outcome in outcomes:
                        if outcome.find_element_by_tag_name("span").text.strip().lower() == self._prediction.lower():
                            prediction_found = True
                            outcome.click()
                            break
                    if not prediction_found:
                        raise PredictionNoFoundException("prediction "+self._prediction+" Not Found")
            if not market_found:
                raise MarketNotFoundException("market "+self.shortCode+" Not Found")


class OneXTwo(SportybetMarketMixin, market.OneXTwo):
    @property
    def shortCode(self)->str:
        return "1X2"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class DoubleChance(SportybetMarketMixin, market.DoubleChance):
    @property
    def shortCode(self)->str:
        return "Double Chance"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class GGNG(SportybetMarketMixin, market.DoubleChance):
    @property
    def shortCode(self)->str:
        return "GG/NG"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class FirstGoal(SportybetMarketMixin, market.FirstGoal):
    @property
    def shortCode(self)->str:
        return "First Goal"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class LastGoal(SportybetMarketMixin, market.LastGoal):
    @property
    def shortCode(self)->str:
        return "Last Goal"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class DN (SportybetMarketMixin, market.DNB):
    @property
    def shortCode(self)->str:
        return "DNB"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class HNB(SportybetMarketMixin, market.HNB):
    @property
    def shortCode(self)->str:
        return "HNB"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class ANB(SportybetMarketMixin, market.ANB):
    @property
    def shortCode(self)->str:
        return "ANB"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)

class Handicap01(SportybetMarketMixin, market.Handicap01):
    @property
    def shortCode(self)->str:
        return "Handicap 1:0"

    def predict(self, prediction: str)->None:
        SportybetMarketMixin.predict(self, prediction)