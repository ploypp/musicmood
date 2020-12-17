import urllib.parse, urllib.request, urllib.error, json
import random
import keys as keys
from flask import Flask, render_template, request

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

## Encode query parameters and create a URL to the API
baseurl = 'https://emoji-api.com/emojis'
paramstr = {"access_key":keys.emojikey}
fullurl = baseurl+"?"+urllib.parse.urlencode(paramstr)

## Handle any errors due to HTTP or connection related exceptions
def safeGet(url):
    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=header)
        x = urllib.request.urlopen(req)
        return x
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("Error trying to retrieve data:", e)
        elif hasattr(e, 'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)
        return None

## The function that takes url to call the API
def callPI(url):
    requeststr = safeGet(url).read()
    return json.loads(requeststr)

emojilist = callPI(fullurl)
emojiGroups = {}
for i in emojilist:
    if i["group"] not in emojiGroups:
        emojiGroups[i["group"]] = []
        emojiGroups[i["group"]].append(i["codePoint"])
    else:
        emojiGroups[i["group"]].append(i["codePoint"])

def getKeywordEmoji(codePoint):
    for i in emojilist:
        if i['codePoint'] == codePoint:
            return i['subGroup']

def noRepeatWord(list):
    newList = []
    if list != [None]:
        for i in list:
            hyphenWords = i.split("-")
            for word in hyphenWords:
                if word not in newList:
                    newList.append(word)
    return newList

@app.route("/")
def main_handler():
    emojihub = []
    emojitext = ""
    tabtext = ""
    for i in emojilist:
        if " " not in i["codePoint"] and i["codePoint"] not in emojihub:
            emojihub.append(i["codePoint"])
    # for i in emojihub:
    #     emojitext += f"<button type='button' id='{i}' class='emojibtn' onClick='myFunction(this)'>&#x{i}</button>\n"
    for i in emojiGroups:
        tabtext += f"<button class='w3-bar-item w3-button' onclick='openEmojiGroup('{i}')'>{i}</button>\n"
    for i in emojiGroups:
        emojitext += f"""
                    <div id='{i}' class='w3-container group' style='display:none'>
                      <h2>{i}</h2>
                      <button type='button' id='{emojiGroups[i]}' class='emojibtn' onClick='myFunction(this)'>&#x{emojiGroups[i]}</button>\n 
                    </div>\n
                    """
    # with open('templates/index.html', 'w') as htmlfile:
    #     htmlfile.write("""<!DOCTYPE html>\n
    #             <html>
    #             <head>
    #                 <meta charset="UTF-8">
    #                 <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    #                 <title>Music Mood</title>
    #                 <style>
    #                     body{font-family:Helvetica,Arial,sans-serif;font-size:16px;}
    #                     .emojibtn{display:inline;background:transparent;border-color:transparent;}
    #                 </style>
    #             </head>
    #             <body>""")
    #     htmlfile.write("""
    #                     <h1>Instructions</h1>
    #                     <p>1. Click to select emoji(s) of your choice</p>
    #                     <p>2. Hit "GO" button</p>
    #                     <p>3. Explore your Spotify track</p>
    #                     """)
    #     # htmlfile.write("<form action='response' onSubmit='onSubmit()'>")
    #     htmlfile.write("""
    #                     <form action='response' method='post'>
    #                     <div class="w3-bar w3-black">
    #                     """)
    #     htmlfile.write(f"{tabtext}")
    #     htmlfile.write("""
    #                     </div>
    #                     """)
    #
    #     htmlfile.write(f"{emojitext}")
    #
    #     # htmlfile.write(f"<script>function getInputValue() var inputVal = document.getElementById('{i}').value;")
    #     htmlfile.write("""
    #                    <input type='text' id='emojilist' name='emojilist' readonly='readonly'/><br />
    #                    <input type='submit' value='Go' name='gobtn'></form>
    #                    """)
    #     htmlfile.write("""
    #                    <script>
    #                     const list = [];
    #                     function myFunction(obj) {
    #                       document.getElementById(obj.id).style.backgroundColor = 'wheat'
    #                       if (list.includes(obj.id) === false) {
    #                         list.push(obj.id)
    #                         document.getElementById("emojilist").value = list
    #                       }
    #                     }
    #                     function openEmojiGroup(groupName) {
    #                       var i;
    #                       var x = document.getElementsByClassName("group");
    #                       for (i = 0; i < x.length; i++) {
    #                         x[i].style.display = "none";
    #                       }
    #                       document.getElementById(groupName).style.display = "block";
    #                     }
    #                     </script>
    #                    """)
    #     htmlfile.write("</body></html>")
    return render_template('index.html', page_title="Emoji Input")

# with open('templates/response.html', 'w') as htmlfile:
#     htmlfile.write("""<!DOCTYPE html>
#     <html><head><meta charset="UTF-8"><title>Music Mood</title>
#     <style>
#         body{font-family:Helvetica,Arial,sans-serif;font-size:16px;}
#         img{display:inline;}
#     </style>
#     </head><body>""")
#     htmlfile.write("""
#                 {% if input %}
#                 <a href="{{input}}">Link to spotify track</a>
#                 {% endif %}
#     """)
#     htmlfile.write("</body></html>")

class spotiClient():
    def __init__(self):
        self.accessToken = None
        self.spotifyAuth()

    def spotifyAuth(self):
        import base64
        authorization = base64.standard_b64encode(("9f8d403081d944b58ca9788d1e9015a3" +
                                                   ':' + keys.spotifykey).encode())
        headers = {"Authorization": "Basic " + authorization.decode()}
        params = {"grant_type": "client_credentials"}
        encodedparams = urllib.parse.urlencode(params).encode()
        request = urllib.request.Request(
            'https://accounts.spotify.com/api/token',
            data=encodedparams, headers=headers)
        resp = urllib.request.urlopen(request)
        respdata = json.load(resp)
        self.accessToken = respdata['access_token']

    def apiRequest(self,
                   version="v1",
                   endpoint="search",
                   item=None,
                   params=None):
        if self.accessToken is None:
            print(
                "Sorry, you must have an access token for this to work.")
            return {}
        baseurl = "https://api.spotify.com/"
        endpointurl = "%s%s/%s" % (baseurl, version, endpoint)
        if item is not None:
            endpointurl = endpointurl + "/" + item
        if params is not None:
            fullurl = endpointurl + "?" + urllib.parse.urlencode(params)
        headers = {"Authorization": "Bearer " + self.accessToken}
        request = urllib.request.Request(fullurl, headers=headers)
        resp = urllib.request.urlopen(request)
        return json.load(resp)

@app.route("/response", methods=['POST'])
def response_handler():

    if request.method == 'POST':
        emoji = request.form.get('emojilist')
        codePointList = emoji.split(",")
        keywords = []
        for i in codePointList:
            keywords.append(getKeywordEmoji(i))

        sclient = spotiClient()
        links = []
        info = {}
        if len(noRepeatWord(keywords)) != 0:
            query = random.choice(noRepeatWord(keywords))
            results = sclient.apiRequest(params={"q": query, "type": "track", "limit": "20"})
            for k in results['tracks']['items']:
                links.append(k['external_urls']['spotify'])
                info[k['external_urls']['spotify']] = {}
                info[k['external_urls']['spotify']]['artist'] = k['artists'][0]['name']
                info[k['external_urls']['spotify']]['img'] = k['album']['images'][0]['url']
                info[k['external_urls']['spotify']]['name'] = k['name']
        else:
            links.append('https://open.spotify.com/track/1OEwH8MNTyvksafcZjSfnL?si=D_bF5gg-Q7aTRo1GPvr-eA')
            info['https://open.spotify.com/track/1OEwH8MNTyvksafcZjSfnL?si=D_bF5gg-Q7aTRo1GPvr-eA'] = {}
            info['https://open.spotify.com/track/1OEwH8MNTyvksafcZjSfnL?si=D_bF5gg-Q7aTRo1GPvr-eA']['artist'] = 'Kevin Farrell'
            info['https://open.spotify.com/track/1OEwH8MNTyvksafcZjSfnL?si=D_bF5gg-Q7aTRo1GPvr-eA']['img'] = 'https://i.scdn.co/image/ab67616d00001e027537b57f46602cca4e47a8d8'
            info['https://open.spotify.com/track/1OEwH8MNTyvksafcZjSfnL?si=D_bF5gg-Q7aTRo1GPvr-eA']['name'] = 'Please Choose One'
        finaltrack = random.choice(links)
        return render_template('response.html', input=finaltrack, image=info[finaltrack]['img'],
                               artist=info[finaltrack]['artist'], trackname=info[finaltrack]['name'])
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True )