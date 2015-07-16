#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Contracts",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Generic Modules/Base",
    "description": """This module allows to define an invoicing schedule for a contract. The screen Contracts To Invoice allows to review the planned invoice schedule until a defined date, to select the invoices to be created, and to create the invoices.""",
    "depends" : ["project","account_analytic_analysis"],
    "update_xml" : [
        'icy_contracts_data.xml',
        'icy_contracts_view.xml',
        ],
    "active": False,
    "installable": True
}
