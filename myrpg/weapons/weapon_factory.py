from myrpg.weapons.swords import *
from myrpg.weapons.piercers import *
from myrpg.weapons.smaller_weapons import *

class WeaponFactory:
    WEAPONS = {
        'RecruitsSword': RecruitsSword,
        'BloodSword': BloodSword,

        'WoodenLance': WoodenLance,
        
        'Sai': Sai
    }

    @staticmethod
    def get_weapon(weapon_name, *params):
        return WeaponFactory.WEAPONS[weapon_name]
    
    @staticmethod    
    def get_weapon_by_index(index, *params):
        return WeaponFactory.WEAPONS[list(WeaponFactory.WEAPONS.keys())[index]]
    
    @staticmethod    
    def get_weapon_count():
        return len(WeaponFactory.WEAPONS)
    
    @staticmethod    
    def get_weapon_graphic(weapon_name):
        return WeaponFactory.WEAPONS[weapon_name].graphic