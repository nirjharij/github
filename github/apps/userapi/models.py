from django.db import models

# Create your models here.
class UserData(models.Model):
    github_id = models.IntegerField()
    username = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=100)
    repos_url = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)

class UserPublicRepoData(models.Model):
    user_id = models.ForeignKey(UserData,on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000,null=True)