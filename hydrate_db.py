import os
import django
import random
from faker import Faker
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raddot.settings')
django.setup()

from user_manager.models import User
from social_app.models.Subraddot import Subraddot
from social_app.models.Post import Post
from social_app.models.Comment import Comment

fake = Faker('fr_FR')

# Create Users
def create_users(n=10):
    users = []
    for _ in range(n):
        username = fake.unique.user_name()
        email = fake.unique.email()
        password = fake.password(length=10)
        user = User.objects.create_user(email=email, username=username, password=password)
        users.append(user)
    return users

# Create Subraddots
def create_subraddots(users, n=5):
    subraddots = []
    for _ in range(n):
        name = fake.unique.word() + fake.unique.word()
        description = fake.sentence()
        creator = random.choice(users)
        subraddot = Subraddot(name=name, description=description, creator=creator)
        # Download a random image from Lorem Picsum for the icon
        response_icon = requests.get('https://picsum.photos/100', timeout=10)
        if response_icon.status_code == 200:
            subraddot.icon.save(f"icon_{name}.jpg", ContentFile(response_icon.content), save=False)
        # Download a random image from Lorem Picsum for the banner
        response_banner = requests.get('https://picsum.photos/600/200', timeout=10)
        if response_banner.status_code == 200:
            subraddot.banner.save(f"banner_{name}.jpg", ContentFile(response_banner.content), save=False)
        subraddot.save()
        subraddots.append(subraddot)
    return subraddots

# Create Posts
def create_posts(users, subraddots, n=20):
    posts = []
    for _ in range(n):
        post_type = random.choice(['text', 'image'])
        title = fake.sentence(nb_words=6)
        content = fake.paragraph() if post_type == 'text' else ''
        user = random.choice(users)
        subraddot = random.choice(subraddots)
        post = Post.objects.create(
            post_type=post_type,
            title=title,
            content=content,
            user=user,
            subraddot=subraddot
        )
        posts.append(post)
    return posts

# Create Comments
def create_comments(users, posts, n=50):
    for _ in range(n):
        content = fake.sentence()
        user = random.choice(users)
        post = random.choice(posts)
        Comment.objects.create(
            content=content,
            user=user,
            post=post
        )

users = create_users(10)
subraddots = create_subraddots(users, 5)
posts = create_posts(users, subraddots, 20)
create_comments(users, posts, 50)
print('Database hydrated with fake data!')
