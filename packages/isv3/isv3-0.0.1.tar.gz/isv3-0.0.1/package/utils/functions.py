import uuid
from random import choice
import random
import datetime
import math
import random as rd

from .get_master_data import *
from .constraints import *



def random_number(begin = None, end = None, type = None):
    if type:
        match type:
            case 'int':
                return rd.randint(begin, end)
            case 'float':
                return rd.uniform(begin, end)


def wirte_file_with_uuid(data):
    unique_id = str(uuid.uuid4())
    with open(get_file_name(unique_id), "w") as f:
        json.dump(data,f)
    return json.dumps(unique_id)


def get_file_name(unique_id):
    return f"assets/{unique_id}.json"


def wirte_file_with_uuid(data):
    unique_id = str(uuid.uuid4())
    with open(get_file_name(unique_id), "w") as f:
        json.dump(data,f)
    return json.dumps(unique_id)


def random_number(begin = None, end = None, type = None):
    if type:
        match type:
            case 'int':
                return random.randint(begin, end)
            case 'float':
                return random.uniform(begin, end)


def random_choice(choice_list = None, type = None):

    if choice_list:
        return choice(choice_list)
    else:
        match type:
            case 'location':
                return choice(["STATION", "HUB"]) #, "DEPOT", "CUSTOMER", "SATELLITE"
            case 'working_time_start':
                return choice(["07:30:00", "08:00:00", "08:30:00", "09:00:00", "09:30:00", "10:00:00"])
            case 'working_time_end':
                return choice(["17:30:00", "18:00:00", "18:30:00", "19:00:00", "19:30:00", "20:00:00"])
            case 'breaktime_lunch_start':
                return choice(["11:30:00", "12:00:00"])
            case 'breaktime_lunch_end':
                return choice(["12:30:00", "13:30:00"])

    

'''
    - get prop for obj with input is identity code for that
        - input:    nb_of_obj = len(location_list), 
                    obj_list = location_list, 
                    obj_code_name = "locationCode", 
                    obj_code = location_code, 
                    prop_name = "lTypes"
        - output:   ['CUSTOMER']  
'''
def get_prop_by_identifier(nb_of_obj, obj_list, obj_code_name, obj_code, prop_name):
    for i in range(int(nb_of_obj)):
        if (obj_list[i][obj_code_name] == obj_code):
            return obj_list[i][prop_name]


# get time with timezone
def datetime_now_with_GMT(timezone):
    datetime_now = datetime.datetime.now(timezone) 
    return str(datetime_now)


# output: { "start": "2022-10-19 06:00:00", "end": "2022-10-19 18:00:00" }
def create_working_time(date = None, w_time_start_list = None, w_time_end_list = None):

    workingTime = {}
    if date: 

        day = date
        if (w_time_start_list and w_time_end_list):
            workingTime["start"] = day + random_choice(choice_list = w_time_start_list)
            workingTime["end"] = day + random_choice(choice_list = w_time_end_list)
        else:
            workingTime["start"] = day + random_choice(type = 'working_time_start')
            workingTime["end"] = day + random_choice(type = 'working_time_end')
    else:
        
        day = datetime_now_with_GMT(timezone_hanoi)[0:11]

        if (w_time_start_list and w_time_end_list):
            workingTime["start"] = day + random_choice(choice_list = w_time_start_list)
            workingTime["end"] = day + random_choice(choice_list = w_time_end_list)
        else:
            workingTime["start"] = day + random_choice(type = 'working_time_start')
            workingTime["end"] = day + random_choice(type = 'working_time_end')

    return workingTime


# ouput: [{ "start": "2022-10-19 11:00:00", "end": "2022-10-19 13:00:00" }]
def create_break_lunch_time(date = None, nb_of_breaktime = None, br_time_start_list = None, br_time_end_list = None):

    breakTimes = []
    temp_time = {}

    if (nb_of_breaktime):
        for i in range(int(nb_of_breaktime)):

            if date:

                day = date
                if (br_time_start_list and br_time_end_list):
                    temp_time["start"] = day + random_choice(choice_list = br_time_start_list)
                    temp_time["end"] = day + random_choice(choice_list = br_time_end_list)
                    breakTimes.append(temp_time)
                else:
                    temp_time["start"] = day + random_choice(type = 'breaktime_lunch_start')
                    temp_time["end"] = day + random_choice(type = 'breaktime_lunch_end')
                    breakTimes.append(temp_time)

            else:

                day = datetime_now_with_GMT(timezone_hanoi)[0:11]

                if (br_time_start_list and br_time_end_list):
                    temp_time["start"] = day + random_choice(choice_list = br_time_start_list)
                    temp_time["end"] = day + random_choice(choice_list = br_time_end_list)
                    breakTimes.append(temp_time)
                else:
                    temp_time["start"] = day + random_choice(type = 'breaktime_lunch_start')
                    temp_time["end"] = day + random_choice(type = 'breaktime_lunch_end')
                    breakTimes.append(temp_time)
    else:
        if date:

            day = date
            if (br_time_start_list and br_time_end_list):
                    temp_time["start"] = day + random_choice(choice_list = br_time_start_list)
                    temp_time["end"] = day + random_choice(choice_list = br_time_end_list)
                    breakTimes.append(temp_time)
            else:
                temp_time["start"] = day + random_choice(type = 'breaktime_lunch_start')
                temp_time["end"] = day + random_choice(type = 'breaktime_lunch_end')
                breakTimes.append(temp_time)

        else:

            day = datetime_now_with_GMT(timezone_hanoi)[0:11]

            if (br_time_start_list and br_time_end_list):
                    temp_time["start"] = day + random_choice(choice_list = br_time_start_list)
                    temp_time["end"] = day + random_choice(choice_list = br_time_end_list)
                    breakTimes.append(temp_time)
            else:
                temp_time["start"] = day + random_choice(type = 'breaktime_lunch_start')
                temp_time["end"] = day + random_choice(type = 'breaktime_lunch_end')
                breakTimes.append(temp_time)

    return breakTimes


