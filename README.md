# sd_notify

Simple sd_notify(3) client functionality implemented in Python 3.

Usage:
```
import sd_notify

notify = sd_notify.Notifier()
if not notify.enabled():
    # Then it's probably not running is systemd with watchdog enabled
    raise Exception("Watchdog not enabled")

# Report a status message
notify.status("Initialising my service...")
time.sleep(3)

# Report that the program init is complete
notify.ready()
notify.status("Waiting for web requests...")
time.sleep(3)

# Report an error to the service manager
notify.notify_error("An irrecoverable error occured!")
# The service manager will probably kill the program here
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

