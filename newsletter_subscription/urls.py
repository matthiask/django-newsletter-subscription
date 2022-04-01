from django.urls import path

from newsletter_subscription.ajax_views import ajax_subscribe
from newsletter_subscription.views import form, resubscribe, subscribe


def newsletter_subscriptions_urlpatterns(**kwargs):
    return [
        path(
            "",
            form,
            kwargs,
            name="newsletter_subscription_form",
        ),
        path(
            "s/<str:code>/",
            subscribe,
            kwargs,
            name="newsletter_subscription_subscribe",
        ),
        path(
            "r/<str:code>/",
            resubscribe,
            kwargs,
            name="newsletter_subscription_resubscribe",
        ),
        path(
            "ajax_subscribe/",
            ajax_subscribe,
            kwargs,
            name="newsletter_subscription_ajax_subscribe",
        ),
    ]
