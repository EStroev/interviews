import os
try:
    import shodan
except ImportError:
    try:
        print('[-] Shodan isn`t found. Try to install it...')
        from setuptools.command import easy_install

        easy_install.main(["-U", "shodan"])
        print('[+] Shodan was installed')
        import shodan
    except ImportError:
        print('[-] Oops. Something went wrong!')
        print('[-] Couldn`t install shodan')
        exit(-1)
from math import ceil
import argparse

parser = argparse.ArgumentParser(description='Console search in Shodan')
parser.add_argument('-o', dest='out_file', action='store', help='Output file for results')
parser.add_argument('-q', dest='query', action='store', help='Search query')
parser.add_argument('-k', dest='shodan_key', action='store', help='Shodan API key')

args = parser.parse_args()

if not args.query:
    print('[-] Search query is not specified!')
    print(parser.print_help())
    exit(-1)
if not args.shodan_key:
    print('[-] Shodan API key is not specified!')
    print(parser.print_help())
    exit(-1)
if args.out_file:
    if not os.path.exists(os.path.dirname(os.path.abspath(args.out_file))):
        print('[-] Output folder %s does not exist!' % os.path.abspath(args.out_file))
        create_out_folder = raw_input('[*] Create output folder? [y/n]: ')
        if create_out_folder in ['Y', 'y']:
            os.makedirs(os.path.dirname(os.path.abspath(args.out_file)))
            print('[+] Create output folder %s' % os.path.abspath(args.out_file))
        else:
            print('[-] You must specify an existing path to the output file!')
            exit(-1)

api = shodan.Shodan(args.shodan_key)

results = api.search(query=args.query)
pages = int(ceil(float(results['total']) / 100))

print('[+] Search query: %s \nResults found: %s \nNumber of pages: %d\n' % (args.query, results['total'], pages))

i = 1
if args.out_file:
    with open(args.out_file, 'w') as out_f:
        for k in xrange(0, pages):
            results = api.search(query=args.query, page=k)
            for result in results['matches']:
                hostname = result['hostnames'][0] if result['hostnames'] else ''
                out_f.write('Hostname: %s\nIP: %s:%s\n\n' % (hostname, result['ip_str'], result['port']))
                print('Hostname: %s\nIP: %s:%s\n' % (hostname, result['ip_str'], result['port']))
                i += 1
    print('[+] Write all records to %s' % os.path.abspath(args.out_file))
else:
    for k in xrange(0, pages):
        results = api.search(query=args.query, page=k)
        for result in results['matches']:
            hostname = result['hostnames'][0] if result['hostnames'] else ''
            print('Hostname: %s\nIP: %s:%s\n' % (hostname, result['ip_str'], result['port']))
            i += 1

print('[+] Finished. Total records: %d' % i)