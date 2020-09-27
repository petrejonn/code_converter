from slip_converter.bookmakers.core import BookMaker


class CodeConverter():
    def __init__(self, init_code: str, from_: BookMaker, to_:BookMaker):
        self._init_code = init_code
        self._from = from_
        self._to = to_
    
    def convert(self)->None:
        games = self._from.loadCode(code=self._init_code)
        print(games)
        self._to.bookGames(games)
        self.new_code = self._to.getBookingCode()

    def getNewCode(self)->str:
        return self.new_code