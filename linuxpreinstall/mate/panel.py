#!/usr/bin/env python
'''
This module controls various aspects of the MATE panel.
'''

from __future__ import print_function
import sys
import os
import json
python_mr = sys.version_info.major
# if python_mr >= 3:
#     import functools  # Python 3
# import sys
import gi
gi.require_version("Gtk", "3.0")
# ^ MATE is now GTK 3
from gi.repository import (
    Gio,
    GLib,
)
from subprocess import Popen


try:
    import linuxpreinstall
except ModuleNotFoundError as ex:
    if "No module named 'linuxpreinstall'" in str(ex):
        mateDir = os.path.dirname(os.path.abspath(__file__))
        moduleDir = os.path.dirname(mateDir)
        repoDir = os.path.dirname(moduleDir)
        tryModulePath = os.path.join(repoDir, 'linuxpreinstall')
        goodModuleFlag = os.path.join(tryModulePath, "__init__.py")
        if os.path.isfile(goodModuleFlag):
            sys.path.append(repoDir)
            import linuxpreinstall
        else:
            raise ex
    else:
        raise ex

from linuxpreinstall.mate.gsettings import (
    GSettings,
)
from linuxpreinstall import (
    echo0,
    echo1,
    echo2,
    set_verbose,
)

echo1("")
echo1("The panel module has started.")

"""
    @property
    def objects(self):
        '''
        Get panel item definitions from /org/mate/panel/objects/
        '''

        '''
        gsettings get org.mate.panel:/org/mate/panel/objects/ objects
        yields:
        'Schema "org.mate.panel" is not relocatable (path must not be
        specified)'
        - The result is the same if the path is "/org/mate/panel".
        - If path is left out, the result is 'No such key "objects"'.
        '''
        # return tuple(self.get_value('objects'))
        # ^ "Settings schema 'org.mate.panel' does not contain a key
        #   named 'objects'"
        # return tuple(self._get('/org/mate/panel/objects/', 'objects'))
        # ^ fails since id is part of path (a list of values is in
        #   readme under MATE.
    @objects.setter
    def objects(self, objects):
        var = GLib.Variant('as', list(items))
        # ^ a: array
        # ^ s: string
        self.set_value('objects', var)
"""

# def is_true_var(var):
#     trueVar = GLib.Variant('b', True)
#    return trueVar == var
# ^ Works, but not necessary since `if var` also works.


