#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Purchasing",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Purchase",
    "description": """
""",
    "depends" : ["base","purchase","stock","icy_custom"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_purchasing_view.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
