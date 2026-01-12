from django.shortcuts import render, redirect
from .forms import DonationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Donation

def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            return redirect('donation:thanks')
    else:
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