class MatePanel(Gio.Settings):
    '''
    A Gio.Settings handler implements dconf-settings.

    Example:
    <https://github.com/bilelmoussaoui/Authenticator>
    '''
    instance = None
    SCHEMA = "org.mate.panel"

    def __init__(self):
        Gio.Settings.__init__(self)
        echo1("* initializing a MatePanel object incorrectly"
              " (use get-default)")
        MatePanel.post_init(self)

    def _get(self, path, key):
        # based on https://askubuntu.com/a/1062671
        schema = self.SCHEMA
        if path is None:
            gsettings = self  # Gio.Settings.new(schema)
        else:
            gsettings = Gio.Settings.new_with_path(schema, path)
        return gsettings.get_value(key)

    def _set(self, path, key, value):
        # based on https://askubuntu.com/a/1062671
        schema = self.SCHEMA
        if path is None:
            gsettings = self  # Gio.Settings.new(schema)
        else:
            gsettings = Gio.Settings.new_with_path(schema, path)
        if isinstance(value, list):
            return gsettings.set_strv(key, value)
        if isinstance(value, str):
            var = GLib.Variant('s', value)
            # ^ a: array
            # ^ s: string
            return gsettings.set_value(key, var)
        if isinstance(value, int):
            return gsettings.set_int(key, value)

    @staticmethod
    def post_init(target):
        target.panel_obj_settings = GSettings('org.mate.panel.object')

    @staticmethod
    def new():
        g_settings = Gio.Settings.new(MatePanel.SCHEMA)
        g_settings.__class__ = MatePanel
        MatePanel.post_init(g_settings)
        return g_settings


    @staticmethod
    def get_default():
        if MatePanel.instance is None:
            MatePanel.instance = MatePanel.new()
        MatePanel.post_init(MatePanel.instance)
        return MatePanel.instance

    @property
    def items(self):
        '''
        Get panel item IDs (object-id-list).
        '''

        '''
        They are from /org/mate/panel/general/
        according to
        <https://forums.linuxmint.com/viewtopic.php?t=326992>
        gsettings get org.mate.panel object-id-list
        works, but
        gsettings get org.mate.panel:/org/mate/panel/general/ \
        object-id-list
        yields: 'Schema "org.mate.panel" is not relocatable (path must
        not be specified)'
        Yet somehow, using the path works when using Gio.
        '''
        # return tuple(self.get_value('object-id-list'))
        return tuple(self._get('/org/mate/panel/general/',
                               'object-id-list'))

    @items.setter
    def items(self, items):
        var = GLib.Variant('as', list(items))
        # ^ a: array
        # ^ s: string
        self.set_value('object-id-list', var)

    def remove_items_where(self, bad_value, key="applet-iid",
            all_ids=None, object_type="applet"):
        '''
        Remove each ID string from object-id-list if key matches
        bad_value in the corresponding /org/mate/panel/objects/<ID>.

        Keyword arguments:
        key -- Check only this key.
        all_ids -- Check only these keys (otherwise, keys will be
            listed).
        object_type -- Remove only this type of object.
        '''
        print("items: {}".format(self.items))
        '''
        ^ It is something like:
        ('notification-area', 'object-3', 'object-4', 'object-1',
        'object-2', 'object-27', 'object-34', 'object-40', 'object-41',
        'object-42', 'object-5', 'object-6', 'object-7')

        The object definitions are in a separate schema called
        org.mate.panel.object according to <https://www.reddit.com/r/
        Fedora/comments/4ti7ao/
        are_the_spins_lacking_complete_integration_simple/>.
        The following works:
        gsettings get \
            org.mate.panel.object:/org/mate/panel/objects/object-1/ \
            applet-iid
        '''
        bad_value_var = GLib.Variant('s', bad_value)
        applet_flag_var = GLib.Variant('s', object_type)
        # ^ s: string
        print("objects:")
        bad_ids = []
        objects_path = "/org/mate/panel/objects/"
        ids_limited = True
        if all_ids is None:
            all_ids = self.items
            ids_limited = False
        # all_ids = self.items + ('object-2', 'object-27', 'object-34')
        # ^ lost--stuck on menu but not in id list. Instead, reset via:
        #   gsettings set org.mate.panel object-id-list "['notification-area', 'object-3', 'object-4', 'object-1', 'object-2', 'object-27', 'object-34', 'object-40', 'object-41', 'object-42', 'object-5', 'object-6', 'object-7']"
        #   nohup mate-panel --replace &
        #
        for iid in all_ids:
            path = "{}{}/".format(objects_path, iid)
            pos = self.panel_obj_settings._get(path, 'position')
            right = self.panel_obj_settings._get(path,
                                                 'panel-right-stick')
            right_msg = ""
            if right:
                right_msg = " (right)"
            echo1("- pos: {}{}".format(pos, right_msg))
            echo1("  path: {}".format(path))
            # echo1("  self.get_has_unapplied(): {}".format(self.get_has_unapplied()))
            # For some reason, get_has_unapplied works on self but not
            #   on panel_obj_settings.
            # echo1("  self.panel_obj_settings.get_has_unnapplied(): {}"
            #       "".format(self.panel_obj_settings.get_has_unapplied()))


            p_s = self.panel_obj_settings
            for extra_k in ('object-type', 'applet-iid',):
                echo2("  {}: {}"
                      "".format(extra_k, p_s._get(path, extra_k)))
            '''
            ^ gsettings get \
              org.mate.panel.object:/org/mate/panel/objects/object-2/ \
              object-type
              # may still exist even if object-2 is not in items such as
              # after:
              Changing panel from
              ('notification-area', 'object-3', 'object-4', 'object-1',
              'object-2', 'object-27', 'object-34',
              'object-40', 'object-41', 'object-42', 'object-5',
              'object-6', 'object-7')
              to
              ['notification-area', 'object-3', 'object-4', 'object-1',
              'object-40', 'object-41', 'object-42', 'object-5',
              'object-6', 'object-7']...

            '''

            # value = self._get(path, key)
            value = self.panel_obj_settings._get(path, key)
            type_var = self.panel_obj_settings._get(path, 'object-type')
            # echo0(" {}: {}".format(key, value))
            # echo1("type({}): {}".format(key, type(value).__name__))
            # break
            if type_var != applet_flag_var:
                echo1("  skipping {} ({} not {})"
                      "".format(iid, type_var, applet_flag_var))
                # good_ids.append(iid)
                continue
            if value == bad_value_var:
                print("  found bad {}: {}"
                      "".format(type_var, iid))
                bad_ids.append(iid)
            else:
                print("  found good {} {}: {}"
                      "".format(type_var, value, iid))
                # good_ids.append(iid)
        good_ids = list(self.items)
        for bad_id in bad_ids:
            if bad_id in good_ids:
                good_ids.remove(bad_id)
            else:
                echo0("WARNING: bad_id {} is not in items.")
        if good_ids != list(self.items):
            echo0("Changing panel from \n  {} to \n  {}..."
                  "".format(self.items, good_ids))
            echo0("NotImplemented: Remove the objects before the keys,"
                  " or the objects will remain on the menu and be"
                  " unable to be enumerated by some code.")
            # self.items = good_ids
        else:
            echo0("There are no panels objects with {}=={}"
                  "".format(key, json.dumps(bad_value)))
        # self.items = sorted(self.items, key=sc_fn_to_name)
        return bad_ids

def main():
    # settings = MatePanel.get_default()
    settings = MatePanel.new()
    bad_item = None
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg.startswith("-"):
            if arg == "--verbose":
                set_verbose(1)
            elif arg == "--debug":
                set_verbose(2)
            else:
                raise ValueError("Unknown argument: {}".format(arg))
        elif bad_item is None:
            bad_item = arg
        else:
            raise ValueError("Unknown argument: {}".format(arg))
    if bad_item is None:
        bad_item = ""
    echo0("Looking for bad applet id {}..."
          "".format(json.dumps(bad_item)))
    remove_ids = ('object-2', 'object-27', 'object-34')
    bad_ids = settings.remove_items_where(
        bad_item,
        # all_ids=remove_ids,
        # object_type="launcher",
    )
    # for bad_id in bad_ids:
    #     settings.remove_items_where('iid', bad_id)
    # items = settings.items
    # ^ gets the desktop filenames
    # print("items: {}".format(items))
    # item_names = items
    # print("item_names: {}".format(item_names))
    if len(bad_ids) > 0:
        echo0("Restarting mate-panel to complete the process...")
        # TODO: p = Popen(['mate-panel', '--replace'])


if __name__ == "__main__":
    main()
