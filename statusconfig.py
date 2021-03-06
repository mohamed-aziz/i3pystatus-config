# coding: utf-8
# use myvenv; simple solution; using exec, execfile is removed from python3

VENV_PATH = '/home/mohamed/vEnvs/i3PyHacking/bin/activate_this.py'
exec(
    compile(open(VENV_PATH, 'r').read(), VENV_PATH, 'exec'), {
        '__file__': VENV_PATH,
        '__name__': '__main__'
    }
)


from i3pystatus import Status # noqa
from i3pystatus.core.command import run_through_shell # noqa
from i3pystatus import IntervalModule # noqa
from shutil import which # noqa
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


# Note: requires both netifaces and basiciw (for essid and quality)
status.register("network",
                interface="wlp3s0",
                format_up="{essid} {quality:03.0f}%",)

# Shows pulseaudio default sink volume
status.register("pulseaudio",
                format=" {volume}",
                format_muted=" {volume}")

status.register(
    "backlight_light",
    format='{icon}  {percentage}{symbole}',
    step=5,
    icon='',)


status.register(
    "mpd",
    format="{title} {status}")


status.register(
    "uname",
    format=" {sysname} {release} {machine}")

status.register(
    "emacs_service",
    format="Emacs is {status}")

status.run()
