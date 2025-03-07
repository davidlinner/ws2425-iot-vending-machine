import gpiozero
from threading import Timer, Lock
import threading

BOX_PINS = [27, 17]
RELAYS = [gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False) for relay_pin in BOX_PINS]

BUTTON_PINS = [18, 22]
BUTTONS = [gpiozero.Button(button_pin) for button_pin in BUTTON_PINS]

_active_relays = set()
_open_doors = set()
# _callbacks = []

# for index, button in enumerate(BUTTONS):
#     button.when_released = lambda: _door_open(index + 1)
#     button.when_pressed = lambda: _door_close(index + 1)
#
# _lock = Lock()


def any_door_open():
    # state = [not button.is_pressed for button in BUTTONS]
    # print(f"state {any(state)}")
    return any([not button.is_pressed for button in BUTTONS])


class LockerMonitor:
    _is_open = False
    _thread = None
    _is_running = False

    def start(self, callback):
        self._is_running = True
        self._thread = threading.Thread(target=self._run, args=(callback,))
        self._thread.start()

    def _run(self, callback):
        while self._is_running:
            if any_door_open() != self._is_open:
                self._is_open = any_door_open()
                callback(self._is_open)

    def stop(self):
        if self._is_running:
            self._is_running = False
            self._thread.join()

# def _door_open(box_number):
#     global _open_doors
#     global _lock
#
#     with _lock:
#         print("release issued")
#         was_open_before = len(_open_doors) > 0
#         _open_doors.add(box_number)
#
#         if not was_open_before:
#             for callback in _callbacks:
#                 callback(True)
#
#
# def _door_close(box_number):
#     print("close issued")
#     global _open_doors
#     global _lock
#
#     with _lock:
#         if box_number not in _open_doors:
#             return
#         _open_doors.remove(box_number)
#
#         if len(_open_doors) == 0:
#             for callback in _callbacks:
#                 callback(False)


def open_box(box_number):
    global _open_doors
    global _active_relays
    if box_number in _active_relays or box_number in _open_doors:
        return

    door_relay = RELAYS[box_number - 1]
    door_relay.on()
    _active_relays.add(box_number)

    Timer(.2, _close_relay, [box_number]).start()


def _close_relay(box_number):
    global _active_relays
    door_relay = RELAYS[box_number - 1]
    door_relay.off()
    _active_relays.remove(box_number)

