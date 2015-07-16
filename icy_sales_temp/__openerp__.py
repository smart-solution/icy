#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Sales",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Base",
    "description": """
""",
    "depends" : ["base","sale","partner_zip_address","product","project","crm","sale_crm","crm_todo"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_sales_temp_view.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
