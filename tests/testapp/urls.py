from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from newsletter_subscription.backend import ModelBackend
from newsletter_subscription.urls import newsletter_subscriptions_urlpatterns

from .models import Subscription

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/', include(newsletter_subscriptions_urlpatterns(
        backend=ModelBackend(Subscription),
        ))),
) + staticfiles_urlpatterns()
