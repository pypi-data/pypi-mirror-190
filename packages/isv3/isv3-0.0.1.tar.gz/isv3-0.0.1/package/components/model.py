
from utils.functions import *

# ---------------------------------------

    # LOCATION

def create_layout_location (location_code, lat, lng, location_type):
    return {
        "locationCode": location_code,
        "lat": lat,
        "lng": lng,
        "lTypes": [ location_type ]
    }


def create_model_location (nb_of_location, nb_of_depot, nb_of_customer, _lat = None, _lng = None):

    locations = []
    location_type_list = []

    for i in range (nb_of_depot):
        location_type_list.append('DEPOT')

    for i in range (nb_of_customer):
        location_type_list.append('CUSTOMER')

    for i in range(nb_of_location):

        try:
            if location_type_list[i]:
                location_type = location_type_list[i] 
        except:
            location_type = random_choice(type = 'location')
        finally:
            location_code = str(i) # "location_" + "1000" + 
            lat = random_number(1.0, _lat, type= 'float') if _lat else random_number(18, 22, type= 'float')
            lng = random_number(1.0, _lng, type= 'float') if _lng else random_number(103, 106, type= 'float')
            locations.append( create_layout_location(location_code, lat, lng, location_type) )

    return locations

# ---------------------------------------

    # CUSTOMER

def create_layout_customer (customer_code, location_code, district, fixed_unload_time, unload_time_per_ton, unload_time_per_cbm, working_time, break_times, cType):
    return {
        "customerCode": customer_code,
        "locationCode": location_code,
        "district": district,
        "fixedUnloadTime": fixed_unload_time,
        "unloadTimePerTon": unload_time_per_ton,
        "unloadTimePerCbm": unload_time_per_cbm,
        "workingTime": working_time,
        "breakTimes": break_times,
        "cType": cType
    }


def create_model_customer(
            nb_of_customer, location_list, _district = None, 
            _unload_time_per_ton = None, _unload_time_per_cbm = None, _fixed_unload_time = None, 
            w_time_start_list = None, w_time_end_list = None,
            nb_of_breaktime = None, date = None,   
            br_time_start_list = None, br_time_end_list = None 
    ):

    customers = []
    customer_code_list = location_code_by_lType(location_list, "CUSTOMER")

    for i in range(int(nb_of_customer)):

        customer_code = "customer_" + "1000" + str(i)
        location_code = random_choice(choice_list= customer_code_list)
        district = str(random_number(1, _district, type = 'int')) if _district else str(random_number(1, 1000, type = 'int'))
        fixed_unload_time = random_number(10, _fixed_unload_time, type = 'int') if _fixed_unload_time else random_number(10, 100, type = 'int')
        unload_time_per_ton = random_number(10, _unload_time_per_ton, type = 'int') if _unload_time_per_ton else random_number(10, 100, type = 'int') 
        unload_time_per_cbm = random_number(10, _unload_time_per_cbm, type = 'int') if _unload_time_per_cbm else random_number(10, 100, type = 'int')
        workingTime = create_working_time(date, w_time_start_list, w_time_end_list)
        breakTimes = create_break_lunch_time(date, nb_of_breaktime, br_time_start_list, br_time_end_list)

        customerType = {}
        for key, value in customer_type.items():
            customerType[key] = value[rd.randint(0, len(value) - 1)]

        customers.append( create_layout_customer( customer_code, location_code, district, fixed_unload_time, unload_time_per_ton, unload_time_per_cbm, workingTime, breakTimes, customerType ) )

    return customers

# ---------------------------------------

    # VEHICLE

def create_layout_vehicle (vehicle_code, cbm, capacity, quantity, size, load_time_per_cbm, unload_time_per_cbm, load_time_per_ton, unload_time_per_ton, start_location_code, start_location_type, end_location_code, end_lcation_type, working_time, break_times, vType ):
    return {
        "vehicleCode": vehicle_code, 
        "cbm": cbm, 
        "capacity": capacity, 
        "quantity": quantity,
        "size": size,
        "loadTimePerCbm": load_time_per_cbm,
        "unloadTimePerCbm": unload_time_per_cbm,
        "loadTimePerTon": load_time_per_ton,
        "unloadTimePerTon": unload_time_per_ton,
        "startLocationCode": start_location_code,
        "startLocationType": start_location_type,
        "endLocationCode": end_location_code,
        "endLocationType": end_lcation_type,
        "workingTime": working_time,
        "breakTimes": break_times,
        "vType": vType
    }


