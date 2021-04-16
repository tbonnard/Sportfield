from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    admin_pro = models.BooleanField(default=False)

    def __str__(self):
        return self.username.capitalize()


class Category(models.Model):
    category = models.CharField(null=False, blank=False, max_length=250)
    image_url = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.category


class Club(models.Model):
    club = models.CharField(null=False, blank=False, max_length=250)
    address = models.CharField(null=False, blank=False, max_length=250)
    address_number = models.IntegerField(null=False, blank=False)
    city = models.CharField(null=False, blank=False, max_length=250)
    zip_code = models.CharField(null=False, blank=False, max_length=20)
    country_list = (("CA",'Canada'), ("USA",'United States of America'))
    country = models.CharField(choices = country_list, null=False, blank=False, max_length=3)
    image_url = models.URLField(null=False, blank=False)
    owner_club = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, related_name='take_clubs_from_user')

    def __str__(self):
        return self.club

    #validate the owner is a pro
    def is_owner_valid(self):
        if self.owner_club.admin_pro == True:
            return True

  
class Field(models.Model):
    field_name= models.CharField(null=True, blank=False, max_length=250)
    club = models.ForeignKey(Club,null=False, blank=False, related_name="take_field_from_club", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=False, on_delete=models.SET_NULL, related_name='take_fields_from_category')
    price = models.DecimalField(null=True, blank=False, max_digits=5, decimal_places=2)
    address = models.CharField(null=False, blank=False, max_length=250)
    address_number = models.IntegerField(null=False, blank=False)
    city = models.CharField(null=False, blank=False, max_length=250)
    zip_code = models.CharField(null=False, blank=False, max_length=20)
    country_list = (("CA",'Canada'), ("USA",'United States of America'))
    country = models.CharField(choices = country_list, null=False, blank=False, max_length=3)

    def __str__(self):
        return self.field_name

    def serialize(self):
        return {
            "id": self.id,
            "field_name": self.field_name,
            #"club": self.club.pk,
            #"category": self.category.pk,
            "price": self.price,
            #"address": self.address,
            #"address_number": self.address_number,
            #"city": self.city,
            #"zip_code": self.zip_code,
            #"country_list": self.country_list,
            #"country": self.country,
            'full_address': f'{self.address_number} {self.address} {self.city} {self.zip_code} {self.country}'
                }


class Schedule(models.Model):
    field = models.ForeignKey(Field, null=False, blank=False, related_name="take_Schedule_from_field", on_delete=models.CASCADE )
    schedule_time = models.TimeField(null=False, blank=False, default="00:00:00")

    def serialize(self):
        return {
            'field': self.field.pk ,
            'schedule_time': self.schedule_time ,
        }

class Booking(models.Model):
    field = models.ForeignKey(Field, null=False, blank=False, related_name="take_Booking_from_field", on_delete=models.CASCADE )
    user = models.ForeignKey(User, null=False, blank=False, related_name="take_Booking_from_user", on_delete=models.CASCADE )
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_book = models.DateField(null=False, blank=False)
    schedule_time_field = models.TimeField(null=False, blank=False, default="00:00:00")
    
    #validate the max number of booking per date based on the schedule number
    def validation_booking(self, date):
        fields = Field.objects.all()
        booking = Booking.objects.all()
        list_fields = [i for i in fields if len(Booking.objects.filter(field=i, date_book=date)) < Schedule.objects.filter(field=i).count()]
        return list_fields
