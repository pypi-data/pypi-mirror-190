'''
ScreenRun

This module is used to manage and monitor commands in Screen sessions.
'''

import hashlib
import os
import subprocess
import time


class ScreenRun:
    '''
    Class to persist, monitor and manage commands running within Screen sessions.
    '''
    def __init__(self):
        # Find absolute paths of programs used
        self.screen_path = self._whereis("screen")
        self.grep_path = self._whereis("grep")

        # Check all programs have been found
        if not self.screen_path or \
           not self.grep_path:
            raise Exception("Missing commands. Please install Screen and Grep.")

        # Build commands
        self.launch_cmd = f'{self.screen_path} -S "{{0}}" -dm bash -c "{{1}}"'

        ## Check command
        ### `screen -ls` lists all running sessions
        ### `grep -q $'.SESSION_NAME\t'` checks if the session name is in the list
        ### 0 == True, because bash
        self.check_cmd = f'{self.screen_path} -ls' \
            + f' | {self.grep_path} -q ".{{}}\t"'

        ## exit command sends two ctrl-c keypresses
        self.exit_cmd = f'{self.screen_path} -dr -S "{{0}}" -X stuff $\'\003\003\''

        self.kill_cmd = f'{self.screen_path} -dr -S "{{0}}" -X quit'

    def execute(self, cmd, name=None, singleton=True):
        '''
        Start a new Screen running the given command.

        Args:
            cmd (str): Shell command to run in screen
            name (str): Name to assign to running screen
            singleton (bool): If True, check if a screen with the same name is
                              already running.

        Returns:
            str: Name of the Screen session that was started.
        '''
        # Generate name if not given
        name = name if name is not None else self._hash_command(cmd)

        # Check if screen is already running
        if singleton and self.check(name=name):
            print('Screen already running')
            return name

        command = self.launch_cmd.format(name, cmd)
        os.system(command)

        return name

    def execute_file(self, path):
        '''
        Execute ScreenRun file

        Args:
            path (str): Path to ScreenRun file

        Note:
            ScreenRun files are simple text files with one command per line. Eg:

            # Comments...
            name command arg0 arg1 ...

            another_name another_command arg0 arg1 ...
        '''
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith('#') or line == '':
                continue

            parts = line.split(' ', 1)
            if len(parts) != 2:
                continue

            name, cmd = parts
            self.persist(cmd, name=name)

    def check(self, cmd=None, name=None):
        '''
        Check if a Screen with the given name is running.

        Args:
            cmd (str): Command running in a Screen session to check.
            name (str): Name of the screen to check.

        Returns:
            bool: True if the named screen is running, False otherwise.
        '''
        # Check input
        if cmd is None and name is None:
            raise Exception("Must provide either cmd or name")

        # Generate name if not given
        name = name if name is not None else self._hash_command(cmd)

        command = self.check_cmd.format(name)
        running = os.system(command) == 0  # 0 == True, because bash
        return running

    def persist(self, cmd, name=None, interval=1, timeout=0):
        '''
        Check if a Screen with the given name is running, and if not, run it.

        Args:
            cmd (str): Shell command to run in screen
            name (str): Name to assign to running screen
            interval (int): Interval in seconds between checks
            timeout (int): Time to keep checking and restarting.
                           0 for run once, -1 for indefinitely.
        '''
        started = time.time()

        # Generate name if not given
        if name is None:
            name = self._hash_command(cmd)

        # Run loop
        while True:
            # Start if not running
            if not self.check(name=name):
                self.execute(cmd, name)

            # Check timeout
            if timeout != -1:
                duration = time.time() - started
                if duration > timeout:
                    break

            # Wait
            time.sleep(interval)

    def kill(self, cmd=None, name=None):
        '''
        Kill the Screen session with the given name or command.

        Args:
            name (str): Name of the screen to kill.
            cmd (str): Command running in a Screen session to kill.

        Returns:
            bool: True if the named screen was killed, False otherwise.
        '''
        # Generate name if not given
        name = name if name is not None else self._hash_command(cmd)

        # Return if session is not running
        if not self.check(name=name):
            return True

        # Issue exit command
        cmd = self.exit_cmd.format(name)
        os.system(cmd)

        # Return if session is not running
        if not self.check(name=name):
            return True

        # Issue kill command
        command = self.kill_cmd.format(name)
        os.system(command)

        result = not self.check(name=name)
        return result

    def restart(self, cmd, name=None):
        '''
        Restart the Screen session with the given name or command.

        Args:
            name (str): Name of the screen to restart.
            cmd (str): Command running in a Screen session to restart.

        Returns:
            bool: True if the named screen was restarted, False otherwise.
        '''
        # Generate name if not given
        name = name if name is not None else self._hash_command(cmd)

        # Kill if running
        if self.check(name=name):
            self.kill(name=name)

        # Check if command is still running
        if self.check(name=name):
            return False

        # Run
        self.execute(cmd, name)

        return True

    def list(self):
        '''
        List all running Screen sessions.

        Returns:
            list: List of running Screen session names.
        '''
        # List all running sessions with `screen -ls`
        result = subprocess.run(
            [self.screen_path, "-ls"],
            capture_output=True,
            check=True,
        )
        output = result.stdout.decode("utf-8")

        # Extract first column of output
        lines = output.splitlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line != ""]  # Remove empty lines
        ## Remove header
        lines = [line for line in lines if not line.startswith("There are")]

        # Remove PID prefixes
        names = [line.split("\t")[0] for line in lines]
        for i, name in enumerate(names):
            parts = name.split(".", 1)
            if len(parts) == 2:
                names[i] = parts[1]

        return names

    @staticmethod
    def _whereis(program):
        '''
        Returns the absolute path of a program or None if not found

        Args:
            program (str): The program to search for

        Returns:
            str: The absolute path of the program or None if not found
        '''
        command = ['whereis', '-b', program]
        output = subprocess.check_output(command)
        output = output.decode('utf-8')

        parts = output.split(" ")
        if len(parts) < 2:
            return None

        path = parts[1]
        path = path.strip()
        return path

    @staticmethod
    def _hash_command(cmd):
        '''
        Returns a hash of a command.

        Args:
            cmd (str): The command to hash

        Returns:
            str: The hash of the command
        '''
        cmd_bytes = cmd.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(cmd_bytes)
        return hasher.hexdigest()[:8]
