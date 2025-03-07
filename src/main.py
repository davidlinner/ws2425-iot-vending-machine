import vending_machine.qr as qr
import time

from vending_machine.inventory import load_inventory
from vending_machine.shop import get_pickup, start_pickup, finish_pickup
from signal import pause

import vending_machine.locker as locker


_current_code = None


def _switch_locker_state(state: bool):
    global _current_code
    if state:
        print(f'Locker is opened for {_current_code}')
        if not start_pickup(_current_code):
            print('failed to change status to started')
    else:
        print(f'Locker is closed for {_current_code}')
        if not finish_pickup(_current_code):
            print('failed to change status to finished')
        _current_code = None

def _process_code(code):
    global _current_code
    if locker.any_door_open():
        print("locker is busy. doing nothing.")
        return

    _current_code = code

    pickup = get_pickup(code)
    inventory = load_inventory()

    for item in pickup.items:
        if item.required < 1:
            continue

        gtin = item.product.gtin

        box_to_open = inventory.stock[gtin].box

        print("opening box:", box_to_open)
        locker.open_box(box_to_open)


def main():

    scanner = qr.QR()
    scanner.start(_process_code)
    monitor = locker.LockerMonitor()
    monitor.start(_switch_locker_state)


    print("Press any key to stop scanning...")
    # input()
    pause()
    scanner.stop()
    monitor.stop()


if __name__ == '__main__':
    main()
