#!/usr/bin/env python
import os

size  = os.get_terminal_size().columns
for i in range(size- 1) :
    print('-', end = '')
print('-')

message = ['________  ___  ___  ________  ________  _________',   
'|\   ____\|\  \|\  \|\   __  \|\   ____\|\___   ___\ ',
' \ \  \___|\ \  \\\\\  \ \  \|\  \ \  \___|\|___ \  \_| ',
' \ \  \  __\ \   __  \ \  \\\\\  \ \_____  \   \ \  \ ',
'   \ \  \|\  \ \  \ \  \ \  \\\\\  \|____|\  \   \ \  \ ',
'     \ \_______\ \__\ \__\ \_______\____\_\  \   \ \__\ ',
'     \|_______|\|__|\|__|\|_______|\_________\   \|__| ',
'                             \|_________|   ', ' ' ]
msgl = [len(m) for m in message]
if all(l > size for l in msgl):
    message = []


ind = list(range(len(message)))
a = 0
b = 6
if len(message) > b:
    b = len(message)
mstpt = int((b - len(message))/2)
ind  = [x+mstpt for x in ind]

for i in range(b):
    print('|', end = '')
    for ii in range(size -1):
        j = ii + 1
        if ind.count(i) > 0:
            stpt = int((size - len(message[i - mstpt]))/2)
            if j == size - stpt:
                print('\033[38;5;33m' + message[i - mstpt] + '\033[0;0m', end='')
            elif (j > stpt) & (j < stpt + len(message[i - mstpt])):
                a = 0
            elif j == size -1:
                print('|')
            else:
                print(' ', end = '')
        elif j != size - 1:
            print(' ', end = '')
        else:
            print('|')

for i in range(size) :
    print('-', end='')