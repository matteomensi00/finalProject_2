#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/python3

def extract_info_pickup(data):
    """With this function we are going to extract the name of the pickup location of the people who took the taxi,
    using geoapify"""
    
    
    longitude = data['pickup_longitude']
    latitude = data['pickup_latitude']
    
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&format=json&apiKey={api_key}"
    #this url takes the coordinates to give back the name of the location
    
    resp = requests.get(url)
    keys = resp.json()['results'][0] #a dict wich contains all the info we can extract related to the name location.
    
    
    """ let's find street flag. if nothing is found, just skip the row"""
    if 'street' in keys:
         street= resp.json()['results'][0]['street']
         
    elif 'road' in keys:
         street= resp.json()['results'][0]['road'] #in some cases the street flag is replaced by road flag. they are the same thing.
    else:
        return pd.Series([None, None,None])
    
    """let's do the same thing for suburb. if nothing is found, just skip the row"""
    if 'suburb' in keys:
        suburb= resp.json()['results'][0]['suburb']
    else:
        return pd.Series([None, None,None])
    
    """let's do the same thing for city. if nothing is found, just skip the row"""
    if 'city' in keys:
        city = resp.json()['results'][0]['city']
    else:
        return pd.Series([None, None,None])

        
    return pd.Series([street, suburb, city])

def extract_info_dropoff(data):
    """With this function we are going to extract the name of the dropoff location of the people who took the taxi,
    using geoapify"""
    
    
    longitude = data['dropoff_longitude']
    latitude = data['dropoff_latitude']
    
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&format=json&apiKey={api_key}"
    #this url takes the coordinates to give back the name of the location
    
    resp = requests.get(url)
    keys = resp.json()['results'][0] #a dict wich contains all the info we can extract related to the name location.
    
    
    """ let's find street flag. if nothing is found, just skip the row"""
    if 'street' in keys:
         street= resp.json()['results'][0]['street']
         
    elif 'road' in keys:
         street= resp.json()['results'][0]['road'] #in some cases the street flag is replaced by road flag. they are the same thing.
    else:
        return pd.Series([None, None,None])
    
    """let's do the same thing for suburb. if nothing is found, just skip the row"""
    if 'suburb' in keys:
        suburb= resp.json()['results'][0]['suburb']
    else:
        return pd.Series([None, None,None])
    
    """let's do the same thing for city. if nothing is found, just skip the row"""
    if 'city' in keys:
        city= resp.json()['results'][0]['city']
    else:
        return pd.Series([None, None,None])

        
    return pd.Series([street, suburb,city])

def calculate_distance(data):
    """We are going to use h3 library to take in input the coordinates in number and 
     calculate the distance between the coordinates given in input"""
    
    pick_latitude = data['pickup_latitude']
    pick_longitude = data['pickup_longitude'] #setting the pickup coordinates
    
    
    drop_latitude = data['dropoff_latitude']
    drop_longitude = data['dropoff_longitude'] #setting the dropoff coordinates
    
    pick_coords = (pick_latitude, pick_longitude)
    drop_coords = (drop_latitude,drop_longitude)
    distance = h3.point_dist(pick_coords, drop_coords)
    distance= distance*0.62
    return round(distance, 2)

def calculate_fare_2016(data):
    """With this function we consider the ny taxi fare from 2016. see the doc to discover more"""
    
    """introducing fare and plus"""
    initial_charge = 2.5
    fare_per_mile = 2.5
    fare_per_minute=0.5
    
    """manipulating the data to extract hour and week day name """
    start_hour = pd.to_datetime(data['pickup_datetime']).hour
    end_hour = pd.to_datetime(data['dropoff_datetime']).hour
    start_day = pd.to_datetime(data['pickup_datetime']).day_name()
    
    
    """Extracting distance and duration """
    distance = data['distance_miles']
    duration = data['trip_duration'] #in seconds
    duration = duration/60  #trasformed in minute
    
    
    
    cost_per_mile = fare_per_mile * distance
    
    cost_per_minute = fare_per_minute * duration
    
    
    
    if start_hour >= 20 and end_hour <=6: #applying supercharge 
        cost_per_mile = cost_per_mile + 1
        cost_per_minute = cost_per_minute + 1
    
    if start_day not in ('Saturday','Sunday'): #applying supercharge 
        cost_per_mile = cost_per_mile + 2.5
        cost_per_minute = cost_per_minute + 2.5
        
    total_cost = initial_charge + cost_per_mile + cost_per_minute
    return round(total_cost, 1)


if __name__== "__main__":
    import pandas as pd
    import requests
    import h3
    import datetime as dt
    data=pd.read_csv("trainsampled.csv")
    
    """ check on Nan of coordinates and any others column. let's exclude everything that is not none"""
    data = data.dropna(thresh=len(data.columns)-1).copy()
    
    """manipulation of the date columns"""
    data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
    data['dropoff_datetime'] = pd.to_datetime(data['dropoff_datetime']) 

    """check on id, if they are unique"""
    data.drop_duplicates(subset=['id'],inplace=True)

    """check on date format"""
    data['pickup_datetime'] = data['pickup_datetime'].dt.strftime("%Y-%m-%d %H:%M:%S")
    data['dropoff_datetime'] = data['dropoff_datetime'].dt.strftime("%Y-%m-%d %H:%M:%S")

    """ check on dates. it should be: pickup_datetime < dropoff_datetime, otherwise there is an error """
    data = data[data['pickup_datetime'] < data['dropoff_datetime']].copy()

    """ check on passenger_count, to set a max number of passenger """
    data = data[(data['passenger_count']> 0) & (data['passenger_count'] <=6)].copy()

    """ check on trip duration: >0 and < 6 hour. 
    we assume that over 6 hours there is an error in the data """
    data = data[(data['trip_duration'] > 0) & (data['trip_duration'] <=21600)].copy()

    api_key="e5eec44335d5436b89247f909654bff2" #api key of geoapify

    data[['pickup_street', 'pickup_suburb','pickup_city']] = data.apply(extract_info_pickup, axis=1) #inserting new data
    data[['dropoff_street', 'dropoff_suburb','dropoff_city']] = data.apply(extract_info_dropoff, axis=1) #inserting new data
    data['distance_miles'] = data.apply(calculate_distance, axis=1) #inserting new data
    data['trip_price'] = data.apply(calculate_fare_2016, axis=1) #inserting new data

    """ drop all rows which contan null values """
    data = data.dropna(thresh=len(data.columns)-1).copy() 
    
    """export the results"""
    data.to_csv("taxi_ny.csv", index=False)

