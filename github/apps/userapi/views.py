import json
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import UserData, UserPublicRepoData

github_user_url = "https://api.github.com/users"

access_token = "04d7d8bc17c76e3514a3872ed480dfc7ba882d37"
client_id = "5110e9d9a9e472890c1d"
client_secret = "4fa22615f5699eabd02907f97edeca09297ff644"

github_url = github_user_url + "?access_token=" + access_token

# Create your views here.
def index(request):
    start = int(request.GET.get('start',1))
    end = int(request.GET.get('end',5))
    return render(request,'userpage.html',{'start':start,'end':end})

def get_user_data(request):
    if request.method == 'GET':
        start = int(request.GET.get('start'))
        end = int(request.GET.get('end'))
        user_data = UserData.objects.all()
        data = []
        for user in user_data[start-1:end]:
            dict_data = {}
            dict_data['id'] = user.id
            dict_data['username'] = user.username
            dict_data['avatar'] = user.avatar_url
            dict_data['user_type'] = user.user_type
            dict_data['public_repos'] = []
            repo_resp = UserPublicRepoData.objects.select_related('user_id').filter(user_id=user.id)
            for repo in repo_resp:
                repo_dict = {}
                repo_dict['name'] = repo.title
                repo_dict['full_name'] = repo.repo_name
                repo_dict['description'] = repo.description
                dict_data['public_repos'].append(repo_dict)
            data.append(dict_data)

            current_url = request.META['HTTP_HOST']

            if ((start+5) > 30):
                next_url = "http://"+ current_url
            else:
                next_url = "http://"+ current_url+ '/?start=' + str(start+5)+ '&end='+ str(end+5)

            if ((start-5) >= 1):
                prev_url = "http://"+ current_url+ '/?start='+str(start-5)+'&end='+ str(end-5)
            else:
                prev_url = "http://"+ current_url
        return JsonResponse({'data': data,'next':next_url,'prev':prev_url}, content_type="application/json")

def get_repo_contents(request):
    repo = request.GET.get('repo', None)
    username = repo.split('/')[0]
    repo_dir = repo.split('/')[1]
    folder_path = request.GET.get('dir', '')
    if folder_path == '':
        repo_contents_url = 'https://api.github.com/repos/' + \
                            repo + '/contents?client_id=' + client_id + "&client_secret=" + client_secret
        bread = [(repo_dir, '')]
        # folder_path = ''
    else:
        repo_contents_url = 'https://api.github.com/repos/' + \
                            repo + '/contents/' + folder_path +'?client_id=' + client_id + "&client_secret=" + client_secret
        bread = []
        path_bread = []
        bread.append(repo_dir)
        bread.extend(folder_path.split('/'))
        bread_path = ''
        bread.remove('')
        for b in bread:
            if b == repo_dir:
                bread_path = ''
            else:
                bread_path = bread_path + "/" + b
            path_bread.append(bread_path)
        bread = zip(bread, path_bread)

    response = requests.get(repo_contents_url)
    json_response = json.loads(response.text)
    data_dict = {'files':[],'directories':[]}
    for resp in json_response:
        # print (resp)
        type_of_content = resp['type']
        if type_of_content == 'file':
            data_dict['files'].append(resp['name'])
        else:
            data_dict['directories'].append(resp['name'])

    return render(
        request, 'repopage.html',
        {'files': data_dict['files'],
         'directories': data_dict['directories'],
         'current_directory': folder_path,
         'bread': bread,
         'username':username,
         'repo':repo
         }
    )

def download(request):
    file_path = request.GET.get('dir', None)
    repo = request.GET.get('repo',None)
    contents_url = 'https://api.github.com/repos/' + repo + '/contents/' + file_path + \
                   '?client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(contents_url)
    json_response = json.loads(response.text)
    download_url = json_response['download_url']

    return HttpResponseRedirect(download_url)
