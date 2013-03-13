from django.conf.urls import patterns, include, url


urlpatterns = patterns('newsletter_registration.views',
    url(r'^$',
        'email_registration_form',
        name='email_registration_form'),
    url(r'^(?P<code>[^/]+)/$',
        'email_registration_confirm',
        name='email_registration_confirm'),
)
