from django.http import JsonResponse
from newsletter_subscription.utils import send_subscription_mail
from django.core.validators import validate_email
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError


@require_POST
def ajax_subscribe(request, backend):
    email = request.POST.get('subscription_email', '')

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'message': 'invalid email'})

    if backend.is_subscribed(email):
        return JsonResponse({'message': 'already subscribed'})

    send_subscription_mail(email, request)

    return JsonResponse({
        'message': 'You should receive a confirmation email.'
    })
