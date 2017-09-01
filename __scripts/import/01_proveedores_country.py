# -*- coding: utf-8 -*-
import sys
import erppeek
import csv

SERVER = 'http://localhost:8069'
DATABASE = 'dta'
USERNAME = 'admin'
PASSWORD = 'r6WuUet2'
CSV_DELIMITER = ','
CSV_QUOTECHAR = '"'
CSV_IGNNORE_FIRST_ROW = True
DEBUG = False  # Solo importa las 10 primeras lineas

# Conectar al ERP
client = erppeek.Client(SERVER, DATABASE, USERNAME, PASSWORD)


def get(row, column, ttype='str'):
    def format_str(value):
        return str(value)

    def format_float(value):
        try:
            return float(value)
        except:
            try:
                return float(str(value).replace(',', '.'))
            except:
                try:
                    import string
                    all = string.maketrans('', '')
                    nodigs = all.translate(all, string.digits)
                    return float(str(value).translate(all, nodigs))
                except:
                    return 0.00

    cols = list('abcdefghijklmnopqrstuvwxyz')
    icol = 0
    for col in column.lower():
        icol += cols.index(col) + len(cols)
    icol = icol - len(cols)
    try:
        value = row[icol]
        if ttype == 'str':
            return format_str(value)
        elif ttype == 'float':
            return format_float(value)
    except:
        return None


def confirm(question, default='yes'):
    valid = {'y': True, 'ye': True, 'yes': True, 's': True,
             'si': True, 'sí': True, 'n': False, 'no': False}

    if default not in valid:
        prompt = " [y/n] "
    elif valid[default]:
        prompt = " [Y/n] "
    else:
        prompt = " [y/N] "

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def import_partner_country(doc):
    partner_obj = client.model('res.partner')
    country_obj = client.model('res.country')
    i = 0
    count = 0
    for row in doc:
        i += 1
        count += 1
        if (count == 0 and CSV_IGNNORE_FIRST_ROW):
            continue

        # Código
        ref = get(row, 'a')
        partner_ids = partner_obj.search([
            ('ref', '=', ref)
        ])
        # Pais
        country_code = get(row, 'b')
        country_ids = country_obj.search([('code', '=', country_code)])
        country_id = country_ids and country_ids[0] or False

        if country_id:
            partner_obj.write(partner_ids, {'country_id': country_id})
        if i == 100:
            i = 0
            print 'Write ...[%d]' % (count,)

    print 'Update [%d] codes' % (count,)


if confirm('Import Partner Country'):
    with open('01_proveedores_country.csv', 'r') as f:
        doc = csv.reader(f, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
        import_partner_country(doc)
