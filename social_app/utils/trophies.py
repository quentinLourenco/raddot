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

def check_trophies(user, subraddot=None):
    return


def check_first_post(user):
    if not Trophy.objects.filter(user=user, name='1er poste').exists():
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
    if not Trophy.objects.filter(user=user, name='5e poste').exists():
        posts_count = user.posts.count()
        if posts_count >= 5:
            Trophy.objects.create(
                user=user,
                subraddot=None,
                name='5e poste',
                icon='trophy/five_post.png',
                description='Vous avez posté 5 messages !',
            )


def check_first_subraddot(user):
    if not Trophy.objects.filter(user=user, name='1er subraddot').exists():
        subraddots_count = user.created_subraddots.count()
        if subraddots_count >= 1:
            Trophy.objects.create(
                user=user,
                subraddot=None,
                name='1er subraddot',
                icon='trophy/first_subraddot.png',
                description='Vous avez créé votre premier subraddot !',
            )


def check_five_subraddot(user):
    if not Trophy.objects.filter(user=user, name='5e subraddot').exists():
        subraddots_count = user.created_subraddots.count()
        if subraddots_count >= 5:
            Trophy.objects.create(
                user=user,
                subraddot=None,
                name='5e subraddot',
                icon='trophy/five_subraddot.png',
                description='Vous avez créé votre 5e subraddot !',
            )


def check_subraddot_first_post(user, subraddot):
    if not Trophy.objects.filter(user=user, subraddot=subraddot, name='1ere contrib').exists():
        posts_count = user.posts.filter(subraddot=subraddot).count()
        if posts_count >= 1:
            Trophy.objects.create(
                user=user,
                subraddot=subraddot,
                name='1ere contrib',
                icon='trophy/sub_first_post.png',
                description='Vous avez posté votre premier message dans ce subraddot !',
            )


def check_subraddot_five_post(user, subraddot):
    if not Trophy.objects.filter(user=user, subraddot=subraddot, name='sub:five post').exists():
        posts_count = user.posts.filter(subraddot=subraddot).count()
        if posts_count >= 5:
            Trophy.objects.create(
                user=user,
                subraddot=subraddot,
                name='5e contrib',
                icon='trophy/sub_five_post.png',
                description='Vous avez posté votre 5e message dans ce subraddot !',
            )
