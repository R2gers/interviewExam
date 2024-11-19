import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

MA_LEN = 5
DATA_READ_INTERVAL = 10
FILE_NAME = 'data.json'

five_ma_array_speed = []
five_ma_array_temp = []


# Desc: Mock an endpoint using a json file
# Input: callback function for each data in json
def read_json(callback):
    try:
        with open(FILE_NAME, 'r') as file:
            data_array = json.load(file)

            for data in data_array:
                callback(data)
                time.sleep(DATA_READ_INTERVAL)

    except Exception as e:
        logging.error(f"Error reading file: {str(e)}")
        return None

# Desc: Maintain the MA array
# Input: The concerned array, its new value to append
# Output: The moving average of the concerned array 
def process_ma_array(array, new_value):

    array.append(new_value)
    if(len(array) < MA_LEN):
        return 0
    if(len(array) > MA_LEN):
        array.pop(0)
    
    return sum(array) / MA_LEN

# Desc: process the MA arrays and print the results
# Input: The new data
def callback(data):
    try:
        ma_speed = process_ma_array(five_ma_array_speed, data['speed'])
        ma_temp = process_ma_array(five_ma_array_temp, data['temperature'])

        json_format = {
            "speed_ma": round(ma_speed,2),
            "temperature_ma": round(ma_temp,2)
        }

        print(json.dumps(json_format))

    except Exception as e:
        logging.error(f"Error during data process: {str(e)}")
        return None

if __name__ == "__main__":
    read_json(callback)