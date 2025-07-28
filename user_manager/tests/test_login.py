from django.test import TestCase, Client
from django.urls import reverse
from user_manager.models.User import User


class LoginTest(TestCase):
    def setUp(self):
        # Créer un client pour les tests
        self.client = Client()

        # Créer un utilisateur de test
        self.test_user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )

        # URL de la page de login
        self.login_url = reverse('user_manager:login')

        # URL de la page d'accueil (pour vérifier la redirection après login)
        self.homepage_url = reverse('social_app:homepage')

    def test_login_page_loads(self):
        """Test que la page de login s'affiche correctement"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_manager/login.html')

    def test_login_success(self):
        """Test qu'un utilisateur peut se connecter avec des identifiants valides"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })

        # Vérifier que l'utilisateur est redirigé vers la page d'accueil après connexion
        self.assertRedirects(response, self.homepage_url)

        # Vérifier que l'utilisateur est authentifié
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, 'test@example.com')

    def test_login_failure_wrong_password(self):
        """Test que la connexion échoue avec un mauvais mot de passe"""
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        # L'utilisateur reste sur la page de login
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_manager/login.html')

        # L'utilisateur n'est pas authentifié
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

        # Un message d'erreur est présent
        self.assertContains(response, "Nom d'utilisateur ou mot de passe incorrect")

    def test_login_failure_nonexistent_user(self):
        """Test que la connexion échoue avec un email inexistant"""
        response = self.client.post(self.login_url, {
            'email': 'nonexistent@example.com',
            'password': 'testpassword123'
        })

        # L'utilisateur reste sur la page de login
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_manager/login.html')

        # L'utilisateur n'est pas authentifié
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

    def test_root_redirect_anonymous(self):
        """Test que la page racine redirige vers login pour un utilisateur anonyme"""
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, self.login_url)

    def test_root_redirect_authenticated(self):
        """Test que la page racine redirige vers homepage pour un utilisateur authentifié"""
        # Se connecter d'abord
        self.client.login(email='test@example.com', password='testpassword123')

        # Ensuite accéder à la racine
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, self.homepage_url)
