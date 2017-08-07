# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import http
from openerp.http import request


class DocumentPage(http.Controller):

    @http.route([
        '/document_page/<string:document_page_code>',
    ], type='http', auth='user', website=True)
    def scanner_call(self,
                     document_page_code=False,
                     **kwargs):
        # TODO: try
        document_page = request.env['document.page'].search([
            ('code', '=', document_page_code)
        ])
        return request.render(
            'website_document_page.document_page_template',
            {'document_page': document_page})
