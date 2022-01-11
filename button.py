class Button:
    def __init__(self, image, position, callback):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback

    def onClick(self, event):
        """
        Call the callback function if the button is left-clicked.

        :param event: the last pygame.event (should always be a mouse click)
        """
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
