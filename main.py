import requests, csv

client_id = '' # redacted
client_secret = '' # redacted
access_token = '' # redacted

csv_header = ["Date First Had","Beer Name","Beer Style","Brewery Name","ABV","IBU","User Rating","Global Rating","Brewery City","Brewery State","Country","Brewery Type"]
csv_data = [] # This will be a list of lists. Each nested list will be one row of the CSV, or, one beer's data.
num_checkins_recorded = 0 # counter variable for determining offset value of each API call
total_user_distinct_count = 0

def make_API_request(first_API_call:bool):
    global num_checkins_recorded, total_user_distinct_count

    if first_API_call is True:
        response = requests.get(f"https://api.untappd.com/v4/user/beers/?access_token={access_token}&limit=50").json()
    else:
        response = requests.get(f"https://api.untappd.com/v4/user/beers/?access_token={access_token}&offset={num_checkins_recorded}&limit=50").json()
    
    distinct_beers = response['response']['beers']['items'] # this is a list of dictionaries
    total_user_distinct_count = response['response'].get('total_count')

    for beer in distinct_beers: # beer is a dictionary
        beer_data = [] # create an empty list and append the following data to it
        beer_data.append(beer.get('first_had')) # date beer was first checked in
        beer_data.append(beer.get('beer').get('beer_name'))
        beer_data.append(beer.get('beer').get('beer_style'))
        beer_data.append(beer.get('brewery').get('brewery_name'))
        beer_data.append(beer.get('beer').get('beer_abv'))
        beer_data.append(beer.get('beer').get('beer_ibu'))
        beer_data.append(beer.get('rating_score')) # user rating
        beer_data.append(beer.get('beer').get('rating_score')) # global rating
        beer_data.append(beer.get('brewery').get('location').get('brewery_city'))
        beer_data.append(beer.get('brewery').get('location').get('brewery_state'))
        beer_data.append(beer.get('brewery').get('country_name'))
        beer_data.append(beer.get('brewery').get('brewery_type'))

        num_checkins_recorded += 1
        print(f'Distinct beers recorded: {num_checkins_recorded} / {total_user_distinct_count}')
        csv_data.append(beer_data) # append list of data for each beer to master list

make_API_request(True)

while num_checkins_recorded < total_user_distinct_count:
    make_API_request(False)

with open('Untappd_distinctbeers_JO_041222.csv','w',newline='',encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_header)

    for line in csv_data:
        csv_writer.writerow(line)

print("Data collection complete.")
