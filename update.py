#!/usr/bin/env python

import json
import requests
import xml.etree.ElementTree as ET


def get_xml(url):
    r = requests.get(url)
    tree = ET.fromstring(r.content)
    return tree


def parse_xml(xml, tag):
    ns = {'default': 'info:lc/xmlns/codelist-v1'}
    parsed = []
    for language in xml.findall('.//default:{0}'.format(tag), ns):
        code = language.find('./default:code', ns).text
        for name in language.findall('.//default:name', ns):
            item = {'id': code, 'text': name.text}
            parsed.append(item)
    return parsed


def update_code_list(list_name):
    url = 'http://www.loc.gov/standards/codelists/{0}.xml'.format(list_name)
    fn = '{0}.json'.format(list_name)
    tag = 'country' if list_name == 'countries' else list_name[:-1]
    xml = get_xml(url)
    parsed = parse_xml(xml, tag)
    parsed.sort(key=lambda x: x['text'])
    with open(fn, 'wb') as f:
        json_data = json.dumps(parsed, ensure_ascii=False, indent=4)
        f.write(json_data.encode('utf8'))


if __name__ == '__main__':
    update_code_list('languages')
    update_code_list('countries')
    update_code_list('gacs')
