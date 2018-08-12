import requests
import json
from github.apps.userapi.models import UserData
from github.apps.userapi.models import UserPublicRepoData


github_user_url = "https://api.github.com/users"
access_token = "04d7d8bc17c76e3514a3872ed480dfc7ba882d37"
client_id = "5110e9d9a9e472890c1d"
client_secret = "4fa22615f5699eabd02907f97edeca09297ff644"
github_url = github_user_url + "?access_token=" + access_token


def get_user_data(url):
    response = requests.get(url)
    json_response = json.loads(response.text)

    for resp in json_response:
        u = UserData(github_id=resp['id'], username=resp['login'], avatar_url=resp['avatar_url'], repos_url=resp['repos_url'],
                     user_type=resp['type'])
        u.save()


def get_user_public_repo():
    user_data = UserData.objects.all()
    for user in user_data:
        repos_url = user.repos_url
        repo_url = repos_url + "?client_id=" + client_id + "&client_secret=" + client_secret
        repo_response = requests.get(repo_url)
        repo_resp = json.loads(repo_response.text)

        for resp in repo_resp:
            r = UserPublicRepoData(user_id=UserData.objects.get(id=user.id),repo_name=resp['full_name'],
                                   title=resp['name'],description=resp['description'])
            r.save()

get_user_public_repo()