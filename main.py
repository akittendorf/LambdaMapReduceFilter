from functools import reduce 
import csv
import json
# Read in data from the Detroit Police Reports file using the CSVREADER and translate this into a list of dictionaries
def csv_to_dict(file):
    police_lsts = []
    with open(file) as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            police_lsts.append(row)
    return(police_lsts)

messy_lst = csv_to_dict('DetroitPolice.csv')

# Filter with lambda functions to exclude dictionaries (rows of the CSV) that have missing data in the Zip, or Neighborhood columns.
def filter_lst(lst):
    filtered_lst = filter(lambda lst: lst['zip_code'] != '0' and lst['neighborhood'] != '', lst)
    filtered_lst = list(filtered_lst)
    return filtered_lst

clean_lst = filter_lst(messy_lst)

# Using lambda functions and Reduce, calculate the average total response time, the average dispatch time, and average total time for the Detroit Police force.
def avg_tot_resp_time(lst):
    filtered = list(filter(lambda lst: lst['totalresponsetime'] != '', lst))
    total = reduce(lambda x, y: x + float(y['totalresponsetime']), filtered, 0)
    average = total / len(filtered)
    return average

avg_tot_resp_time(clean_lst)

def avg_dis_time(lst):
    filtered = list(filter(lambda lst: lst['dispatchtime'] != '', lst))
    total = reduce(lambda x, y: x + float(y['dispatchtime']), filtered, 0)
    average = total / len(filtered)
    return average

avg_dis_time(clean_lst)

def avg_tot_time(lst):
    filtered = list(filter(lambda lst: lst['totaltime'] != '', lst))
    total = reduce(lambda x, y: x + float(y['totaltime']), filtered, 0)
    average = total / len(filtered)
    return average

avg_tot_time(clean_lst)
    
# Using lambda and Map functions, or lambda and Filter, divide the list of dictionaries into smaller lists of dictionaries separated by neighborhood.
def neighborhood_division(lst):
    neighborhoods = []
    neighborhood_times = []
    for item in lst:
        if item['neighborhood'] in neighborhoods:
            continue
        else:
            neighborhoods.append(item['neighborhood'])
    for neighborhood in neighborhoods:
        neighborhood_lst = list(filter(lambda lst: lst['neighborhood'] == neighborhood, lst))
# Using lambda and Reduce, find the average total response time for each neighborhood, the average dispatch time for each neighborhood, and the average total time for each neighborhood and store this into a list of dictionaries.
        neighborhood_dict = {}
        neighborhood_dict['neighborhood'] = neighborhood
        neighborhood_dict['avg_tot_resp_time'] = avg_tot_resp_time(neighborhood_lst)
        neighborhood_dict['avg_dis_time'] = avg_dis_time(neighborhood_lst)
        neighborhood_dict['avg_tot_time'] = avg_tot_time(neighborhood_lst)
        neighborhood_times.append(neighborhood_dict)
    return neighborhood_times

neighborhood_lst_dict = neighborhood_division(clean_lst)


def write_json_file(lst):
# Using the JSON module, format your list of dictionaries as a JSON and test the output with the JSON lint website 
    json_lst = json.dumps(lst, indent=4)
# Write the tested JSON to a file
    with open('Neighborhood_Response_Times.json', 'w') as outfile:
        outfile.write(json_lst)
    return

write_json_file(neighborhood_lst_dict)