# input: location_code = '4000', location_list = list
# output: 'CUSTOMER' 
def get_location_type(location_code, location_list):
    result = str(get_prop_by_identifier(len(location_list), location_list, "locationCode", location_code, "lTypes"))
    result = result.lstrip('[')
    result = result.lstrip('\'')
    result = result.rstrip(']')
    result = result.rstrip('\'')
    return result



''' 
    - get location code with location type
        - input:    locationList = list, locationTypeName = 'CUSTOMER'
        - output:   locationCode = ['0001004238', '0001004448', '0003000441', '0001003008', '0001000554', '0001004440', '0001004624', '0001000116', '0003000430']
'''
def location_code_by_lType(locationList, locationTypeName):
    result = []
    for i in range(len(locationList)): 
        if(locationList[i]["lTypes"] == [locationTypeName]):
           result.append( locationList[i]["locationCode"] )
    return result



'''
    - Discover coordinates by latitude & longitude: https://support.google.com/maps/answer/18539?hl=en&co=GENIE.Platform%3DDesktop 
    - Ho Chi Minh's Mausoleum (21.0369023, 105.832478)
    - Temple Of Literature (21.0272877, 105.8339036) 
        - input: lat1 = 21.0369023, lon1 = 105.832478, lat2 = 21.0272877, lon2 = 105.8339036
        - ouput: 1.0792846643321892
'''
def distance_between_coordinates(lat1, lon1, lat2, lon2):     
    R = 6371
    d_lat = (lat2 - lat1) * (math.pi / 180)
    d_lon = (lon2 - lon1) * (math.pi / 180)
    lat1_to_rad = lat1 * (math.pi / 180)
    lat2_to_rad = lat2 * (math.pi / 180)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(lat1_to_rad) * math.cos(lat2_to_rad) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def time_interval_random(working_time, working_time_ratio, random_time_ratio, interval_range=2):
    work_start = datetime.datetime.strptime(working_time["start"], "%Y-%m-%d %H:%M:%S")
    work_end = datetime.datetime.strptime(working_time["end"], "%Y-%m-%d %H:%M:%S")
    delta_working_time = work_end - work_start
    seed = rd.random()
    if seed < working_time_ratio:
        return [working_time]
    elif seed < working_time_ratio + random_time_ratio:
        random_hours = rd.randint(0, delta_working_time.seconds // 3600 - interval_range)
        hour_start = work_start + datetime.timedelta(hours=random_hours)
        hour_end = hour_start + datetime.timedelta(hours=interval_range)
        value = {
            "start": hour_start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": hour_end.strftime("%Y-%m-%d %H:%M:%S")
        }
        return [value]
    else:
        return []


def random_matrix(base_value, list_type1, type_name1, list_type2=[], type_name2="", random_stg='cost'):
    matrix = []

    if len(list_type2) == 0 and type_name2 == "":

        for i in range(len(list_type1)):
            temp = {type_name1: list_type1[i], "value": base_value}
            if random_stg == 'cost':
                base_value += math.ceil(base_value * (rd.randint(30, 80) / 100))
            matrix.append(temp)
    else:
        for i in range(len(list_type1)):
            for j in range(len(list_type2)):
                temp = {type_name1: list_type1[i], type_name2: list_type2[j]}
                if i == j:
                    temp["value"] = base_value
                elif random_stg == 'cost':
                    temp["value"] = base_value * rd.randint(8, 30)
                elif random_stg == 'binary':
                    temp["value"] = rd.randint(0, 1)
                elif random_stg == 'time':
                    temp["value"] = time_interval_random(base_value[0], 0.1, 0.3, 1)

                matrix.append(temp)

    return matrix



'''
    - get LocationCode with List of ingredients
        - input:    _list = JSON_INPUT_SVRP['customers']
        - output:   ['loc_code_3', 'loc_code_5'] 
'''
def get_location_code_list(_list):
    result = []
    for i in range(len(_list)):
        result.append(_list[i]['locationCode'])

    return result

