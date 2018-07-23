import minimalmodbus

ser = minimalmodbus.Instrument('COM16', 1, mode='rtu')

# temp = ser.read_register(289, 1)
# def defaultset():
#     ser.bytesize = 8
#     ser.parity = 'N'
#     ser.stopbits = 1
#     ser.timeout = None
#     ser.xonxoff = 0
#     ser.rtscts = 0
#     ser.dsrdtr = False
#     ser.writeTimeout = 0
#     ser.baudrate = 9600
# read = ser.read_registers(738,1,  3)

# print(read)

# read = ser.read_long(512,3, True)
# print(read)
# read = hex(read)
# print(read)

# write = ser.write_float(544, 25.0, 2)
# read = ser.read_float(548, 3, 2)
# read = ser.read_long(516, 3, False)
# a = ser.read_register(576, 0, 3, False)
# b = ser.read_float(528, 3, 2)
# c = ser.read_register(643, 0, 3, False)
# d = ser.write_register(643, 0, 0, 16, False)
# e = ser.read_register(655, 0, 3, False)
# f = ser.write_register(655, 7, 0, 16, False)
# g = ser.read_register(560, 0, 3, False)
# ser.write_register(576, 1, 0, 16, False)
# system_state = ser.read_register(576, 0, 3, False)
output_1 = ser.read_register(560, 0, 3, False)
output_1 = ser.read_register(561, 0, 3, False)
print(output_1)

