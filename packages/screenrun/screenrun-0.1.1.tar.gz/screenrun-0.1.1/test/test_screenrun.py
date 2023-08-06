'''
Unit tests for ScreenRun module
'''

import os
import unittest

from screenrun import ScreenRun


PREFIX = os.urandom(3).hex()


class TestScreenRun(unittest.TestCase):
    '''Unit tests for ScreenRun module'''

    def test_check_and_execute(self):
        '''Test check() and run() methods'''
        screenrun = ScreenRun()

        name = PREFIX + '_test0'

        exists = screenrun.check(name=name)
        assert exists is False

        screenrun.execute("sleep 5", name=name)

        exists = screenrun.check(name=name)
        assert exists is True

        screenrun.kill(name=name)

    def test_kill(self):
        '''Test kill() method'''
        screenrun = ScreenRun()

        name = PREFIX + '_test1'

        screenrun.execute("sleep 5", name=name)

        exists = screenrun.check(name=name)
        assert exists is True

        screenrun.kill(name=name)

        exists = screenrun.check(name=name)
        assert exists is False

    def test_persist(self):
        '''Test persist() method'''
        screenrun = ScreenRun()

        name = PREFIX + '_test2'

        screenrun.persist("sleep 5", name=name)
        screenrun.persist("sleep 5", name=name)
        screenrun.persist("sleep 5", name=name)

        exists = screenrun.check(name=name)
        assert exists is True

        screenrun.kill(name=name)

        screenrun.persist("sleep 5", name=name)

        exists = screenrun.check(name=name)
        assert exists is True

        screenrun.kill(name=name)

    def test_list(self):
        '''Test list() method'''
        screenrun = ScreenRun()

        name_0 = PREFIX + '_test3'
        name_1 = PREFIX + '_test4'

        screenrun.execute("sleep 5", name=name_0)
        screenrun.execute("sleep 5", name=name_1)

        sessions = screenrun.list()

        assert name_0 in sessions
        assert name_1 in sessions

        screenrun.kill(name=name_0)
        screenrun.kill(name=name_1)
