from django import template
from social_app.components import TrophyComponent, TrophiesComponent

register = template.Library()

@register.inclusion_tag('social_app/components/trophy.html', takes_context=True)
def render_trophy(context, trophy):
    trophy_component = TrophyComponent(trophy)
    ctx = trophy_component.get_context()
    return ctx

@register.inclusion_tag('social_app/components/trophies.html', takes_context=True)
def render_trophies(context, trophies, subraddot=None):
    trophies_component = TrophiesComponent(trophies, subraddot)
    ctx = trophies_component.get_context()
    return ctx