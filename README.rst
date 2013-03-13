==============================
django-newsletter-subscription
==============================

Another newsletter subscription app.


Subscription flow
=================

- User enters his/her email address.
- A mail is sent to the given address containing a link.
- Upon visiting the link the user is immediately subscribed for the newsletter.
  Optionally, a form asking the user for additional data is shown.

- ``/newsletter/``
- ``/newsletter/s/<signed_data>/``


Unsubscription flow
===================

- The user enters his/her email address and is immediately unsubscribed.
- An email is sent to the user informing him/her that the unsubscription took
  place. A link is provided to immediately subscribe again in case the
  unsubscription was not meant to take place.

- ``/newsletter/``
- ``/newsletter/r/<signed_data>/``


Subscription model
==================

The minimal set of database fields is as follows:

- ``email`` (unique)
- ``is_active``


Usage
=====

This example assumes you are using a recent version of Django, jQuery and
Twitter Bootstrap.

1. Install ``django-newsletter-subscription`` using pip.

2. Add a concrete model inheriting
   ``newsletter_subscription.models.SubscriptionBase`` or coming with the same
   fields somewhere in your project.

3. Add the URLconf entry::

       from .newsletter.models import Subscription

       from newsletter_subscription.backend import ModelBackend
       from newsletter_subscription.urls import newsletter_subscriptions_urlpatterns

       urlpatterns += patterns(
          url(r'^newsletter/', include(newsletter_subscriptions_urlpatterns(
              backend=ModelBackend(Subscription),
              ))),
       )

4. Add ``newsletter_subscription`` to ``INSTALLED_APPS`` if you want to use
   the bundled templates.
