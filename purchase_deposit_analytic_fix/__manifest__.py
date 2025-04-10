# -*- coding: utf-8 -*-
{
    'name': 'Purchase Deposit Analytic Fix',
    'version': '17.0.1.0.0',
    'summary': 'Ensures analytic account from PO lines is passed to deposit move lines.',
    'description': """
        This module patches the purchase_deposit module to correctly copy
        the analytic distribution from the first relevant Purchase Order line
        to the corresponding account move line created for the deposit payment.
        This helps satisfy analytic requirements set by modules like account_analytic_required.

        IMPORTANT: The Python code in this module is a template and might
        need adjustments based on the specific version and implementation
        of your 'purchase_deposit' module.
    """,
    'category': 'Accounting/Accounting',
    'author': 'Variate Solar IT Team', # You can change this
    'license': 'LGPL-3', # Or AGPL-3 if purchase_deposit is AGPL-3
    'depends': [
        'purchase_deposit', # MAKE SURE this is the exact technical name of your OCA module
    ],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
