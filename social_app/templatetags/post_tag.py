from django import template

register = template.Library()

@register.inclusion_tag('social_app/components/post.html')
def render_post(post, on_subhomepage=False):
    return {
        'post': post,
        'on_subhomepage': on_subhomepage,
    }
