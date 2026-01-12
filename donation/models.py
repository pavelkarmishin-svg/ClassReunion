from django.db import models
import uuid

# Create your models here.
class Donation(models.Model):
    amount = models.PositiveIntegerField()
    email = models.EmailField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('created', 'Создан'),
            ('paid', 'Оплачен'),
            ('failed', 'Ошибка'),
        ],
        default='created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.amount} ₽ ({self.status})"