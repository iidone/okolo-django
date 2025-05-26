from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal, CATEGORY_CHOICES, CONDITION_CHOICES

class AdTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client = Client()

        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test description',
            category='electronics',
            condition='new',
            contact_info='test@example.com'
        )

    def test_ad_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_ad'), {
            'title': 'New Test Ad',
            'description': 'New description',
            'category': 'clothing',
            'condition': 'used',
            'contact_info': 'new@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_edit(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('edit_ad', args=[self.ad.id]), {
            'title': 'Updated Ad',
            'description': 'Updated description',
            'category': 'auto',
            'condition': 'broken',
            'contact_info': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Ad')

    def test_ad_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('delete_ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 0)

    def test_ad_search(self):
        response = self.client.get(reverse('home'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ad')

class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        self.client = Client()

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Ad 1',
            description='Description 1',
            category='electronics',
            condition='new'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Ad 2',
            description='Description 2',
            category='clothing',
            condition='used'
        )

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Test proposal'
        )

    def test_proposal_creation(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('current_ad', args=[self.ad2.id]), {
            'exchange_proposal': '1',
            'selected_ad': self.ad1.id,
            'comment': 'New exchange proposal'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeProposal.objects.count(), 2)

    def test_proposal_status_update(self):
        self.client.login(username='user2', password='testpass123')

        response = self.client.get(reverse('update_proposal', args=[self.proposal.id, 'accepted']))
        self.assertEqual(response.status_code, 302)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'accepted')

        response = self.client.get(reverse('update_proposal', args=[self.proposal.id, 'rejected']))
        self.assertEqual(response.status_code, 302)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, 'rejected')

    def test_proposal_list_view(self):
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad 2')