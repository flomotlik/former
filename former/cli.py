import argparse
import json
import sys
import traceback

import yaml

import former


def arguments():
    parser = argparse.ArgumentParser(description='Print CloudFormation Resources')
    parser.add_argument('service')
    parser.add_argument('type')
    parser.add_argument('subtype', default='', nargs='?')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--debug', '-d', action='store_true')

    return parser.parse_args()


def main():
    args = arguments()

    try:
        from former.resource import Resource
    except Exception as e:
        print("Couldn't get spec for CloudFormation resources - usually this is a network issue.")
        if args.debug:
            traceback.print_exc()
        else:
            print("Use `former --debug` to get the full traceback")
        sys.exit(1)

    type = former.resource.type_key(args.service, args.type, args.subtype)
    if type:
        resource = Resource(type)
        cf_resource = {'Type': type}

        cf_resource['Properties'] = resource.parameters()

        data = {'Resources': {''.join(e for e in type if e.isalnum()): cf_resource}}
        if args.json:
            output = json.dumps(data, indent=2)
        else:
            output = yaml.safe_dump(data, allow_unicode=True, default_flow_style=False)
        print(output)
    else:
        print('Resource not found for: {} {} {}'.format(args.service, args.type, args.subtype))
        sys.exit(1)
