# Copyright (C) 2021-2023 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import threading
from platform import system


def is_linux_os() -> bool:
    """Returns True if running on Linux"""
    return True if system() == "Linux" else False


def is_windows_os() -> bool:
    """Returns True if running on Windows"""
    return True if system() == "Windows" else False


def is_mac_os() -> bool:
    """Returns True if running on Mac"""
    return True if system() == "Darwin" else False


def str_to_bool(s: str) -> bool:
    """Returns a boolean based on the passed in string"""
    return s.lower() in ("true", "yes", "1")


def threaded(fn):
    """Decorator for a threaded function"""
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
