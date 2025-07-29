import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from social_app.models.Subraddot import Subraddot
from social_app.forms.create_subraddot import CreateSubraddotForm

User = get_user_model()

class CreateSubraddotTest(TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test."""
        self.client = Client()
        # Création d'un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        # URL pour la création de subraddot
        self.create_url = reverse('social_app:create_subraddot')

    def test_create_subraddot_view_requires_login(self):
        """Test pour vérifier que la vue de création nécessite une connexion."""
        # Tenter d'accéder à la page sans être connecté
        response = self.client.get(self.create_url)
        # Vérifier la redirection vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/auth/login/' in response.url)

    def test_create_subraddot_view_accessible_when_logged_in(self):
        """Test pour vérifier que la page est accessible après connexion."""
        # Connexion de l'utilisateur
        self.client.login(email='test@example.com', password='testpassword123')
        # Accès à la page
        response = self.client.get(self.create_url)
        # Vérifier que la page s'affiche correctement
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social_app/subraddot_create.html')
        self.assertIsInstance(response.context['form'], CreateSubraddotForm)

    def test_create_subraddot_with_valid_data(self):
        """Test pour vérifier la création d'un subraddot avec des données valides."""
        # Connexion de l'utilisateur
        self.client.login(email='test@example.com', password='testpassword123')

        # Données du formulaire
        form_data = {
            'name': 'testsubraddot',
            'description': 'Ceci est une description de test'
        }

        # Envoi du formulaire
        response = self.client.post(self.create_url, form_data)

        # Vérifier qu'un subraddot a été créé
        self.assertEqual(Subraddot.objects.count(), 1)
        subraddot = Subraddot.objects.first()
        self.assertEqual(subraddot.name, 'testsubraddot')
        self.assertEqual(subraddot.description, 'Ceci est une description de test')
        self.assertEqual(subraddot.creator, self.user)

    def test_create_subraddot_with_invalid_name(self):
        """Test pour vérifier la validation du nom de subraddot."""
        # Connexion de l'utilisateur
        self.client.login(email='test@example.com', password='testpassword123')

        # Données du formulaire avec un nom invalide (caractères spéciaux)
        form_data = {
            'name': 'test@subraddot!',
            'description': 'Description test'
        }

        # Envoi du formulaire
        response = self.client.post(self.create_url, form_data)

        # Vérifier qu'aucun subraddot n'a été créé
        self.assertEqual(Subraddot.objects.count(), 0)

        # Vérifier que le formulaire contient des erreurs
        self.assertFormError(response, 'form', 'name',
                             "Le nom du subraddot ne peut contenir que des lettres, des chiffres, des tirets et des underscores.")

    def test_create_subraddot_with_duplicate_name(self):
        """Test pour vérifier la validation de l'unicité du nom."""
        # Créer un subraddot existant
        Subraddot.objects.create(
            name='existingsubraddot',
            description='Description existante',
            creator=self.user
        )

        # Connexion de l'utilisateur
        self.client.login(email='test@example.com', password='testpassword123')

        # Données du formulaire avec un nom déjà existant
        form_data = {
            'name': 'existingsubraddot',
            'description': 'Nouvelle description'
        }

        # Envoi du formulaire
        response = self.client.post(self.create_url, form_data)

        # Vérifier qu'aucun nouveau subraddot n'a été créé
        self.assertEqual(Subraddot.objects.count(), 1)

        # Vérifier que le formulaire contient des erreurs d'unicité
        self.assertFormError(response, 'form', 'name',
                             "Un subraddot avec ce nom existe déjà.")

    def test_create_subraddot_with_files(self):
        """Test pour vérifier le téléchargement de fichiers (bannière et icône)."""
        # Connexion de l'utilisateur
        self.client.login(email='test@example.com', password='testpassword123')

        # Création de petits fichiers image de test
        banner = SimpleUploadedFile(
            name='test_banner.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x44\x00\x3b',
            content_type='image/jpeg'
        )

        icon = SimpleUploadedFile(
            name='test_icon.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x44\x00\x3b',
            content_type='image/jpeg'
        )

        # Données du formulaire avec des fichiers
        form_data = {
            'name': 'filesubraddot',
            'description': 'Subraddot avec fichiers',
            'banner': banner,
            'icon': icon
        }

        # Envoi du formulaire avec des fichiers
        response = self.client.post(self.create_url, form_data, format='multipart')

        # Vérifier qu'un subraddot a été créé
        self.assertEqual(Subraddot.objects.count(), 1)
        subraddot = Subraddot.objects.first()
        self.assertEqual(subraddot.name, 'filesubraddot')

        # Vérifier que les fichiers ont été enregistrés
        self.assertTrue(subraddot.banner)
        self.assertTrue(subraddot.icon)

        # Nettoyer les fichiers créés pour le test
        if os.path.exists(subraddot.banner.path):
            os.remove(subraddot.banner.path)
        if os.path.exists(subraddot.icon.path):
            os.remove(subraddot.icon.path)
