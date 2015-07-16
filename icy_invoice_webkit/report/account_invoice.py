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

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def pakbon_print(self, cr, uid, ids, context=None):
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice_pakbon',
            'datas': datas,
            'nodestroy' : True
        }

class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'

    _columns = {
        'order_lines': fields.many2many('sale.order.line', 'sale_order_line_invoice_rel', 'invoice_id', 'order_line_id', 'Order Lines', readonly=True),
                }
    
class AccountInvoice_Report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(AccountInvoice_Report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
            'company_vat': self._get_company_vat,
        })


    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr, self.uid, self.uid).company_id.partner_id.vat
        if company_vat:
            return company_vat
        else:
            return False

report_sxw.report_sxw('report.account.invoice.webkit',
                      'account.invoice',
                      'icy_invoice_webkit/report/account_invoice.mako',
                      parser=AccountInvoice_Report)

class AccountInvoicePakbon_Report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(AccountInvoicePakbon_Report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
            'company_vat': self._get_company_vat,
        })


    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr, self.uid, self.uid).company_id.partner_id.vat
        if company_vat:
            return company_vat
        else:
            return False

report_sxw.report_sxw('report.account.invoice.pakbon.webkit',
                      'account.invoice.pakbon',
                      'icy_invoice_webkit/report/deliveryslip.mako',
                      parser=AccountInvoicePakbon_Report)
