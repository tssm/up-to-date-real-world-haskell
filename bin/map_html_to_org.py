import os

data_file = 'data/chapter_links.txt'

with open(data_file, 'r') as f:
    html_files = [line.strip() for line in f.readlines()]

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
    return "sed -i 's/\\[file:{infile}\\]/\\[file:{outfile}\\]/g' *.org".format(infile=i, outfile=o)

print('')
print('sed commands:')
for h, o in mapping.items():
    print(format_sed_cmd(h, o))
