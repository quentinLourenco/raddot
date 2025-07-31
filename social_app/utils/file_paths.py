import hashlib

def get_post_image_path(instance, filename):
    user_hash = hashlib.md5(instance.user.username.encode()).hexdigest()[:10]
    post_hash = hashlib.md5(instance.title.encode()).hexdigest()[:10]
    ext = filename.split('.')[-1] if '.' in filename else ''

    return f'users/{user_hash}/posts/{post_hash}_img.{ext}'

def get_subraddot_icon_path(instance, filename):
    hash_name = hashlib.md5(instance.name.encode()).hexdigest()[:10]
    ext = filename.split('.')[-1] if '.' in filename else ''

    return f'subraddot/{hash_name}/{hash_name}_icon.{ext}'

def get_subraddot_banner_path(instance, filename):
    hash_name = hashlib.md5(instance.name.encode()).hexdigest()[:10]
    ext = filename.split('.')[-1] if '.' in filename else ''

    return f'subraddot/{hash_name}/{hash_name}_banner.{ext}'
