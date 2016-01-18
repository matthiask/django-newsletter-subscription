from django.conf.urls import url

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
    ]
