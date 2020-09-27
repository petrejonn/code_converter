from slip_converter.converter import CodeConverter
from slip_converter.bookmakers.betking import Betking
from slip_converter.bookmakers.bet9ja import Bet9ja
# from slip_converter.bookmakers.sportybet import Sportybet
from flask import Flask, render_template, request, json
gamble = Flask(__name__, static_url_path='')

@gamble.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@gamble.route('/', methods=['POST'])
def api_convert():
    bookmaker = {
        "Bet9ja":Bet9ja,
        "Betking":Betking,
    }
    code =  request.form['code'];
    from_ = request.form['from'];
    to_ = request.form['to'];
    conv = CodeConverter(code,bookmaker.get(from_),bookmaker.get(to_)())
    conv.convert()
    return json.dumps({'status':'OK','code':conv.getNewCode()});

if __name__ == "__main__":
    gamble.run()