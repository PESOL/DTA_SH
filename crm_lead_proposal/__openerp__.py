# -*- encoding: utf-8 -*-

{
    'name': "CRM Lead Proposal",
    'version': "10.0.1.0.0",
    'author': "PESOL",
    'category': 'CRM',
    'description': """
CRM Lead Proposal
    """,
    'license': "AGPL-3",
    'depends': [
        'crm',
        'report'
    ],
    'data': [
        'views/crm_lead_proposal_view.xml',
        'views/report_proposal.xml'
    ],
    'installable': True,
}
