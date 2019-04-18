###hw3
###Name: Yihan Xu
###ID# 47011405
###main module
###AppKey = 'Fmjtd%7Cluu821u2nl%2Crl%3Do5-94ax5r'

import hw32
import hw33

###Ask users to input how many locations are in the trip
def how_many_location():
    number_of_location = input()
    
    return number_of_location


###Ask users to input the location that contain in the trip, append them into
###a list
def read_location(number_of_location):
    locations_list = []
    for i in range(int(number_of_location)):
        location = input()
        locations_list.append(location)
        
    return locations_list

###Ask users to input how many output he want to generate
def how_many_output():
    number_of_output = input()
    
    return number_of_output


###Append all the output users want to generate to a list
def read_output_type(number_of_output):
    output_require_list = []
    for j in range(int(number_of_output)):
        output_type = input()
        output_require_list.append(output_type)
        
    return output_require_list

###create a dictionary, which gives each string that users might input a value
###the value is the class in class module
###call the transfer function in class module for each class we need
def run_transfer(necessary_class, result):
    require_dictionary = {'STEPS': hw33.STEPS(), 'TOTALDISTANCE': hw33.TOTALDISTANCE(), 'TOTALTIME': hw33.TOTALTIME(), 'LATLONG': hw33.LATLONG(), 'ELEVATION': hw33.ELEVATION()}
    for Class in necessary_class:
        general_result = Class.transfer(result)
        
    return general_result

###get the list of class that user needed by get the value of string
###that users input(which is same as the key in dictionary)
def get_necessary_class_list(require_list):
    necessary_class = []
    require_dictionary = {'STEPS': hw33.STEPS(), 'TOTALDISTANCE': hw33.TOTALDISTANCE(), 'TOTALTIME': hw33.TOTALTIME(), 'LATLONG': hw33.LATLONG(), 'ELEVATION': hw33.ELEVATION()}
    for require in require_list:
        necessary_class.append(require_dictionary[require])
    
    return necessary_class

def main():
    ###call function to get how many location and what is the location list
    ###meanwhile, check if the number is integer and bigger than 1
    ###call function to get how many output and what is the type of output
    ###meanwhile, check if the number is integer and bigger than 0
    ###if they are not stop function

    try:
        num_of_loc = int(how_many_location())
        if num_of_loc <= 1 or num_of_loc > 50:
            return
    except:
        return
    
    ###call function to get the location and required output in a list
    loc_list = read_location(num_of_loc)
    
    try:
        num_of_output = int(how_many_output())
        if num_of_output <= 0 or num_of_output > 5:
            return
    except:
        return
    
    output_list = read_output_type(int(num_of_output))
    
    ###call function to get the json result
    parameter = hw32.build_parameter(int(num_of_loc), loc_list)
    
    Url_to_send = hw32.build_url(parameter)
    results = hw32.read_result(Url_to_send)
    if results == -1:
        return

    needed_class = get_necessary_class_list(output_list)

    ###call function to run the function and go through all the class that
    ###mentioned in output list
    run_transfer(needed_class, results)

    print()
    print('Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors')
        



if __name__ == '__main__':
    main()







