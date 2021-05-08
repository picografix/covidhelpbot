#Add your credentials here
from datetime import datetime
import pytz
import timeago
import tweepy
import pandas as pd
from config import twitter_keys

s1=['created_at','id_str','full_text','retweet_count','user.name','user.screen_name',
'user.followers_count','user.verified','user.favourites_count']
append_str = 'retweeted_status.'
s2=[append_str + sub for sub in s1]
#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
def input_triggers_spinner(city,ess):
    squery=city+" "+ess+" available verified"
    # for r in api.search(q=squery,result_type='recent',tweet_mode='extended',count=3):
    #     print(r)
    df = [r._json for r in api.search(q=squery,result_type='recent',tweet_mode='extended',count=5)]
    df = pd.json_normalize(df)
    og=df[~df['retweeted_status.full_text'].isnull()][s2]
    nog=df[df['retweeted_status.full_text'].isnull()][s1]
    og.columns=s1
    df=pd.concat([nog,og]).drop_duplicates(subset=['full_text'], keep='first',ignore_index=True)
    df["id_str"]= 'https://twitter.com/twitter/statuses/' + df["id_str"]
    for i in df.index:
        df.at[i,'created_at']=datetime.strftime(datetime.strptime(df.at[i,'created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    df=df.sort_values(by=['created_at'],ascending=False,ignore_index=True)   
    t=datetime.now(pytz.timezone('GMT')).strftime("%Y-%m-%d %H:%M:%S")
    for i in df.index:
        df.at[i,'created_at']=timeago.format(df.at[i,'created_at'],t)
    rows = []
    links = df['id_str'].to_list()
    for x in links:
        link = '[Link](' +str(x) + ')'
        rows.append(link) 
    df['id_str']=rows
    df=df.to_dict('records')
    return df

# we=input_triggers_spinner('delhi','oxygen')
# print(we[0]['full_text'])