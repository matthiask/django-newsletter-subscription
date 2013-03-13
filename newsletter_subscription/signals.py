from django.dispatch import Signal


subscribed = Signal(providing_args=['request', 'subscription'])
unsubscribed = Signal(providing_args=['request', 'subscription'])
