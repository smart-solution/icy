# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier, Bessi Nicolas, Vincent Renaville
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{   'name': 'Claim Address label using Webkit Library',
    'version': '1.1.0',
    'category': 'Reports/Webkit',
    'description': """
        Replaces the legacy rml Invoice report by a brand new webkit report.
    """,
    'author': 'Smartsolution',
    'website': 'http://www.smartsolution.com',
    'depends': ['base', 'report_webkit', 'base_headers_webkit', 'crm','crm_helpdesk', 'partner_zip_address'],
    'data': ['security/ir.model.access.csv',
             'icy_claim_address_label_report.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
