from collections import defaultdict

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
    def __init__(self, trophies, subraddot=None, show_subraddot_titles=True):
        self.trophies = trophies
        self.subraddot = subraddot
        self.show_subraddot_titles = show_subraddot_titles

    def get_context(self):
        if self.subraddot:
            filtered_trophies = [t for t in self.trophies if t.subraddot == self.subraddot]
            return {
                'trophy_groups': [
                    {
                        'subraddot': self.subraddot if self.show_subraddot_titles else None,
                        'trophies': filtered_trophies
                    }
                ],
                'show_subraddot_titles': self.show_subraddot_titles,
            }
        else:
            # Organiser par groupes
            trophy_groups = []

            # Grouper les trophées par subraddot
            grouped_trophies = defaultdict(list)
            for trophy in self.trophies:
                grouped_trophies[trophy.subraddot].append(trophy)

            # trophées généraux (subraddot=None)
            if None in grouped_trophies:
                trophy_groups.append({
                    'subraddot': None,
                    'trophies': grouped_trophies[None]
                })

            subraddots_with_trophies = [sub for sub in grouped_trophies.keys() if sub is not None]
            subraddots_with_trophies.sort(key=lambda x: len(grouped_trophies[x]), reverse=True)
            subraddots_with_trophies = subraddots_with_trophies[:4]  # Limiter à 4 subraddots

            for subraddot in subraddots_with_trophies:
                trophy_groups.append({
                    'subraddot': subraddot,
                    'trophies': grouped_trophies[subraddot]
                })

            return {
                'trophy_groups': trophy_groups,
                'show_subraddot_titles': self.show_subraddot_titles,
            }
