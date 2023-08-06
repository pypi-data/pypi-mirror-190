import logging
import argparse
import pathlib
import sys
import yaml

def _validate_cfg(args):
    cfg = yaml.safe_load(args['config'])
    print(cfg)
    logging.info('Configuration check OK')
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

    logging.basicConfig(level=logging.DEBUG if in_args['debug'] == True else logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # print(in_args)
    if in_args['config'] == None:
            logging.warning("No valid configuration was specified, exiting now...")
            sys.exit(0)
    else:
        if _validate_cfg(in_args) == False:
            logging.error('Invalid configuration, aborting generation...')
            sys.exit(1)
        else:
            if in_args['validate'] == True:
                logging.info('Validate only enabled, exiting now...')
                sys.exit(0)
        _gen(in_args)

if __name__ == '__main__':
    main()
