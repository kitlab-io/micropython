from jem import jemled, jembuzzer

led = jemled.JemLed()


def led_red():
    led.set_color((100, 0, 0))


def led_blue():
    led.set_color((0, 0, 100))


def run():
    print("Demo Kit start, nothing to do except use the mobile App")
