import pygame

from myrpg.weapons.weapon_factory import WeaponFactory
from myrpg.abilities.ability_factory import AbilityFactory
from myrpg.base_settings import *
from myrpg.player import MyRPGPlayer

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, size=UI_FONT_SIZE)

        self.health_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 35, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_surfaces = {}
        for weapon in WeaponFactory.WEAPONS.keys():
            self.weapon_surfaces[weapon] = pygame.image.load(WeaponFactory.WEAPONS[weapon].graphic).convert_alpha()

        self.ability_surfaces = {}
        for ability in AbilityFactory.ABILITIES:
            self.ability_surfaces[ability] = pygame.image.load(AbilityFactory.get_ability_graphic(ability)).convert_alpha()

    def show_bar(self, current_amount, max_amount, bg_rect, colour):
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)
        ratio = current_amount / max_amount
        current_amount_width = bg_rect.width * ratio
        current_amount_rect = bg_rect.copy()
        current_amount_rect.width = current_amount_width
        text_surface = self.font.render(f"{int(current_amount)}/{max_amount}", False, TEXT_COLOUR)
        pygame.draw.rect(self.display_surface, colour, current_amount_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)
        text_rect = text_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(text_surface, text_rect)
        

    def show_xp(self, xp):
        text_surface = self.font.render(str(int(xp)), False, TEXT_COLOUR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, text_rect.inflate(20, 20), 3)

    def show_selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOUR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_ACTIVE_COLOUR, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOUR, bg_rect, 3)
        return bg_rect

    def show_weapon_overlay(self, weapon_entry, has_switched_weapons):
        bg_rect = self.show_selection_box(10, 550, has_switched_weapons)
        weapon_surface = self.weapon_surfaces[weapon_entry.codename]
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def show_ability_overlay(self, ability_entry, has_switched_abilities):
        bg_rect = self.show_selection_box(60, 550, has_switched_abilities)
        ability_surface = self.ability_surfaces[ability_entry.codename]
        ability_rect = ability_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(ability_surface, ability_rect)

    def display(self, player: MyRPGPlayer):
        self.show_bar(player.health, player.stats['MaxHealth'], self.health_bar, HEALTH_COLOUR)
        self.show_bar(player.energy, player.stats['MaxEnergy'], self.energy_bar, ENERGY_COLOUR)
        self.show_xp(player.total_xp)
        self.show_weapon_overlay(player.weapon, not player.can_switch_weapons)
        self.show_ability_overlay(player.ability_entry, not player.can_switch_abilities)
        
