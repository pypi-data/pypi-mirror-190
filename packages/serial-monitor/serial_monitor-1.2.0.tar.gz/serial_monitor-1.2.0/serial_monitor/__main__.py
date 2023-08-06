"""notify serial changes"""
# pylint: disable=wrong-import-position
from pathlib import Path
import os
import sys
import re
import time
import pkgutil
import psutil
import gi
from serial.tools.list_ports import comports

gi.require_version("Notify", "0.7")
from gi.repository import Notify, GdkPixbuf


def check_process() -> int:
    """checks to see if flrig is in the active process list"""
    count = 0
    for proc in psutil.process_iter():
        if bool(re.match("serial_monitor", proc.name().lower())):
            count += 1
    return count


class PortChecker:
    """Checks serialports for changes"""

    def __init__(self):
        self.ports = set(comports())
        self.new_ports = None
        Notify.init("serial_monitor")
        self.summary = ""
        self.body = ""
        self.notification = Notify.Notification.new(self.summary, self.body)
        self.connected = GdkPixbuf.Pixbuf.new_from_file("usb_plug_connected.png")
        self.disconnected = GdkPixbuf.Pixbuf.new_from_file("usb_plug_disconnected.png")

    def check_ports(self):
        """Check the ports"""
        self.new_ports = set(comports())
        for port in self.ports - self.new_ports:
            self.notification.set_image_from_pixbuf(self.disconnected)
            self.summary = f"{port.device} disconnected"
            self.notification.update(self.summary)
            self.notification.show()

        for port in self.new_ports - self.ports:
            self.notification.set_image_from_pixbuf(self.connected)
            self.summary = f"{port.device} connected"
            self.notification.update(self.summary)
            self.notification.show()

        self.ports = self.new_ports


def main():
    """main entry"""
    process_count = check_process()
    if process_count > 1:
        sys.exit(0)
    path = os.path.dirname(pkgutil.get_loader("serial_monitor").get_filename())
    os.system(
        "xdg-icon-resource install --size 64 --context apps --mode user "
        f"{path}/k6gte-serial_monitor-64.png k6gte-serial_monitor"
    )
    os.system(
        "xdg-icon-resource install --size 32 --context apps --mode user "
        f"{path}/k6gte-serial_monitor-32.png k6gte-serial_monitor"
    )
    os.system(f"xdg-desktop-menu install {path}/k6gte-serial_monitor.desktop")
    os.chdir(Path(__file__).parent)
    job = PortChecker()
    while True:
        job.check_ports()
        time.sleep(3)


if __name__ == "__main__":
    main()
