from flask import Flask, request
from flask import json
from loguru import logger
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

app = Flask(__name__)
# Logger format
logger.add("debug.json", format="{time} {level} {message}", level="DEBUG", rotation="10 KB", compression="zip", serialize=True)


@logger.catch
@app.route("/idareas", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # Receiving data from Postman API
        api_data = request.json
        count_areas_persons(api_data)
        return api_data
    else:
        with open("example.json") as file:
            data = json.load(file)
            count_areas_persons(data)
        return data

# Function to count all necessary data from api
def count_areas_persons(json_data):
    data = json_data
    all_areas_list = data['example']
    sum_idareas = [key['idarea'] for key in all_areas_list if key.get('idarea')]
    all_persons_list = [item['personList'] for item in data['example']]
    count_person = 0
    total_male = 0
    total_female = 0
    for persons in all_persons_list:
        count_person += len(persons)
        for i in range(len(persons)):
            if persons[i]['gender'] == 'male':
                total_male += 1
            elif persons[i]['gender'] == 'female':
                total_female += 1

    print(f"We support {len(sum_idareas)} areas.")
    print(f"In total we have {count_person} persons in the database.")
    print(f"{total_male} of them are male.")
    print(f"{total_female} of them are female.")

# --------------------------------- OSC ------------------------------------
# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("127.0.0.1", 5000, "tester")

msg = oscbuildparse.OSCMessage("/test/me", None, ["text", 672, 8.871])
osc_send(msg, "tester")
osc_process()

if __name__ == "__main__":
    app.run(debug=True)