#!/usr/bin/python
# coding: utf-8

import time
import signal, ctypes
ucrtbase = ctypes.CDLL('ucrtbase')
c_raise = ucrtbase['raise']
foo = lambda *a: print('foo')
signal.signal(signal.SIGABRT, foo)

c_raise(signal.SIGABRT)

def printer(signal, stek):
    """
    Обработчик таймера
    """
    print(signal)


# Назначаем обработчик сигналу таймера
#signal.signal(signal.SIGUSR1, printer)

# Посылаем сигнал таймера через 2 секунды
# signal.alarm(2)

# Посылаем сигнал таймера через 10 сек. с переодичностью 2 сек.
#signal.setitimer(signal.ITIMER_REAL, 10, 2)

# заглушка
while True:
    time.sleep(0.1)