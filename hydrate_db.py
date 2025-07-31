import os
import django
import random
from faker import Faker
import requests
from django.core.files.base import ContentFile

from social_app.models import VotePost

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raddot.settings')
django.setup()

from user_manager.models import User
from social_app.models.Subraddot import Subraddot
from social_app.models.Post import Post
from social_app.models.Comment import Comment
from social_app.models.Trophy import Trophy

fake = Faker('fr_FR')

# Liste des trophées disponibles
TROPHY_DEFINITIONS = [
    # Trophées généraux
    {'subraddot': None, 'name': '1er poste', 'icon': 'trophy/first_post.png',
     'description': 'Félicitations pour votre premier post !'},
    {'subraddot': None, 'name': '5e poste', 'icon': 'trophy/five_post.png',
     'description': 'Vous avez publié 5 posts !'},
    {'subraddot': None, 'name': '1er subraddot', 'icon': 'trophy/first_subraddot.png',
     'description': 'Vous avez créé votre premier subraddot !'},
    {'subraddot': None, 'name': '5e subraddot', 'icon': 'trophy/five_subraddot.png',
     'description': 'Vous avez créé 5 subraddots !'},
    # Trophées par subraddot (seront créés dynamiquement)
    {'subraddot': 'DYNAMIC', 'name': '1ere contrib', 'icon': 'trophy/sub_first_post.png',
     'description': 'Première contribution dans ce subraddot !'},
    {'subraddot': 'DYNAMIC', 'name': '5e contrib', 'icon': 'trophy/sub_five_post.png',
     'description': '5 contributions dans ce subraddot !'},
]


def create_users(n=15):
    """Crée des utilisateurs avec des données variées"""
    users = []
    print(f"Création de {n} utilisateurs...")

    for i in range(n):
        username = fake.unique.user_name()
        email = fake.unique.email()
        password = 'password'
        first_name = fake.first_name()
        last_name = fake.last_name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date
        )
        users.append(user)

    print(f"✓ {len(users)} utilisateurs créés")
    return users


def create_subraddots(users, n=8):
    """Crée des subraddots avec des créateurs variés"""
    subraddots = []
    print(f"Création de {n} subraddots...")

    for i in range(n):
        name = fake.unique.word().capitalize() + fake.unique.word().capitalize()
        description = fake.paragraph(nb_sentences=3)
        creator = random.choice(users)

        subraddot = Subraddot(name=name, description=description, creator=creator)

        # Télécharger une image aléatoire pour l'icône
        try:
            response_icon = requests.get('https://picsum.photos/100/100', timeout=10)
            if response_icon.status_code == 200:
                subraddot.icon.save(f"icon_{name.lower()}.jpg", ContentFile(response_icon.content), save=False)
        except:
            pass

        # Télécharger une image aléatoire pour la bannière
        try:
            response_banner = requests.get('https://picsum.photos/800/200', timeout=10)
            if response_banner.status_code == 200:
                subraddot.banner.save(f"banner_{name.lower()}.jpg", ContentFile(response_banner.content), save=False)
        except:
            pass

        subraddot.save()

        # Ajouter des membres aléatoirement (incluant le créateur)
        members_count = random.randint(2, min(8, len(users)))
        members = random.sample(users, members_count)
        if creator not in members:
            members.append(creator)
        subraddot.members.set(members)

        subraddots.append(subraddot)

    print(f"✓ {len(subraddots)} subraddots créés")
    return subraddots


def create_posts(users, subraddots, n=50):
    """Crée des posts variés (texte et image)"""
    posts = []
    print(f"Création de {n} posts...")

    for i in range(n):
        post_type = random.choice(['text', 'image'])
        title = fake.sentence(nb_words=random.randint(4, 10)).rstrip('.')
        user = random.choice(users)
        subraddot = random.choice(subraddots)

        # Générer du contenu selon le type
        if post_type == 'text':
            content = fake.paragraph(nb_sentences=random.randint(3, 8))
        else:
            content = fake.sentence() if random.choice([True, False]) else ''

        post = Post.objects.create(
            post_type=post_type,
            title=title,
            content=content,
            user=user,
            subraddot=subraddot
        )

        # Ajouter une image pour les posts de type image
        if post_type == 'image':
            try:
                width, height = random.choice([(800, 600), (600, 400), (1024, 768)])
                response_img = requests.get(f'https://picsum.photos/{width}/{height}', timeout=10)
                if response_img.status_code == 200:
                    post.img.save(f"post_{post.id}.jpg", ContentFile(response_img.content), save=True)
            except:
                pass

        posts.append(post)

    print(f"✓ {len(posts)} posts créés")
    return posts


def create_comments(users, posts, n=120):
    """Crée des commentaires sur les posts"""
    comments = []
    print(f"Création de {n} commentaires...")

    for i in range(n):
        content = fake.paragraph(nb_sentences=random.randint(1, 4))
        user = random.choice(users)
        post = random.choice(posts)

        comment = Comment.objects.create(
            content=content,
            user=user,
            post=post
        )
        comments.append(comment)

    print(f"✓ {len(comments)} commentaires créés")
    return comments


