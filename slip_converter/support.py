from slip_converter.prediction.market import Market

def marketFactory(shortCode:str, bookMaker:str)->Market:
    if bookMaker == "sportybet":
        from slip_converter.prediction import sportybet as module
    elif bookMaker == "bet9ja":
        from slip_converter.prediction import bet9ja as module
    elif bookMaker == "betking":
        from slip_converter.prediction import betking as module
    return {
        "1x2":module.OneXTwo
    }.get(shortCode,None)


def serializePrediction(pred:str)->str:
    pred_ = pred.lower()
    return {
        "1": "Home",
        "x": "Draw",
        "2": "Away"
    }.get(pred_, pred)