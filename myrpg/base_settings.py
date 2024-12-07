GAME_WIDTH = 800
GAME_HEIGHT = 600

FPS = 60
TILE_SIZE = 32

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 150
ITEM_BOX_SIZE = 40
UI_FONT = 'fonts\\small_pixel.ttf'
UI_FONT_SIZE = 15

WATER_COLOUR = '#71ddee'
UI_BG_COLOUR = '#222222'
UI_BORDER_COLOUR = '#111111'
TEXT_COLOUR = '#eeeeee'

HEALTH_COLOUR = 'red'
ENERGY_COLOUR = 'blue'
UI_BORDER_ACTIVE_COLOUR = 'gold'

ENEMY_DATA = {
    "Blobble": {
        "EnemyID": 0,
        "Name": "Blobble",
        "CodeName": "Blobble",
        "MaxHealth": 30,
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