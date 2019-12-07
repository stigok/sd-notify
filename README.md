# sd_notify

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

## Reference
### `<class 'sd_notify.Notifier'>`
#### `_send(msg)`
Send string `msg` as bytes on the notification socket

#### `enabled()`
Return a boolean stating whether watchdog is enabled

#### `notify()`
Report a healthy service state

#### `notify_error(msg=None)`
Report a watchdog error. This program will likely be killed by the
service manager.

If `msg` is not None, it will be reported as an error message to the
service manager.

#### `ready()`
Report ready service state, i.e. completed initialisation

#### `status(msg)`
Set a service status message

