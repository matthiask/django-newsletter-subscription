from django.db import models

from newsletter_subscription.models import SubscriptionBase


class Subscription(SubscriptionBase):
    full_name = models.CharField(max_length=100, blank=True)
