import os
import argparse


def generate_html(api_key):
    # read template html
    html = open('template.html').read()
    html = html.replace("API_KEY", api_key)
    open("index.html", 'w').write(html)

def generate_js(filename):
    # read template html
    js = open('template.js').read()
    js += '\n'
    js += txt2js(filename)
    open("index.js", 'w').write(js)

def txt2js(filename):
    lines = open(filename).readlines()
    js_txt = "const locations = ["

    for line in lines:
        line = line.strip().split('*')
        try:
            js_txt += '{{ title: "{}", Institute :"{}", Latitude:{}, Longtitude:{} }},\n'.format(line[0], line[1], line[2], line[3])
        except:
            print(line)

    js_txt += "];"
    return js_txt

def parse_args():
    """parse input arguments"""""
    parser = argparse.ArgumentParser(description='CitationMap')
    parser.add_argument('--api_key', type=str, default='AIzaSyCPS6c2_TlFen5D_J9bTuQlQeC4njTcrJ8')
    parser.add_argument('--filename', type=str, default='data.txt')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    generate_html(args.api_key)
    generate_js(args.filename)
