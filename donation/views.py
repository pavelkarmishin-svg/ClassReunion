from django.shortcuts import render, redirect
from .forms import DonationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Donation
from urllib.parse import urlencode
from django.shortcuts import redirect
from donation.yoomoney import build_payment_url

def donate(request):
    form = DonationForm()
    return render(request, 'donations/donate.html', {'form': form})


def thanks(request):
    return render(request, 'donations/thanks.html')

def yoomoney_return(request):
    return render(request, 'donations/return.html')

@csrf_exempt
def payment_notification(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    payment_id = request.POST.get('label')
    status = request.POST.get('unaccepted')  # или status — зависит от API

    try:
        donation = Donation.objects.get(id=payment_id)
    except Donation.DoesNotExist:
        return HttpResponse(status=404)

    # упрощённо
    donation.status = 'paid'
    donation.save()

    return HttpResponse('OK')


def start_payment(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    form = DonationForm(request.POST)
    if not form.is_valid():
        return render(request, "donations/donate.html", {"form": form})

    donation = form.save(commit=False)
    donation.user = request.user if request.user.is_authenticated else None
    donation.status = "pending"
    donation.save()

    return redirect(build_payment_url(donation))