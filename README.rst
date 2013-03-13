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

2. Add ``newsletter_subscription`` to ``INSTALLED_APPS`` and
   include ``newsletter_subscription.urls`` in your URLconf.

3. Run ``migrate``.
