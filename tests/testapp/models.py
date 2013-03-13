from django.db import models
from django.utils.timezone import now

from newsletter_subscription.models import SubscriptionBase


class Subscription(SubscriptionBase):
    full_name = models.CharField(max_length=100, blank=True)
