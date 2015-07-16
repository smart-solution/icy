#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Checklist",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Base",
    "description": """
""",
    "depends" : ["base","survey","crm","icy_sales"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_checklist_view.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
