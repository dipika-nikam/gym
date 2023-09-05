from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django import forms
from django_countries.fields import CountryField


studio_type = [
     ('Bootcamp (Outdoor)', 'Bootcamp (Outdoor)'),
     ('Bootcamp (Studio)', 'Bootcamp (Studio)'),
     ('Boxing', 'Boxing'),
     ('CrossFit', 'CrossFit'),
     ('Health Club', 'Health Club'),
     ('Martial Arts', 'Martial Arts'),
     ('Personal Training', 'Personal Training'),
     ('Pilates', 'Pilates'),
     ('Spin', 'Spin'),
     ('Strength and Conditioning', 'Strength and Conditioning'),
     ('Yoga', 'Yoga'),
     ('Weightlifting', 'Weightlifting'),
     ('Other', 'Other'),
]
Business = [
     ('Yes', 'Yes'),
     ('No', 'No'),
]

Revenue = [
     ('$0 - $5k', '$0 - $5k'),
     ('$5k - $10k', '$5k - $10k'),
     ('$10k - $14k', '$10k - $14k'),
     ('$14k - $25k', '$14k - $25k'),
     ('$25k - $35k', '$25k - $35k'),
     ('$35k - $50k', '$35k - $50k'),
     ('More', 'More'),
]

Primary_revenue=[
     ('Class-Based Memberships','Class-Based Memberships'),
     ('Personal Training','Personal Training'),
     ('Hybrid (class and personal training)','Hybrid (class and personal training)'),
     ('Remote Coaching','Remote Coaching'),
     ('24hr Gym Access','24hr Gym Access'),
     ('Other','Other'),
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
    country = CountryField(blank=True)
    studio_type = models.CharField(max_length=200, choices=studio_type, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    subscribed_type = models.CharField(max_length=50, choices=subs, null=True, blank=True)
    business = models.CharField(max_length=50, choices=Business, null=True, blank=True)
    revenue = models.CharField(max_length=50, choices=Revenue, null=True, blank=True)
    primary_revenue = models.CharField(max_length=50, choices=Primary_revenue, null=True, blank=True)
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


REFERED = (
    ('Walk-in', 'Walk-in'),
    ('Google', 'Google'),
    ('Facebook', 'Facebook'),
    ('Advertisement', 'Advertisement'),
    ('Website / Blog', 'Website / Blog'),
    ('Existing Member', 'Existing Member'),
    ('Staff Member', 'Staff Member'),
    ('Other', 'Other'),
)
class AddUsers(models.Model):
    COUNTRY = (
        ('UK', 'UK'),
        ('India', 'India'),
        ('USA', 'USA'),
        ('Canada', 'Canada'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank = True, null = True)
    profile = models.ImageField(upload_to="profileimage")
    country = models.CharField(max_length=50, choices=COUNTRY, blank = True, null = True)
    assigned_to = models.ForeignKey(Profile,on_delete=models.CASCADE)
    refered_by = models.CharField(max_length=50, choices=REFERED)

    def __str__(self):
         return self.name

class Lead(models.Model):
    STATUS = (
        ('New Lead', 'New Lead'),
        ('Attempted', 'Attempted'),
        ('Contacted', 'Contacted'),
        ('In Discussion', 'In Discussion'),
        ('Converted', 'Converted'),
        ('Disqualified', 'Disqualified'),
    )

    OBJECTIVES = (
        ('Weight Loss', 'Weight Loss'),
        ('Athletic Performance', 'Athletic Performance'),
        ('Health Reasons', 'Health Reasons'),
        ('Others', 'Others'),
    )

    status = models.CharField(max_length = 50 , choices=STATUS)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    birthday = models.CharField(max_length=15)
    postal_code = models.IntegerField()
    mobile_no = models.CharField(max_length=15)
    objectives = models.CharField(choices=OBJECTIVES, max_length=20)
    refered_by = models.CharField(max_length=50, choices=REFERED)
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
         return self.name
