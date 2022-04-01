from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from newsletter_subscription.utils import send_subscription_mail


@require_POST
def ajax_subscribe(request, backend):
    email = request.POST.get("subscription_email", "")

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": _("Invalid email")})

    if backend.is_subscribed(email):
        return JsonResponse(
            {"error": _("This address is already subscribed to our newsletter.")}
        )

    send_subscription_mail(email, request)

    return JsonResponse(
        {"success": _("You should receive a confirmation email shortly.")}
    )
