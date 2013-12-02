from django.core.management import BaseCommand
from datetime import timedelta, datetime
from optparse import make_option
from dateutil.parser import parse
import sys


RETURN_CODES = {
    0: 'OK',
    1: 'WARNING',
    2: 'CRITICAL',
    3: 'UNKNOWN',
    4: 'DEPENDENT',
}


class MonitoringMeta(type):
    def __new__(cls, name, bases, dct):
        monitor = super(MonitoringMeta, cls).__new__(cls, name, bases, dct)
        if hasattr(monitor, "handle"):
            monitor._orig_handle = monitor.handle
        if hasattr(monitor, "monitoring_handle"):
            monitor.handle = monitor.monitoring_handle
        return monitor
#
#
#class MonitoringCommand(BaseCommand):
#    __metaclass__ = MonitoringMeta
#
#    def monitoring_handle(self, *args, **options):
#        if "monitor_it" in options:
#            print "you got monitoredddd"
#        else:
#            print "11"
#            self._orig_handle(*args, **options)
#            filename = "/tmp/%s.txt" % __name__
#            result_file = open(filename, "w")
#            now = datetime.datetime.now()
#            result_file.write(now.isoformat())
#
#
#class Command(MonitoringCommand):
#    def handle(self, *args, **options):
#        print "I handle stuff"
#
#    def monitoring_handle(self, *args, **options):
#        print "nice"

class MonitoringCommand(BaseCommand):
    __metaclass__ = MonitoringMeta

    option_list = BaseCommand.option_list + (
        make_option(
            '--monitor',
            action='store_true',
            dest='monitor',
            default=False,
        ),
    )

    @property
    def filepath(self):
        return "/tmp/%s.txt" % str(self.__module__)

    def monitoring_handle(self, *args, **options):
        print 1
        self._orig_handle(*args, **options)
        result_file = open(self.filepath, "w")
        now = datetime.datetime.now()
        result_file.write(now.isoformat())

    def run_from_argv(self, argv):
        if '--monitor' in argv:
            self.monitor()
        else:
            super(MonitoringCommand, self).run_from_argv(argv)

    def monitor(self):
        check_file = open(self.filepath, "r")
        check_date = parse(check_file.readline())

        now = datetime.now()

        if now - check_date < timedelta(hours=1):
            self.log_exit(0, "Everything is fine")
        else:
            self.log_exit(2, "No Cron output for at least %d hours" % 1)

    def log_exit(self, level, message):
        level_handle = RETURN_CODES[level]

        print "%s - %s" % (level_handle, message)

        sys.exit(level)