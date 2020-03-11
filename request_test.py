import requests
import json
import pprint


class SpicyApiTest:
    def __init__(self, url='http://localhost:5000/'):
        self.url = url

    def get_vehicle_id_test(self):
        # Construct the URL and message to send to the microservice
        endpoint = self.url+'get_vehicle_id'
        json_message = {
            "username": "michael.bishop@ttu.edu",
            "password": "blah"
        }

        # Using the requests library, send a POST request with the following
        # message to the URL.
        response = requests.post(url=endpoint,
                                 json=json_message)

        # Extract the status code and returned text
        status_code = response.status_code
        response_body = response.text
        id_list = json.loads(response_body).values()

        if status_code == 200:
            print("Test Passed!")
            print(f"response: {response_body}\n\n")
        else:
            print(f"Test Failed with {status_code} status code.")
            print(f"response: {response_body}\n\n")

        return id_list

    def get_vehicle_data_test(self, vehicle_id):
        endpoint = self.url+"get_vehicle_data"
        message = {
            "vehicle_id": vehicle_id
        }

        response = requests.post(url=endpoint,
                                 json=message)

        # Extract the status code and returned text
        status_code = response.status_code
        response_body = response.text
        vehicle_data = json.loads(response_body)

        if status_code == 200:
            print("Test Passed!")
            print(f"response: {response_body}\n\n")
        else:
            print(f"Test Failed with {status_code} status code.")
            print(f"response: {response_body}\n\n")

        return vehicle_data

    def set_val_test(self, message):
        endpoint = self.url + "set_val"


        response = requests.post(url=endpoint,
                                 json=message)

        # Extract the status code and returned text
        status_code = response.status_code
        response_body = response.text

        if status_code == 200:
            print("Test Passed!")
            print(f"response: {response_body}\n\n")
        else:
            print(f"Test Failed with {status_code} status code.")
            print(f"response: {response_body}\n\n")


if __name__ == "__main__":
    test_obj = SpicyApiTest()
    vehicle_id_list = test_obj.get_vehicle_id_test()

    vehicles = {}
    for vehicle_id in vehicle_id_list:
        vehicles[vehicle_id] = test_obj.get_vehicle_data_test(vehicle_id)

    pprint.pprint(vehicles)

    print("\n\n")

    dict1 = {
        "vehicle_id": "V-1",
        "key": "carLock",
        "subkey": None,
        "new_val": False
    }

    dict2 = {
        "vehicle_id": "V-2",
        "key": "seatHeater",
        "subkey": "fDriver",
        "new_val": True
    }

    test_obj.set_val_test(message=dict1)
    test_obj.set_val_test(message=dict2)
