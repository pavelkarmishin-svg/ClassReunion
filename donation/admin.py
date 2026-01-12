from django.contrib import admin

from donation.models import Donation


# Register your models here.
class DonationAdmin(admin.ModelAdmin):
    model = Donation
    list_display = ('id', 'amount', 'created_at')

admin.site.register(Donation, DonationAdmin)