from django.contrib import admin
from . models import Profile, Contact, Product, Order, OrderItem, ClassSchedule, AddUsers

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ClassSchedule)
admin.site.register(AddUsers)


