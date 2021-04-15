from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class GenreField(models.Model):
    """
    Different Genre For Each Sectors
    """
    genre_type = models.CharField(max_length=56,unique=True)


    def __str__(self):
        return (f'{self.genre_type}')[:15]


class SectorField(models.Model):
    """
    Relation For Each Sector, Example: Travel, Sports"
    """
    name = models.CharField(max_length=56,unique=True)
    image = models.URLField()
    genre = models.ManyToManyField(GenreField,related_name='sec')


    def __str__(self):
        return (f'{self.name}')[:15]



class Request(models.Model):
    """
    Relation For Request Posted By User
    """
    requester = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='req')
    sector = models.ForeignKey(SectorField,on_delete=models.CASCADE,related_name='reqsec')
    genre = models.CharField(max_length=56,null=True,blank=True)
    subject = models.CharField(max_length=128)
    content = models.TextField()
    match_with_same_gender = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    is_first_year_req = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        subject = (self.subject)[:15]
        return f'By {self.requester}: {subject}'



class InitialMatchingRequest(models.Model):
    """
    Relation to Store Match after initial "Request" Send by User
    """
    request = models.ForeignKey(Request,on_delete=models.CASCADE,related_name='initialmatch')
    req_users = models.ManyToManyField(User)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'Initial Match of {self.request}'


class FinalMatchingRequest(models.Model):
    """
    Relation to Store Match after Final "Accept Back"
    """
    request = models.ForeignKey(Request,on_delete=models.CASCADE,related_name='finalmatch')
    final_req_users = models.ManyToManyField(User)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'Final Match of {self.request}'
