#remember to pip install dateparser
import dateparser
from flask import Flask, request, jsonify
from flask_cors import CORS

#intialize flask instance, everything needed is in the program
app = Flask(__name__)

#Explicitly enable CORS options needed
CORS(app)


@app.route('/dtg', methods=['POST'])
def POST_DTG():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON payload provided"}, 400)

    raw_start = data.get('start_time')
    raw_end = data.get('end_time')

    parse_settings = {
        'PREFER_DATES_FROM': 'future',
        'RETURN_AS_TIMEZONE_AWARE': False
    }

    parsed_start = dateparser.parse(raw_start, settings=parse_settings)
    parsed_end = dateparser.parse(raw_end, settings=parse_settings)

    return jsonify({
        "start_time":parsed_start.isoformat(),
        "end_time":parsed_end.isoformat()}), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)