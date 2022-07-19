from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    phone = models.CharField(max_length=10, null=True)
    profile_image = models.ImageField(upload_to='profile_pic')
    user_address = models.TextField(null=True)

class Bikes(models.Model):

    own_type=(
        ('First owner', 'First owner'),
        ('Second owner', 'Second owner'),
        ('Third owner', 'Third owner')
    )
    added_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_by')
    bike_name= models.CharField(max_length=20)
    image=models.ImageField(upload_to="bike_images")
    bike_manufacturer= models.CharField(max_length=20)
    bike_model= models.PositiveIntegerField(default=0)
    bike_price= models.PositiveIntegerField()
    bike_km= models.PositiveIntegerField(null=True)
    bike_capacity=models.FloatField(null=True)
    bike_description= models.CharField(max_length=40)
    owner_type= models.CharField(max_length=20, choices=own_type)
    address= models.TextField(null=True)
    date= models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    # def __str__(self):
    #     return self.bike_name

class BikeImages(models.Model):

    bikes= models.ForeignKey(Bikes, on_delete=models.CASCADE, related_name='bikemdl')
    image= models.ImageField(upload_to='bike_images',null=True)
    date= models.DateTimeField(auto_now_add=True)



class InterestedBikes(models.Model):
    status = (
        ('Interested', 'Interested'),
        ('Not Interested', 'Not Interested'),
        ('Sold','Sold'),
        ('Rejected','Rejected')


    )
    bike=models.ForeignKey(Bikes,on_delete=models.CASCADE,related_name='bikes')
    users=models.ForeignKey(User,on_delete=models.CASCADE,related_name='interested_user')
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bike_owner')
    status=models.CharField(max_length=65,choices=status)
