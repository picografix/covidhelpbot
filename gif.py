import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import urllib.request
import ssl
from bs4 import BeautifulSoup as bs
from random import randint
def give_url(incoming_msg):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC' # str | Giphy API Key.
    q = incoming_msg # str | Search query term or prhase.
    limit = 10 # int | The maximum number of records to return. (optional) (default to 25)
    offset = 0 # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating = 'g' # str | Filters results by specified rating. (optional)
    lang = 'en' # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'json' # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try: 
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang, fmt=fmt)
        L=api_response.data
        i=randint(0,len(L)//3)
        url=L[i].embed_url
        a=urllib.request.urlopen(url,context=ctx).read()
        soup=bs(a,'lxml')
        L=soup.find_all('meta')
        url=L[11].get('content')
        #width: 480px;
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
    return url
if __name__=="__main__":
    print(give_url("Bye"))