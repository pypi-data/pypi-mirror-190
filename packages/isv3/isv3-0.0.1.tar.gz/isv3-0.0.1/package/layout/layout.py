import copy 

from components.model import *



def get_input(nb_of_vehicle, nb_of_customer, nb_of_depot, nb_of_request, nb_of_location):

    result = {}

    result['locations'] = create_model_location(nb_of_location, nb_of_depot, nb_of_customer)
    location_list = copy.deepcopy(result['locations'])

    result['depots'] = create_model_depot(nb_of_depot, location_list) 
    result['vehicles'] = create_model_vehicle(nb_of_vehicle, location_list, result['depots'])
    result['customers'] = create_model_customer(nb_of_customer, location_list)
    result['distances'] = create_model_distance(location_list)
    result['requests'] = create_model_request(nb_of_request, result['depots'], result['customers'])
    result['matrixConfig'] = create_model_matrix_config()

    print('data: ', result)

    id = wirte_file_with_uuid(result)

    return id

