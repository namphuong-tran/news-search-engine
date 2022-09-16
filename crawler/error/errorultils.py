from crawler.newschannels import NewsChannels


def read_error_url(channel):
    f = open(get_file_name(channel), 'r')
    url_list = f.read().splitlines()
    f.close()
    return url_list


def write_error_url(url_list, channel):
    f = open(get_file_name(channel), 'w')
    for url in url_list:
        f.write(url)
        f.write('\n')
    f.close()


def get_file_name(channel):
    if (channel == NewsChannels.CBNC.value):
        return 'error/cnbc.txt'
    if (channel == NewsChannels.CNN.value):
        return 'error/cnn.txt'
    if (channel == NewsChannels.NBC.value):
        return 'error/nbc.txt'
    if (channel == NewsChannels.REUTERS.value):
        return 'error/reuters.txt'
    if (channel == NewsChannels.USATODAY.value):
        return 'error/usatoday.txt'
