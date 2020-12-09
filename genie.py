#!/usr/bin/env python3
# coding: utf8

import quopri
from fpdf import FPDF


def parse_vcards(s: str) -> list:
    vcards = []
    s = s.replace('=\n', '')
    for vcard in s.split('BEGIN:VCARD\n')[1:]:
        vcards.append(parse_vcard(vcard))
    return vcards

def parse_vcard(s: str) -> dict:
    vcard = {
        'version': "",
        'name': "",
        'phones': []
    }
    for row in s.split('\n'):
        if row.startswith('VERSION'):
            vcard['version'] = parse_version(row)
        elif row.startswith('FN:') or row.startswith('FN;'):
            vcard['name'] = parse_name(row)
        elif row.startswith('TEL:') or row.startswith('TEL;'):
            vcard['phones'].append(parse_phone(row))
    return vcard


def get_value(row: str) -> str:
    return row.split(':')[1].strip('\n').strip(' ')


def parse_version(row: str) -> str:
    return get_value(row)


def parse_name(row: str) -> str:
    # converting 'QUOTED-PRINTABLE' to 'UTF-8'
    row = quopri.decodestring(row).decode('utf-8')
    return get_value(row).replace(',', '')


def parse_phone(row: str) -> str:
    phone = get_value(row).strip(' ').replace(' ', '').replace('-', '')
    if phone.startswith('8'):
        phone = '+7' + phone[1:]
    return phone


def output_table(vcards: list) -> str:
    out = ""
    for i, vc in enumerate(vcards):
        # out += f"№ {str(i+1):>3}|{vc['version']:3}|{vc['name']:45}|{', '.join(vc['phones'])}\n"
        out += f"{str(i+1)},{vc['name']},{', '.join(vc['phones'])}\n"
    return out


def run():
    vcf_filepath = './00001.vcf'
    with open(vcf_filepath) as vcf_file:
        vcf_file = vcf_file.read()
        vcards_out = output_table(parse_vcards(vcf_file))
        # print(vcards_out)
        print(vcards_out)
        with open('./test.csv', 'w') as of:
            of.write(vcards_out)
        # print(type(vcards_out.encode('utf-8')))
        # print(type(vcards_out.encode('utf-8').decode('cp1252')))
        # import sys
        # print(sys.getdefaultencoding())
 
        # pdf = FPDF()
        # pdf.add_page()
        # pdf.set_font('Arial', 'B', 16)
        # pdf.cell(40, 10, vcards_out.encode('utf-8', ignore).decode('latin-1'))
        # # pdf.output('example1.pdf', dest='F').encode('utf-8')
        # pdf.output('example1.pdf', 'F')


if __name__ == '__main__':
    run()
