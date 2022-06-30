# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os

mod = "mod4"
terminal = guess_terminal()
scripts_home = f"{os.path.expanduser('~')}/.local/bin/"
user = os.getenv("USER")

keys = [

    # spawn
    Key([mod], "n", lazy.spawn("qutebrowser"), desc='Open browser'),
    Key([mod], "v", lazy.spawn(f"{terminal} -e nvim"), desc='Open Vim'),
    Key([mod], "m", lazy.spawn(f"{terminal} -e ncmpcpp"), desc='Open Music Panel'),
    Key([mod], "p", lazy.spawn(f"gnome-screenshot -i"), desc='Take screenshot'),
    Key([mod], "s", lazy.spawn(f"{terminal} -e htop"), desc='Open task manager'),
    Key([mod], "f", lazy.spawn(f"{terminal} -e lf"), desc='Open file manager'),
    Key([mod], "u", lazy.spawn(f"{scripts_home}upgrade"), desc='Sysupdate'),

    # audio
    Key(["control", "mod1"], "k", lazy.spawn(f"{scripts_home}pulsevolume --increase"), desc='Volume up'),
    Key(["control", "mod1"], "j", lazy.spawn(f"{scripts_home}pulsevolume --decrease"), desc='Volume down'),
    Key(["control", "mod1"], "m", lazy.spawn(f"{scripts_home}pulsevolume --mute"), desc='Toggle mute'),
    Key(["control", "mod1"], "p", lazy.spawn(f"mpc toggle"), desc='Pause music'),
    Key(["control", "mod1"], "l", lazy.spawn(f"mpc next"), desc='Next song'),
    Key(["control", "mod1"], "h", lazy.spawn(f"mpc prev"), desc='Previous song'),
    # Key(["control", "mod1"], "=", lazy.spawn(f"mpc volume +10"), desc='Music volume up'),
    # Key(["control", "mod1"], "-", lazy.spawn(f"mpc volume -10"), desc='Music volume down'),
    Key(["control", "mod1"], "c", lazy.spawn(f"mpc clear"), desc='Clear playlist'),

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.spawn(f"killall -u {user}"), desc="Shutdown Qtile"),
    Key([mod], "a", lazy.spawncmd(), desc="Spawn prompt"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts_defaults = dict(
    border_focus = '#F5C2E7',
    border_normal = '#1E1E2E',
    border_width = 4,
    margin = 15,
    margin_on_single = 15,
)

layouts = [
    layout.Tile(**layouts_defaults, ratio=0.5),
    layout.Max(**layouts_defaults),
    layout.Floating(**layouts_defaults),
]

widget_defaults = dict(
    font="Fira Code Nerd Font",
    foreground = '#D9E0EE',
    background = '#1E1E2E',
    fontsize=20,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.8),
                widget.LaunchBar(
                    progs = [ 
                        ('爵 ', 'qutebrowser',            'Browser'), 
                        (' ',  f'{terminal} -e nvim',    'NyanVim'), 
                        (' ', terminal,                     'Terminal'), 
                        (' ', f'{terminal} -e ncmpcpp', 'Music Panel'), 
                    ]
                ),
                widget.Prompt(prompt='run: '),

                widget.WindowName(fmt=''),

                widget.GroupBox(
                    block_highlight_text_color = '#1E1E2E',
                    active = '#D9E0EE',
                    hide_unused = True,
                    highlight_method = "block",
                    rounded = False,
                    this_current_screen_border = '#F5C2E7',
                ),

                widget.WindowName(fmt=''),

                widget.Clock(
                    format = "  %a %b %d ",
                    background = '#F28FAD',
                    foreground = '#1E1E2E',
                ),
                widget.Clock(
                    format = "  %H:%M ",
                    background = '#96CDFB',
                    foreground = '#1E1E2E',
                ),
                widget.TextBox(' ',
                    background = '#FAE3B0',
                    foreground = '#1E1E2E',
                ),
                widget.PulseVolume(
                    background = '#FAE3B0',
                    foreground = '#1E1E2E',
                ),
                widget.BatteryIcon(
                    background = '#FAE3B0',
                    foreground = '#1E1E2E',
                ),
            ],
            26, background='#1E1E2E', margin=10,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
