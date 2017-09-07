# encoding: utf-8
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Account Invoice Report Default",
    'version': "10.0.1.0.0",
    'author': "PESOL",
    'category': 'Custom Reporting',
    'description': """
This module allows set the invoice template.
    """,
    'license': "GPL-3",
    'depends': [
        'account',
        'base_layout_report_dta',
        'sale_layout_print_grouped'
    ],
    'data': [
        'views/report_invoice.xml',
    ],
    'installable': True,
}
