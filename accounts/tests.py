from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class HomePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for key elements
        self.assertContains(response, 'Elden Ring Builds Community')
        self.assertContains(response, 'Discover, share, and perfect')
        self.assertContains(response, 'Why Choose Our Platform?')

    def test_home_page_shows_stats(self):
        """Test that home page displays community statistics"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for stats display
        self.assertContains(response, 'Builds')
        self.assertContains(response, 'Warriors')
        self.assertContains(response, 'Comments')

    def test_home_page_anonymous_user_cta(self):
        """Test that home page shows appropriate CTA for anonymous users"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for join community and browse builds buttons
        self.assertContains(response, 'Join Community')
        self.assertContains(response, 'Browse Builds')
        self.assertContains(response, 'Sign Up Free')

    def test_home_page_authenticated_user_cta(self):
        """Test that home page shows appropriate CTA for authenticated users"""
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check for create build button
        self.assertContains(response, 'Create Build')


class LoginPageStylingTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page_uses_bootstrap_styling(self):
        """Test that login page uses Bootstrap card styling"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # Check for current Bootstrap card structure
        self.assertContains(response, 'class="card"')
        self.assertContains(response, 'card-body')  # More flexible check
        
        # Check for form styling
        self.assertContains(response, 'class="form-label"')
        self.assertContains(response, 'btn btn-primary')  # More flexible check
        
        # Check for proper title and Elden Ring theme
        self.assertContains(response, 'Welcome Back, Tarnished')
        self.assertContains(response, 'Enter the Lands Between')

    def test_login_page_has_register_link(self):
        """Test that login page has link to registration"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        # Check for register link with current text
        self.assertContains(response, 'New to the Lands Between?')
        self.assertContains(response, 'Create Account')

    def test_logged_out_page_styling(self):
        """Test that logged out page redirects properly"""
        # Login first
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Logout and check the redirect (goes to home, not login)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))


class LogoutConfirmationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_logout_with_post_request(self):
        """Test that logout works with POST request"""
        self.client.login(username='testuser', password='testpass123')
        
        # Verify user is logged in
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'testuser')
        
        # Logout with POST request (redirects to home, not login)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        
        # Verify user is logged out
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'testuser')
        self.assertContains(response, 'Login')

    def test_logout_with_get_request_redirects(self):
        """Test that GET request to logout redirects to home"""
        self.client.login(username='testuser', password='testpass123')
        
        # GET request should redirect without logging out
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        
        # User should still be logged in
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'testuser')

    def test_logout_confirmation_modal_in_navbar(self):
        """Test that logout confirmation modal is present in navbar"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that modal elements are present
        self.assertContains(response, 'id="logoutModal"')
        self.assertContains(response, 'Confirm Logout')
        self.assertContains(response, 'Are you sure you want to log out?')
        self.assertContains(response, 'data-bs-toggle="modal"')
        self.assertContains(response, 'data-bs-target="#logoutModal"')

    def test_logout_modal_shows_user_info(self):
        """Test that logout modal displays user information"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Check that user info is displayed in modal
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.profile.get_display_name())

    def test_anonymous_user_no_logout_button(self):
        """Test that anonymous users don't see logout button"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Anonymous users should see login/register, not logout
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Register')
        self.assertNotContains(response, 'logoutModal')
        self.assertNotContains(response, 'data-bs-toggle="modal"')
        self.assertNotContains(response, 'Confirm Logout')


class FormValidationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_username_length_validation_login(self):
        """Test that login form accepts usernames up to 25 characters"""
        from .forms import CustomAuthenticationForm
        
        # Create a user with 25-character username
        username_25 = 'a' * 25
        User.objects.create_user(username=username_25, password='testpass123')
        
        # Test that login form accepts this username
        form_data = {
            'username': username_25,
            'password': 'testpass123'
        }
        form = CustomAuthenticationForm(data=form_data)
        # Note: form.is_valid() might fail due to authentication, but username field should not have length errors
        form.full_clean()
        self.assertNotIn('username', form.errors, "25-character username should not have length validation errors")
