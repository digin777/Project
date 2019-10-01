import datetime as dt
import time
from threading import Thread

global count


def newalaram(tme, count):
    while 1:
        current = str(dt.datetime.now().time())
        current = current[:5]
        if current == tme:
            print("POPUP ALARM")
            print("Alarm - " + str(count) + " scoped")
            break


def setalaram(h, m):
    count = 0
    tme = str(dt.time(h, m, 0))
    tme = tme[:5]
    try:
        count += 1
        t = Thread(target=newalaram, args=(tme, count,), daemon=True)
        t.start()
        time.sleep(5)
        print("Alarm Seted")
        # t.join()

    except Exception as e:
        print(" Unable to set Alarm", e.args)


if __name__ == '__main__':
    main()
