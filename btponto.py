#!/usr/bin/env python
# btponto.py - Register the bluetooth devices around the computer
# Copyright (C) 2007  Osvaldo Santana Neto <osantana@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import sys
import os

import time

try:
    import bluetooth
except ImportError, e:
    sys.stderr.write("Cannot import bluetooth module. Pleas install the Python BlueZ bindings.\n")
    sys.exit(1)

import ConfigParser
from optparse import OptionParser

data_dir = os.path.join(os.path.expanduser('~'), '.btponto')
state_file = os.path.join(data_dir, 'state')
log_file = os.path.join(data_dir, time.strftime("bluetooth-%Y%m.log", time.localtime()))

def error(errmsg):
    sys.stderr.write("%s\n" % (errmsg))
    sys.exit(1)

def setup():
    if not os.path.exists(data_dir):
        try:
            os.mkdir(data_dir)
        except IOError, e:
            error("Cannot create data dir %s" % (data_dir))

def load_last_devices():
    try:
        f = open(state_file, "r")
        ret = set(device.strip() for device in f.readlines())
        f.close()
        return ret
    except IOError, e:
        return set()

def save_last_devices(devices):
    try:
        f = open(state_file, "w")
        f.write("%s\n" % ("\n".join(devices)))
        f.close()
    except IOError, e:
        error("Cannot save the current state file %s" % (state_file))

def append_log(in_, out):
    f = open(log_file, "a")
    now = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())

    for device in in_:
        f.write("%s  IN   %s\n" % (now, device))
    for device in out:
        f.write("%s  OUT  %s\n" % (now, device))

    f.close()

def poll():
    last_devices = load_last_devices()
    devices = set(bluetooth.discover_devices(flush_cache=True))

    in_ = devices - last_devices
    out = last_devices - devices
    append_log(in_, out)

    save_last_devices(devices)

class Day(object):
    def __init__(self, date):
        self.date = date
        self._in = ""
        self.out = ""

    def set_in(self, in_):
        if not self._in:
            self._in = in_
    def get_in(self):
        return self._in
    in_ = property(get_in, set_in)

    def __str__(self):
        return "%-10s  %-8s  %-8s" % (self.date, self.in_, self.out)

class User(object):
    def __init__(self, username):
        self.username = username
        self.fullname = ""
        self.occupation = ""
        self.bt = ""
        self.records = {}

    def render(self):
        days = self.records.keys()
        days.sort()

        ret = []
        for day in days:
            ret.append(str(self.records[day]))

        return '\n'.join(ret)

def load_bt_table(conf_file):
    bt_table = {}

    config = ConfigParser.ConfigParser()
    config.read([conf_file])

    for username in config.sections():
        user = User(username)
        user.fullname = config.get(username, "name")
        user.occupation = config.get(username, "occupation")
        user.bt = config.get(username, "bt")
        bt_table[user.bt] = user

    return bt_table

def report(conf_file, log_file):
    bt_table = load_bt_table(conf_file)

    log = open(log_file, "r")
    for line in log:
        raw_line = line.strip()

        try:
            date, time, rec_type, bt = raw_line.split()
        except ValueError:
            continue # FIXME: sometimes the record does not include the BT MAC.
                     #        We need to fix this bug in the future but until
                     #        there we will skip these records.
        if bt not in bt_table:
            continue

        user = bt_table[bt]

        if date in user.records:
            day = user.records[date]
        else:
            day = Day(date)
            user.records[date] = day

        if rec_type == 'IN':
            day.in_ = time
        else:
            day.out = time

    log.close()

    for user in bt_table.values():
        print "-" * 72
        print "Username: %s" % (user.username)
        print "Fullname: %s" % (user.fullname)
        print "BT Mac:   %s" % (user.bt)
        print
        print "%-10s  %-8s  %-8s" % ("Date", "In", "Out")
        print user.render()
        print

if __name__ == '__main__':
    usage = "usage: %prog [-f config_file log_file]"
    version = "%prog 0.1"

    parser = OptionParser(usage=usage, version=version)
    parser.add_option(
            "-f", "--file",
            dest="filename",
            help="write report to FILE",
            metavar="FILE")
    (options, args) = parser.parse_args()

    setup()
    if options.filename is None:
        poll()
    else:
        if not args:
            parser.print_help()
            sys.exit(0)

        report(options.filename, args[0])
