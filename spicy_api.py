from flask import Flask, request
from firebase_interface import FirebaseInterface
import json
import string
import random

spicy_api = Flask(__name__)

with open("creds.json") as file:
    creds = json.load(file)

FIREBASE_OBJ = FirebaseInterface(creds_dict=creds)


def encode(raw_string):
    encoded_string = raw_string.replace(".", "_DOT_")
    return encoded_string


def decode(encoded_string):
    raw_string = encoded_string.replace("_DOT_", ".")
    return raw_string


def turn_off_vehicle(id):
    # retrieve the data corresponding to the desired vehicle
    vehicle_data = FIREBASE_OBJ.get_data(key=f'vehicles',
                                         subkey=id)

    # isolate the vehicle's states
    current_states = vehicle_data['states']

    # Turn the car off
    current_states['carOn'] = False

    # Turn all defrosting off
    new_defrost = current_states['defrost']

    for key in new_defrost.keys():
        new_defrost[key] = False

    # Turn all seat heaters off
    new_seat_heater = current_states['seatHeater']

    for key in new_seat_heater.keys():
        new_seat_heater[key] = False

    # add the updated values to the states dictionary
    current_states['defrost'] = new_defrost
    current_states['seatHeater'] = new_seat_heater

    # pass the updated dictionary to the firebase database
    set_response = FIREBASE_OBJ.change_value(key=f'vehicles/{id}',
                                             subkey='states',
                                             val=current_states)

    return set_response

# Temporary, we shouldn't keep this long term
@spicy_api.route("/get_full_database", methods=['GET'])
def index():
    return FIREBASE_OBJ.get_data()

# Attempt to log in to the server, returns the error message if it fails or the provided credentials are invalid
@spicy_api.route("/attempt_login", methods=['POST'])
def attempt_login():
    post_request = request.json
    username = None
    password = None

    try:
        username = post_request['username']
        password = post_request['password']
    except KeyError:
        return "Error: Missing username or password."

    if password is None or username is None:
        return "Error: Missing username or password."

    user = FIREBASE_OBJ.get_data(key=f'users',
                                 subkey=encode(username))

    if user is None:
        return "Invalid username or password."

    if password == user['password']:
        token = gen_token()
        # TODO store the hash of the token in the database
        return '{"token": "'+token+'"}'
    else:
        return "Invalid username or password."

def gen_token():
    possibleChars = string.ascii_lowercase+string.ascii_uppercase+string.digits
    return ''.join(random.choice(possibleChars) for i in range(random.randint(25, 35)))

@spicy_api.route("/get_vehicle_id", methods=['POST'])
def user_info():
    post_request = request.json
    username = None
    password = None

    try:
        username = post_request['username']
        password = post_request['password']
    except KeyError:
        return "Error: Missing required key value pair."

    if password is None:
        if username is None:
            return "Error: password and username keys have no values."
        return "Error: password key has no value."

    if username is None:
        return "Error: username key has no value."

    user = FIREBASE_OBJ.get_data(key=f'users',
                                 subkey=encode(username))

    if user is None:
        return f"Error: username {username} not found."

    if password == user['password']:
        return user['vehicle']
        # return user
    else:
        return "Fetch Unsuccessful: Invalid Password"


@spicy_api.route("/get_vehicle_data", methods=['POST'])
def get_vehicle_data():
    """

    post_request sample: {
        "vehicle_id": "vehicle1",
    }

    :return:
    """

    post_request = request.json

    try:
        vehicle_id = post_request['vehicle_id']
    except KeyError:
        return "Error: vehicle_id key not provided in POST request."

    if vehicle_id is None or vehicle_id == "":
        return "Error: No vehicle id provided."

    vehicle_data = FIREBASE_OBJ.get_data(key=f'vehicles',
                                         subkey=vehicle_id)

    if vehicle_id is None:
        return f"Error: No vehicle data found for {vehicle_id}."

    return vehicle_data


@spicy_api.route("/set_val", methods=['POST'])
def set_val():
    """

    Example POST Request
    post_request = {
        "vehicle_id": "string",
        "key": "string",
        "subkey": "string",  # Optional
        "new_val": bool
    }

    :return: bool indicating whether or not the update was successful

    """

    post_request = request.json

    vehicle_id = post_request['vehicle_id']
    key = post_request['key']
    new_val = post_request['new_val']

    try:
        subkey = post_request['subkey']
    except KeyError:
        subkey = None

    # check if the request is to turn off the car
    if key == 'carOn' and new_val == False:
        set_response = turn_off_vehicle(vehicle_id)

        if set_response is None:
            return "False"
        else:
            return "True"

    response = FIREBASE_OBJ.change_value(key=f"vehicles/{vehicle_id}/states/{key}",
                                         subkey=subkey,
                                         val=new_val)

    if response is None:
        return "False"
    else:
        return "True"


if __name__ == "__main__":
    spicy_api.run(debug=True, host='0.0.0.0', port="8080")

