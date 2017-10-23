import struct
from collections import namedtuple
from random import randint


def decoder(data):

    """ Декодируем данные транзакции из строки вида b'zz0x23270x14eb0x000x020xd30x230x2d'
    """
    transaction_rcvd = struct.unpack('!2s6s6s4s4s4s4s4s', data)

    Transaction = namedtuple('Transaction',
                             ('tr_header', 'tr_date', 'tr_time', 'tr_type', 'tr_data', 'tr_transaction_id',
                              'partner_id', 'payment'))
    data = Transaction(*transaction_rcvd)

    # дата
    trdate = int(data.tr_date, 16)
    tr_year = (trdate & 0xfe00) >> 9
    tr_month = (trdate & 0x1e0) >> 5
    tr_day = (trdate & 0x1f) & 31
    tr_decoded_date = '20{}-{}-{} '.format(tr_year, tr_month, tr_day)

    # время
    trtime = int(data.tr_time, 16)
    tr_hour = (trtime & 0x1f000) >> 12
    tr_min = (trtime & 0xfc0) >> 6
    tr_sec = trtime & 0x3f
    # tr_decoded_time = tr_hour * 3600 + tr_min * 60 + tr_sec  # + 10800 for Moscow

    datetime = '{} {}:{}:{}'.format(tr_decoded_date, tr_hour, tr_min, tr_sec)

    # id транзакции
    tr_transaction_id = int(data.tr_transaction_id, 16)

    # тип транзакции
    tr_type = tr_data = str
    if data.tr_type == b'0x00':
        tr_type = 'сервисная транзакция'
    else:
        pass

    # данные транзакции
    if data.tr_data == b'0x00':
        tr_data = 'включение'
    elif data.tr_data == b'0x01':
        tr_data = 'перезагрузка'
    elif data.tr_data == b'0x02':
        tr_data = 'выключение'
    elif data.tr_data == b'0x03':
        tr_data = 'активация датчика X'
    elif data.tr_data == b'0x04':
        tr_data = 'блокировка, требуется инкассация'

    # id терминала
    terminal_id = randint(111, 999)

    partner_id = int(data.partner_id, 16)
    partner_name = "emobi"
    payment = int(data.payment, 16)
    cmnt = 'cmnt'

    data_deco = (datetime, terminal_id, tr_transaction_id, tr_type, tr_data, partner_id, partner_name, payment, cmnt)

    Trans_deco = namedtuple('Trans_deco', ('datetime', 'terminal_id', 'tr_transaction_id',
                                           'tr_type', 'tr_data', 'partner_id',
                                           'partner_name', 'payment', 'cmnt'))

    data_decoded = Trans_deco(*data_deco)

    return data_decoded
