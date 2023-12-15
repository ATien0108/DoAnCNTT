class Colors:
    dark_grey = (105, 105, 105)
    green = (127, 255, 212)
    red = (255, 0, 0)
    orange = (255, 140, 0)
    yellow = (255, 255, 0)
    purple = (221, 160, 221)
    cyan = (21, 204, 209)
    blue = (30, 144, 255)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    blue_mint = (64, 248, 255)
    navy = (12, 53, 106)
    blue_light = (39, 158, 255)
    green_milk = (213, 255, 208)

    black = (0, 0, 0)
    nude = (244, 223, 200)
    nude_light = (244, 234, 224)
    light = (250, 246, 240)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
    