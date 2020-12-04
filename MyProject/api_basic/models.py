from django.db import models
from account.models import Account


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=5000, null=False, blank=False)
    author = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(default='default.png')
    date_published = models.DateTimeField(verbose_name='date_published',
                                          auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='date_published',
                                        auto_now=True)

    def __str__(self):
        return self.title
