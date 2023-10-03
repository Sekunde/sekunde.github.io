import os
import requests
import argparse

from time import sleep
from scholarly import scholarly

def csv2dict(lines):
    data = {}
    if len(lines) == 0:
        return data

    for line in lines:
        line = line.strip().split('*')
        if line[0].strip() not in data:
            data[line[0].strip()] = {}
            data[line[0]]['institute'] = line[1].strip()
            data[line[0]]['latitude'] = float(line[2].strip())
            data[line[0]]['longtitude'] = float(line[3].strip())
    return data

def dict2csv(data, filename, filter_invalid=False):
    keywords = ['institute', 'latitude', 'longtitude']
    writelines = []

    for title in data:
        if data[title]['latitude'] == -1 and data[title]['longtitude'] == -1 and filter_invalid:
            continue
        try:
            txt = "*".join([title]+[str(data[title][keyword]) for keyword in keywords])
        except:
            import ipdb
            ipdb.set_trace()

        writelines.append(txt + '\n')

    f = open(filename, 'w')
    f.writelines(writelines)

def get_citations(author_name, filename, api_key):
    if os.path.exists(filename):
        lines = open(filename).readlines()
    data = csv2dict(lines)
    search_query = scholarly.search_author(author_name)
    author = scholarly.fill(next(search_query))

    for counter, pub in enumerate(author['publications']):
        title = pub['bib']['title']
        print('Title: ', title)
        pub = scholarly.fill(pub)
        try:
            citations = scholarly.citedby(pub)
        except:
            import ipdb
            ipdb.set_trace()
            continue

        for counter, citation in enumerate(citations):
            if citation['bib']['title'] in data:
                continue
            print("citedby", citation['bib']['title'])
            import ipdb
            ipdb.set_trace()

            firstAuthorId = None
            data[citation['bib']['title']] = {}
            if len(citation['author_id']) != 0:
              firstAuthorId = citation['author_id'][0]

            if firstAuthorId == None or len(firstAuthorId) == 0:
              data[citation['bib']['title']]['institue'] = -1
              data[citation['bib']['title']]['latitude'] = -1
              data[citation['bib']['title']]['longtitude'] = -1
              continue

            author = scholarly.search_author_id(firstAuthorId)
            lat, lon = get_location(author['affiliation'], api_key)
            data[citation['bib']['title']]['institue'] = author['affiliation']
            data[citation['bib']['title']]['latitude'] = lat
            data[citation['bib']['title']]['longtitude'] = lon
            dict2csv(data, filename)

def get_location(address, api_key):
    address = '+'.join(address.split())
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}'.format(api_key, address))
    resp_json_payload = response.json()
    if len(resp_json_payload['results']) == 0:
        return -1,-1
    res = resp_json_payload['results'][0]['geometry']['location']
    return res['lat'], res['lng']

def parse_args():
    """parse input arguments"""""
    parser = argparse.ArgumentParser(description='CitationMap')
    parser.add_argument('--author', type=str, default='Ji Hou')
    parser.add_argument('--api_key', type=str, default='AIzaSyDkod3qQAWRHvXAZHCya7cioliUZ93Bv1M')
    parser.add_argument('--filename', type=str, default='data.txt')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    get_citations(args.author, args.filename, args.api_key)
