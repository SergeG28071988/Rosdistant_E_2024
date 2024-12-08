from django.db import models

# Create your models here.


class Human(models.Model):
    surname = models.CharField(max_length=100, verbose_name='Enter Surname')
    name = models.CharField(max_length=100, verbose_name='Enter Name')
    date_birth = models.DateField(null=True, blank=True, verbose_name='Enter Date of Birth')
    place_residence = models.CharField(max_length=100, verbose_name='Enter Place Residence')

    def __str__(self):
        return self.surname
    
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        