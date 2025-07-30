from django import template

from social_app.components import SidebarNavComponent, SidebarItemComponent

register = template.Library()

@register.inclusion_tag('social_app/components/sidebar_nav.html', takes_context=True)
def render_sidebar_nav(context):
    user = context['user']
    sidebar = SidebarNavComponent(user)
    ctx = sidebar.get_context()
    return ctx

@register.inclusion_tag('social_app/components/sidebar_item.html', takes_context=True)
def render_sidebar_item(context, subraddot):
    sidebar_item = SidebarItemComponent(subraddot)
    return sidebar_item.get_context()