#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Stock Shortages",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Inventory",
    "description": """
""",
    "depends" : ["base","stock","purchase","mrp","procurement"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_stock_shortages_view.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
