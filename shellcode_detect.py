#!/usr/bin/env python2
# Simple Shellcode detector using the libemu API.
# Can be used as a naive but still solid basis IDS for testing purpose.
# Needs to be run as a daemon.
# TODO: adding self recognition of encoded shellcodes.

__author__='''
[Cs133]
Twitter: @133_cesium
'''

import sys
import pylibemu
from time import strftime
from datetime import datetime

file_log = "/tmp/shellcode-detector.log"    # Put the chosen log file path here
buffer = ""

def get_ma_time():
  return strftime(str(datetime.now()))

def main():
  try:
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
        logger.write("[+] New shellcode detected @ " + get_ma_time())
        logger.write("\nOffset=" + str(offset))
        logger.write("\nShellcode=" + bytearray(buffer))
        logger.write(emulator.emu_profile_output)

    else:
      print "[-] Nothing here, sir"

      with open(file_log, "a+") as logger:
        logger.write("[~] Input @ " + get_ma_time())
        logger.write("\nOffset=" + str(offset))
        logger.write("\nInput detected=" + bytearray(buffer))

      # /!\ /!\ /!\
      emulator.run(buffer)  # Could be devastating in case of home built encoded shellcodes.

    return 0
  
  except:
    raise
    return 1

if __name__ == "__main__":
  sys.exit(main())
