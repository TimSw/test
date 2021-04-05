from time import sleep, time
import threading


class Numbers(object):
    def __init__(self, numbers):
        self.data = numbers
        self.lastUpdate = time()


class SimpleUpdater(object):
    def __init__(self):
        self.i = 5
        self.updateDelta = 5
        self.numbers = Numbers(list(range(self.i)))
        self._start_update_thread()

    def _start_update_thread(self):
        # Only call this function once
        update_thread = threading.Thread(target=self._update_loop)
        update_thread.daemon = True
        update_thread.start()

    def _update_loop(self):
        print("Staring Update Thread")
        while True:
            self.update_numbers()
            sleep(.001)

    def update_numbers(self):
        numbers = self.numbers
        delta = time() - numbers.lastUpdate
        if delta < self.updateDelta:
            return
        print('Starting Update')
        # artificial calculation time
        sleep(4)
        numbers = Numbers(list(range(self.i)))
        self.numbers = numbers
        print('Done Updating')

    def run_counter(self):
        # Take self.numbers once, then only use local `numbers`.
        numbers = self.numbers
        for j in numbers.data:
            print(j)
            sleep(0.5)
        # do more with numbers
        self.i += 1


if __name__ == '__main__':
    S = SimpleUpdater()
    while True:
        S.run_counter()
