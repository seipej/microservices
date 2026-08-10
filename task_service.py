#import flask, request object to parse the data, and jsonify object for python data
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

#import uuid to make unique universal IDs
import uuid

#intialize flask instance, everything needed is in the program
app = Flask(__name__)

#Explicitly enable CORS options needed
CORS(app, resources={r"/tasks/*": {"origins": "*"}}, methods=["GET", "POST", "DELETE", "OPTIONS"])

#store tasks in a dictionary while the service is running
task_db = {}

#app.route decorator to match functional requirement spec
@app.route('/tasks', methods=['POST'])
def POST_task():

    #get_json parses the incoming JSON request data and returns it
    data = request.get_json()
    
    #assert that the data sent exists
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    #assert the required fields match functional requirement spec
    #Start time and end time, must be ISO8601 time format YYYY-MM-DDTHH:MM:SS
    #required_fields = ['title', 'description','location', 'start_time', 'end_time']
    required_fields = ['title']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    #assert end time is not before the start time
    if data['end_time'] and data['start_time']:
        if data['end_time'] <= data['start_time']:
            return jsonify({"error": "End time must be later than start time"}), 400

    #-------------------------------------------------------------------------
    #call dtg microservice to convert to ISO8601
    dtg_payload = {
        "start_time": data['start_time'],
        "end_time": data['end_time']
    }

    dtg_response = requests.post('http://localhost:5003/dtg', json=dtg_payload)
    parsed_dtg = dtg_response.json()

    if dtg_response.status_code == 200:
       data['start_time'] = parsed_dtg.get('start_time')
       data['end_time'] = parsed_dtg.get('end_time')

    #-------------------------------------------------------------------------
    

    #generate universal unique ID ensure events with duplicate names times are still unique
    task_id = str(uuid.uuid4())

    #populate the event object
    new_task = {
        "task_id": task_id,
        "title": data['title'],
        "description": data.get('description', ''),
        "location": data.get('location', ''),
        "start_time": data.get('start_time', ''),
        "end_time": data.get('end_time', ''),
    }

    #assign the event to the uuid in the local_db
    task_db[task_id] = new_task

    #return the event and a 201 for status
    return jsonify(new_task), 200

@app.route('/tasks', methods=['GET'])
def GET_task():

    task_list = list(task_db.values())    

    return jsonify(task_list), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
def DELETE_task(task_id):
    if task_id in task_db:
        task_db.pop(task_id)
        return jsonify({"message": "Task deleted successfully", "task": task_id}), 200
    
    return jsonify({"error": "Task not found"}), 404


if __name__ == '__main__':
    app.run(port=5002, debug=True)