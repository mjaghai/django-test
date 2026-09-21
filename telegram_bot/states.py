"""States برای ConversationHandler"""

from enum import Enum


class NewPostState(Enum):
    TITLE = 0
    DESCRIPTION = 1
    CONTENT = 2
    BRAND = 3
    MODEL = 4
    YEAR = 5
    ENGINE = 6
    HORSEPOWER = 7
    PRICE = 8
    CONFIRM = 9
