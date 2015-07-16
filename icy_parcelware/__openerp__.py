#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Parcelware",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Stock",
    "description": """aanmaken file voor Parcelware vanaf stock.picking.out
""",
    "depends" : ["base","stock","partner_zip_address"],
#    "init_xml" : [],
     "update_xml" : [
         'icy_parcelware_view.xml',
#        'security/ir.model.access.csv'
         ],
    "active": False,
    "installable": True
}
