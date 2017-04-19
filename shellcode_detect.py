#!/usr/bin/env python2
# Simple Shellcode detector using the libemu API.
# Can be used as a naïve but still solid basis IDS for testing purpose.
# Needs to be run as a daemon.
# TODO: adding self recognition of encoded shellcodes.

__author__:'''
[Cs133]
Twit: @133_cesium
'''

import sys
import pylibemu
import datetime
import time

file_log = "/tmp/shellcode-detector.log"    # Put the chosen log file path here
buffer = ""

for line in sys.stdin.readlines():
  buffer += line

print "[+] Testing buffer of size %dB ..." % (len(buffer))

emulator = pylibemu.Emulator()
offset = emulator.shellcode_getpc_test(buffer)

if offset >= 0:
  print "[+] Shellcode I Catch You !"
  emulator.prepare(buffer, offset)
  emulator.test()
  print emulator.emu_profile_output
  
  with open(file_log, "a+") as logger:
    logger.write("[+] New shellcode detected; " + time.strftime(str(datetime.datetime.now())))
    logger.write("Offset=" + offset)
    logger.write("Shellcode=" + bytearray(buffer))
    logger.write(emulator.emu_profile_output)

else:
  print "[-] Nothing here, sir"
  
  with open(file_log, "a+") as logger:
    logger.write("[~] Input; " + time.strftime(str(datetime.datetime.now())))
    logger.write("Offset=" + offset)
    logger.write("Input detected=" + bytearray(buffer))
  
  # /!\ /!\ /!\
  emulator.run()  # Could be devastating in case of home built encoded shellcodes.
