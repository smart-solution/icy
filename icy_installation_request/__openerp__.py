#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ICY Installation Request",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Helpdesk",
    "description": """
""",
    "depends" : ["base","icy_service","mail"],
#    "init_xml" : [],
    "update_xml" : [
        'icy_installation_request_data.xml',
        'icy_installation_request_view.xml',
	"security/ir.model.access.csv",
        ],
    "active": False,
    "installable": True
}
