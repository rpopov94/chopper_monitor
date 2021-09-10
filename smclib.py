import serial
import sys
import glob
import serial.tools.list_ports
from time import time

global ERROR
global ser
ERROR = []


def serial_ports():
    '''
    :return: list comname which connected
    '''
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


block_list = [str(i) for i in range(16)]


def strconvert(response):
    global ERROR
    response = response.decode('utf-8')
    if response != '' and ser.isOpen():
        response = response.split('|')
    else:
        ERROR.append(f'Некоректный ответ с порта {ser.name}')
        return '0'
    return str(int(response[4], 16))


def config():
    '''
    :return: dict of config
    '''
    ld = dict()
    s = []
    with open('config.txt', 'r') as f:
        nums = f.read().splitlines()
    for n in nums:
        s.append(n.split(':'))
    for i in range(len(nums)):
        ld[s[i][1]] = s[i][0]
    return ld


def ch_connect(name):
    '''
    :param name: comname
    :return: true if connect is successful
    '''
    global ser
    global ERROR
    try:
        ser = serial.Serial(
            port=name.upper(),
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=2,
            timeout=0.1,
            writeTimeout=1,
        )
        return True
    except:
        ERROR.append(f'{name} не подключен!')
        return False


def ch_disconnect():
    '''
    close from com port
    '''
    global ERROR
    if ser.isOpen():
        ser.close()
    ERROR.append(f"{ser.name} отключен!")


def command(nblock, register, cmd, data):
    """
    :param nblock: номер блока
    :param register: номер регистра
    :param cmd: команда чтения/запись
    :param data: слово состояния
    """
    global ERROR
    mode = ''
    STX = '%c' % 2
    HSC = '%c' % 0x7c
    bl = '%02x' % nblock
    Reg = '%03x' % register
    if cmd.upper() == 'R':
        mode = '%c' % 0x52
    elif cmd.upper() == 'W':
        mode = '%c' % 0x57
    ENQ = '%c' % 5
    DATA = '%04x' % data
    ETX = '%c' % 3
    request = f'{STX}{HSC}{bl}{HSC}{Reg}{HSC}{mode}{HSC}' \
              f'{DATA}{HSC}{ENQ}{HSC}{ETX}'.encode('utf-8')
    # print('Request is:  ', request)
    ser.write(request)
    mes = ser.readline()
    if mes == b'':
        ERROR.append(f'Блок {bl} не отвечает!')
    return mes


def reply(bl_number):
    '''
    :param bl_number: number of block
    :param com_name: name com port
    :return: dict 16 bit
    '''
    global ERROR
    try:
        if ser.isOpen:
            req = command(int(bl_number), 0, "R", 0)
            req = strconvert(req)
            req = str(bin(int(req)))[2:]
            req = '%016d' % int(req)
            req = list(req)[::-1]
            ch_disconnect()
    except:
            ERROR.append(f'Блок с именем {bl_number} не существует!')
            req = ['0', '0', '0', '0', '0', '0', '0', '0',
                   '0', '0', '0', '0', '0', '0', '0', '0']
    res = dict(firstbit=req[0],
               twobit=req[1],
               threebit=req[2],
               fourbit=req[3],
               fivebit=req[4],
               sixbit=req[5],
               sevenbit=req[6],
               eightbit=req[7],
               ninebit=req[8],
               tenbit=req[9],
               elevenbit=req[10],
               twentybit=req[11],
               thirtybit=req[12],
               fourteenbit=req[13],
               fifteenbit=req[14],
               sixteenbit=req[15],
               bl_number=str(bl_number),
               )
    return res

def online_parameters(block):
    '''функция опроса онлайн параметров'''
    conf = config()
    com_name = conf[block]
    params = [1, 2, 3, 4, 344, 234, 236, 345]
    rep = []
    for p in params:
        # tic = time()
        ch_connect(com_name)
        response = command(int(block), p, 'R', 0)
        req = strconvert(response)
        rep.append(req)
        ch_disconnect()
        # toc = time()
        # print(toc - tic)
    res = dict(
        f=rep[0],
        ts=rep[1],
        tp=rep[2],
        pst=rep[3],
        win=rep[4],
        ps=rep[5],
        psel=rep[6],
        ppst=rep[7],
    )
    # print(toc-tic)
    return res

message = '\n'.join(map(str, ERROR))
