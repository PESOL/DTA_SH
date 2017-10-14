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

parameter_obj = client.model('ir.config_parameter')

param_ids = parameter_obj.search([('key', '=', 'database.expiration_date')])
parameter_obj.write(param_ids, {'value': '2017-012-30 08:11:01'})
