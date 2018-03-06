from django import forms
from django.contrib import messages
from django.core.signing import BadSignature
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _, ugettext_lazy

from newsletter_subscription.utils import (
    get_signer, send_subscription_mail, send_unsubscription_mail)


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        label=ugettext_lazy('email address'),
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': ugettext_lazy('email address'),
        }),
    )
    action = forms.ChoiceField(
        label=ugettext_lazy('action'),
        choices=(
            ('subscribe', ugettext_lazy('subscribe')),
            ('unsubscribe', ugettext_lazy('unsubscribe')),
        ),
        widget=forms.RadioSelect,
        initial='subscribe',
    )

    def __init__(self, *args, **kwargs):
        self.backend = kwargs.pop('backend')
        self.request = kwargs.pop('request')
        super(NewsletterForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(NewsletterForm, self).clean()
        email = data.get('email')

        if not email:
            return data

        action = data.get('action')

        if action == 'subscribe' and self.backend.is_subscribed(email):
            raise forms.ValidationError(
                _('This address is already subscribed to our newsletter.'))

        elif action == 'unsubscribe' and not self.backend.is_subscribed(email):
            raise forms.ValidationError(
                _('This address is not subscribed to our newsletter.'))

        return data

    def process(self):
        action = self.cleaned_data['action']
        email = self.cleaned_data['email']

        if action == 'subscribe':
            send_subscription_mail(email, self.request)
            messages.success(
                self.request,
                _('You should receive a confirmation email shortly.'))
        else:
            self.backend.unsubscribe(email)
            send_unsubscription_mail(email, self.request)
            messages.success(self.request, _('You have been unsubscribed.'))


def form(request, backend):
    form = NewsletterForm(
        request.POST or None,
        backend=backend,
        request=request,
        initial={
            'email': request.user.email,
        } if request.user.is_authenticated else None,
    )

    if request.method == 'POST' and form.is_valid():
        form.process()
        return redirect(request.path)

    return render(request, 'newsletter_subscription/form.html', {
        'form': form,
    })


def subscribe(request, code, backend):
    try:
        email = get_signer().unsign(code)
    except BadSignature:
        messages.error(request, _('We are sorry. This link is broken.'))
        return redirect('newsletter_subscription_form')

    if backend.subscribe(email):
        messages.success(request, _('Your subscription has been activated.'))

    form = backend.subscription_details_form(email, request=request)
    if form is None:
        return redirect('newsletter_subscription_form')

    elif request.method == 'POST':
        if form.is_valid():
            messages.success(
                request,
                _('Thank you! The subscription details have been updated.'))
            form.save()

            return redirect(request.path)

    return render(request, 'newsletter_subscription/subscribe.html', {
        'email': email,
        'form': form,
    })


def resubscribe(request, code, backend):
    try:
        email = get_signer().unsign(code)
    except BadSignature:
        messages.error(request, _('We are sorry. This link is broken.'))
        return redirect('newsletter_subscription_form')

    if backend.is_subscribed(email):
        messages.info(
            request, _('Your subscription is already active.'))

    return redirect('newsletter_subscription_subscribe', code=code)
