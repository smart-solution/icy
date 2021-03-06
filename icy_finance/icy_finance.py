#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
from datetime import datetime, date, time
from dateutil import parser

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    _columns = {
        'blocked_payment': fields.boolean('Geblokkeerd'),
    }

    _sql_constraints = [
            ('supplier_number_uniq', 'unique(supplier_invoice_number, partner_id, company_id, type)', 'Error! The supplier invoice reference number already exists for this supplier within this company!'),
    ]

    def create(self, cr, uid, vals, context=None):
        if 'journal_id' in vals and vals['journal_id'] == 4:
            if ((not 'partner_bank_id' in vals) or ('partner_bank_id' in vals and not vals['partner_bank_id'])) and 'partner_id' in vals:
                sql_stat = '''select id as partner_bank_id from res_partner_bank where partner_id =  %d order by sequence limit 1''' % (vals['partner_id'], )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res['partner_bank_id']:
                    vals['partner_bank_id'] = sql_res['partner_bank_id']
        return super(account_invoice, self).create(cr, uid, vals, context=context)

account_invoice()

class account_move_line(osv.osv):
    _inherit = 'account.move.line'

    def _function_blocked(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids):
            if inv.id:
                blocked = False
                sql_stat = "select blocked_payment from account_invoice where move_id = %d" % (inv.move_id.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    blocked = sql_res['blocked_payment']
                res[inv.id] = blocked
        return res

    _columns = {
        'blocked_payment': fields.function(_function_blocked, string='Geblokkeerd', type='boolean', select=True),
    }

account_move_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

