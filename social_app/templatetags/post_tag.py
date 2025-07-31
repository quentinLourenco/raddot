from django import template
from django.db.models import Sum

register = template.Library()

@register.inclusion_tag('social_app/components/post.html')
def render_post(post, on_subhomepage=False):
    comments_count = post.comments.count()
    total_votes = post.votes.aggregate(total=Sum('value'))['total'] or 0
    return {
        'post': post,
        'comments_count': comments_count,
        'on_subhomepage': on_subhomepage,
        'total_votes': total_votes,
    }
