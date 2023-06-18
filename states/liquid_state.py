from aiogram.utils.helper import Helper, HelperMode, ListItem


class LiquidStates(Helper):
    mode = HelperMode.snake_case

    WATER = ListItem()
    TEA = ListItem()
    COFFEE = ListItem()
    JUICE = ListItem()
    MILK = ListItem()
    ALCOHOL = ListItem()
    SPARKLINH_WATER = ListItem()