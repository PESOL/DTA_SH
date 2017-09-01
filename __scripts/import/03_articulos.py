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
    product_obj = client.model('product.product')
    categ_obj = client.model('product.category')
    partner_obj = client.model('res.partner')
    categories_dict = {}
    supplier_dict = {}
    i = 0
    count = 0
    for row in doc:
        i += 1
        count += 1
        if (count == 0 and CSV_IGNNORE_FIRST_ROW):
            continue

        # Referencia Product
        default_code = get(row, 'a')
        # Descripción
        name = get(row, 'b')
        # COSTE
        standard_price = get(row, 'c')
        # Referencia Proveed
        product_supplier_code = get(row, 'd')
        # Código Proveedor
        # Nombre Proveedor
        supplier_code = get(row, 'e')
        supplier_id = supplier_dict.get(supplier_code)
        if not supplier_id:
            supplier = partner_obj.search(
                [('supplier', '=', True), ('ref', '=', supplier_code)])
            supplier_id = supplier and supplier.id
            supplier_dict.update({supplier_code: supplier_id})
        # Códig Familia
        # Nombre Familia
        category_name = get(row, 'h')
        categ_id = categories_dict.get(category_name)
        if not categ_id:
            categ_ids = categ_obj.search([('name', '=', category_name)])
            if not categ_ids:
                categ = categ_obj.create({'name': category_name})
                categ_id = categ.id
            else:
                categ_id = categ_ids[0] or False
            categories_dict.update({category_name: categ_id})
        # Fecha Alta
        # Bajo pedido
        # STOCK

        data = {
            'sale_ok': True,
            'purchase_ok': True,
            'default_code': default_code,
            'name': name,
            'standard_price': standard_price,
            'barcode': product_supplier_code,
            'categ_id': categ_id,
        }
        if supplier_id:
            supplier_data = {
                'name': supplier_id,
                'price': standard_price,
                'product_code': product_supplier_code
            }
            data.update({'seller_ids': [(0, 0, supplier_data)]})
        try:
            product = product_obj.create(data)
        except Exception as e:
            print 'ERROR %s' % (default_code)

        if i == 100:
            i = 0
            print 'Write ...[%d]' % (count,)

    print 'Update [%d] codes' % (count,)


if confirm('Import products'):
    with open('03_articulos.csv', 'r') as f:
        doc = csv.reader(f, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
        import_partner(doc)
