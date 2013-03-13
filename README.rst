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
- ``subscribed_on`` (nullable)
- ``unsubscribed_on`` (nullable)


Usage
=====

This example assumes you are using a recent version of Django, jQuery and
Twitter Bootstrap.

1. Install ``django-newsletter-subscription`` using pip.

2. Copy this code somewhere on your login or registration page::

    <h2>{% trans "Send an activation link" %}</h2>
    <form method="post" action="{% url "email_registration_form" %}"
        class="well" id="registration">
      {% csrf_token %}
      <div class="controls">
        <input id="id_email" type="text" name="email" maxlength="30"
          placeholder="{% trans "E-mail address" %}">
      </div>
      <button type="submit" class="btn btn-primary">
        {% trans "Register" %}</button>
    </form>

    <script>
    function init_registration($) {
      $('#registration').on('submit', function() {
        var $form = $(this);
        $.post(this.action, $form.serialize(), function(data) {
          $('#registration').replaceWith(data);
          init_registration($);
        });
        return false;
      });
    }
    $(init_registration);
    </script>

   (Alternatively, include the template snippet
   ``registration/email_registration_include.html`` somewhere.)

3. Add ``email_registration`` to ``INSTALLED_APPS`` and include
   ``email_registration.urls`` somewhere in your URLconf.

4. Presto.
