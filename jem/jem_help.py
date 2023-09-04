""" jem_help.py
    Prints out the example code in each jem module / driver if available

    To have jem_help find example code, add your example to py file like this:
    if __name__ == "__main__":
        # your example code heartbeat

    jem_help.py will find this code and print to terminal if user selects help
    for that module or driver or general python file

    ex:
    >> jem_help(jemled)
    # example code in jemled.py
    import time
    led = JemLed()

    red = 0xFF0000
    print("turn on led")
    led.set_color(red) # set color to red
    print("sleep")
    time.sleep(3) # wait 3 seconds
    print("turn off led")
    led.off() # turn off the led
"""
JEM_HELP_MAP = {
                'jemimu': None, 'jemled': None, 'jem': None, 'jembarometer': None, \
                'jemlight': None, 'jemrange': None, \
                'jembuzzer': None, 'jembattery': None, 'jemwifi': None
                }

def jem_help_get_all():
    for k in JEM_HELP_MAP:
        ex_code = jem_help_get(k)
        JEM_HELP_MAP[k] = ex_code # save so we don't do this again
    return JEM_HELP_MAP

def jem_help(file_name=None):
    """ prints out the example code in the file_name python file"""
    if not file_name:
        print("\n# example using jem_help:\n")
        for k in JEM_HELP_MAP:
            ex_help = "jem_help('%s')" % k
            print(ex_help)
        return

    try:
        if file_name in JEM_HELP_MAP and JEM_HELP_MAP[file_name]:
            ex_code = JEM_HELP_MAP[file_name] # already saved ex from prev read
        else:
            ex_code = jem_help_get(file_name)
            if file_name in JEM_HELP_MAP:
                JEM_HELP_MAP[file_name] = ex_code # save so we don't do this again
        print(ex_code)
    except Exception as e:
        print("jem_help(%s) failed: %s" % (file_name, e))

def jem_help_get(file_name):
    try:
        ex_code = "\n# %s: example code \n" % file_name
        py_file = file_name + ".py"
        with open(py_file, "r") as f: # opens and then closes file after done
            d = f.read()
            match_str = 'if __name__ == "__main__":'
            str_len = len(match_str)
            i = d.find(match_str)
            if i >= 0:
                ex_code += d[i + str_len:]
    except Exception as e:
        print("jem_help_get failed: %s" % e)

    return ex_code

if __name__ == "__main__":
    ex = jem_help("jemled")
    print(ex)
