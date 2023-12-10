import sys
sys.implementation

import uos
d = uos.uname()
print('board name:', d[4])
print('micropython version:', d[2])
print('\nbuildin modules:')
help('modules')
 
import machine
print('\nsystem freq: {} MHz'.format(machine.freq()//1000000))
 
import gc
print('memory:', gc.mem_free() + gc.mem_alloc())
 
d = uos.statvfs('/')
print('Disk size:')
print('total:', d[0]*d[2])
print('free:', d[0]*d[3])