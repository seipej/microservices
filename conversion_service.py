from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/distance_conversion', methods=['POST'])
def convert():

    data = request.get_json()

    if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400


    #Fields
    ### raw_num: the number to convert
    ### from: valid values are [1,2,3,4]
    ### to: valid values are [1,2,3,4]
    ### 1 = mile
    ### 2 = km
    ### 3 = feet
    ### 4 = meter
    required_fields = ['raw_num', 'from', 'to']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

        #assert from is not to
    if data['from'] == data['to']:
        return jsonify({"error": "There is no conversion to make"}), 400

    converted = 0

    #convert from miles ---------------------------------------------------------
    if data['from'] == 1:

        #miles to km
        if data['to'] == 2:
            converted = data['raw_num'] * 1.60934
        #miles to feet
        if data['to'] == 3:
            converted = data['raw_num'] * 5280
        #miles to meters
        if data['to'] == 4:
            converted = data['raw_num'] * 1609.34

    #convert from km ---------------------------------------------------------
    if data['from'] == 2:
        #to miles
        if data['to'] == 1:
            converted = data['raw_num'] * 0.621371
        #to feet
        if data['to'] == 3:
            converted = data['raw_num'] * 3280.839
        #to meters
        if data['to'] == 4:
            converted = data['raw_num'] * 1000

    #convert from feet ---------------------------------------------------------
    if data['from'] == 3:
        #to miles
        if data['to'] == 1:
            converted = data['raw_num'] / 5280
        #to km
        if data['to'] == 2:
            converted = data['raw_num'] * 0.0003048
        #to meters
        if data['to'] == 4:
            converted = data['raw_num'] * 0.3048

    #convert from meter ---------------------------------------------------------
    if data['from'] == 4:
        #to miles
        if data['to'] == 1:
            converted = data['raw_num'] * 0.00062137
        #to km
        if data['to'] == 2:
            converted = data['raw_num'] / 1000
        #to feet
        if data['to'] == 3:
            converted = data['raw_num'] * 3.28084

    return jsonify({
        "input_num": data['raw_num'],
        "from": data['from'],
        "to": data['to'],
        "converted": converted
    }), 200

if __name__ == '__main__':
    app.run(port=5002, debug=False)