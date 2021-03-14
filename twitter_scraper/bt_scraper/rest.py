import requests

def run_query(url, token = -1, cookies = None):
    ua = "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.8 Firefox/68.0 PaleMoon/29.0.1"
    auth = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    c = None


    if (-1 == token):
        headers = { "User-Agent": ua }
    else:
        if (None == cookies):
            headers = { "User-Agent": ua, "authorization": auth, "x-guest-token": token }
        else:
            headers = { "User-Agent": ua, "authorization": auth, "x-csrf-token": cookies['token'] }
            c = { 'ct0': cookies['token'], 'auth_token': cookies['auth'] }

    if (None == c):
        r = requests.get(url, headers=headers)
    else:
        r = requests.get(url, headers=headers, cookies=c)
    return r.text
