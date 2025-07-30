from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from social_app.models.Subraddot import Subraddot
from social_app.models.Post import Post

User = get_user_model()


class CreatePostTests(TestCase):
    def setUp(self):
        """Préparation des données pour les tests."""
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

        # Créer un Subraddot
        self.subraddot = Subraddot.objects.create(
            name='testcommunity',
            description='Test community description',
            creator=self.user
        )

        # Ajouter l'utilisateur aux membres du Subraddot
        self.subraddot.members.add(self.user)

        # Initialiser le client
        self.client = Client()
        # Se connecter avec l'utilisateur de test
        self.client.login(username='testuser', password='password123')

        # URL pour la création de post
        self.create_post_url = reverse('social_app:create_post', kwargs={'name': 'testcommunity'})

    def test_create_text_post(self):
        """Tester la création d'un post de type texte."""
        # Données du formulaire pour un post texte
        form_data = {
            'title': 'Test Text Post',
            'post_type': 'text',
            'content': 'This is a test content'
        }

        # Envoi de la requête POST
        response = self.client.post(self.create_post_url, form_data)

        # Vérifier la redirection
        self.assertEqual(response.status_code, 302)

        # Vérifier que le post a été créé
        post = Post.objects.filter(title='Test Text Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'This is a test content')
        self.assertEqual(post.post_type, 'text')
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.subraddot, self.subraddot)

    def test_create_image_post(self):
        """Tester la création d'un post de type image."""
        # Créer une image de test
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'dummy image content',
            content_type='image/jpeg'
        )

        # Données du formulaire pour un post image
        form_data = {
            'title': 'Test Image Post',
            'post_type': 'image',
            'img': image  # Notez que le nom du champ ici est 'img' comme dans le HTML
        }

        # Envoi de la requête POST
        response = self.client.post(self.create_post_url, form_data)

        # Vérifier la redirection
        self.assertEqual(response.status_code, 302)

        # Vérifier que le post a été créé
        post = Post.objects.filter(title='Test Image Post').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.post_type, 'image')
        self.assertIsNotNone(post.img)  # Vérifier que l'image a été enregistrée

    def test_create_image_post_missing_file(self):
        """Tester le cas où l'image est manquante."""
        form_data = {
            'title': 'Test Missing Image',
            'post_type': 'image',
            # Pas d'image fournie
        }

        # Envoi de la requête POST
        response = self.client.post(self.create_post_url, form_data)

        # Vérifier la redirection
        self.assertEqual(response.status_code, 302)

        # Vérifier qu'aucun post n'a été créé
        posts = Post.objects.filter(title='Test Missing Image')
        self.assertEqual(posts.count(), 0)

    def test_non_member_cannot_create_post(self):
        """Tester qu'un non-membre ne peut pas créer de post."""
        # Créer un nouvel utilisateur non membre
        non_member = User.objects.create_user(
            username='nonmember',
            email='nonmember@example.com',
            password='password123'
        )

        # Se connecter avec l'utilisateur non membre
        self.client.login(username='nonmember', password='password123')

        # Tenter de créer un post
        form_data = {
            'title': 'Post by Non-Member',
            'post_type': 'text',
            'content': 'This should not be allowed'
        }

        response = self.client.post(self.create_post_url, form_data)

        # Vérifier la redirection
        self.assertEqual(response.status_code, 302)

        # Vérifier qu'aucun post n'a été créé
        posts = Post.objects.filter(title='Post by Non-Member')
        self.assertEqual(posts.count(), 0)

    def test_missing_title(self):
        """Tester le cas où le titre est manquant."""
        form_data = {
            'post_type': 'text',
            'content': 'Content without title'
            # Pas de titre fourni
        }

        response = self.client.post(self.create_post_url, form_data)

        # Vérifier la redirection
        self.assertEqual(response.status_code, 302)

        # Vérifier qu'aucun post n'a été créé
        posts = Post.objects.filter(content='Content without title')
        self.assertEqual(posts.count(), 0)
