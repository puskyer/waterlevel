from OmegaExpansion import onionI2C
import time
import sys

print('Starting: onionI2C module testing...')

i2c 	= onionI2C.OnionI2C(0)

# set the verbosity
i2c.setVerbosity(1)

devAddr = 0x08
addr = 0x0

print("")
if sys.version_info[0] < 3:
    ret = raw_input('  Ready to  write byte / read byte test?')
else:
    ret = input('  Ready to write byte / read byte test?')


# perform write
size 	= 1
value	= [0x01]
print('Writing to device 0x%02x, address: 0x%02x, writing: 0x%02x'%(devAddr, addr, value[0]))
val 	= i2c.writeBytes(devAddr, addr, value)
print('   writeBytes returned: %s'%(val))

# read back the value
size 	= 1
print('Reading from device 0x%02x, address: 0x%02x'%(devAddr, addr))
val 	= i2c.readBytes(devAddr, addr, size)
print('   Read returned: %s'%(val))


print("")
if sys.version_info[0] < 3:
    ret = raw_input('  Ready to  write word / read word test?')
else:
    ret = input('  Ready to write word / read word test?')

# perform write
size 	= 2
value 	= [0x08, 0x01]
print('Writing to device 0x%02x, list is: %s'%(devAddr, value))
val 	= i2c.write(devAddr, value)
print('   write returned: %s'%(val))

# read back the value
size 	= 2
print('Reading from device 0x%02x, address: 0x%02x'%(devAddr, addr))
val 	= i2c.readBytes(devAddr, addr, size)
print('   Read returned: %s'%(val))


print('Done!')


