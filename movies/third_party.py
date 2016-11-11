import json
import requests


class YouTube(object):

    BASE_VIDEO_URL = "https://www.youtube.com/watch?v="
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"
    API_KEY = "AIzaSyCNiNYR8Ge9Gy3nSspZSVrmSTHS0S0Ms7Q"
    PARAMS = {
        "key": API_KEY,
        "part": "snippet",
    }

    def search(self, query):

        params = self.PARAMS
        params["q"] = query

        response = requests.get(
            url=self.BASE_URL,
            params=params
        )

        if response.status_code != 200:
            return None

        return json.loads(response.text)

    def search_trailer(self, movie_name):

        query = "{} {}".format(movie_name, "trailer")

        youtube_data = self.search(query)

        if youtube_data['items']:
            return "{}{}".format(
                self.BASE_VIDEO_URL,
                youtube_data['items'][0]['id']['videoId'],
            )

        return None


YouTube = YouTube()
