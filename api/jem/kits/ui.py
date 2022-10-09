"""
ui.py: UI classes that user can use to create buttons / sliders ..etc that app with display
ex: led_btn = UI_KitButton(name="LED Toggle", func=button_toggle_led)
ex: slider = UI_KitSlider(name="Slider", func=my_slider, max=100, min=0, start=50)
now app will grab all ui elements using: elements = json.dumps( UI_KitElement.get_all() )
"""
import json

class UI_KitElement():
    BUTTON = 'buttons'
    SLIDER = 'sliders'

    # singletone class
    _elements = [] # we add the button, sliders ..etc class instances here

    @staticmethod
    def get_all():
        elements_dict = { "buttons": [], "sliders": [] }
        for el in UI_KitElement._elements:
            elements_dict[el.ui_type].append(el.get_dict())
        return json.dumps(elements_dict)

    def __init__(self, ui_type, name, func, params=None):
        self.name = name
        self.func = func
        self.params = params
        self.ui_type = ui_type
        UI_KitElement._elements.append(self)

    def get_dict(self):
        func_ptr_name = str(self.func) # ex: '<function test at 0x3f9502e0>'
        end = func_ptr_name.find('at 0x')
        func_name = func_ptr_name[len('<function'):end].rstrip().lstrip()
        d = {"func": func_name, "title": self.name, "params": self.params}
        return d


class UI_KitButton(UI_KitElement):
    def __init__(self, name, func):
        params = {"desc": "this is a button"}
        super(UI_KitButton, self).__init__(ui_type=UI_KitElement.BUTTON, name=name, func=func, params=params)

class UI_KitSlider(UI_KitElement):
    def __init__(self, name, func, max, min, start):
        params = {"desc": "this is a slider", "max": max, "min": min, "value": start}
        super(UI_KitButton, self).__init__(ui_type=UI_KitElement.SLIDER, name=name, func=func, params=params)