def create_model_vehicle (
            nb_of_vehicle, location_list, depot_list,
            quantity_min = None, quantity_max = None, 
            load_time_cbm_min = None, load_time_cbm_max = None, 
            upload_time_cbm_min = None, upload_time_cbm_max = None, 
            load_time_ton_min = None, load_time_ton_max = None, 
            upload_time_ton_min = None,  upload_time_ton_max = None, 
            w_time_start_list = None, w_time_end_list = None,
            nb_of_breaktime = None, date = None,  
            br_time_start_list = None, br_time_end_list = None 
    ):

    vehicles = []
    dep_location_list = get_location_code_list(depot_list)

    location_code_list = location_code_by_lType(location_list, 'CUSTOMER')
    location_code_list.extend( location_code_by_lType(location_list, 'SATELLITE') )
    location_code_list.extend( location_code_by_lType(location_list, 'STATION') )
    
    for i in range(int(nb_of_vehicle)):

        vehicle_code = "vehicle_" + "1000" + str(i)
        rd_vhc = rd.randint(0, len(vehicle_categories) - 1)
        cbm = vehicle_categories[rd_vhc]["cbm"]
        capacity = vehicle_categories[rd_vhc]["capacity"]
        size = vehicle_categories[rd_vhc]["size"]
        quantity = random_number(quantity_min, quantity_max, type = 'int') if (quantity_min and quantity_max) else 1

        load_time_per_cbm = round(random_number(load_time_cbm_min, load_time_cbm_max, type = 'int'), 2) if (load_time_cbm_min and load_time_cbm_max) else round(random_number(10, 100, type = 'int'), 2)
        unload_time_per_cbm = round(random_number(upload_time_cbm_min, upload_time_cbm_max, type = 'int'), 2) if (upload_time_cbm_min and upload_time_cbm_max) else round(random_number(10, 100, type = 'int'), 2)
        load_time_per_ton = round(random_number(load_time_ton_min, load_time_ton_max, type = 'int'), 2) if (load_time_ton_min and load_time_ton_max) else round(random_number(10, 100, type = 'int'), 2)
        unload_time_per_ton = round(random_number(upload_time_ton_min, upload_time_ton_max, type = 'int'), 2) if (upload_time_ton_min and upload_time_ton_max) else round(random_number(10, 100, type = 'int'), 2)

        temp_location_code = str(random_choice(choice_list = dep_location_list))
        start_location_code = temp_location_code
        start_location_type = get_location_type(start_location_code, location_list)
        end_location_code = temp_location_code
        end_location_type = get_location_type(end_location_code, location_list)

        workingTime = create_working_time(date, w_time_start_list, w_time_end_list)
        breakTimes = [] #create_break_lunch_time(date, nb_of_breaktime, br_time_start_list, br_time_end_list)

        vehicleType = {}
        for key, value in vehicle_type.items():
            vehicleType[key] = value[rd.randint(0, len(value) - 1)]

        vehicles.append(
            create_layout_vehicle (
                vehicle_code, cbm, capacity, quantity, size, load_time_per_cbm, unload_time_per_cbm, load_time_per_ton, 
                unload_time_per_ton, start_location_code, start_location_type, end_location_code, 
                end_location_type, workingTime, breakTimes, vehicleType 
            )
        )

    return vehicles

# ---------------------------------------

    # DEPOT

def create_layout_depot (depot_code, location_code, fixed_load_time, load_time_per_ton, load_time_per_cbm, working_time, break_times, dType ):
    return {
        "depotCode": depot_code,
        "locationCode": location_code,
        "fixedLoadTime": fixed_load_time,
        "loadTimePerTon": load_time_per_ton,
        "loadTimePerCbm": load_time_per_cbm,
        "workingTime": working_time,
        "breakTimes": break_times,
        "dType": dType
    }


def create_model_depot (
            nb_of_depot, location_list,
            fixed_load_time_min = None, fixed_load_time_max = None, 
            load_time_per_ton_min = None, load_time_per_ton_max = None, 
            load_time_per_cbm_min = None, load_time_per_cbm_max = None, 
            w_time_start_list = None, w_time_end_list = None,
            nb_of_breaktime = None, date = None, 
            br_time_start_list = None, br_time_end_list = None 
    ):

    depots = []
    depot_code_list = location_code_by_lType(location_list, "DEPOT")

    for i in range(nb_of_depot):

        depot_code = "depot_" + "1000" + str(i)
        location_code = random_choice(choice_list = depot_code_list)
        fixed_load_time = random_number(fixed_load_time_min, fixed_load_time_max, type = 'int') if (fixed_load_time_min and fixed_load_time_max) else random_number(10, 100, type = 'int')
        load_time_per_ton = random_number(load_time_per_ton_min, load_time_per_ton_max, type = 'int') if (load_time_per_ton_min and load_time_per_ton_max) else random_number(10, 100, type = 'int')
        load_time_per_cbm = random_number(load_time_per_cbm_min, load_time_per_cbm_max, type = 'int') if (load_time_per_cbm_min and load_time_per_cbm_max) else random_number(10, 100, type = 'int')
        workingTime = create_working_time(date, w_time_start_list, w_time_end_list)
        breakTimes = create_break_lunch_time(date, nb_of_breaktime, br_time_start_list, br_time_end_list)

        depotType = {}
        for key, value in depot_type.items():
            depotType[key] = value[rd.randint(0, len(value) - 1)]

        depots.append( create_layout_depot( depot_code, location_code, fixed_load_time, load_time_per_ton, load_time_per_cbm, workingTime, breakTimes, depotType))

    return depots

# ---------------------------------------

    # DISTANCE

