from django.db import models

# Create your models here.

class Announcement(models.Model):
    #owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    owner = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)#add timestamps when create
    updated = models.DateTimeField(auto_now=True)#add timestamps when update
 
    class Meta:
        #To order by updated descending,
        ordering = ('-updated',)