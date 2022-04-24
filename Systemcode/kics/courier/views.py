from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from datetime import datetime

from .models import *
from .rules_engine import shipping_estimates as se_rules
from subprocess import run, PIPE
import sys

# Create your views here.

def index(request):
    min_date = f"{datetime.now().date().year}-{datetime.now().date().month}-{datetime.now().date().day}"
    max_date = f"{datetime.now().date().year if (datetime.now().date().month+3)<=12 else datetime.now().date().year+1}-{(datetime.now().date().month + 3) if (datetime.now().date().month+3)<=12 else (datetime.now().date().month+3-12)}-{datetime.now().date().day}"
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        originPostCode = request.POST.get('OriginPostcode')
        destination = request.POST.get('Destination')
        destinationPostcode = request.POST.get('DestinationPostcode')
        pickUp_date = request.POST.get('PickUpDate')
        delivery_date = request.POST.get('DeliveryDate')

        return render(request, 'courier/index.html', {
            'origin': origin,
            'destination': destination,
            'pickUp_date' : pickUp_date,
            'delivery_date' : delivery_date,
            'min_date': min_date,
            'max_date': max_date,
            'origin_postcode': originPostCode,
            'destination_postcode': destinationPostcode
        })
    else:
         return render(request, 'courier/index.html', {
             'min_date': min_date,
             'max_date': max_date
         })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            
        else:
            return render(request, "courier/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "courier/login.html")
            
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "courier/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(request, "courier/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "courier/register.html")



@csrf_exempt
def courier(request):

    origin = request.GET.get('Origin')
    originArea = request.GET.get('OriginArea')
    originPostCode = request.GET.get('OriginPostcode')
    destination = request.GET.get('Destination')
    destinationArea = request.GET.get('DestinationArea')
    destPostCode = request.GET.get('DestinationPostcode')
    destination = request.GET.get('Destination')
    weight = request.GET.get('Weight')
    Width = request.GET.get('Width')
    length = request.GET.get('Length')
    height = request.GET.get('Height')
    pickUpDate = request.GET.get('PickUpDate')
    pickUp_date = datetime.strptime(pickUpDate, "%Y-%m-%d")
    deliveryDate = request.GET.get('DeliveryDate')
    delivery_date = datetime.strptime(deliveryDate, "%Y-%m-%d")
    
    deliveryDate = request.GET.get('Category')
    transportation = request.GET.get('Transportation')
    priority = request.GET.get('Priority')

    couriers = Courier.objects.all()
    
    couriers = list(couriers)
    dest_country = destination

    weight = float(weight)
    dim_lwh = (float(length), float(Width), float(height))

    # Function call to fetch shipping estimates.
    estimates = se_rules.get_shipping_estimates(dest_country, weight, weight_unit="kg", dim_lwh=dim_lwh, dim_unit="cm")
    estimatesList = []
    estimateslistCopy = []
    for estimate in estimates:
        estimated = list(estimate.values())
        estimatesList.append(estimated)
        estimateslistCopy.append(estimated)

    
    estimateslistCopy = sorted(estimatesList, key=lambda x: x[2])

    try:
        max_price = estimateslistCopy[-1][2] + 1
        min_price = estimateslistCopy[0][2]
    except:
        max_price = 0
        min_price = 0


    if priority == 'Price':
        estimatesList = sorted(estimatesList, key=lambda x: x[2])
    elif priority == 'Insurance':
        estimatesList = sorted(estimatesList, key=lambda x: x[5], reverse=True)
    elif priority == 'Re-Delivery':
        estimatesList = sorted(estimatesList, key=lambda x: x[6], reverse=True)
    elif priority == 'Home Pick Up':
        estimatesList = sorted(estimatesList, key=lambda x: x[7], reverse=True)
    elif priority == 'Delivery Date':
        estimatesList = sorted(estimatesList, key=lambda x: x[3][0])

    couriervalue = ''
    
    return render(request, "courier/courier_search.html", {
        'couriers': couriers,
        'origin': origin,
        'originArea': originArea,
        'destination': destination,
        'destinationArea': destinationArea,
        'pickUp_date' : pickUp_date,
        'delivery_date' : delivery_date,
        'max_price' : max_price,
        'min_price' : min_price,
        'estimates': estimates,
        'couriervalue': couriervalue,
        'estimatesList': estimatesList
    })


def external(request):
    out = run([sys.executable,
               'courier/measure_object_size/measure_object_size_camera.py'],
              shell=False, stdout=PIPE)

    return render(request, 'courier/index.html', {'data1': out.stdout})
