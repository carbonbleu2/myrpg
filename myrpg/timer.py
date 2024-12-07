import pygame

class AbilityTimer:
    def __init__(self, duration, trigger_on_end, *params):
        self.active = False
        self.start = 0
        self.duration = duration
        self.trigger_on_end = trigger_on_end
        self.trigger_params = params

    def activate(self):
        self.active = True
        self.start = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        self.trigger_on_end(*self.trigger_params)

    def update(self):
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.start >= self.duration:
                self.deactivate()