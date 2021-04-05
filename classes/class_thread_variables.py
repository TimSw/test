#!/usr/bin/python3
import threading
import time


class ImportData:
    print("enter ImportData")
    var_1 = 0
    print("var_1 = ", var_1)

    def __init__(self):
        print("enter init ImportData")

    def get_data(self):
        print("enter get_data")
        while True:
            try:
                ImportData.var_1 = input("ImportData in loop = \n")
                print("ImportData in loop = ", ImportData.var_1)
            except Exception as e:
                print(e)

    def run(self):
        print("enter run get_data")
        thread_1 = threading.Thread(target=self.get_data)
        thread_1.start()


class ProcessData:
    print("enter ProcessData")

    def __init__(self):
        print("enter init ProcessData")

    def process_data(self):
        print("enter process_data")
        counter = 0
        # data = ImportData.var_1
        print("counter = ", counter)
        while True:
            try:
                print("ImportData.var_1 = ", ImportData.var_1)
                counter = counter + 1
                print("counter = ", counter)
                time.sleep(5)
            except Exception as e:
                print(e)

    def run(self):
        print("enter run process_data")
        thread_1 = threading.Thread(target=self.process_data, daemon=True)
        thread_1.start()


if __name__ == "__main__":
    print("enter __main__")

    imports = ImportData()
    imports.run()
    pd = ProcessData()
    pd.run()
