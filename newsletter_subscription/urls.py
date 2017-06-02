from django.conf.urls import url

from newsletter_subscription.ajax_views import ajax_subscribe
from newsletter_subscription.views import form, subscribe, resubscribe


def newsletter_subscriptions_urlpatterns(**kwargs):
    return [
        url(
            r'^$',
            form,
            kwargs,
            name='newsletter_subscription_form',
        ),
        url(
            r'^s/(?P<code>[^/]+)/$',
            subscribe,
            kwargs,
            name='newsletter_subscription_subscribe',
        ),
        url(
            r'^r/(?P<code>[^/]+)/$',
            resubscribe,
            kwargs,
            name='newsletter_subscription_resubscribe',
        ),

        url(
            r'^ajax_subscribe/$',
            ajax_subscribe,
            kwargs,
            name='newsletter_subscription_ajax_subscribe',
        ),
    ]
