from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileUpdateForm
from builds.models import Build, Comment

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Profile should be created automatically via signals
        self.profile = self.user.profile

    def test_user_profile_creation(self):
        """Test that user profile is created automatically when user is created"""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='password123'
        )
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsInstance(new_user.profile, UserProfile)

    def test_profile_view(self):
        """Test that user profile page loads correctly"""
        response = self.client.get(reverse('user-profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_profile_edit_requires_login(self):
        """Test that profile edit requires authentication"""
        response = self.client.get(reverse('profile-edit'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_edit_form(self):
        """Test profile edit form functionality"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('profile-edit'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'updated@example.com',
            'display_name': 'Test Display Name',
            'bio': 'This is my bio',
            'location': 'Test City',
            'favorite_weapon': 'Bloodhound\'s Fang'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful save
        
        # Refresh user and profile from database
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.profile.display_name, 'Test Display Name')
        self.assertEqual(self.profile.bio, 'This is my bio')

    def test_get_display_name(self):
        """Test the get_display_name method"""
        # Should return username when display_name is empty
        self.assertEqual(self.profile.get_display_name(), self.user.username)
        
        # Should return display_name when set
        self.profile.display_name = 'Custom Name'
        self.profile.save()
        self.assertEqual(self.profile.get_display_name(), 'Custom Name')

    def test_profile_stats(self):
        """Test profile statistics methods"""
        # Create some builds and comments
        build = Build.objects.create(
            user=self.user,
            title='Test Build',
            description='Test Description',
            weapons='Test Weapon',
            armor='Test Armor',
            talismans='Test Talisman',
            category='PVE'
        )
        
        comment = Comment.objects.create(
            build=build,
            user=self.user,
            content='Test comment'
        )
        
        # Like someone else's build
        other_user = User.objects.create_user(username='other', password='pass')
        other_build = Build.objects.create(
            user=other_user,
            title='Other Build',
            description='Other Description',
            weapons='Other Weapon',
            armor='Other Armor',
            talismans='Other Talisman',
            category='PVP'
        )
        other_build.liked_by.add(self.user)
        
        self.assertEqual(self.profile.total_builds(), 1)
        self.assertEqual(self.profile.total_comments(), 1)
        self.assertEqual(self.profile.total_liked_builds(), 1)

    def test_profile_tabs(self):
        """Test profile page tabs functionality"""
        # Test builds tab
        response = self.client.get(reverse('user-profile', kwargs={'username': self.user.username}) + '?tab=builds')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_tab'], 'builds')
        
        # Test liked builds tab
        response = self.client.get(reverse('user-profile', kwargs={'username': self.user.username}) + '?tab=liked')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_tab'], 'liked')
        
        # Test comments tab
        response = self.client.get(reverse('user-profile', kwargs={'username': self.user.username}) + '?tab=comments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_tab'], 'comments')

    def test_registration_form(self):
        """Test user registration form"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertTrue(hasattr(user, 'profile'))

    def test_get_profile_picture_url(self):
        """Test profile picture URL generation"""
        # Should return placeholder URL when no picture
        url = self.profile.get_profile_picture_url()
        self.assertIn('ui-avatars.com', url)
        self.assertIn(self.user.username, url)

    def test_profile_picture_in_navbar(self):
        """Test that profile pictures appear in navbar"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('build-list'))
        self.assertEqual(response.status_code, 200)
        # Check that profile picture URL is in the response (accounting for HTML escaping)
        expected_url = self.user.profile.get_profile_picture_url().replace('&', '&amp;')
        self.assertContains(response, expected_url)
        # Check that user's display name is in the navbar
        self.assertContains(response, self.user.profile.get_display_name())


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

    def test_own_profile_context(self):
        """Test that is_own_profile context is set correctly"""
        self.client.login(username='user1', password='password123')
        
        # Viewing own profile
        response = self.client.get(reverse('user-profile', kwargs={'username': 'user1'}))
        self.assertTrue(response.context['is_own_profile'])
        
        # Viewing someone else's profile
        response = self.client.get(reverse('user-profile', kwargs={'username': 'user2'}))
        self.assertFalse(response.context['is_own_profile'])

    def test_my_profile_redirect(self):
        """Test my-profile URL redirects to user's profile"""
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('my-profile'))
        self.assertRedirects(response, reverse('user-profile', kwargs={'username': 'user1'}))
