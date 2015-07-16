# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier, Vincent Renaville, Nicolas Bessi
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
import time
from openerp.osv import fields, osv
from openerp.report import report_sxw

class crm_helpdesk(osv.osv):
    _inherit = 'crm.helpdesk'
    
    def label_print(self, cr, uid, ids, context=None):
         datas = {
              'ids': ids,
              'model': 'crm.helpdesk',
              'form': self.read(cr, uid, ids[0], context=context)
         }
         return {
             'type': 'ir.actions.report.xml',
#             'report_name': 'Address_label',
              'report_name': 'crm_label_helpdesk',
             'datas': datas,
             'nodestroy' : True
         }
 
crm_helpdesk()

class icy_claim_address_label(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(icy_claim_address_label, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
        })

report_sxw.report_sxw('report.crm_label_helpdesk',
                       'crm.helpdesk',
                       'addons/icy_claim_address_label/report/icy_claim_address_label.mako',
                       parser=icy_claim_address_label, 
                      header="external")
