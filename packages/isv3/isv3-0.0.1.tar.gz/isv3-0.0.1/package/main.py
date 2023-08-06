from utils.functions import *
from layout.layout import *


def create_input_SVRP():

    # nb_of_vehicle = random_number(10, 10, type = 'int')
    # nb_of_customer = random_number(2, 2, type = 'int')  
    # nb_of_depot = 1 #random_number(1, 1, type = 'int')
    # nb_of_request = random_number(20, 20, type = 'int')
    # nb_of_location = random_number(10, 10, type = 'int')

    nb_of_vehicle = 10
    nb_of_customer = 2
    nb_of_depot = 1
    nb_of_request = 20
    nb_of_location = 10
    
    return get_input(nb_of_vehicle, nb_of_customer, nb_of_depot, nb_of_request, nb_of_location)


if __name__=="__main__":
    create_input_SVRP()
    