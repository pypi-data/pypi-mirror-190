#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : ipsocgen_cli.py
# License           : MIT license <Check LICENSE>
# Author            : Anderson Ignacio da Silva (aignacio) <anderson@aignacio.com>
# Date              : 06.02.2023
# Last Modified Date: 06.02.2023
import logging
import argparse
import pathlib
import sys
import yaml
from constants import options, CustomFormatter

def _validate_cfg(args):
    try:
        cfg = yaml.safe_load(args['config'])
    except yaml.YAMLError as exc:
        logging.error('Error while parsing YAML file:')
        if hasattr(exc, 'problem_mark'):
            if exc.context != None:
                logging.error('  parser says\n' + str(exc.problem_mark) + '\n  '+
                              str(exc.problem) + ' ' + str(exc.context) +
                              '\nPlease correct data and retry.')
                sys.exit(1)
            else:
                logging.error('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                              str(exc.problem)+
                              '\nPlease correct data and retry.')
                sys.exit(1)
        else:
            logging.error('Something went wrong while parsing yaml file')
            sys.exit(1)
    logging.debug('YAML file parse done without errors')


    # Mandatory entries
    for option in options.INIT_ENTRIES:
        if option not in cfg:
            logging.error('Missing mandatory key - '+option)
            return False

    logging.info('Validate entries of: '+cfg['proj_name'])

    # Available type options
    if cfg['type'] not in options.TYPES:
        logging.error('Invalid type on configuration file')
        return False

    # Available FPGA options
    if cfg['fpga_board'] not in options.FPGA_BOARD:
        logging.error('Invalid fpga_board on configuration file')
        return False

    # Log main entries
    for key, value in cfg.items():
        logging.debug(key+'='+value) if isinstance(key, str) and isinstance(value, str) else ''

    if cfg['type'] == 'soc':
        if 'soc_description' not in cfg:
            logging.error('SoC description missing')
            return False
    else:
        if 'mpsoc_description' not in cfg:
            logging.error('MPSoC description missing')
            return False
    return True

def _gen(args):
    return True

def main():
    parser = argparse.ArgumentParser(description='IP SoC Generator CLI')

    parser.add_argument('-c','--cfg',
                        nargs='?',
                        type=argparse.FileType('r'),
                        help='YAML file with the configuration of the MP/SoC')
    parser.add_argument('-o','--output',
                        nargs='?',
                        type=pathlib.Path,
                        help='Output directory of the generated design',
                        default='./output')

    parser.add_argument('-v','--validate',
                        action='store_true',
                        help='Validate only configuration file')

    parser.add_argument('-d','--debug',
                        action='store_true',
                        help='Enable debug mode')

    in_args = {}
    in_args['config']   = parser.parse_args().cfg
    in_args['output']   = parser.parse_args().output
    in_args['validate'] = parser.parse_args().validate
    in_args['debug']    = parser.parse_args().debug

    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logging.basicConfig(level=logging.DEBUG if in_args['debug'] == True else logging.INFO,
                        handlers=[handler])
    # print(in_args)
    if in_args['config'] == None:
            logging.warning("No valid configuration was specified, exiting now...")
            sys.exit(0)
    else:
        if _validate_cfg(in_args) == False:
            logging.error('Aborting generation...')
            sys.exit(1)
        else:
            if in_args['validate'] == True:
                logging.info('Validate only enabled, exiting now...')
                sys.exit(0)
        _gen(in_args)

if __name__ == '__main__':
    main()
