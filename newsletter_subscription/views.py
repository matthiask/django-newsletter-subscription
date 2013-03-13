from django import forms
from django.contrib import messages
from django.core.signing import BadSignature
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _, ugettext_lazy

from newsletter_subscription.utils import (get_signer,
    send_subscription_mail, send_unsubscription_mail)


### Generic API START

from newsletter_subscription.models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ('email', 'is_active')


class backend(object):
    @staticmethod
    def is_subscribed(email):
        return Subscription.objects.filter(
            email=email,
            is_active=True,
            ).exists()

    @staticmethod
    def subscribe(email):
        subscription, created = Subscription.objects.get_or_create(email=email)
        if not subscription.is_active:
            subscription.is_active = True
            subscription.save()
            return True
        return False

    @staticmethod
    def unsubscribe(email):
        try:
            subscription = Subscription.objects.get(email=email)
        except Subscription.DoesNotExist:
            return

        subscription.is_active = False
        subscription.save()

    @staticmethod
    def subscription_details_form(email, request):
        try:
            instance = Subscription.objects.get(email=email)
        except Subscription.DoesNotExist:
            instance = None

        if request.method == 'POST':
            return SubscriptionForm(request.POST, instance=instance)
        return SubscriptionForm(instance=instance)

### Generic API END


class NewsletterForm(forms.Form):
    email = forms.EmailField(label=ugettext_lazy('email address'),
        widget=forms.TextInput(attrs={
            'placeholder': ugettext_lazy('email address'),
            }), max_length=254)
    action = forms.ChoiceField(label=ugettext_lazy('action'), choices=(
        ('subscribe', _('subscribe')),
        ('unsubscribe', _('unsubscribe')),
        ), widget=forms.RadioSelect, initial='subscribe')

    def clean(self):
        data = super(NewsletterForm, self).clean()
        email = data.get('email')

        if not email:
            return data

        ction = data.get('action')
        if action == 'subscribe' and backend.is_subscribed(email):
            raise forms.ValidationError(
                _('This address is already subscribed to our newsletter.'))

        elif action == 'unsubscribe' and not backend.is_subscribed(email):
            raise forms.ValidationError(
                _('This address is not subscribed to our newsletter.'))

        return data


def form(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            action = form.cleaned_data['action']
            email = form.cleaned_data['email']

            if action == 'subscribe':
                send_subscription_mail(email, request)
                messages.success(request,
                    _('You should receive a confirmation email shortly.'))
            else:
                backend.unsubscribe(email)
                send_unsubscription_mail(email, request)
                messages.success(request, _('You have been unsubscribed.'))

            return redirect('.')

    else:
        form = NewsletterForm()

    return render(request, 'newsletter_subscription/form.html', {
        'form': form,
        })


def subscribe(request, code, form_class=SubscriptionForm):
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
            messages.success(request,
                _('Thank you! The subscription details have been updated.'))
            form.save()

            return redirect('.')

    return render(request, 'newsletter_subscription/subscribe.html', {
        'email': email,
        'form': form,
        })


def resubscribe(request, code):
    try:
        email = get_signer().unsign(code)
    except BadSignature:
        messages.error(request, _('We are sorry. This link is broken.'))
        return redirect('newsletter_subscription_form')

    if backend.is_subscribed(email):
        messages.info(request,
            _('Your subscription is already active.'))

    return redirect('newsletter_subscription_subscribe', code=code)
