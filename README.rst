==============================
django-newsletter-subscription
==============================

Another newsletter subscription app.

.. image:: https://travis-ci.org/matthiask/django-newsletter-subscription.png?branch=master
   :target: https://travis-ci.org/matthiask/django-newsletter-subscription


Subscription flow
=================

- User enters his/her email address on ``/newsletter/``.
- A mail is sent to the given address containing a link of the form
  ``/newsletter/s/<signed_email_address>/``.
- Upon visiting the link the user is immediately subscribed for the newsletter.
  Optionally, a form asking the user for additional data is shown.


Unsubscription flow
===================

- The user enters his/her email address on ``/newsletter/`` and is immediately
  unsubscribed.
- An email is sent to the user informing him/her that the unsubscription took
  place. A link is provided to immediately subscribe again in case the
  unsubscription was not meant to take place. The link is of the form
  ``/newsletter/r/<signed_email_address>/``.


Subscription model
==================

The minimal set of database fields is as follows:

- ``email`` (``EmailField``, unique)
- ``is_active`` (``BooleanField``, defaults to ``False``)


Usage
=====

This example assumes you are using at least Django 1.4.

1. Install ``django-newsletter-subscription`` using pip.

2. Add a concrete model inheriting
   ``newsletter_subscription.models.SubscriptionBase`` with optionally
   additional fields about the subscription. You should be prepared to work
   without those additional fields -- their presence is not enforced as per
   the subscription flow description above. A full example:

   .. code-block:: python

        from django.db import models
        from django.utils.translation import ugettext_lazy as _

        from newsletter_subscription.models import SubscriptionBase

        class Subscription(SubscriptionBase):
            full_name = models.CharField(_('full name'), max_length=100, blank=True)

3. Add the URLconf entry:

   .. code-block:: python

        from .newsletter.models import Subscription

        from newsletter_subscription.backend import ModelBackend
        from newsletter_subscription.urls import newsletter_subscriptions_urlpatterns

        urlpatterns += patterns(
            '',
            url(
                r'^newsletter/',
                include(newsletter_subscriptions_urlpatterns(
                    backend=ModelBackend(Subscription),
                )),
            ),
        )

4. Register your own subscription model with ``django.contrib.admin``.

5. Add ``newsletter_subscription`` to ``INSTALLED_APPS`` if you want to use
   the bundled templates. The templates require
   `Towel <https://github.com/matthiask/towel/>`_'s ``towel_form_tags``
   template tag library.

6. Ensure that Django's
   `messages framework <https://docs.djangoproject.com/en/1.9/ref/contrib/messages/>`__
   is activated and that the messages are included in your templates, otherwise
   the notifications from ``django-newsletter-subscriptions`` will not be shown to the
   users.
