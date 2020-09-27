from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bookmakers.core import BookMaker
from game import FootBallGame
from support import marketFactory
import sys
sys.path.append("..")


class Sportybet(BookMaker):
    def __init__(self):
        self._footBallBaseUrl = "https://www.sportybet.com/ng/sport/football/"
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        # self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self._driver = webdriver.Chrome(options=chrome_options)
        self._action = ActionChains(self._driver)
        self._reloadBaseUrl()
        self._betslipGames = []

    def _bookGame(self, game: tuple) -> None:
        game_ = game[0]
        market = game[1]
        pred_ = game[2]
        marketType = marketFactory(market, "sportybet")
        prediction = marketType(
            pred_, self._driver, game_, self._action, 'data/sportybetmatches.csv')
        game = FootBallGame(game_[0], game_[1], pred_, prediction)
        game.makePrediction()

    def bookGames(self, games: tuple) -> None:
        for game in games:
            self._bookGame(game)

    def getBookingCode(self) -> str:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "m-share--wrapper"))
            )
        finally:
            share_area = self._driver.find_element_by_class_name(
                "m-share--wrapper")
            share_link = share_area.find_elements_by_tag_name("span")[0]
            share_link.click()
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "m-share-wrapper"))
                )
            finally:
                code_area = self._driver.find_element_by_class_name(
                    "m-share-wrapper")
                code_value = code_area.find_element_by_class_name("m-value")
                code = code_value.text
                return code

    @classmethod
    def loadCode(cls, code: str) -> tuple:
        instance = cls()
        instance._insertCode(code)
        return instance.getBookingGames()

    def _insertCode(self, code: str) -> None:
        """
        @Desc: Insert code into betslip input field of Site
        """
        self._reloadBaseUrl()
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "m-betslip-search"))
            )
        finally:
            code_field_area = self._driver.find_element_by_class_name(
                "m-betslip-search")
            code_field = code_field_area.find_element_by_tag_name("input")
            code_field.send_keys(code)
            code_field_button = code_field_area.find_element_by_tag_name(
                "button")
            code_field_button.click()

    def getBookingGames(self) -> tuple:
        """
        @return: A tuple of all the games in the betslip
        """
        self._serializeBetslipGames()
        return tuple(self._betslipGames)

    def _reloadBaseUrl(self,) -> None:
        self._driver.get(self._footBallBaseUrl)

    def _serializeBetslipGames(self) -> None:
        """
        @Desc: create Game Objects of all games in betslip
        """
        self._betslipGames = []
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m-list"))
            )
        finally:
            game_elements_wrapper = self._driver.find_element_by_class_name(
                "m-list")
            game_elements = game_elements_wrapper.find_elements_by_class_name(
                "m-item")
            for game_element in game_elements:
                home, away = self._getBetslipHomeTeam(game_element)
                prediction = self._getBetslipPrediction(game_element)
                market = self._getBetslipMarket(game_element)
                odds = self._getBetslipOdds(game_element)
                self._betslipGames.append([home, away, market, prediction, odds])

    def _getBetslipHomeTeam(self, webElement: WebElement) -> str:
        teamsRawText = webElement.find_element_by_class_name(
            "m-item-team").text
        teamsRawText = teamsRawText.strip().split()
        return (teamsRawText[-3], teamsRawText[-1])

    def _getBetslipAwayTeam(self, webElement: WebElement) -> str:
        pass

    def _getBetslipPrediction(self, webElement: WebElement) -> str:
        prediction = webElement.find_element_by_class_name("m-item-play")
        return prediction.find_element_by_tag_name("span").text

    def _getBetslipMarket(self, webElement: WebElement) -> str:
        return webElement.find_element_by_class_name("m-item-market").text

    def _getBetslipOdds(self, webElement: WebElement) -> str:
        return webElement.find_element_by_class_name("m-text-main").text
