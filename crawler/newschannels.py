from enum import Enum, unique


@unique
class NewsChannels(Enum):
    CNN = 'CNN'
    CBNC = 'CNBC'
    NBC = 'NBC'
    REUTERS = 'REUTERS'
    USATODAY = 'USATODAY'
