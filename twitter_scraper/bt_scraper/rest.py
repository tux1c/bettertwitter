import requests

def run_query(url, token = -1, cookie = -1):
    ua = "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.8 Firefox/68.0 PaleMoon/29.0.1"
    auth = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

    if (-1 == token):
        headers = { "User-Agent": ua }
    else:
        headers = { "User-Agent": ua, "authorization": auth, "x-guest-token": token }

    r = requests.get(url, headers=headers)
    return r.text
