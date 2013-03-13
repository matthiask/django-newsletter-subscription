from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscription(models.Model):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_active = models.BooleanField(_('is active'), default=False)
    full_name = models.CharField(_('full name'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __unicode__(self):
        return self.email
