import vending_machine.qr as qr
import time

from vending_machine.inventory import load_inventory
from vending_machine.shop import get_pickup


def _process_code(code):
    pickup = get_pickup(code)
    inventory = load_inventory()

    for item in pickup['data']['items']:
        gtin = item['product']['gtin']

        box_to_open = inventory.stock[gtin].box

        print("opening box:", box_to_open)


def main():

    scanner = qr.QR()
    scanner.start(_process_code)

    print("Press any key to stop scanning...")
    input()
    scanner.stop()


if __name__ == '__main__':
    main()
