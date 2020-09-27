from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from slip_converter.bookmakers.core import BookMaker
from slip_converter.game import FootBallGame
from slip_converter.support import marketFactory, serializePrediction
import sys
sys.path.append("..")


class Bet9ja(BookMaker):
    def __init__(self):
        self._footBallBaseUrl = "https://web.bet9ja.com/Sport/Default.aspx"
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
        market = game[1].lower()
        pred_ = serializePrediction(game[2])
        marketType = marketFactory(market, "bet9ja")
        prediction = marketType(
            pred_, self._driver, game_, self._action, 'data/bet9jamatches.csv')
        game = FootBallGame(game_[0], game_[1], pred_, prediction)
        game.makePrediction()
    
    def bookGames(self, games: tuple) -> None:
        for game in games:
            self._bookGame(game)


    def getBookingCode(self) -> str:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btnCoupon.dx"))
            )
        finally:
            self._driver.find_element_by_class_name("btnCoupon.dx").click()
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "iframePrenotatoreSco"))
                )
            finally:
                self._driver.switch_to.frame("iframePrenotatoreSco")
                code_span = self._driver.find_element_by_class_name("number")
                code = code_span.find_element_by_tag_name("span").text.strip()
                self._driver.switch_to.default_content()
                return code

    @classmethod
    def loadCode(cls, code: str) -> tuple:
        instance = cls()
        instance._insertCode(code)
        return instance.getBookingGames()

    def _insertCode(self, code: str) -> None:
        self._reloadBaseUrl()
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "divNumPrenotato"))
            )
        finally:
            code_area_wrapper = self._driver.find_element_by_class_name("divNumPrenotato")
            code_area = code_area_wrapper.find_element_by_class_name("value")
            code_area.find_element_by_tag_name("input").send_keys(code)
            code_area.find_element_by_tag_name("a").click()

    def getBookingGames(self) -> tuple:
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
                EC.presence_of_element_located((By.CLASS_NAME, "CItem"))\
                or EC.presence_of_element_located((By.CLASS_NAME, "CItem"))
            )
        finally:
            games =  self._driver.find_elements_by_class_name("CItem")
            for game_element in games:
                home, away = self._getBetslipHomeTeam(game_element)
                prediction = self._getBetslipPrediction(game_element)
                market = self._getBetslipMarket(game_element)
                odds = self._getBetslipOdds(game_element)
                self._betslipGames.append([(home, away), market, prediction, odds])

    def _getBetslipHomeTeam(self, webElement: WebElement) -> str:
        teams = webElement.find_element_by_class_name("CSubEv")
        teamsRawText = teams.find_element_by_tag_name(
            "span").text
        print(teamsRawText)
        teamsRawText = teamsRawText.strip().split(" - ")
        return (teamsRawText[0], teamsRawText[1])

    def _getBetslipAwayTeam(self, webElement: WebElement) -> str:
        pass

    def _getBetslipPrediction(self, webElement: WebElement) -> str:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "CSegno"))
            )
        finally:
            prediction = webElement.find_element_by_class_name("CSegno").text.strip().split()[0]
            return prediction

    def _getBetslipMarket(self, webElement: WebElement) -> str:
        market = webElement.find_element_by_class_name("CqSegno").text.strip()
        return market

    def _getBetslipOdds(self, webElement: WebElement) -> str:
        odds = webElement.find_element_by_class_name("valQuota_1").text.strip()
        return odds