import os
import argparse
import xml.etree.ElementTree as et

try:
    import requests
except ImportError:
    try:
        print('[-] Requests isn`t found. Try to install it...')
        import pip
        pip.main(['install', 'requests'])
        import requests
    except ImportError:
        print('[-] Pip isn`t found. Try to install it...')
        import subprocess

        from subprocess import STDOUT
        import os

        process = subprocess.Popen('sudo apt-get install python-pip', shell=True,
                                   stdout=subprocess.PIPE, stderr=STDOUT, executable="/bin/bash")
        output, error = process.communicate()
        import pip
        print('[+] Pip was installed')

        pip.main(['install', 'requests'])
        import requests
        print('[+] Requests was installed')
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        print('[-] Bs4 isn`t found. Try to install it...')
        import pip
        pip.main(['install', 'bs4'])
        from bs4 import BeautifulSoup
    except ImportError:
        print('[-] Pip isn`t found. Try to install it...')
        import subprocess

        from subprocess import STDOUT
        import os

        process = subprocess.Popen('sudo apt-get install python-pip', shell=True,
                                   stdout=subprocess.PIPE, stderr=STDOUT, executable="/bin/bash")
        output, error = process.communicate()
        import pip
        print('[+] Pip was installed')

        pip.main(['install', 'bs4'])
        from bs4 import BeautifulSoup
        print('[+] Bs4 was installed')


def escaping_characters(data):
    return data.replace('"', '%22').replace(':', '%3A').replace(' ', '+').replace('[', '%5B').replace(']', '%5D')

parser = argparse.ArgumentParser(description='Console search in Yandex with Yandex.XML API')
parser.add_argument('-o', dest='out_file', action='store', help='Output file for results')
parser.add_argument('-q', dest='query', action='store', help='Search query')
parser.add_argument('-k', dest='key', action='store', help='Yandex API key')
parser.add_argument('-u', dest='user', action='store', help='Yandex user')
parser.add_argument('-m', dest='max_pages', action='store', default='5', help='Max Pages')
args = parser.parse_args()

if not args.query:
    print('[-] Search query is not specified!')
    print(parser.print_help())
    exit(-1)
if not args.key:
    print('[-] Yandex API key is not specified!')
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
if not args.user:
    print('[-] Yandex user is not specified!')
    print(parser.print_help())
    exit(-1)
if not args.max_pages:
    print('[-] Yandex user is not specified!')
    print(parser.print_help())
    exit(-1)
if not args.user:
    print('[-] Yandex user is not specified!')
    print(parser.print_help())
    exit(-1)

for page in xrange(0, int(args.max_pages)):
    url = 'https://yandex.ru/search/xml?' \
          + 'user=%s&' % args.user \
          + 'key=%s&' % args.key \
          + 'query=%s&' % escaping_characters(args.query) \
          + 'l10n=ru&sortby=rlv&' \
          + 'filter=none&' \
          + 'maxpassages=%s' % args.max_pages \
          + '&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D100.docs-in-group%3D1&' \
          + 'page=%s' % page

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')

    root = et.fromstring(str(soup))

    error = root.findtext('response/error')
    if error:
        print('[-] Error: %s' % error)
        exit(-1)
    query = root.findtext('request/query')
    total_found = root.findtext('response/found')
    print('Search query: %s' % query.strip('\n').strip().split('title:')[1])
    print('Results found: %s\n' % total_found.strip('\n').strip())

    results = root.findall('response/results/grouping/group/doc/url')
    if args.out_file:
        with open(args.out_file, 'a') as f_out:
            for result in results:
                f_out.write(result.text.strip().strip('\n'))
                f_out.write('\n')
                print(result.text.strip().strip('\n'))
        print('\n[+] Write all records to %s' % os.path.abspath(args.out_file))
    else:
        for result in results:
            print(result.text.strip().strip('\n'))

print('[+] Finished. Total records: %s' % len(results))