from django.conf.urls import patterns, url


urlpatterns = patterns('newsletter_subscription.views',
    url(r'^$', 'form',
        name='newsletter_subscription_form',
        ),
    url(r'^s/(?P<code>[^/]+)/$', 'subscribe',
        name='newsletter_subscription_subscribe',
        ),
    url(r'^r/(?P<code>[^/]+)/$', 'resubscribe',
        name='newsletter_subscription_resubscribe',
        ),
)
