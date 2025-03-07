from typing import Callable
import cv2
from pyzbar import pyzbar
import threading


class QR:

    def __init__(self):
        self._running = False
        self._thread = None

    def start(self, callback: Callable[[str], None]):
        self._running = True
        self._thread = threading.Thread(target=self.__run, args=(callback,))
        self._thread.start()

    def stop(self):
        if self._running and self._thread:
            self._running = False
            self._thread.join()

    def __run(self, callback: Callable[[str], None]):

        cap = cv2.VideoCapture(0)

        while self._running:
            retval, frame = cap.read()

            if retval:
                decoded_objects = pyzbar.decode(frame)

                for obj in decoded_objects:
                    qr_data = obj.data.decode('utf-8')
                    callback(qr_data)

        cap.release()
