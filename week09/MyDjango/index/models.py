from django.db import models


class Maoyan(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'maoyan'
