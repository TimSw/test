#!/usr/bin/python3
import threading
import time


class Eerste:
    var_eerste_voor_init = 0
    print("var_eerste_voor_init = ", var_eerste_voor_init)

    def __init__(self):
        var_eerste_in_init = 0
        print("var_eerste_in_init = ", var_eerste_in_init)

    def eerste_functie(self, var_in):
        var_eerste_functie = 0
        print("var_eerste_functie = ", var_eerste_functie)
        while True:
            try:
                print("var_eerste_functie in loop = ", var_eerste_functie)
                var_eerste_functie = var_eerste_functie + 1
                print("var_tweede_voor_init in loop eerste = ", var_in)
                time.sleep(5)
            except Exception as e:
                print(e)

    def run(self):
        var_run = 0
        print("var_run = ", var_run)
        thread_1 = threading.Thread(target=self.eerste_functie,
                                    args=(Tweede.var_tweede_voor_init, ))
        thread_1.start()


class Tweede:
    var_tweede_voor_init = 0
    print("var_tweede_voor_init = ", var_tweede_voor_init)

    def __init__(self):
        var_tweede_in_init = 0
        print("var_tweede_in_init = ", var_tweede_in_init)

    def tweede_functie(self):
        var_tweede_functie = 0
        print("var_tweede_functie = ", var_tweede_functie)
        while True:
            try:
                print("var_tweede_voor_init in loop = ",
                      self.var_tweede_voor_init)
                self.var_tweede_voor_init = self.var_tweede_voor_init + 1
                time.sleep(5)
            except Exception as e:
                print(e)

    def run(self):
        var_run = 0
        print("var_run = ", var_run)
        thread_1 = threading.Thread(target=self.tweede_functie)
        thread_1.start()


if __name__ == "__main__":
    var_start_main = 0
    print("var_start_main = ", var_start_main)

    e = Eerste()
    e.run()
    t = Tweede()
    t.run()
