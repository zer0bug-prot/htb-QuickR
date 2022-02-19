import struct
from telnetlib import Telnet

from PIL import Image
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol

if __name__ == '__main__':
    tn = Telnet('178.62.5.61', 30611)

    input_str = tn.read_until(b'string:').decode('utf-8')
    qr_code = input_str[548:]
    # print(qr_code)
    qr_code_binary = qr_code.replace(' ', '')
    qr_code_binary = qr_code_binary.replace('\x1B[7m', '1,').replace('\x1B[0m', '')
    qr_code_binary = qr_code_binary.replace('\x1B[41m', '0,')
    qr_code_binary = qr_code_binary[0:qr_code_binary.index('\t\n')].replace('\t', '')
    qr_code_binary = qr_code_binary + ('0,' * 51) + '\n'
    qr_code_binary = qr_code_binary[:-2]
    print(qr_code_binary)
    rows = qr_code_binary.count('\n')
    # print(rows)
    qr_code_binary_arr = qr_code_binary.replace('\n', '').split(',')
    # print(qr_code_binary_arr)

    size = 51, rows
    arr_size = len(qr_code_binary_arr)
    # print(arr_size)
    data = struct.pack('B' * arr_size, *[int(pixel) * 255 for pixel in qr_code_binary_arr])
    img = Image.frombuffer('L', size, data)
    img.save('img.png')
    img.close()

    im = Image.open("img.png")
    qr_out = decode(im, symbols=[ZBarSymbol.QRCODE])
    qr_data = qr_out[0].data.decode("utf-8").replace('=', '').replace('x', '*')
    print(qr_data)
    qr_result = str(eval(qr_data)).encode('utf-8')
    print(qr_result)
    tn.write(qr_result + b'\n')
    print(tn.read_all().decode('utf-8'))
