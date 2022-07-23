from tabnanny import verbose
from django.db import models
from Authentication.models import MyBaseModel, UsersInfo
from datetime import date
from Merchent.models import TheterInformation
from django.utils import timezone

# Create your models here.
class Movies(MyBaseModel):
    movie_name = models.CharField(max_length=255,
                                  blank=False,
                                  null=False)

    movie_description = models.TextField(blank=False,
                                         null=False,
                                         )          

    movie_rating = models.IntegerField(default=0,
                                       blank=True,
                                       null=True)

    movie_release_date = models.DateField(default=timezone.now(),
                                          blank=True,
                                          null=True)

    movie_langauge = models.CharField(max_length=255,
                                      blank=False,
                                      null=False)  

    def __str__(self) -> str:
        return str(self.movie_name)  

    class Meta:
        verbose_name = "Movies" 
        verbose_name_plural = "Movies"
                                  

class MovieAllocations(MyBaseModel):
    movie = models.ForeignKey(Movies,
                              on_delete=models.PROTECT,
                              related_name="movie",
                              blank=False,
                              null=False)          

    theter = models.ForeignKey(TheterInformation,
                               on_delete=models.PROTECT,
                               related_name="thetersinfo",
                               blank=False,
                               null=False)                                                                                         
