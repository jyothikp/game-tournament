from flask import Flask
from flask import request

from tournament.Interface import GameInterface
from tournament.logger import Logger

app = Flask(__name__)


@app.route("/")
def index():
    return """
  <h1>Hey This is a sample search Project!</h1>
  <p>A sample game search project for fun!.</p>
  """


@app.route('/game/v1.0/search/<match_id>', methods=['GET'])
def search(match_id):
    return GameInterface().get_match(match_id)


@app.route('/game/v1.0/search/', methods=['POST'])
def search_all():
    Logger().info('search_request_received', query=request.json)
    return GameInterface().get_matches(request.json['query'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

