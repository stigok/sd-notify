"""
Simple sd_notify(3) client functionality implemented in Python 3.

Usage:
```
notif = SdNotify()
if not notif.enabled():
    raise Exception("Watchdog not enabled")

notif.status("Starting things up...")
time.sleep(3)

notif.ready() # Init complete
notif.status("Waiting for requests...")
time.sleep(3)

notif.notify_error("Making the program quit with error!")
# systemd will kill the program here
time.sleep(3)
```

Author: stig@stigok.com Dec 2019
"""
import os
import socket

class Notifier():
    def __init__(self, *, sock=None, addr=None):
        self.socket = sock or socket.socket(family=socket.AF_UNIX,
                                            type=socket.SOCK_DGRAM)
        self.address = addr or os.getenv("NOTIFY_SOCKET")

    def _send(self, msg):
        """Send string `msg` as bytes on the notification socket"""
        self.socket.sendto(msg.encode(), self.address)

    def enabled(self):
        """Return a boolean stating whether watchdog is enabled"""
        return bool(self.address)

    def ready(self):
        """Report ready service state, i.e. completed initialisation"""
        self._send("READY=1\n")

    def status(self, msg):
        """Set a service status message"""
        self._send("STATUS=%s\n" % (msg,))

    def notify(self):
        """Report a healthy service state"""
        self._send("WATCHDOG=1\n")

    def notify_error(self, msg=None):
        """
        Report a watchdog error. This program will likely be killed by the
        service manager.

        If `msg` is not None, it will be reported as an error message to the
        service manager.
        """
        if msg:
            self.status(msg)

        self._send("WATCHDOG=trigger\n")
