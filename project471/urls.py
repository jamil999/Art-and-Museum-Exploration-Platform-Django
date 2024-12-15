"""
URL configuration for project471 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from projectapp import views  # e

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexpage, name='home'),  # e
    path('about', views.aboutpage, name='about'),  # e
    path('tologin', views.usersdologin, name='login'),
    path('tologout', views.ilogout, name='logout'),
    path('buyticket/', views.buyticket, name='ticket'),
    path('addtocart/<str:pk>/', views.addcart2, name='addtocart2'),
    path('museums/<str:pk>/', views.muedetail, name='detail'),
    path('gallery/', views.gallarypage, name='home'),  # e
    path('cart/', views.cartView, name="cart"),
    #path('process_payment/', views.process_payment, name='process_payment'),

    path('payment_successful', views.payment_successful, name='payment_successful'),
	path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
	path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('blogs/', views.blogs, name="blogs"),
    path('singleblog/<str:pk>', views.singleblog, name="singleblog"),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)