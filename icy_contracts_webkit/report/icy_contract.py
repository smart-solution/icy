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

class account_analytic_account(osv.osv):
    _inherit = 'account.analytic.account'

    def contract_request_print(self, cr, uid, ids, context=None):
        datas = {
             'ids': ids,
             'model': 'account.analytic.account',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'icy_contract',
            'datas': datas,
            'nodestroy' : True
        }

class icy_contracts(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(icy_contracts, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
        })

report_sxw.report_sxw('report.icy_contract',
                       'account_analytic.account',
                       'addons/icy_contracts_webkit/report/icy_contract.mako',
                       parser=icy_contracts, 
                      header="external")
