"""Watchdog: no Brain contact for timeout_s while a task is active →
posture(safe) + stop. Spine-local, works with Wi-Fi down.

The clock is injectable so tests can drive time; run() starts the real
background thread for the daemon.
"""

import threading
import time
from typing import Callable


class Watchdog:
    def __init__(self, timeout_s: float, on_timeout: Callable[[], None],
                 clock: Callable[[], float] = time.monotonic):
        self.timeout_s = timeout_s
        self.on_timeout = on_timeout
        self.clock = clock
        self._last_contact = clock()
        self._active = False        # a task is in flight / robot not parked safe
        self._fired = False
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def touch(self) -> None:
        """Record Brain contact. Any /act arms the watchdog; motion keeps it armed."""
        with self._lock:
            self._last_contact = self.clock()
            self._fired = False

    def set_active(self, active: bool) -> None:
        with self._lock:
            self._active = active

    @property
    def fired(self) -> bool:
        return self._fired

    def check(self) -> bool:
        """Fire on_timeout once if the Brain has gone silent mid-task."""
        with self._lock:
            expired = (self._active and not self._fired
                       and self.clock() - self._last_contact > self.timeout_s)
            if expired:
                self._fired = True
                self._active = False
        if expired:
            self.on_timeout()
        return expired

    def run(self) -> None:
        """Start the background checker thread (daemon use, not tests)."""
        if self._thread is not None:
            return
        self._stop_event.clear()

        def loop():
            while not self._stop_event.wait(min(1.0, self.timeout_s / 4)):
                self.check()

        self._thread = threading.Thread(target=loop, daemon=True,
                                        name="spine-watchdog")
        self._thread.start()

    def shutdown(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None
