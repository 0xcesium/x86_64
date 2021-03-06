#!/usr/bin/env python2
#-*- coding:utf-8 -*-

__author__='''
[Cs133]
Twitter: @133_cesium
'''
__license__='''
<+> Under the terms of the GPL v3 License.
'''
__description__='''
Simple Shellcode detector using the libemu API.
Can be used as a naive but still solid basis IDS for testing purpose.
Could be run as a daemon.

Could potentially feeds logs with false positives sometimes...

TODO: adding self recognition of encoded shellcodes.
'''

import sys
import pylibemu
from time import strftime
from datetime import datetime

file_log = "/tmp/shellcode-detector.log"    # Put the chosen log file path here

def get_ma_time():
  return strftime(str(datetime.now()))

def main():
  buffer = ""
  try:
    for line in sys.stdin.readlines():
      buffer += line

    print "[+] Testing buffer of size %dB ..." % (len(buffer))

    emulator  = pylibemu.Emulator()
    offset    = emulator.shellcode_getpc_test(buffer)

    if offset >= 0:
      print "[+] Shellcode I Catch You !"
      emulator.prepare(buffer, offset)
      emulator.test()

      if emulator.emu_profile_output:
        print emulator.emu_profile_output

      with open(file_log, "a+") as logger:
        logger.write("[+] New shellcode detected @ " + get_ma_time())
        logger.write("\nOffset=" + str(offset))
        logger.write("\nShellcode=" + bytearray(buffer))
        logger.write(emulator.emu_profile_output)

    else:
      print "[*] Modifying offset !"
      offset = 0

      with open(file_log, "a+") as logger:
        logger.write("[~] Input @ " + get_ma_time())
        logger.write("\nOffset=" + str(offset))
        logger.write("\nInput detected=" + bytearray(buffer))

      # /!\ /!\ /!\
      emulator.prepare(buffer, offset)
      emulator.test()

      if emulator.emu_profile_output:
        print emulator.emu_profile_output

      emulator.run(buffer)  # Could be devastating in case of home built encoded shellcodes.

    return 0
 
  except Excepetion as e:
    print '[-] Error: Shellcode emulation failed!\n{}'.format(e.__class__)
    return 1

if __name__ == "__main__":
  sys.exit(main())