def create_votes(users, posts, vote_ratio=0.7):
    """Crée des votes sur les posts (70% des posts ont au moins un vote)"""
    votes = []
    print("Création des votes...")

    posts_to_vote = random.sample(posts, int(len(posts) * vote_ratio))

    for post in posts_to_vote:
        # Nombre d'utilisateurs qui voteront sur ce post
        voters_count = random.randint(1, min(10, len(users)))
        voters = random.sample(users, voters_count)

        for voter in voters:
            # 60% upvote, 40% downvote
            vote_value = 1 if random.random() < 0.6 else -1

            vote = VotePost.objects.create(
                user=voter,
                post=post,
                value=vote_value
            )
            votes.append(vote)

    print(f"✓ {len(votes)} votes créés")
    return votes


def create_trophies(users, subraddots):
    """Crée des trophées basés sur les achievements des utilisateurs"""
    trophies = []
    print("Attribution des trophées...")

    for user in users:
        user_posts_count = user.posts.count()
        user_subraddots_count = user.created_subraddots.count()

        # Trophée "1er poste"
        if user_posts_count >= 1:
            trophy = Trophy.objects.create(
                user=user,
                subraddot=None,
                name='1er poste',
                icon='trophy/first_post.png',
                description='Félicitations pour votre premier post !'
            )
            trophies.append(trophy)

        # Trophée "5e poste"
        if user_posts_count >= 5:
            trophy = Trophy.objects.create(
                user=user,
                subraddot=None,
                name='5e poste',
                icon='trophy/five_post.png',
                description='Vous avez publié 5 posts !'
            )
            trophies.append(trophy)

        # Trophée "1er subraddot"
        if user_subraddots_count >= 1:
            trophy = Trophy.objects.create(
                user=user,
                subraddot=None,
                name='1er subraddot',
                icon='trophy/first_subraddot.png',
                description='Vous avez créé votre premier subraddot !'
            )
            trophies.append(trophy)

        # Trophée "5e subraddot" (rare, probablement personne ne l'aura)
        if user_subraddots_count >= 5:
            trophy = Trophy.objects.create(
                user=user,
                subraddot=None,
                name='5e subraddot',
                icon='trophy/five_subraddot.png',
                description='Vous avez créé 5 subraddots !'
            )
            trophies.append(trophy)

        # Trophées par subraddot
        for subraddot in subraddots:
            user_posts_in_sub = user.posts.filter(subraddot=subraddot).count()

            # Trophée "1ere contrib"
            if user_posts_in_sub >= 1:
                trophy = Trophy.objects.create(
                    user=user,
                    subraddot=subraddot,
                    name='1ere contrib',
                    icon='trophy/sub_first_post.png',
                    description=f'Première contribution dans {subraddot.name} !'
                )
                trophies.append(trophy)

            # Trophée "5e contrib"
            if user_posts_in_sub >= 5:
                trophy = Trophy.objects.create(
                    user=user,
                    subraddot=subraddot,
                    name='5e contrib',
                    icon='trophy/sub_five_post.png',
                    description=f'5 contributions dans {subraddot.name} !'
                )
                trophies.append(trophy)

    print(f"✓ {len(trophies)} trophées attribués")
    return trophies


def print_statistics():
    """Affiche des statistiques sur les données créées"""
    print("\n" + "=" * 50)
    print("STATISTIQUES DE LA BASE DE DONNÉES")
    print("=" * 50)

    print(f"👥 Utilisateurs: {User.objects.count()}")
    print(f"🏠 Subraddots: {Subraddot.objects.count()}")
    print(f"📝 Posts: {Post.objects.count()}")
    print(f"   - Posts texte: {Post.objects.filter(post_type='text').count()}")
    print(f"   - Posts image: {Post.objects.filter(post_type='image').count()}")
    print(f"💬 Commentaires: {Comment.objects.count()}")
    print(f"👍 Votes: {VotePost.objects.count()}")
    print(f"   - Upvotes: {VotePost.objects.filter(value=1).count()}")
    print(f"   - Downvotes: {VotePost.objects.filter(value=-1).count()}")
    print(f"🏆 Trophées: {Trophy.objects.count()}")
    print(f"   - Trophées généraux: {Trophy.objects.filter(subraddot__isnull=True).count()}")
    print(f"   - Trophées de subraddot: {Trophy.objects.filter(subraddot__isnull=False).count()}")

    # Top users
    print(f"\n👑 TOP USERS:")
    top_users = User.objects.all()[:5]
    for user in top_users:
        posts_count = user.posts.count()
        trophies_count = user.trophies.count()
        votes_count = user.votes.count()
        print(f"   - {user.username}: {posts_count} posts, {trophies_count} trophées, {votes_count} votes")


def main():
    print("🚀 GÉNÉRATION D'UNE BASE DE DONNÉES COMPLEXE")
    print("=" * 50)

    # Supprimer les données existantes automatiquement
    print("🗑️ Suppression des données existantes...")
    Trophy.objects.all().delete()
    VotePost.objects.all().delete()
    Comment.objects.all().delete()
    Post.objects.all().delete()
    Subraddot.objects.all().delete()
    User.objects.all().delete()
    print("✓ Données supprimées")

    # Créer les données
    users = create_users(15)
    subraddots = create_subraddots(users, 8)
    posts = create_posts(users, subraddots, 50)
    comments = create_comments(users, posts, 120)
    votes = create_votes(users, posts, 0.7)
    trophies = create_trophies(users, subraddots)

    print_statistics()
    print("\n🎉 Base de données générée avec succès !")


# Exécuter automatiquement
main()