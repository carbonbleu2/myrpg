GAME_WIDTH = 800
GAME_HEIGHT = 600

FPS = 60
TILE_SIZE = 32

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
ITEM_BOX_SIZE = 40
UI_FONT = 'fonts\\small_pixel.ttf'
UI_FONT_SIZE = 18

WATER_COLOUR = '#71ddee'
UI_BG_COLOUR = '#222222'
UI_BORDER_COLOUR = '#111111'
TEXT_COLOUR = '#eeeeee'

HEALTH_COLOUR = 'red'
ENERGY_COLOUR = 'blue'
UI_BORDER_ACTIVE_COLOUR = 'gold'

WEAPON_DATA = {
    "RecruitsSword": {
        "Name": "Recruit's Sword",
        "Cooldown": 100,
        "Damage": 15,
        "Graphic": "graphics\\weapons\\swords\\RecruitsSword.png",
        "Category": "swords",
        "CodeName": "RecruitsSword"
    },
    "WoodenLance": {
        "Name": "Wooden Lance",
        "Cooldown": 200,
        "Damage": 18,
        "Graphic": "graphics\\weapons\\piercers\\WoodenLance.png",
        "Category": "piercers",
        "CodeName": "WoodenLance"
    },
    "Sai": {
        "Name": "Sai",
        "Cooldown": 50,
        "Damage": 8,
        "Graphic": "graphics\\weapons\\smaller_weapons\\Sai.png",
        "Category": "smaller_weapons",
        "CodeName": "Sai"
    }
}

ABILITY_DATA = {
    "Fireball": {
        "Name": "Fireball",
        "Strength": 5,
        "Cost": 15,
        "Graphic": "graphics\\abilities\\flame\\Fireball.png",
        "Category": "flame",
        "CodeName": "Fireball"
    },
    "FirstAid": {
        "Name": "First Aid",
        "Strength": 20,
        "Cost": 10,
        "Graphic": "graphics\\abilities\\support\\FirstAid.png",
        "Category": "support",
        "CodeName": "FirstAid"
    },
}

ENEMY_DATA = {
    "Blobble": {
        "EnemyID": 0,
        "Name": "Blobble",
        "CodeName": "Blobble",
        "MaxHealth": 100,
        "ExpGain": 50,
        "Damage": 20,
        "AttackType": "Bump",
        "Speed": 2,
        "Resistance": 5,
        "AttackRadius": 10,
        "NoticeRadius": 100
    }
}

ENEMY_ID = {
    0: "Blobble"
} 