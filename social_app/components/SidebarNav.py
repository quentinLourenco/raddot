class SidebarNavComponent:
    def __init__(self, user):
        self.user = user
        self.created_subraddots = user.created_subraddots.all()
        self.joined_subraddots = user.joined_subraddots.exclude(id__in=self.created_subraddots.values_list('id', flat=True))[:5]

    def get_context(self):
        return {
            'created_subraddots': self.created_subraddots,
            'joined_subraddots': self.joined_subraddots,
        }


class SidebarItemComponent:
    def __init__(self, subraddot):
        self.subraddot = subraddot

    def get_context(self):
        return {
            'name': self.subraddot.name,
            'icon': self.subraddot.icon,
            'url': self.subraddot.get_absolute_url(),
        }