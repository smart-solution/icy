#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Custom Development",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Base",
    "description": """
""",
    "depends" : ["base","product","mrp","base_setup"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_custom_view.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
