from myrpg.abilities.flame import *
from myrpg.abilities.support import *
from myrpg.abilities.warrior import *

class AbilityFactory:
    ABILITIES = {
        # Flame abilities
        'Fireball': Fireball(None),

        # Support abilities
        'FirstAid': FirstAid(None),

        # Warrior abilities:
        'WarriorsResolve': WarriorsResolve(None)
    }

    @staticmethod
    def get_ability(ability_name, *params):
        return AbilityFactory.ABILITIES[ability_name]
    
    @staticmethod
    def get_ability_by_index(index, *params):
        return AbilityFactory.ABILITIES[list(AbilityFactory.ABILITIES.keys())[index]]
    
    @staticmethod
    def get_ability_count():
        return len(AbilityFactory.ABILITIES)
    
    @staticmethod
    def get_ability_graphic(ability_name):
        return AbilityFactory.ABILITIES[ability_name].graphic
    
    @staticmethod
    def set_animation_manager(animation_manager):
        for ability in AbilityFactory.ABILITIES:
            AbilityFactory.ABILITIES[ability].set_animation_manager(animation_manager)