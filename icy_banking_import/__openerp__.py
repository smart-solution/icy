#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "icy_banking_import",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Generic Modules/Base",
    "description": """
""",
    "depends" : ["base","account"],
    "update_xml" : [
        'icy_banking_import_view.xml',
#        'security/icy_banking_import_security.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
