from django.http import JsonResponse
from newsletter_subscription.utils import send_subscription_mail
from django.core.validators import validate_email
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


@require_POST
def ajax_subscribe(request, backend):
    email = request.POST.get('subscription_email', '')

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'message': _('Invalid email')})

    if backend.is_subscribed(email):
        return JsonResponse({
            'message': _(
                'This address is already subscribed to our newsletter.'
            )
        })

    send_subscription_mail(email, request)

    return JsonResponse({
        'message': _('You should receive a confirmation email shortly.')
    })
