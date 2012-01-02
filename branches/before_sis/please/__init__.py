#!/usr/bin/python

"""Please is a command-line tool, which helps in developing and maintaining 
programming contests and problems."""

from . import contexts
from . import locale
from . import logging

import os.path
import sys

def _set_log_level(args, log):
    for item in args:
        if item == '--verbose':
            log.level = logging.DEBUG
            args.remove(item)
        elif item == '--silent':
            log.level = logging.NO_LOGGING
            args.remove(item)
    return args


def main(directory='.', args=None, log=None):
    """Main method to run please tool.
    
    Args:
        directory - root directory where to work from. Default is current dir.
        args - arguments (including command). Default are sys.argv.
        log - log instance. Default is console logger.
    """
    
    directory = os.path.abspath(directory)
    if args is None:
        args = sys.argv[1:]
    if log is None:
        log = logging.ConsoleLog()
    
    args = _set_log_level(args, log)
    
    log.info(locale.get('main.header'))
    
    context = contexts.guess(directory, log)
    if context is None:
        log.error(locale.get('main.unknown-context'))
        return 1
        
    log.debug(locale.get('main.assuming-context').format(context))
    context.handle(args)
    return 0