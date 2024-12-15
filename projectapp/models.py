from django.db import models
from django.contrib.auth.models import User

#from app_users.models import AppUser
from django.db.models.signals import post_save
from django.dispatch import receiver
#import uuid
# Create your models here.

class UserPayment(models.Model):
	app_user = models.ForeignKey(User, on_delete=models.CASCADE)
	payment_bool = models.BooleanField(default=False)
	stripe_checkout_id = models.CharField(max_length=500)



#pppppppppppppppppppppppppppppppp

class museums(models.Model):
    name = models.CharField(max_length= 100)
    des = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    img = models.ImageField(upload_to = 'static/img/')

    def __str__(self):
        return self.name

    #@staticmethod
    #def allMuseums():
        #return museums.objects.all()

class userpro(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE )
    full_name = models.CharField(max_length=255, blank= True, null= True)
    interest = models.CharField(max_length=50, blank= True, null= True)
    Date_joined = models.DateField(auto_now_add=True)

    #def __str__(self):
        #return f"{self.user.username}'s Profile"

    def __str__(self):
        return f"{self.full_name}"
# @receiver(post_save, sender = User)
# def createpro(sender, instance, created, **kwardgs):
#     if created:
#         userpro.objects.create(user = instance)

# def savepro(sender, instance, **kwardgs):
#     instance.profile.save()

class ticketcart(models.Model):    
    user = models.ForeignKey(userpro, on_delete= models.CASCADE)
    item = models.ForeignKey(museums, on_delete= models.CASCADE)
    total_p = models.IntegerField(default=1)
    quant = models.IntegerField(default=1)
    pur= models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.CharField(max_length=255, blank= True, null= True)

    def __str__(self):
        return f'Bought {self.quant} tickets of {self.item}'

# class ticketcart(models.Model):
#     user = models.ForeignKey(userpro, on_delete= models.CASCADE)
#     item = models.ForeignKey(museums, on_delete= models.CASCADE)
#     quant = models.IntegerField(default=1)
#     pur= models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)

    
    # def get_total(self):
    #     total = self.item.price() * self.quant
    #     return total
    
# class order(models.Model):
#     user = models.ForeignKey(User, on_delete= models.CASCADE)
#     orderitem = models.ManyToManyField(ticketcart)
#     ordered = models.BooleanField(default= False)
#     created = models.DateTimeField(auto_now_add=True)
#     payid = models.CharField(max_length= 200, blank = True, null = True)
#     orid = models.CharField(max_length= 255, blank = True, null = True)

#     def get_totals(self):
#         total = 0
#         for orderitem in self.orderitems.all():
#             total += float(orderitem.get_total)

#         return total
    
# class kkk(models.Model):
#     pass

class comments(models.Model):    
    user = models.ForeignKey(userpro, on_delete= models.CASCADE)
    comment_on_mu = models.ForeignKey(museums, on_delete= models.CASCADE)
    comment = models.CharField(max_length= 500, blank = True, null = True)
    when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} commented {self.when}'
    
class Coupon(models.Model):    
    coup_name = models.CharField(max_length= 100)
    multi = models.IntegerField(default=1)

    def __str__(self):
        return f'This {self.coup_name} will reduce amount to {self.multi}'
    
class blogs(models.Model):    
    user = models.ForeignKey(userpro, on_delete= models.CASCADE)
    catag = models.CharField(max_length=50, blank= True, null= True)
    headline = models.CharField(max_length=100, blank= True, null= True)
    descrip = models.CharField(max_length= 1000, blank = True, null = True)
    when = models.DateTimeField(auto_now_add=True)
    #image = models.ImageField(upload_to = 'static/img/')

    def __str__(self):
        return f'{self.user} written blogs on {self.headline}'
    
class blogs1(models.Model):    
    user = models.ForeignKey(userpro, on_delete= models.CASCADE)
    catag = models.CharField(max_length=50, blank= True, null= True)
    headline = models.CharField(max_length=100, blank= True, null= True)
    intro = models.CharField(max_length=500, blank= True, null= True)
    descrip = models.CharField(max_length= 2500, blank = True, null = True)
    when = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'static/img/')

    def __str__(self):
        return f'{self.user} written blogs on {self.headline}'