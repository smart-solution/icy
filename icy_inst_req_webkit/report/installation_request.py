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

from openerp.report import report_sxw
from openerp import pooler
from openerp.osv import osv, fields

class crm_installation_request(osv.osv):
    _inherit = 'crm.installation.request'

    def installation_request_print(self, cr, uid, ids, context=None):
        datas = {
             'ids': ids,
             'model': 'crm.installation.request',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'crm.installatie_aanvraag',
            'datas': datas,
            'nodestroy' : True
        }

class installatie_aanvraag(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(installatie_aanvraag, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
        })

report_sxw.report_sxw('report.crm_installatie_aanvraag',
                       'crm.installation.request',
                       'addons/icy_inst_req_webkit/report/installation_request.mako',
                       parser=installatie_aanvraag, 
                      header="external")
