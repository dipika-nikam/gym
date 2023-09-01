from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django import forms


country=[
     ('India', 'India'),
     ('India', 'India'),
     ('India', 'India'),
     ('India', 'India'),
]

studio_type = [
     ('Yoga', 'Yoga'),
     ('Yoga', 'Yoga'),
     ('Yoga', 'Yoga'),
     ('Yoga', 'Yoga'),
     ('Yoga', 'Yoga'),
]
class Profile(models.Model):
    subs = [
        ("all", "All round fitness"),
        ("body_building", "Body Building"),
        ("muscle_building", "Muscle Building")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, null=True, upload_to='images/')
    phone_no = models.CharField(max_length=15)
    country = models.CharField(max_length=200, choices=country, null=True, blank=True)
    studio_type = models.CharField(max_length=200, choices=studio_type, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    subscribed_type = models.CharField(max_length=50, choices=subs, null=True, blank=True)
    checkout_session = models.CharField(max_length=200, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to="products")

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING','PENDING'),
        ('ACCEPTED','ACCEPTED'),
        ('PACKED','PACKED'),
        ('ON THE WAY','ON THE WAY'),
        ('DELIVERED','DELIVERED'),
        ('CANCELED','CANCELED'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICES, default='PENDING', max_length=50)
    ordered = models.BooleanField(default=False)
    checkout_session =models.CharField(max_length=200, null=True, blank=True)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class ClassSchedule(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )

    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    instructor = models.CharField(max_length=100)

    @property
    def time_slot(self):
        start_time = self.start_time.strftime('%I:%M%p')
        end_time = self.end_time.strftime('%I:%M%p')
        return f"{start_time} - {end_time}"

    def __str__(self):
        return f"{self.day} - {self.time_slot}"


class AddUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank = True, null = True)
    profileimage = models.ImageField(upload_to="profileimage", blank = True, null = True)
    country = models.CharField(max_length=50, blank = True, null = True)

    def __str__(self):
         return self.name
