import os
from unittest import TestCase
from unittest.mock import Mock, patch, sentinel

from sd_notify import Notifier


class NotifierTestCase(TestCase):
    def test_send(self):
        cut = Notifier(sock=Mock(spec=["sendto"]), addr=sentinel.address)
        cut._send("Hello, world!")
        cut.socket.sendto.assert_called_once_with(b"Hello, world!", sentinel.address)

    def test_enabled(self):
        # With no environment set
        with patch("os.getenv", return_value=None) as getenv_mock:
            cut = Notifier(sock=Mock(spec=["sendto"]))
            res = cut.enabled()
            getenv_mock.assert_called_once_with("NOTIFY_SOCKET")
            self.assertIs(res, False)

        # With empty string set
        with patch("os.getenv", return_value="") as getenv_mock:
            cut = Notifier(sock=Mock(spec=["sendto"]))
            res = cut.enabled()
            getenv_mock.assert_called_once_with("NOTIFY_SOCKET")
            self.assertIs(res, False)

        # With environment set
        with patch("os.getenv", return_value="a string") as getenv_mock:
            cut = Notifier(sock=Mock(spec=["sendto"]))
            res = cut.enabled()
            getenv_mock.assert_called_once_with("NOTIFY_SOCKET")
            self.assertIs(res, True)

    def test_ready(self):
        cut = Notifier(sock=Mock(spec=["sendto"]), addr=sentinel.address)
        with patch('sd_notify.Notifier._send') as patched_send:
            cut.ready()
            patched_send.assert_called_once_with("READY=1\n")

    def test_status(self):
        cut = Notifier(sock=Mock(spec=["sendto"]), addr=sentinel.address)
        with patch('sd_notify.Notifier._send') as patched_send:
            cut.status("Hello, world!")
            patched_send.assert_called_once_with("STATUS=Hello, world!\n")

    def test_notify(self):
        cut = Notifier(sock=Mock(spec=["sendto"]), addr=sentinel.address)
        with patch('sd_notify.Notifier._send') as patched_send:
            cut.notify()
            patched_send.assert_called_once_with("WATCHDOG=1\n")

    def test_notify_error(self):
        cut = Notifier(sock=Mock(spec=["sendto"]), addr=sentinel.address)
        with patch('sd_notify.Notifier._send') as patched_send:
            # Without msg arg
            cut.notify_error()
            patched_send.assert_called_once_with("WATCHDOG=trigger\n")

    def test_notify_error_with_message(self):
        cut = Notifier(sock=Mock(spec=["sendto"]), addr=sentinel.address)
        with patch('sd_notify.Notifier._send') as patched_send:
            cut.notify_error(msg="Hello world!")
            self.assertEqual(patched_send.call_count, 2)
            patched_send.assert_any_call("WATCHDOG=trigger\n")
            patched_send.assert_any_call("STATUS=Hello world!\n")
