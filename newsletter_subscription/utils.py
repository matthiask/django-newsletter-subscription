from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.template.loader import TemplateDoesNotExist, render_to_string
try:
    from django.urls import reverse
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse


def get_signer(salt='newsletter_subscription'):
    """
    Returns the signer instance used to sign and unsign the registration
    link tokens
    """
    return signing.Signer(salt=salt)


def send_subscription_mail(email, request):
    """
    Sends the subscription mail

    * ``email``: The email address where the subscription link should be
      sent to.
    * ``request``: A HTTP request instance, used to construct the complete
      URL (including protocol and domain) for the registration link.

    The mail is rendered using the following two templates:

    * ``newsletter_subscription/subscription_email.txt``: The first line of
      this template will be the subject, the third to the last line the body
      of the email.
    * ``newsletter_subscription/subscription_email.html``: The body of the
      HTML version of the mail. This template is **NOT** available by default
      and is not required either.
    """

    url = request.build_absolute_uri(
        reverse('newsletter_subscription_subscribe', kwargs={
            'code': get_signer().sign(email),
        }))

    render_to_mail(
        'newsletter_subscription/subscription_email',
        {
            'subscribe_url': url,
        },
        to=[email],
    ).send()


def send_unsubscription_mail(email, request):
    url = request.build_absolute_uri(
        reverse(
            'newsletter_subscription_resubscribe',
            kwargs={
                'code': get_signer().sign(email),
            }))

    render_to_mail(
        'newsletter_subscription/unsubscription_email',
        {
            'resubscribe_url': url,
        },
        to=[email],
    ).send()


def render_to_mail(template, context, **kwargs):
    """
    Renders a mail and returns the resulting ``EmailMultiAlternatives``
    instance

    * ``template``: The base name of the text and HTML (optional) version of
      the mail.
    * ``context``: The context used to render the mail. This context instance
      should contain everything required.
    * Additional keyword arguments are passed to the ``EmailMultiAlternatives``
      instantiation. Use those to specify the ``to``, ``headers`` etc.
      arguments.

    Usage example::

        # Render the template myproject/hello_mail.txt (first line contains
        # the subject, third to last the body) and optionally the template
        # myproject/hello_mail.html containing the alternative HTML
        # representation.
        message = render_to_mail('myproject/hello_mail', {}, to=[email])
        message.send()
    """
    lines = iter(render_to_string('%s.txt' % template, context).splitlines())

    subject = u''
    while True:
        line = next(lines)
        if line:
            subject = line
            break

    body = u'\n'.join(lines).strip('\n')
    message = EmailMultiAlternatives(subject=subject, body=body, **kwargs)

    try:
        message.attach_alternative(
            render_to_string('%s.html' % template, context),
            'text/html')
    except TemplateDoesNotExist:
        pass

    return message
