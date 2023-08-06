'''Usage:

screenrun execute [--name <name>] <cmd>
          file <path>
          persist [--name <name>] <cmd>
          cron [--name <name>] <cmd>
          restart [--name <name>] <cmd>
          check [--name <name>] <cmd>
          kill --name <name> | <cmd>
          list
'''

import sys

from screenrun import ScreenRun


FUNCTIONS = (
    'execute',
    'file',
    'persist',
    'cron',
    'restart',
    'check',
    'kill',
    'list',
)


def usage():
    '''Print usage information and exit.'''
    sys.stderr.write(__doc__)
    sys.exit(1)

def main(args=None):
    '''Main entry point for the package.'''

    sceenrun = ScreenRun()

    # Parse arguments
    args = args or sys.argv[1:]
    if len(args) == 0:
        usage()

    ## Get function and remove it from args
    function = args[0]
    args = args[1:]
    if function not in FUNCTIONS:
        usage()

    ## Get name of the Screen session specified by the user, and remove it from args
    name = None
    if '--name' in args:
        name_index = args.index('--name') + 1
        try:
            name = args[name_index]
        except IndexError:
            sys.stderr.write('Missing name argument')
            sys.exit(1)

        args.pop(name_index)
        args.pop(name_index - 1)

    ## Any remaining arguments are the command to run, or the path to the file
    cmd = ' '.join(args)

    # Execute function
    if function == 'execute':
        sceenrun.execute(cmd, name=name)

    elif function == 'file':
        path = cmd
        sceenrun.execute_file(path)

    elif function == 'persist':
        sceenrun.persist(cmd, name=name)

    elif function == 'cron':
        sceenrun.persist(cmd, name=name, timeout=59)

    elif function == 'restart':
        sceenrun.restart(cmd, name=name)

    elif function == 'check':
        result = sceenrun.check(cmd=cmd, name=name)

        msg = 'Running' if result else 'Not running'
        print(msg)

        return 0 if result else 1  # Return 0 if running, 1 if not

    elif function == 'kill':
        result = sceenrun.kill(cmd=cmd, name=name)

        if result is False:
            sys.stderr.write('Cound not kill session')
            sys.exit(1)

    elif function == 'list':
        results = sceenrun.list()
        for name in results:
            print(name)

    return 0


if __name__ == '__main__':
    sys.exit(main())
