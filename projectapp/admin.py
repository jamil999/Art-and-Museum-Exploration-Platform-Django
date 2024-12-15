from django.contrib import admin

# Register your models here.
from .models import userpro, museums, ticketcart, UserPayment, comments, Coupon, blogs1

admin.site.register(museums)
admin.site.register(userpro)
admin.site.register(ticketcart)
admin.site.register(UserPayment)
admin.site.register(comments)
admin.site.register(Coupon)
admin.site.register(blogs1)