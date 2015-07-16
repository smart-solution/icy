#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Finance",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Base",
    "description": """
""",
    "depends" : ["base","account"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_finance_view.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
