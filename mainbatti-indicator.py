#!/usr/bin/env python3
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator

import os
import subprocess
import RoutineReader
import signal
import configUI
import mainbatti_gadget


window = Gtk.Window()
screen = window.get_screen()
parentPath = os.path.dirname(os.path.realpath(__file__))

def update():
    pass

def Update(w):
    u = update()

    if not u:
        dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "Couldn't update")
        dialog.run()
        dialog.destroy()

def OpenMainbattiTalika(w):
    width = 125     # for 24-hr format display width = 160
    height = 26
    scr_w = screen.get_width()
    scr_h = screen.get_height()
    geomstr = str(width) + "x" + str(height) + "+" \
                + str(int(scr_w/2-width*4.28)) + "+" + str(int(scr_h/2 - height*10))

    subprocess.call(["gnome-terminal", "--working-directory="+parentPath, "--geometry="+geomstr, "--title=Mainbatti Talika", "--command=python3 " + os.path.dirname(os.path.realpath(__file__)) + "/mainbatti-talika.py"])

def SettingsChanged():
    if gadget:
        gadget.Refresh()

def Settings(w):
    configUI.ChangeHandler = SettingsChanged
    configUI.main()

def Quit(w):
    Gtk.main_quit()

def ShowGadget(w, i, d):
    if gadget:
        gadget.window.Present()

def GadgetToggle(w):
    global gadget
    if w.get_active():
        gadget = mainbatti_gadget.TalikaGadget()
    else:
        gadget.window.close()
        del gadget

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    config = configUI.LoadConfig()
    if config["Auto-Update"]:
        update()

    os.chdir(parentPath)

    global gadget
    gadget = mainbatti_gadget.TalikaGadget()

    ind = appindicator.Indicator.new_with_path(
                          "Mainbatti-Talika",
                          "mainbatti",
                          appindicator.IndicatorCategory.APPLICATION_STATUS,
                          parentPath)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()
    
    mitem = Gtk.MenuItem("Mainbatti-Talika")
    menu.append(mitem)
    mitem.connect("activate", OpenMainbattiTalika)

    mitem = Gtk.MenuItem("Settings")
    menu.append(mitem)
    mitem.connect("activate", Settings)
 
    mitem = Gtk.MenuItem("Check for updates")
    menu.append(mitem)
    mitem.connect("activate", Update)   

    mitem = Gtk.SeparatorMenuItem()
    menu.append(mitem)

    mitem = Gtk.CheckMenuItem("Gadget")
    mitem.set_active(True)
    mitem.connect("toggled", GadgetToggle)
    menu.append(mitem)
    
    mitem = Gtk.SeparatorMenuItem()
    menu.append(mitem)

    mitem = Gtk.MenuItem("Quit")
    mitem.connect("activate", Quit)
    menu.append(mitem)

    menu.show_all()
    ind.set_menu(menu)

    ind.connect("scroll-event", ShowGadget)

    Gtk.main()
