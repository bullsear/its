#!/usr/bin/env python
#
#  sshcmd version 0.2. 
#  Answer ssh and scp password queries.
#  Copyright (C) 2000 Peter Åstrand <peter@cendio.se>, Cendio Systems.
#  All rights reserved. 
#
#  This program is free software; you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by 
#  the Free Software Foundation; either version 2 of the License, or 
#  (at your option) any later version.
#
#  You need ExpectPy. Fetch it from:
#  http://starship.python.net/~arcege/ExpectPy/
#
#  Example usage from Python:
#
#  import sshcmd
#  cmdline = "scp /tmp/foofile root@myhost.mydomain.com:/tmp/barfile"
#  sshsess = sshcmd.sshcmd(cmdline)
#  sshsess.login("reallysecret")
#
#  Example usage from shellscript:
#
#  # !/bin/bash
#
#  SSHUSER="root"
#  SSHHOST="myhost.mydomain.com"
#  SSHCMD="/bin/ls"
#  PWFILE=`mktemp ./.XXXXXX`
#
#  trap cleanup 1 2 3 4 5 6 7 8 9 10 11 12 13 15 18 19 20
#  cleanup ()
#  {
#      if [ -e $PWFILE ]; then
#  	rm $PWFILE
#      fi
#      stty echo
#      exit
#  }
#  echo -n "${SSHUSER}@${SSHHOST}'s password: "
#  stty -echo
#  read PW
#  stty echo
#  echo
#  touch $PWFILE
#  chmod 600 $PWFILE
#  echo $PW > $PWFILE
#  ./sshcmd.py $PWFILE ssh ${SSHUSER}@${SSHHOST} ${SSHCMD}
#  cleanup


import os, string, sys
import ExpectPy

class sshcmd:
  def __init__(self, cmdline, verbose=None):
    if verbose is not None:
      ExpectPy.settings.loguser = 1      
    self._fp = apply(ExpectPy.spawn, [None] + string.split(cmdline, " "))
    
  def _send_password(self, match):
    self._fp.send(self.passwd + '\r')
    self._fp.expect((ExpectPy.EXACT, "\r\n", None))

  def _send_yes(self, match):
    self._fp.send("yes" + '\r')
    self._fp.expect((ExpectPy.EXACT, "\r\n", None))
    self._fp.cont()

  def _host_changed(self, match):
    print "Error connecting, got HOST IDENTIFICATION HAS CHANGED!"

  def _connection_error(self, match):
    print "Error connecting, bad hostname?"

  def login(self, password):
    self.passwd = password
    self._fp.expect(
      (ExpectPy.EXACT, "continue connecting (yes/no)?", self._send_yes),
      (ExpectPy.EXACT, "assword:", self._send_password),
      (ExpectPy.EXACT, "HOST IDENTIFICATION HAS CHANGED", self._host_changed),
      (ExpectPy.EXACT, "Bad host name:", self._connection_error),
      (ExpectPy.EXACT, "Name or service not known", self._connection_error),
      )
    tty=ExpectPy.tty_spawn_id
    original_tty_values = tty.stty()
    try:
      tty.stty('-echo', 'raw')
      ExpectPy.settings.timeout = -1
      self._fp.interact((sys.stdin, sys.stdout))
    except EOFError:
      pass
    tty.stty(original_tty_values)

if __name__ == '__main__':
  if len(sys.argv) < 3: 
    print "usage: ", sys.argv[0], " <filename with password> <ssh commandline>"
  else:                                                                       
    f = open(sys.argv[1], "r")
    passwd = string.strip(f.readline())
    f.close()
    cmdline = string.join(sys.argv[2:], " ")
    sshcmd = sshcmd(cmdline)
    sshcmd.login(passwd)







