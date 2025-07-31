from social_app.views import subraddot


class TrophyComponent:
    def __init__(self, trophy):
        self.trophy = trophy

    def get_context(self):
        return {
            'name': self.trophy.name,
            'icon': self.trophy.icon,
            'description': self.trophy.description,
        }

class TrophiesComponent:
    def __init__(self, trophies, subraddot=None):
        self.trophies = trophies
        self.subraddot = subraddot

    def get_context(self):
        return {
            'trophies': self.trophies,
            'subraddot': self.subraddot,
        }