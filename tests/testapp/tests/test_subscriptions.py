from urllib.parse import unquote

from django.core import mail
from django.test import TestCase
from testapp.models import Subscription
from testapp.urls import TestModelBackend


class MockRequest:
    GET = {}
    POST = {}


class SubscriptionTest(TestCase):
    def test_model(self):
        model = Subscription.objects.create(email="blasdasd@asdasd.ch")
        self.assertEqual(str(model), "blasdasd@asdasd.ch")

    def test_subscription(self):
        self.assertContains(self.client.get("/newsletter/"), 'id="id_email"', 1)

        response = self.client.post(
            "/newsletter/",
            {
                "email": "",
                "action": "subscribe",
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/newsletter/",
            {
                "email": "test@example.com",
                "action": "subscribe",
            },
        )
        self.assertRedirects(response, "/newsletter/")
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        subscribe_url = unquote(
            [line for line in body.splitlines() if "testserver" in line][0]
        )

        self.assertEqual(Subscription.objects.count(), 0)
        response = self.client.get(subscribe_url)
        self.assertEqual(Subscription.objects.filter(is_active=True).count(), 1)

        self.assertContains(
            self.client.get(
                subscribe_url.replace("com:", "ch:"),
                follow=True,
            ),
            "We are sorry. This link is broken.",
            status_code=200,
        )

        self.assertContains(response, 'id="id_full_name"')
        response = self.client.post(
            subscribe_url,
            {
                "full_name": "",
            },
        )
        self.assertContains(response, "This field is required.", 1)

        response = self.client.post(
            subscribe_url,
            {
                "full_name": "Hans Muster",
            },
        )

        self.assertRedirects(
            response,
            subscribe_url.replace("http://testserver", ""),
        )
        subscription = Subscription.objects.get()
        self.assertTrue(subscription.is_active)
        self.assertEqual(subscription.email, "test@example.com")
        self.assertEqual(subscription.full_name, "Hans Muster")

        self.assertContains(
            self.client.post(
                "/newsletter/",
                {
                    "email": "test@example.com",
                    "action": "subscribe",
                },
            ),
            "This address is already subscribed to our newsletter.",
        )

        self.assertContains(
            self.client.post(
                "/newsletter/",
                {
                    "email": "test@example.com",
                    "action": "unsubscribe",
                },
                follow=True,
            ),
            "You have been unsubscribed.",
        )

        self.assertEqual(Subscription.objects.filter(is_active=True).count(), 0)

        self.assertContains(
            self.client.post(
                "/newsletter/",
                {
                    "email": "test@example.com",
                    "action": "unsubscribe",
                },
                follow=False,
            ),
            "This address is not subscribed to our newsletter.",
        )

        self.assertEqual(len(mail.outbox), 2)
        body = mail.outbox[1].body
        resubscribe_url = unquote(
            [line for line in body.splitlines() if "testserver" in line][0]
        )

        self.assertContains(
            self.client.get(resubscribe_url, follow=True),
            "Your subscription has been activated.",
        )
        self.assertEqual(Subscription.objects.filter(is_active=True).count(), 1)

        self.assertContains(
            self.client.get(resubscribe_url, follow=True),
            "Your subscription is already active.",
        )

        self.assertContains(
            self.client.get(
                # Purposefully break the link.
                resubscribe_url.replace("com:", "ch:"),
                follow=True,
            ),
            "We are sorry. This link is broken.",
            status_code=200,
        )

    def test_backend(self):
        backend = TestModelBackend(Subscription)

        # Not subscribed yet.
        self.assertFalse(backend.is_subscribed("test@example.com"))

        # Subscribe.
        self.assertTrue(backend.subscribe("test@example.com"))

        # Already subscribed.
        self.assertFalse(backend.subscribe("test@example.com"))

        subscription = Subscription.objects.get()
        self.assertEqual(subscription.email, "test@example.com")
        self.assertTrue(subscription.is_active)

        # Unsubscribe
        self.assertEqual(None, backend.unsubscribe("test@example.com"))

        subscription = Subscription.objects.get()
        self.assertFalse(subscription.is_active)

        # Does not exist, silent failure
        self.assertEqual(None, backend.unsubscribe("test22@example.com"))

        subscription.is_active = True
        subscription.save()

        form = backend.subscription_details_form("test@example.com", MockRequest())
        self.assertEqual(["full_name"], list(form.fields.keys()))

        # That is the current behavior.
        form = backend.subscription_details_form("test22@example.com", MockRequest())
        self.assertEqual(None, form)

    def test_42(self):
        response = self.client.post(
            "/newsletter/",
            {
                "email": "test42@example.com",
                "action": "subscribe",
            },
        )
        self.assertRedirects(response, "/newsletter/")
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        subscribe_url = unquote(
            [line for line in body.splitlines() if "testserver" in line][0]
        )

        self.assertEqual(Subscription.objects.count(), 0)
        response = self.client.get(subscribe_url)
        self.assertRedirects(response, "/newsletter/")
        self.assertEqual(Subscription.objects.filter(is_active=True).count(), 1)

    def test_ajax_subscription(self):
        for email in ["", "mnwr@@ewrwer.com", "@"]:
            response = self.client.post(
                "/newsletter/ajax_subscribe/", {"subscription_email": email}
            )
            self.assertContains(response, "Invalid email")

        response = self.client.post(
            "/newsletter/ajax_subscribe/", {"subscription_email": "test@example.com"}
        )
        self.assertContains(response, "You should receive a confirmation email shortly")
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        subscribe_url = unquote(
            [line for line in body.splitlines() if "testserver" in line][0]
        )

        self.assertEqual(Subscription.objects.count(), 0)
        response = self.client.get(subscribe_url)
        self.assertEqual(Subscription.objects.filter(is_active=True).count(), 1)

        response = self.client.post(
            "/newsletter/ajax_subscribe/", {"subscription_email": "test@example.com"}
        )
        self.assertContains(response, "already subscribed")
