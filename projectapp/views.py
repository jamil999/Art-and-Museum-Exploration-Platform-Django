from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect  # e
from django.contrib.auth import authenticate, login, logout  # e
from django.contrib import messages  # e
from .models import museums, userpro, ticketcart, UserPayment, comments, Coupon, blogs1  # e
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

# Create your views here.


#####################
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
import stripe
import time

# stripe.api_key = settings.STRIPE_PRIVATE_KEY


# def process_payment(request):
#     stripe.api_key = settings.STRIPE_PRIVATE_KEY

#     session = stripe.checkout.Session.create(
#         success_url= request.build_absulute_uri(reverse('thanks')) + '?session_id = {CHECKOUT_SESSION_ID}',
#         line_items=[
#             {
#                 "price": "price_1NZEAfCpeYkube08JnKKZM3U",
#                 "quantity": 1,
#             },
#         ],
#         mode="payment", )

#     return render(request, 'cartview2.html', {'session_id': session.id, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

###############################


def indexpage(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')


def usersdologin(request):
    if request.method == 'POST':
        username = request.POST.get("user1")
        password = request.POST.get("pass1")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, "Invalid")
            return redirect('login')

    return render(request, 'login.html')


def ilogout(request):
    # if request.method == 'POST':
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('login')
    return render(request, 'blog-home.html')


def buyticket(request):
    all2 = museums.objects.all()
    # print(all2)
    return render(request, 'ticket.html', {'mus': all2})


def addcart2(request, pk):
    # mdetail = museums.objects.get(id=pk)
    # user1 = userpro.objects.get(user=request.user)

    # if request.method == 'POST':
    #     quan = int(request.POST['quanti'])

    #     print('hvjhv.', quan)

    #     print('THis is :', user1, mdetail)
    #     adding = ticketcart.objects.create(user=user1, item=mdetail)
    #     adding.save()
    #     return
    # print(mdetail.price)
    # adding = ticketcart.objects.create(user=User, course_name=course_name, course_description=course_description, course_credit=course_credit, course_faculty=course_faculty, course_department=department)

    return HttpResponse("Hello")


# def addcart(request, pk):
#      item = get_object_or_404(museums, pk = pk)
#      orderitem = ticketcart.objects.get_or_create(item = item, user = request.user)
#      orderqs = order.objects.filter(user = request.user)
#      if orderqs.exists():
#         order = orderqs[0]
#         if order.orderitems.filter(item = item).exists():
#              orderitem[0]
#              if order.orderitems.filter(item = item).exists():
#                   orderitem[0].quantity += 1
#                   orderitem[0].save()
#                   return redirect('ticket')

#              else:
#                   order.orderitems.add(orderitem[0])
#                   return redirect('ticket')

#      else:
#           order = order(user = request.user)
#           order.save()
#           order.orderitems.add(orderitem[0])
#           return redirect('ticket')
def cartView(request):
    prod_lst = ticketcart.objects.filter(
        user=userpro.objects.get(user=request.user))

    total_prod = len(prod_lst)
    # serial = 0
    lst1 = []
    total_sum = 0
    for i in prod_lst:
        x = int(i.item.price) * int(i.quant)

        prod_lst.total_p = x

        lst1.append(x)
        total_sum += x

    print(total_prod, total_sum, lst1)

    allcoup = Coupon.objects.all()
    cupname = [row.coup_name for row in allcoup]
    cupvalue = [row.multi for row in allcoup]
    print(cupname, cupvalue)

    ####################################################
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

    showmess = ''
    if 'coupon1' in request.POST:
        given = request.POST['coupon1']
        print(given)
        if given in cupname:
            # print(total_sum, 'ok')
            ind = cupname.index(given)
            print(ind, 'index')
            total_sum = total_sum * (cupvalue[ind]/100)
            print(total_sum)
            diss = str(100 - cupvalue[ind])
            messages.success(
                request, f'Congratulation! You got {diss}% of disscount. Currently your total amount is {total_sum} Tk')
        else:
            #
            messages.success(request, 'Your COUPON was not right')

        # mess
        return redirect(cartView)

    if 'pay1' in request.POST:
        # if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN +
            '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
        # return render(request, 'user_payment/product_page.html')

    return render(request, "cartview2.html", {"cart": prod_lst, 'total_prod': total_prod, 'total_sum': total_sum, 'lst1': lst1, 'showmess': showmess})


# pppppppppppppppp

def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.user_id
    user_payment = UserPayment.objects.get(app_user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'user_payment/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, 'user_payment/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)
# ppppppppppppppppp


def muedetail(request, pk):
    item = museums.objects.get(id=pk)
    print(item,'lll')
    print(request.user,'sdd')
    mdetail = museums.objects.get(id=pk)

    print(request.user,'gchgch')
    user1 = userpro.objects.get(user=request.user)

    commentsall1 = comments.objects.filter(
        comment_on_mu=museums.objects.get(id=pk))

    if request.method == 'POST':
        print("########################################")

        if 'quanti' in request.POST:
            quan = int(request.POST['quanti'])

            print('hvjhv.', quan)

            print('THis is :', user1, mdetail)
            adding = ticketcart.objects.create(
                user=user1, item=mdetail, quant=quan)
            adding.save()
            return redirect(cartView)

        elif 'comm' in request.POST:
            print("######################ufg#############")
            comment = request.POST['comm']

            print('comm.', comment)

            # print('THis is :', user1, mdetail)
            adding2 = comments.objects.create(
                user=user1, comment_on_mu=mdetail, comment=comment)
            adding2.save()
            return redirect(cartView)

    return render(request, 'ticketdetail.html', {'item': item, 'commentsall1': commentsall1})


def gallarypage(request):
    return render(request, 'gallery.html')

def blogs(request):

    allblog = blogs1.objects.all()

    return render(request, 'blog-home.html', {'allblog': allblog})


def singleblog(request, pk):
    print(pk,'kkkkkkkk')
    sinblog = blogs1.objects.get(id=pk)
    #{'sinblog': sinblog}
    return render(request, 'blog-single.html',{'sinblog': sinblog} )