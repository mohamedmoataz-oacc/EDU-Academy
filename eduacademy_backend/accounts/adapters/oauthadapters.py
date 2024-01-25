import datetime
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
import requests
import json

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)

        person_fields = ['birthdays', 'genders']
        data = requests.get(
            f'https://people.googleapis.com/v1/people/me?access_token={token}&personFields={",".join(person_fields)}'
        )
        data = json.loads(data.text)
        login.user.gender = data['genders'][0]['formattedValue'][0]
        birth_date = data['birthdays'][0]['date']
        login.user.birth_date = f"{birth_date['year']}-{birth_date['month']}-{birth_date['day']}"
        return login

class CustomFacebookOAuth2Adapter(FacebookOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)

        fields = ['gender', 'birthday']
        data = requests.get(
            f'https://graph.facebook.com/v18.0/me?fields={",".join(fields)}&access_token={token}'
        )
        data = json.loads(data.text)
        login.user.gender = data["gender"][0].capitalize()
        login.user.birth_date = datetime.datetime.strptime(data["birthday"], '%m/%d/%Y').strftime('%Y-%m-%d')
        return login