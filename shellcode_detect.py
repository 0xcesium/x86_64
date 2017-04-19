#!/usr/bin/env python2
#
# Simple Shellcode detector using the libemu API
#

import sys
import pylibemu

buffer = ""
for line in sys.stdin.readlines():
  buffer += line

print "[+] Testing buffer of fize %dB ..." % (len(buffer))

emulator = pylibemu.Emulator()
offset = emulator.shellcode_getpc_test(buffer)

if offset >= 0:
  print "[+] Shellcode I Catch You !"
  emulator.prepare(buffer, offset)
  emulator.test()
  print emulator.emu_profile_output
else:
  print "[-] Nothing here, sir"
