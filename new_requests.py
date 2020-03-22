# usage:
# retries default to be 3
# req = new_requests.get('https://www.peterbe.com')
# req.status_code
# req == None if fail
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# https://www.peterbe.com/plog/best-practice-with-retries-with-requests


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None):

    # usage:
    # s = requests.Session()
    # s.auth = ('user', 'pass')
    # user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    # s.headers.update({'User-Agent': user_agent})
    #
    # default retries is 3
    # response = requests_retry_session(session=s, retries=3).get(
    #     'https://www.peterbe.com'
    # )
    # print(response.status_code)

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get(url, retries=3):
    s = requests.Session()
    # s.auth = ('user', 'pass')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    s.headers.update({'User-Agent': user_agent})
    try:
        response = requests_retry_session(session=s, retries=retries).get(
            url
        )
    except Exception as e:
        print('It failed :(', e.__class__.__name__)
        print(e)
        return None
    else:
        print('It eventually worked', response.status_code)
    return response
