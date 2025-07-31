from social_app.models.Trophy import Trophy

TROPHY_NAME = [
    'First post',
    'Five posts',
    'First subraddot',
    'sub:First post',
    'sub:Five posts',
    'sub:First member',
]

# user_post_count = Post.objects.filter(user=request.user, subraddot=subraddot).count()

def check_trophies(user, trophy_name=None, subraddot=None):
    # verifier si l'utilisateur a le trophee
    # appeller la fonction de vérification du trophée
    check_first_post(user)
    check_five_post(user)


def check_first_post(user):
    if not Trophy.objects.filter(user=user, name='First post').exists():
        posts_count = user.posts.count()
        print(f"{posts_count} posts found")
        if posts_count >= 1:
            Trophy.objects.create(
                user=user,
                subraddot=None,
                name='1er poste',
                icon='trophy/first_post.png',
                description='Vous avez posté votre premier message !',
            )


def check_five_post(user):
    if not Trophy.objects.filter(user=user, name='Five post').exists():
        posts_count = user.posts.count()
        if posts_count >= 5:
            Trophy.objects.create(
                user=user,
                subraddot=None,
                name='5e poste',
                icon='trophy/five_post.png',
                description='Vous avez posté 5 messages !',
            )
