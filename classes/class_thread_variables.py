#!/usr/bin/python3

if __name__ == '__main__':

    # LightTimer class
    lt = LightTimer()
    lt.run()
    ao = AirstoneOutput()
    ao.run()

    # Threading
    # logger.info("Voor creëren thread process_timers")
    # thread_1 = threading.Thread(target=process_timers, daemon=True)
    # logger.info("Voor creëren thread process_timers")
    # thread_1.start()