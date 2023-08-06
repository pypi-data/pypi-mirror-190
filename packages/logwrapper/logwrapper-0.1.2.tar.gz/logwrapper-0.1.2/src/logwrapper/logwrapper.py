#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: logwrapper.py
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2021-04-25 08:54:08

Description: Generate logger
"""

import logging
import os
from logging import handlers


def get_logger(logfolder, config):
    """Initialize the log module and get logger

    :logfolder: str -- Log folder name
    :config: dict   -- Log Configuration Parameters
    :return: logger

    """
    LEVEL = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    to_console = config.get('to_console', False)  # Output to console?
    console_level = config.get('console_level', 'DEBUG')  # console log level
    to_file = config.get('to_file', True)  # Output to file?
    log_format = config.get('format', '%(message)s')  # log format

    # Create and set up a logger
    logger = logging.getLogger()
    logger.setLevel(LEVEL['WARNING'])
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Output to file
    if to_file:
        # If the log folder does not exist, create it
        if not os.path.exists(logfolder):
            os.makedirs(logfolder)

        # Instantiate the rotated file handler
        # INFO Level
        info_logfile = '{}{}{}'.format(logfolder, os.path.sep, 'info.log')
        info_filehandler = handlers.TimedRotatingFileHandler(
            filename=info_logfile,
            when='midnight',
            interval=1,
            backupCount=0,
            encoding='UTF-8')
        info_filehandler.setLevel(LEVEL['INFO'])
        info_filehandler.setFormatter(formatter)
        # WARNING Level
        warning_logfile = '{}{}{}'.format(logfolder, os.path.sep,
                                          'warning.log')
        warning_filehandler = handlers.TimedRotatingFileHandler(
            filename=warning_logfile,
            when='midnight',
            interval=1,
            backupCount=0,
            encoding='UTF-8')
        warning_filehandler.setLevel(LEVEL['WARNING'])
        warning_filehandler.setFormatter(formatter)
        # ERROR Level
        error_logfile = '{}{}{}'.format(logfolder, os.path.sep, 'error.log')
        error_filehandler = handlers.TimedRotatingFileHandler(
            filename=error_logfile,
            when='midnight',
            interval=1,
            backupCount=0,
            encoding='UTF-8')
        error_filehandler.setLevel(LEVEL['ERROR'])
        error_filehandler.setFormatter(formatter)
        # CRITICAL Level
        critical_logfile = '{}{}{}'.format(logfolder, os.path.sep,
                                           'critical.log')
        critical_filehandler = handlers.TimedRotatingFileHandler(
            filename=critical_logfile,
            when='midnight',
            interval=1,
            backupCount=0,
            encoding='UTF-8')
        critical_filehandler.setLevel(LEVEL['CRITICAL'])
        critical_filehandler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(info_filehandler)
        logger.addHandler(warning_filehandler)
        logger.addHandler(error_filehandler)
        logger.addHandler(critical_filehandler)

    # Output to console
    if to_console:
        # # Instantiate a stream handler
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(LEVEL[console_level])
        consolehandler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(consolehandler)

    return logger
