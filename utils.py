#imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
# from scipy.integrate import solve_ivp
import datetime
from copy import deepcopy
from scipy.stats import norm
from scipy.optimize import differential_evolution
import pdb
from IPython.core.display import HTML
from math import ceil, floor
from itertools import chain
# from scipy.signal import savgol_filter
# from scipy.special import expit
# from scipy.integrate import solve_ivp
from itertools import product
import tqdm
import os
from pathlib import Path
import datetime

class DataFetcher:
    """
    Fetch data for the entire country from covid19india. 
    
    Example usage:
    ```
    fetcher = DataFetcher() 
    fetcher.fetch()             # This command retrieves and processes data 
    fetcher.cases_time_series   # Cumulative confirmed cases are now stored in this field
    ```
    """

    def __init__(self, url="https://api.covid19india.org/data.json"):
        self.url = url
        self.json_data = None
        self.cases_time_series = None
        
    def fetch(self):
        r = requests.get(url=self.url)
        self.json_data = r.json()
        
        # Get the fields
        fields = list(self.json_data['cases_time_series'][0].keys())
        self.cases_time_series = {}
        
        for field in fields:
            if field == 'date':
                self.cases_time_series[field] = [x[field] for x in self.json_data['cases_time_series']]
            else:
                self.cases_time_series[field] = np.array([float(x[field]) for x in self.json_data['cases_time_series']])
        
    def train_data(self, threshold):
        self.fetch()
        index = np.where(self.cases_time_series["totaldeceased"] > threshold)[0][0]
        startdate = self.cases_time_series["date"][index]
        return self.cases_time_series["totaldeceased"][index:], startdate

class DataFetcherState:
    """
        Fetch state-wise COVID19 data from the covid19india website
        Example usage:
        ```
        fetcher = DataFetcher() 
        fetcher.fetch()             # This command retrieves and processes data 
        ```
        
        The `fetch` method retrives and processes data and stores it in the `data` dictionary. E
        Example usage:
        ```
        fetcher.data['mh']['deceased']      # Cumulative number of deceased people in maharashtra
        fetcher.data['dl']['recovered']     # Cumulative number of recovered people in delhi
        fetcher.data['gj']['confirmed']     # Cumulative number of confirmed cases in Gujarat
        ```
    """
    
    def __init__(self):
        self.data = None
        self.raw_data = None
    
    def fetch(self):
        # Fetch the raw data
        r = requests.get(url="https://api.covid19india.org/states_daily.json")
        self.raw_data = r.json()
        self.data = {}
        
        # Iterate over the days and record the data
        for entry in self.raw_data['states_daily']:
            status = entry['status'].lower()
            for state in entry:
                if state == "date" or state == "status":
                    continue
                    
                if state not in self.data:
                    # Initialize this state
                    self.data[state] = {
                        'deceased' : [],
                        'recovered': [],
                        'confirmed': []
                    }
                
                # Append the data
                self.data[state][status].append(entry[state])
        
                
    def start_date(self):
        return self.raw_data['states_daily'][0]['date']


def giveArray(df,s,commulative=True):
    # data_mh = np.array(fetcher.data['tt']['deceased'], dtype=float) # Starting date is 14th March #use tt for india data 
    # data_mh = np.concatenate((np.zeros(27), data_mh))
    # df = pd.DataFrame(fetcher.data) #convert to pandas dataframe
    recovered = np.array(df[s]['recovered']).astype(np.float)
    death = np.array(df[s]['deceased']).astype(np.float)  
    confirmed = np.array(df[s]['confirmed']).astype(np.float)
    active = confirmed - recovered - death
    if(not commulative):
        return confirmed,recovered, death, active
    for i in range(1,len(death)): #loop for cummulative deaths
        death[i] = death[i] + death[i-1]
        active[i] = active[i]+active[i-1]
        recovered[i] = recovered[i] + recovered[i-1]
        confirmed[i] = confirmed[i] + confirmed[i-1]
    
    return confirmed,recovered, death, active
    
def allStates(State_dict, india =True):
    all_states = list(State_dict.keys())
    all_states.pop(all_states.index('dateymd'))
    if(india):
        return all_states
    else:
        all_states.pop(all_states.index('tt'))
        return all_states
