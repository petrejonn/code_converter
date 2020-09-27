from slip_converter.scrap.sportybet import SportybetMatchScraper
from slip_converter.scrap.bet9ja import Bet9jaMatchScraper
from slip_converter.scrap.betking import BetkingMatchScraper


def scrapeBet9ja():
    inst = Bet9jaMatchScraper()
    inst.scrape()

def scrapeSportybet():
    inst = SportybetMatchScraper()
    inst.scrape()

def scrapeBetking():
    inst = BetkingMatchScraper()
    inst.scrape()