from django.conf.urls import patterns, url


def newsletter_subscriptions_urlpatterns(**kwargs):
    return patterns('newsletter_subscription.views',
        url(r'^$', 'form', kwargs,
            name='newsletter_subscription_form',
            ),
        url(r'^s/(?P<code>[^/]+)/$', 'subscribe', kwargs,
            name='newsletter_subscription_subscribe',
            ),
        url(r'^r/(?P<code>[^/]+)/$', 'resubscribe', kwargs,
            name='newsletter_subscription_resubscribe',
            ),
        )
