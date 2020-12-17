# MUSICMOOD

MusicMood is a web application that will turn your mood into a song. You can select the emoji(s) of your choice, and MusicMood will generate a track for you. Get ready and go explore the music of your mood at https://musicmoodspotify.appspot.com/.

## A Change in Project Proposal

In this project, I have built an interactive web application that takes an emoji as input from the user and give a Spotify music track. This app will pair a song with moods from the emoji of the user’s choice Initially, I was planing to use tags in Gemoji library to get more keywords, but after reviewing them, I decided not to include Gemoji because the tags are too broad and probably will affect search results.

## API Keys

I did not push "keys.py" file to GitHub, so you might need to create that file in order to make the code works. Inside "keys.py" file, I have three lines of code indicating "spotifyid", "spotifykey" and "emojikey".

To get "emojikey", you can go to https://emoji-api.com/ and register for a key using your email, then copy the API key from their website directly.

To get "spotifyid" and "spotifykey", you can go to https://developer.spotify.com/, then go to Dashboard and login/sign up for the key. Spotify API is a little bit different from Open Emoji API since it has Client ID provided for each developer. You can use that Client ID for "spotifyid" and Client Secret for "spotifykey".

And that should be it. You should be able to run my project now!