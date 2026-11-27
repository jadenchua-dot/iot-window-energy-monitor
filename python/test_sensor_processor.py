"""Tests for the Raspberry Pi logic, with the serial port and database faked.

Run from the repository root:  python -m unittest discover -s python -v
"""
import sys
import types
import unittest

# The logic doesn't need real hardware: stub the modules if they aren't installed.
for name in ("serial", "pymysql"):
    if name not in sys.modules:
        try:
            __import__(name)
        except ImportError:
            sys.modules[name] = types.ModuleType(name)

import sensor_processor as sp  # noqa: E402


class ParseLine(unittest.TestCase):
    def test_reads_key_and_value(self):
        self.assertEqual(sp.parse_line(b"Time_Limit:30\r\n"), ("Time_Limit", 30.0))
        self.assertEqual(sp.parse_line(b"Window_Status:1\r\n"), ("Window_Status", 1.0))

    def test_ignores_noise(self):
        self.assertIsNone(sp.parse_line(b"\xff\xfe\r\n"))
        self.assertIsNone(sp.parse_line(b"Window_Status:\r\n"))
        self.assertIsNone(sp.parse_line(b""))


class Decide(unittest.TestCase):
    def test_closed_window_resets_the_timer(self):
        self.assertEqual(sp.decide(False, 12, 10), (0, "System Secure", "Alert: OFF", b"L"))

    def test_open_within_the_limit_is_ventilating(self):
        self.assertEqual(sp.decide(True, 4, 10), (5, "Open", "Alert: OFF (Ventilating)", b"L"))

    def test_open_past_the_limit_sounds_the_alarm(self):
        self.assertEqual(sp.decide(True, 10, 10), (11, "Open", "Alert: ON (Time Exceeded!)", b"H"))


class FakeSerial:
    def __init__(self, lines):
        self.lines, self.written, self.closed = list(lines), [], False

    def readline(self):
        if not self.lines:
            raise KeyboardInterrupt  # end of the recording: stop like Ctrl+C
        return self.lines.pop(0)

    def write(self, data):
        self.written.append(data)

    def close(self):
        self.closed = True


class FakeDb:
    def __init__(self):
        self.rows, self.closed = [], False

    def cursor(self):
        return self

    def execute(self, sql, params):
        self.rows.append(params)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        self.closed = True


class MainLoop(unittest.TestCase):
    def test_starts_mid_stream_and_alarms_after_the_limit(self):
        # The capture starts halfway through a line, as it does when the Pi
        # opens the port while the Arduino is already talking.
        port = FakeSerial([b"dow_Status:1\r\n"] +
                          [b"Time_Limit:2\r\n", b"Window_Status:1\r\n"] * 3 +
                          [b"Time_Limit:2\r\n", b"Window_Status:0\r\n"])
        db = FakeDb()
        old_serial = getattr(sp.serial, "Serial", None)
        old_connect = getattr(sp.pymysql, "connect", None)
        sp.serial.Serial = lambda *a, **k: port
        sp.pymysql.connect = lambda **k: db
        try:
            sp.main()
        finally:
            if old_serial is not None:
                sp.serial.Serial = old_serial
            if old_connect is not None:
                sp.pymysql.connect = old_connect

        # open 1 s, 2 s (limit 2), 3 s -> alarm, closed -> off, then off on exit
        self.assertEqual(port.written, [b"L", b"L", b"H", b"L", b"L"])
        self.assertEqual([r[3] for r in db.rows], [
            "Alert: OFF (Ventilating)", "Alert: OFF (Ventilating)",
            "Alert: ON (Time Exceeded!)", "Alert: OFF"])
        self.assertTrue(port.closed and db.closed)


if __name__ == "__main__":
    unittest.main()
