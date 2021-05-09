from utils import *
import pandas as pd
import csv
fetcher = DataFetcherState() #declare fetch
fetcher.fetch() #initiate fetch

def stats(state):
    # data_mh = np.array(fetcher.data[state]['deceased'], dtype=float) # Starting date is 14th March #use tt for india data 
    # data_mh = np.concatenate((np.zeros(27), data_mh))
    df = pd.DataFrame(fetcher.data) #convert to pandas dataframe
    c,r,d,a = giveArray(df,state, True)
    return int(c[-1]),int(r[-1]),int(d[-1]),int(a[-1])


# print(allStates(fetcher.data))
# reader = csv.DictReader(open('states.csv'))
# dictobj = next(reader)
df = pd.read_csv("states.csv")
code = list(df['code'])
statename = list(df['state'])
states = dict(zip(statename,code))

# print(states)
def driver(statename):
    return stats(states[statename])
print(driver('andaman and nicobar'))