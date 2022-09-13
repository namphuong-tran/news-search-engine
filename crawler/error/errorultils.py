from crawler import channel_name
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
    if (channel == channel_name.CBNC):
        return 'error/cnbc.txt'
    if(channel == channel_name.CNN):
        return 'error/cnn.txt'
    if(channel == channel_name.NBC):
        return 'error/nbc.txt'
    if(channel == channel_name.REUTERS):
        return 'error/reuters.txt'
    if(channel == channel_name.USATODAY):
        return 'error/usatoday.txt'

