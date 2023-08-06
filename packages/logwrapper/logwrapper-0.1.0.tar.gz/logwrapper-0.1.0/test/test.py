#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: test.py
Author: YJ
Email: yj1516268@outlook.com
Created Time: 2023-02-08 14:32:12

Description:
"""

from logwrapper import get_logger

log_conf = {
    'to_console':
    True,
    'console_level':
    'DEBUG',
    'to_file':
    True,
    'format':
    '''%(asctime)s | %(levelname)-8s | <%(threadName)s> '''
    '''%(module)s.%(funcName)s [%(lineno)d]: %(message)s'''
}


def main():
    """docstring for main"""
    logger = get_logger(logfolder='logs', config=log_conf)

    logger.warning('Warning')
    logger.error('Error')
    logger.critical('Error')


if __name__ == "__main__":
    main()