def create_layout_distance (src_code, dest_code, distance, travel_time):
    return {
        "srcCode": src_code,
        "destCode": dest_code,
        "distance": distance,
        "travelTime": travel_time
    }


def create_model_distance (location_list):

    distances = []

    for i in range(len(location_list)):
        for j in range(len(location_list)):

            srcCode = location_list[i]["locationCode"]
            destCode = location_list[j]["locationCode"]

            if i == j:
                distance = 0
            else:
                distance = distance_between_coordinates(location_list[i]["lat"], location_list[i]["lng"], location_list[j]["lat"], location_list[j]["lng"])
            
            travel_time = math.floor((distance / 60) * 3600)
            distances.append( create_layout_distance( srcCode, destCode, distance, travel_time ) )

    return distances

# ---------------------------------------

    # REQUEST

def create_layout_item(item_code, quantity, weight, cbm, width_size, length_size, height_size, iType ):
    return {
        "itemCode": item_code,
        "quantity": quantity,
        "weight": weight,
        "cbm": cbm,
        "size": {
            "width": width_size,
            "length": length_size,
            "height": height_size
        },
        "iType": iType
    }


def create_layout_request (order_code, depot_code, customer_code, pickup_location_code, delivery_location_code, items):
    return {
        "orderCode": order_code,
        "depotCode": depot_code,
        "customerCode": customer_code,
        "pickupLocationCode": pickup_location_code,
        "deliveryLocationCode": delivery_location_code,
        "items": items
    }


def create_model_request (
        nb_of_request, depot_list, customer_list,
        quantity_min = None, quantity_max = None,
        weight_min = None, weight_max = None,
        cbm_min = None, cbm_max = None,
        width_size_min = None, width_size_max = None,
        length_size_min = None, length_size_max = None,
        height_size_min = None, height_size_max = None
    ):

    requests = []
    depot_code_list = get_location_code_list(depot_list) 
    customer_code_list = get_location_code_list(customer_list) 
    for i in range(int(nb_of_request)):

        order_code = "order_" + "1000" + str(i)
        pickuploc_code = random_choice(choice_list = depot_code_list)
        deliveryloc_code = random_choice(choice_list = customer_code_list)
        depot_code = get_prop_by_identifier(len(depot_list), depot_list, "locationCode", pickuploc_code, "depotCode")
        customer_code = get_prop_by_identifier(len(customer_list), customer_list, "locationCode", deliveryloc_code, "customerCode")
        nb_of_item = random_number(2, 20, type = 'int')
        items = []

        for i in range(int(nb_of_item)):
            itemCode = "item_" + "1000" + str(i)
            quantity = random_number(quantity_min, quantity_max, type = 'int') if (quantity_min and quantity_max) else random_number(1, 20, type = 'int')
            weight = random_number(weight_min, weight_max, type = 'int') if (weight_min and weight_max) else random_number(10, 50, type = 'int')
            cbm = random_number(cbm_min, cbm_max, type = 'int') if (cbm_min and cbm_max) else random_number(10, 50, type = 'int')
            width_size = random_number(width_size_min, width_size_max, type = 'int') if (width_size_min and width_size_max) else random_number(1, 10, type = 'int')
            length_size = random_number(length_size_min, length_size_max, type = 'int') if (length_size_min and length_size_max) else random_number(1, 10, type = 'int')
            height_size = random_number(height_size_min, height_size_max, type = 'int') if (height_size_min and height_size_max) else random_number(1, 10, type = 'int')

            itemType = {}
            for key, value in item_type.items():
                itemType[key] = value[rd.randint(0, len(value) - 1)]

            items.append(create_layout_item(itemCode, quantity, weight, cbm, width_size, length_size, height_size, itemType ))
        
        requests.append(create_layout_request (order_code, depot_code, customer_code, pickuploc_code, deliveryloc_code, items))
    
    return requests

# ---------------------------------------

    # MATRIX CONFIG

def create_layout_matrix_config (matrix_config):
    return { 'matrixConfig': matrix_config }


def create_model_matrix_config():

    for key, relation in matrix_outline.items():

        for key_c, constraints in relation.items():
            params = []
            # print(constraints)
            for key_t, any_type in constraints["referenceType"].items():
                list_type = dict_for_fucking_name[key_t]["value_set"][any_type]
                type_name = dict_for_fucking_name[key_t]["name"]
                params.append(list_type)
                params.append(type_name)
            base_value = constraints["base_value"]
            try:
                random_stg = constraints["random_stg"]
                del constraints["random_stg"]
            except:
                random_stg = 'cost'
            constraints["matrix"] = random_matrix(constraints["base_value"], *params, random_stg=random_stg)
            del constraints["base_value"]
            
    return matrix_outline

# ---------------------------------------

    # ALGO PARAMS

def create_layout_algo_params (algo_params):
    return { 'algoParams': algo_params }


def create_model_algo_params():
    algoParams = {}
    algoParams["objective"] = {}
    algoParams["objective"]["minimizeTotalDistance"] = {}
    algoParams["objective"]["minimizeNumberVehicle"] = {}
    algoParams["objective"]["maximizeFullFillRate"] = {}
    return algoParams

# ---------------------------------------























