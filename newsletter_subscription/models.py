from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class SubscriptionBase(models.Model):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_active = models.BooleanField(_('is active'), default=False)

    class Meta:
        abstract = True
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __str__(self):
        return self.email
