# sd_notify

sd_notify(3) and sd_watchdog_enabled(3) client functionality implemented in Python 3

## Install
```
$ pip install sd-notify
```
or
```
$ git clone ...
$ make install
```

## Usage

```python
import sd_notify

notify = sd_notify.Notifier()
if not notify.enabled():
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

## Public Reference
### `<class 'sd_notify.Notifier'>`

#### `is_enabled`
Boolean property stating whether watchdog capability is enabled.
Legacy version `enabled()` is also available.

#### `timeout`
Property reporting the number of microseconds (int) before process will be killed.

It is recommended that you call `notify()` once roughly half of this interval has passed (see `notify_due`).

#### `timeout_td`
Property that is the same as `timeout` but presented as `datetime.timedelta` for easier manipulation.

#### `notify_due`
Boolean property indicating more than half of the watchdog interval has passed since last update.

#### `notify()`
Report a healthy service state. Other calls, _e.g._ `status()` do *not* reset the watchdog.

#### `notify_error(msg=None)`
Report an error to the watchdog manager. This program will likely be killed upon receipt.

If `msg` is provided, it will be reported as a status message prior to the error.

#### `ready()`
Report ready service state, _i.e._ completed initialisation (only needed with `Type=notify`)

#### `status(msg)`
Send a service status message.

## Original Author

stig@stigok.com Dec 2019
 * Additional contributors can be found in GitHub repository history

## License

See LICENSE file
