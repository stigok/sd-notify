"""
sd_notify(3) and sd_watchdog_enabled(3) client functionality implemented in Python 3

Usage:
```
import sd_notify

notify = sd_notify.Notifier()
if not notify.is_enabled:
    # Then it's probably not running is systemd with watchdog enabled
        raise Exception("Watchdog not enabled")

# Report a status message
notify.status("Starting my service...")
time.sleep(3)

# Report that the program init is complete
notify.ready()
notify.status("Waiting for web requests...")
notify.notify()
time.sleep(3)

# Compute time between notifications
timeout_half_sec = int(float(notify.timeout) / 2e6)  # Convert us->s and half that
time.sleep(timeout_half_sec)
notify.notify()

# Report an error to the service manager
notify.notify_error("An irrecoverable error occured!")
# The service manager will probably kill the program here
time.sleep(3)
```
"""
from datetime import timedelta, datetime
import os
import socket

class Notifier():
    def __init__(self, sock=None, addr=None):
        self._socket = sock or socket.socket(family=socket.AF_UNIX,
                                             type=socket.SOCK_DGRAM)
        self._address = addr or os.getenv("NOTIFY_SOCKET")
        self._timeout_td = timedelta(0)
        self._lastcall = datetime.fromordinal(1)

        # Note this fix is untested in a live system; https://unix.stackexchange.com/q/206386
        if self._address and self._address[0] == '@':
            self._address = '\0'+self._address[1:]

        # Check for our timeout
        if self._address:
            wtime = os.getenv("WATCHDOG_USEC")
            wpid = os.getenv("WATCHDOG_PID")
            if wtime and wtime.isdigit():
                if wpid is None or (wpid.isdigit() and (wpid == str(os.getpid()))):
                    self._timeout_td = timedelta(microseconds=int(wtime))

    def _send(self, msg):
        """Send string `msg` as bytes on the notification socket"""
        if self.is_enabled:
            self._socket.sendto(msg.encode(), self._address)

    def enabled(self):
        """Return a boolean stating whether watchdog is enabled"""
        return bool(self._address)

    @property
    def is_enabled(self):
        """Property indicating whether watchdog is enabled"""
        return self.enabled()

    def notify(self):
        """Report a healthy service state"""
        self._lastcall = datetime.now()
        self._send("WATCHDOG=1\n")

    @property
    def notify_due(self):
        return (datetime.now() - self._lastcall) >= (self._timeout_td / 2)

    def notify_error(self, msg=None):
        """
        Report a watchdog error. This program will likely be killed by the
        service manager.

        If `msg` is provided, it will be reported as a status message prior to the error.
        """
        if msg:
            self.status(msg)

        self._send("WATCHDOG=trigger\n")

    def ready(self):
        """Report ready service state, i.e. completed initialisation"""
        self._send("READY=1\n")

    @property
    def timeout(self):
        """Report the watchdog window in microseconds as int (cf. sd_watchdog_enabled(3) )"""
        return int(self._timeout_td/timedelta(microseconds=1))

    @property
    def timeout_td(self):
        """Report the watchdog window as datetime.timedelta (cf. sd_watchdog_enabled(3) )"""
        return self._timeout_td

    def status(self, msg):
        """Set a service status message"""
        self._send("STATUS=%s\n" % (msg,))
