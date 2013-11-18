from django.core import mail
from django.test import TestCase
from django.utils.six.moves.urllib.parse import unquote

from testapp.models import Subscription


class SubscriptionTest(TestCase):
    def test_subscription(self):
        self.client.get('/newsletter/')
        pass

        response = self.client.post('/newsletter/', {
            'email': 'test@example.com',
            'action': 'subscribe',
            })
        self.assertRedirects(response, '/newsletter/')
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        subscribe_url = unquote([
            line for line in body.splitlines() if 'testserver' in line][0])

        self.assertEqual(Subscription.objects.count(), 0)
        response = self.client.get(subscribe_url)
        self.assertEqual(
            Subscription.objects.filter(is_active=True).count(), 1)

        self.assertContains(response, 'id="id_full_name"')
        response = self.client.post(subscribe_url, {
            'full_name': 'Hans Muster',
            })

        self.assertRedirects(response, subscribe_url)
        subscription = Subscription.objects.get()
        self.assertTrue(subscription.is_active)
        self.assertEqual(subscription.email, 'test@example.com')
        self.assertEqual(subscription.full_name, 'Hans Muster')

        self.assertContains(self.client.post('/newsletter/', {
            'email': 'test@example.com',
            'action': 'subscribe',
            }),
            'This address is already subscribed to our newsletter.')

        self.assertContains(self.client.post('/newsletter/', {
            'email': 'test@example.com',
            'action': 'unsubscribe',
            }, follow=True),
            'You have been unsubscribed.')

        self.assertEqual(
            Subscription.objects.filter(is_active=True).count(), 0)

        self.assertEqual(len(mail.outbox), 2)
        body = mail.outbox[1].body
        resubscribe_url = unquote([
            line for line in body.splitlines() if 'testserver' in line][0])

        self.assertContains(
            self.client.get(resubscribe_url, follow=True),
            'Your subscription has been activated.')
        self.assertEqual(
            Subscription.objects.filter(is_active=True).count(), 1)

        self.assertContains(
            self.client.get(resubscribe_url, follow=True),
            'Your subscription is already active.')
