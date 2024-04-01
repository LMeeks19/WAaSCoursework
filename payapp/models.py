from django.db import models


class TransactionStatus(models.TextChoices):
    PENDING = 'PENDING',
    CLEARED = 'CLEARED',
    REJECTED = 'REJECTED',


class TransactionType(models.TextChoices):
    DIRECT = 'DIRECT',
    REQUEST = 'REQUEST',


class Transaction(models.Model):
    sender_email = models.EmailField()
    receiver_email = models.EmailField()
    reference = models.CharField(max_length=50)
    amount = models.IntegerField()
    send_date = models.DateTimeField()
    status = models.CharField(default="PENDING", max_length=8)
    type = models.CharField(default="DIRECT", max_length=7)
