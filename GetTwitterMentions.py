# pip install requests
# pip install requests-oauthlib
import urlparse
import json
import requests
from requests_oauthlib import OAuth1
from pprint import pprint

stateFull = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District Of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
stateAbbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NM', 'NY', 'NJ', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


# API secrets. NEVER share these with anyone!
CLIENT_KEY = "4Vw0po0lRx2v0E1odV2VbUDww"
CLIENT_SECRET = "NBdRk244bB3vdCBKewlOnfTQeIiEk4Dcqq6D89jDaQFwrJUkDj"


API_URL = "https://api.twitter.com"
REQUEST_TOKEN_URL = API_URL + "/oauth/request_token"
AUTHORIZE_URL = API_URL + "/oauth/authorize?oauth_token={request_token}"
ACCESS_TOKEN_URL = API_URL + "/oauth/access_token"
TIMELINE_URL = API_URL + "/1.1/statuses/home_timeline.json"
MENTIONS_URL = API_URL + "/1.1/statuses/mentions_timeline.json"


def get_request_token():
    """ Get a token allowing us to request user authorization """
    oauth = OAuth1(CLIENT_KEY, client_secret=CLIENT_SECRET)
    response = requests.post(REQUEST_TOKEN_URL,
                             auth=oauth)
    credentials = urlparse.parse_qs(response.content)

    request_token = credentials.get("oauth_token")[0]
    request_secret = credentials.get("oauth_token_secret")[0]
    return request_token, request_secret


def get_access_token(request_token, request_secret, verifier):
    """"
    Get a token which will allow us to make requests to the API
    """
    oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   resource_owner_key=request_token,
                   resource_owner_secret=request_secret,
                   verifier=verifier)

    response = requests.post(ACCESS_TOKEN_URL, auth=oauth)
    credentials = urlparse.parse_qs(response.content)
    access_token = credentials.get('oauth_token')[0]
    access_secret = credentials.get('oauth_token_secret')[0]
    return access_token, access_secret


def get_user_authorization(request_token):
    """
    Redirect the user to authorize the client, and get them to give us the
    verification code.
    """
    authorize_url = AUTHORIZE_URL
    authorize_url = authorize_url.format(request_token=request_token)
    print 'Please go here and authorize: ' + authorize_url
    return raw_input('Please input the verifier: ')


def store_credentials(access_token, access_secret):
    """ Save our access credentials in a json file """
    with open("access.json", "w") as f:
        json.dump({"access_token": access_token,
                   "access_secret": access_secret}, f)


def get_stored_credentials():
    """ Try to retrieve stored access credentials from a json file """
    with open("access.json", "r") as f:
        credentials = json.load(f)
        return credentials["access_token"], credentials["access_secret"]


def authorize():
    """ A complete OAuth authentication flow """
    try:
        access_token, access_secret = get_stored_credentials()
    except IOError:
        request_token, request_secret = get_request_token()
        verifier = get_user_authorization(request_token)
        access_token, access_secret = get_access_token(request_token,
                                                       request_secret,
                                                       verifier)
        store_credentials(access_token, access_secret)

    oauth = OAuth1(CLIENT_KEY,
                   client_secret=CLIENT_SECRET,
                   resource_owner_key=access_token,
                   resource_owner_secret=access_secret)
    return oauth

def GetUsernameAndText():
    auth = authorize()
    response = requests.get(MENTIONS_URL, auth=auth)
    j = response.json()
    # print j[0].keys() 
    #create a list
    TweetInfo=[]
    for i in j:
        screen_name = i['user']['screen_name']
        text = i['text']
        #append (screenname, text) to list
        x = (screen_name, text)
        TweetInfo.append(x)
    #return the list of everything   
    return TweetInfo
    #[('FOO','tweet'), ('Lady Gaga', 'raarh')]


def find_state(tweet):
    return next((state for state in stateFull if state in tweet), None)

#In Function Below I learned how to append multiple values to a repeated key
def extract_state_and_sn():
    state_dict= {}
    extracting = GetUsernameAndText()
    
    for sn, text in extracting:
        state = find_state(text)
        state_dict.setdefault(sn,[]).append(state)
    return state_dict
    #[('ladygaga', 'Arkansas'), ('BarackObama', 'California')]

# def compose_tweet():


def main():
    """ Main function """
    authorize()
    y= extract_state_and_sn()
    print "-------"*10
    print y
    print "-------"*10

    # tweets_with_states = extract_states(TweetInfo)
    
    #keep track of who i've already tweeted at
    
    #for (username, tweet) in tweet_list:
    #     parse_state(tweet)


    #instructions for if use dict
    #for (username, tweet) in tweet_dict.iteritems()
    #for username in tweet_dict:
    #     parse_state(tweet_dict[username])
    


if __name__=="__main__":
    main()