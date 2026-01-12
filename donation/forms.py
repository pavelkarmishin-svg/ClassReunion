from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ('amount', 'email')
        widgets = {
            'amount': forms.NumberInput(attrs={
                'min': 50,
                'step': 50,
                'placeholder': 'Сумма, ₽'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email (необязательно)'
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 10:
            raise forms.ValidationError("Минимальный донат — 10 ₽")
        return amount