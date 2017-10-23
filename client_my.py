import socket
import struct
import random
import datetime
import threading


now = datetime.datetime.now()


def id_gen(int_from=1111, int_to=8888):
    """Генерирует случайное число в заданом диапазоне
       transaction_id
    """
    m = [i for i in range(int_from, int_to)]
    random.shuffle(m)
    return m


ids = id_gen()
try:
    transaction_id = ids.pop()
    print(transaction_id)
except IndexError:
    print('Возможные id для данного диапазона исчерпаны')

# Данные транзакции
tr_header = b'zz'
tr_date = hex(((now.year - 2000 << 9) | (now.month << 5) | (now.day & 31)) & 0xFFFF).encode('utf-8')
tr_time = hex((now.hour << 12) | (now.minute << 6) | (now.second & 60)).encode('utf-8')

# id транзакции
transaction_id = hex(transaction_id).encode('utf-8')

partner_id = 35
partner_id = hex(partner_id).encode('utf-8')
payment = 45
payment = hex(payment).encode('utf-8')
tr_type = '0x00'.encode('utf-8')
data = ['0x00', '0x01', '0x02', '0x03', '0x04']
tr_data = random.choice(data).encode('utf-8')
transaction = struct.pack('!2s6s6s4s4s4s4s4s', b'zz', tr_date, tr_time, tr_type,
                          tr_data, transaction_id, partner_id, payment)
print('transaction =', transaction)




def client(HOST, PORT, transaction):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # HOST, PORT = 'localhost', 9999
        sock.connect((HOST, PORT))
        sock.sendall(transaction)
        print('Данные отправлены')
        recvd = str(sock.recv(1024), 'utf-8')
        print(recvd)


if __name__ == "__main__":

    HOST, PORT = 'localhost', 9999
    client(HOST, PORT, transaction)
    print(threading.current_thread())
    transaction1 = b'zz0x23230x4c040x000x020x200x230x2d'
    client(HOST, PORT, transaction1)
    print(threading.current_thread())
