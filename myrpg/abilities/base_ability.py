from abc import abstractmethod

class BaseAbility:
    def __init__(self, animation_manager):
        self.animation_manager = animation_manager

    @abstractmethod
    def on_cast(self, player, groups, **kwargs):
        if 'cost' in kwargs:
            self.cost = kwargs['cost']
        if 'strength' in kwargs:
            self.strength = kwargs['strength']

    def set_animation_manager(self, animation_manager):
        self.animation_manager = animation_manager