from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_file_size


class Category(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=55)
    slug = models.SlugField(default='', null=False)
    
    def __str__(self) -> str:
        return self.title

class Chef(models.Model):
    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    CHEF_LURKER = 'B'
    CHEF_RESIPI_CREATOR = 'S'
    CHEF_RESIPI_SUPER_CREATOR = 'G'

    MEMBERSHIP_CHOICES = [
        (CHEF_LURKER, 'Lurker'),
        (CHEF_RESIPI_CREATOR, 'Creator'),
        (CHEF_RESIPI_SUPER_CREATOR, 'Super Creator'),
    ]
    phone = models.CharField(max_length=12, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=CHEF_LURKER)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                                    on_delete=models.CASCADE)
    #resipis = models.ForeignKey('Resipi', null=True, blank=True, 
     #   on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

class Resipi(models.Model):
    class Meta:
        ordering = ['title']

    title = models.CharField(max_length=55)
    description = models.TextField()
    ingredients = models.TextField()
    how_to = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, 
        related_name='resipis')
    slug = models.SlugField()
    last_update = models.DateTimeField(auto_now=True)
    chef = models.ForeignKey(Chef, on_delete=models.PROTECT)
    number_of_rating = models.IntegerField(default=0, null=True)
    avg_rating = models.FloatField(default=0, null=True)

    def __str__(self) -> str:
        return self.title

class ResipiImage(models.Model):
    resipi = models.ForeignKey(Resipi, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='foodresipi/images', 
                                        validators=[validate_file_size])

class ResipiRating(models.Model):
    resipi = models.ForeignKey(Resipi, on_delete=models.CASCADE)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0, validators=[MaxValueValidator(5),
        MinValueValidator(0)])

class Review(models.Model):
    resipi = models.ForeignKey(Resipi, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=55)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


