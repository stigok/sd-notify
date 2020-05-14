#!/bin/env python3
import sd_notify
import time

notify = sd_notify.Notifier()

if not notify.enabled():
    # Then it's probably not running is systemd with watchdog enabled
    raise Exception("Watchdog not enabled")

# Report a status message
notify.status("Starting my service...")
time.sleep(1)

# Report that the program init is complete - "systemctl start" won't return until ready() called
notify.ready()
notify.notify()

timeout_half_sec = int(float(notify.timeout) / 2e6)  # Convert us->s and half that
notify.status("Waiting {} seconds (1/2)".format(timeout_half_sec))
time.sleep(timeout_half_sec)
notify.notify()

notify.status("Waiting {} seconds (2/2)".format(timeout_half_sec))
time.sleep(timeout_half_sec)
notify.notify()

count = 0
while not notify.notify_due:
    count += 1
    notify.status("Waiting for notify_due flag: iteration {}".format(count))
    time.sleep(0.1)  # BUSY LOOPS ARE BAD

# Report an error to the service manager
# notify.notify_error("Blowing up on purpose!")
# The service manager will probably kill the program here

notify.status("Simulating hang")
notify.notify()
time.sleep(120)
