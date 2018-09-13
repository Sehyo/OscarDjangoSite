from django.db import models

class NewsPost(models.Model):
    post_title = models.CharField(max_length = 64)
    post_text = models.CharField(max_length = 1024)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.post_title