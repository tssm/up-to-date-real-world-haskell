import os
import re

data_file = 'data/chapter_links.txt'

with open(data_file, 'r') as f:
    html_files = list(set([line.strip() for line in f.readlines()]))

# Sort so that longest file names are first
html_files = sorted(html_files, key=lambda x: -len(x))

org_files_orig = [f for f in os.listdir('.') if f.endswith('.org')]

org_files = list(org_files_orig)

mapping = {}

# Hardcode some mappings

mapping = {'advanced-library-design-building-a-bloom-filter.html': '26-building-a-bloom-filter.org',
           'code-case-study-parsing-a-binary-data-format.html': '10-parsing-a-binary-data-format.org',
           'extended-example-web-client-programming.html': '22-web-client-programming.org',
           'interfacing-with-c-the-ffi.html': '17-interfacing-with-c.org',
           'writing-a-library-working-with-json-data.html': '5-writing-a-library.org',
           'io-case-study-a-library-for-searching-the-filesystem.html': '9-a-library-for-searching-the-file-system.org',
           'gui-programming-with-gtk-hs.html': '23-gui-programming-with-gtk2hs.org',
           }

for f_raw in html_files:
    f = f_raw.replace('.html', '.org')

    match = None
    for o in org_files:
        if f in o:
            match = o
            break
    if match is not None:
        org_files = [f for f in org_files if f != match]
        mapping[f_raw] = match

print('<Unmapped chapters>')
print([f for f in html_files if f not in mapping])
print('</Unmapped chapters>')

print('<Unmapped ORG>')
print([f for f in org_files if f not in mapping.values()])
print('</Unmapped ORG>')


def format_sed_cmd(i, o):
    return ("sed -i 's/\\[file:{infile}\\]/\\[file:{outfile}\\]/g' *.org"
            ).format(infile=i, outfile=o)


print('')
print('sed commands:')
for h, o in mapping.items():
    print(format_sed_cmd(h, o))

def fn_replace_section_ref(matchobj, html_mapping=mapping):
    """This gets called in re.sub(...)"""
    (html, _, sec) = matchobj.groups()
    org = html_mapping.get(html, html.replace('.html', '.org'))

    return '[[file:{a1}::*{a3}][the section called \"{a3}\"]]'.format(a1=org, a3=sec)


def replace_section_ref(line, html_mapping):
    """
    >>> replace_section_ref('', {})
    ''

    >>> replace_section_ref('abc', {})
    'abc'

    >>> replace_section_ref('[[file:xyz.html#abc][the section called "blah"]]', {"xyz.html": "0-xyz.org"})
    '[[file:0-xyz.org::*blah][the section called \"blah\"]]'
    """

    # return re.sub('\[\[file:([^ ]+.html)#([^ \]]+)\]\[the section called “([^“]+)”\].*', '[[file:\\1::*\\3][the section called \"\\3\"]]', line)
    return re.sub('\[\[file:([^ ]+.html)#([^ \]]+)\]\[the section called [“"]([^“]+)[”"]\]\]',
                  lambda s: fn_replace_section_ref(s, html_mapping), line)


if __name__ == '__main__':
    import sys

    # print(sys.argv[1:])

    files_to_format = [f for f in sys.argv[1:] if f.endswith('.org')]
    # files_to_format = [f for f in files_to_format if f.startswith('2-')]

    print('To format: {}'.format(files_to_format))

    if True and files_to_format:
        import fileinput
        for line in fileinput.input(files=files_to_format, inplace=True, backup='.bak'):
            print(re.sub('\[\[file:([^ ]+.html)#([^ \]]+)\]\[the section called “([^“]+)”\].*', fn_replace_section_ref, line), end='')
