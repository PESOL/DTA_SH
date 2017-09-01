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


def import_partner(doc):
    partner_obj = client.model('res.partner')
    state_obj = client.model('res.country.state')
    currency_obj = client.model('res.currency')
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
        # D.N.I. / N.I.F.
        vat = get(row, 'b').replace('-', '')
        # Nombre
        name = get(row, 'c')
        # Dirección
        street = get(row, 'd')
        # Provincia
        state_name = get(row, 'e')
        state_ids = state_obj.search([('name', '=', state_name)])
        state_id = state_ids and state_ids[0] or False
        # Población
        city = get(row, 'f')
        # C.Postal
        zip = get(row, 'g')
        # Teléfono
        phone = get(row, 'h')
        # Fax
        fax = get(row, 'i')
        # Pais
        country_code = get(row, 'j')
        country_ids = country_obj.search(
            [('code', '=', country_code)])
        country_id = country_ids and country_ids[0] or False
        # Forma de pago
        payment_mode = get(row, 'k')
        # TODO
        # Descripción forma de pago
        payment_mode_desc = get(row, 'l')
        # TODO
        # Divisa
        property_purchase_currency_name = get(row, 'm')
        currency_ids = currency_obj.search(
            [('name', '=', property_purchase_currency_name)])
        property_purchase_currency_name_id = currency_ids and currency_ids[
            0] or False
        # TODO IBAN de banco
        # ref = get(row, 'n')
        # TODO BIC de banc
        # ref = get(row, 'o')
        # TODO Nacional/Extranjero	Régimen IVA
        # ref = get(row, 'p')
        data = {
            'supplier': False,
            'customer': True,
            'ref': ref,
            'name': name,
            'street': street,
            'state_id': state_id,
            'city': city,
            'zip': zip,
            'phone': phone,
            'fax': fax,
        }
        try:
            partner = partner_obj.create(data)
        except Exception as e:
            print 'ERROR %s' % (ref)

        try:
            partner.write({'vat': vat})
        except Exception as e:
            try:
                partner.write({'vat': 'ES%s' % (vat)})
            except Exception as e:
                print 'ERROR VAT %s' % (vat)

        if i == 100:
            i = 0
            print 'Write ...[%d]' % (count,)

    print 'Update [%d] codes' % (count,)


if confirm('Import Partner'):
    with open('02_clientes.csv', 'r') as f:
        doc = csv.reader(f, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
        import_partner(doc)
