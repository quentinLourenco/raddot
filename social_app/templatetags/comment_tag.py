from django import template
from social_app.forms import CreateCommentForm

register = template.Library()

@register.inclusion_tag('social_app/components/create_comment.html', takes_context=True)
def render_create_comment(context, post):
    ctx = context.flatten()
    ctx.update({
        'form': CreateCommentForm(),
        'post': post,
    })
    return ctx

@register.inclusion_tag('social_app/components/comment.html')
def render_comment(comment):
    return {
        'comment': comment,
    }