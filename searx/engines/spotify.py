"""
 Spotify (Music)

 @website     https://spotify.com
 @provide-api yes (https://developer.spotify.com/web-api/search-item/)

 @using-api   yes
 @results     JSON
 @stable      yes
 @parse       url, title, content, embedded
"""

from json import loads
from urllib.parse import urlencode
import requests
import base64

# engine dependent config
categories = ['music']
paging = True
api_client_id = None
api_client_secret = None

# search-url
url = 'https://api.spotify.com/'
search_url = url + 'v1/search?{query}&type=track&offset={offset}'

embedded_url = '<iframe data-src="https://embed.spotify.com/?uri=spotify:track:{audioid}"\
     width="300" height="80" frameborder="0" allowtransparency="true"></iframe>'


# do search-request
def request(query, params):
    offset = (params['pageno'] - 1) * 20

    params['url'] = search_url.format(query=urlencode({'q': query}), offset=offset)

    r = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        headers={'Authorization': 'Basic ' + base64.b64encode(
            "{}:{}".format(api_client_id, api_client_secret).encode()
        ).decode()}
    )
    j = loads(r.text)
    params['headers'] = {'Authorization': 'Bearer {}'.format(j.get('access_token'))}

    return params


# get response from search-request
def response(resp):
    results = []

    search_res = loads(resp.text)

    # parse results
    for result in search_res.get('tracks', {}).get('items', {}):
        if result['type'] == 'track':
            title = result['name']
            url = result['external_urls']['spotify']
            content = '{} - {} - {}'.format(
                result['artists'][0]['name'],
                result['album']['name'],
                result['name'])

            embedded = embedded_url.format(audioid=result['id'])

            # append result
            results.append({'url': url,
                            'title': title,
                            'embedded': embedded,
                            'content': content})

    # return results
    return results
