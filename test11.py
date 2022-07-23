import time
import sys

import termuxgui as tg


with tg.Connection() as c:
    
    a = tg.Activity(c, dialog=True)
    
    l = tg.LinearLayout(a)
    
    t = tg.TextView(a, "Enter Transaction", l)
    t.settextsize(40)
    
    # s = tg.Spinner(a, l)
    # s.setlist(("a","b","c"))
    
    # rg = tg.RadioGroup(a, l)
    # r1 = tg.RadioButton(a, "RadioButton 1", rg)
    # r2 = tg.RadioButton(a, "RadioButton 2", rg)
    # r3 = tg.RadioButton(a, "RadioButton 3", rg)
    
    # tb = tg.ToggleButton(a, l, checked=True)
    # sw = tg.Switch(a, "Switch 1", l)
    
    # cb = tg.Checkbox(a, 'CB', l)

    ed = tg.EditText(a, '', l, singleline=False, line=True, blockinput=False, inputtype='text')
    print(ed.gettext())
    
    for ev in c.events():
        print(ev.type, ev.value)
        if ev.type == "destroy":
            sys.exit()
    print(ed)
