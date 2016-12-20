# coding: utf-8
# use myvenv; simple solution; using exec, execfile is removed from python3

VENV_PATH = '/home/mohamed/vEnvs/i3PyHacking/bin/activate_this.py'
exec(
    compile(open(VENV_PATH, 'r').read(), VENV_PATH, 'exec'),{
        '__file__': VENV_PATH,
        '__name__': '__main__'
    }
)


from i3pystatus import Status
from i3pystatus.core.command import run_through_shell
from i3pystatus import IntervalModule
from shutil import which

status = Status()

# Displays clock like this:
# Tue 30 Jul 11:59:46 PM
status.register("clock", format="%A %-d %B %X",)


# Shows the average load of the last minute and the last 5 minutes
status.register("load")


# The battery monitor has many formatting options, see README for details

# This would look like this, when discharging (or charging)
# \u219314.22W 56.15% [77.81%] 2h:41m
# And like this if full:
# =14.22W 100.0% [91.21%]
#
# This would also display a desktop notification (via D-Bus) if the percentage
# goes below 5 percent while discharging. The block will also color RED.
# If you don't have a desktop notification demon yet, take a look at dunst:
#   http://www.knopwob.org/dunst/
status.register("battery",
    format="{status}/{consumption:.2f}W {percentage:.2f}% {remaining:%E%hh:%Mm}",
    alert=True,
    alert_percentage=5,
    status={
        "DIS": "\u2193",
        "CHR": "\u2191",
        "FULL": "=",
    },)

# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces
status.register("network",
                interface="enp2s0",
                format_up="{v4cidr}",)

# Note: requires both netifaces and basiciw (for essid and quality)
status.register("network",
                interface="wlp3s0",
                format_up="{essid} {quality:03.0f}%",)

# Shows pulseaudio default sink volume
status.register("pulseaudio",
                format=" {volume}",
                format_muted=" {volume}"
)

class MyBacklight(IntervalModule):

    settings = (
        ('format', 'the format used to display backlight'),
        ('step', 'The step of increase or decrease'),
        ('icon', 'Icon to decorate'),
    )

    format = "{icon}{percentage}{symbole}"
    step = 5
    interval = 5
    icon = ''
    on_upscroll = "lighter"
    on_downscroll = "darker"

    has_light = which('light') is not None


    def run(self):
        if self.has_light:
            self.percentage = run_through_shell(['light']).out.splitlines()[0]
            self.output = {
                'full_text': self.format.format(**{
                    'percentage': self.percentage,
                    'symbole': '%',
                    'icon': self.icon
                })
            }
    
    def lighter(self):
        if self.has_light:
            run_through_shell(["light", "-A", str(self.step)])

    def darker(self):
        if self.has_light:
            run_through_shell(["light", "-U", str(self.step)])


status.register(
    MyBacklight,
    format='{icon}  {percentage}{symbole}',
    step=5,
    icon='',
)


status.register(
    "cmus"
)


status.register(
    "pomodoro",
    sound="/home/mohamed/i3pyconfig/beep.ogg",
)


status.run()
