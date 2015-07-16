#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.tools.translate import _
from openerp.osv import fields, osv
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openerp.netsvc

class contract_type(osv.osv):
    _name = 'contract.type'
    _description = 'Type Contract'

    _columns = { 
        'name': fields.char('Name', size=32, required=True, select=True, searchable=True),
        'note': fields.text('Tekst'),
        'type': fields.selection([('contract', 'Contract'),('project', 'Project')], 'Type', required=True),
        'years': fields.integer('Aantal jaren'),
        'cost_account_id': fields.many2one('account.account', 'Grootboekrekening', required=True),
        'tax_code_id': fields.many2one('account.tax', 'Tax Code', required=True),
        'text_ids': fields.one2many('contract.texts', 'contract_type_id', 'Teksten'),
    }

contract_type()

class contract_texts(osv.osv):
    _name = 'contract.texts'
    _description = 'Teksten Contract'

    _columns = { 
        'contract_type_id': fields.many2one('contract.type', 'Contract Type', select=True),
        'sequence': fields.integer('Volgnummer'),
        'name': fields.char('Naam', required=True),
        'prefix': fields.char('Prefix', size=6), 
        'text': fields.text('Tekst 1', required=True),
        'text2': fields.text('Tekst 2'),
        'bold': fields.boolean('Vet'),
        'underlined': fields.boolean('Onderlijnd'),
        'page_skip_after': fields.boolean('Gevolgd door bladsprong'),
        'product_table': fields.boolean('Producttabel'),
        'field_ids': fields.one2many('contract.text.fields', 'contract_text_id', 'Te vervangen teksten'),
    }

    _order = 'contract_type_id, sequence'

contract_texts()

class contract_text_fields(osv.osv):
    _name = 'contract.text.fields'

    _columns = {
        'contract_text_id': fields.many2one('contract.texts', 'Contract Tekst', select=True),
        'label': fields.char('Label'),
        'dbfield': fields.text('DB Rubriek'),
    }

contract_text_fields()

class account_analytic_schedule_line(osv.osv):
    _name = 'account.analytic.schedule.line'
    _description = 'Account Analytic Schedule Line'

    def action_invoice_create(self, cr, uid, ids, states=None, date_invoice = False, context=None):
        schedule_obj = self.pool.get('account.analytic.schedule.line')
        analytic_account_obj = self.pool.get('account.analytic.account')
        res_partner_obj = self.pool.get('res.partner')
        account_payment_term_obj = self.pool.get('account.payment.term')
        invoice_obj = self.pool.get('account.invoice')
        product_obj = self.pool.get('product.product')
        pro_price_obj = self.pool.get('product.pricelist')
        fiscal_pos_obj = self.pool.get('account.fiscal.position')
        product_uom_obj = self.pool.get('product.uom')
        invoice_line_obj = self.pool.get('account.invoice.line')
        invoices = []
        if context is None:
            context = {}

        for line in self.pool.get('account.analytic.schedule.line').browse(cr, uid, ids, context=context):
            partner = line.analytic_account_id.partner_id
            if (not partner) or not (line.analytic_account_id.pricelist_id):
                raise osv.except_osv(_('Analytic Account incomplete'),
                        _('Please fill in the Partner or Customer and Sale Pricelist fields in the Analytic Account:\n%s') % (account.name,))

            date_due = False
            if partner.property_payment_term:
                pterm_list= account_payment_term_obj.compute(cr, uid,
                        partner.property_payment_term.id, value=1,
                        date_ref=date_invoice)
                if pterm_list:
                    pterm_list = [term[0] for term in pterm_list]
                    pterm_list.sort()
                    date_due = pterm_list[-1]

            curr_invoice = {
                'name': line.analytic_account_id.name,
                'partner_id': line.analytic_account_id.partner_id.id,
                'payment_term': partner.property_payment_term.id or False,
                'account_id': partner.property_account_receivable.id,
                'currency_id': line.analytic_account_id.pricelist_id.currency_id.id,
                'date_invoice': date_invoice,
                'date_due': date_due,
                'fiscal_position': partner.property_account_position.id 
            }
            last_invoice = invoice_obj.create(cr, uid, curr_invoice, context=context)
            invoices.append(last_invoice)

            taxes = [line.tax_code_id]
            print'TAXES:',taxes
            tax = fiscal_pos_obj.map_tax(cr, uid, line.analytic_account_id.partner_id.property_account_position, taxes, context=context)

            account_id = line.cost_account_id.id
            if not account_id:
                raise osv.except_osv(_("Configuration Error"), _("No income account defined for product '%s'") % product.name)
            curr_line = {
                'price_unit': line.amount,
                'quantity': 1,
                'discount':0,
                'invoice_line_tax_id': [(6,0,tax )],
                'invoice_id': last_invoice,
                'name': line.name,
                'account_id': account_id,
                'account_analytic_id': line.analytic_account_id.id,
            }

            invoice_line_obj.create(cr, uid, curr_line, context=context)
            cr.execute("update account_analytic_schedule_line set invoice_id = %s WHERE id = %s", (last_invoice, line.id,))

            invoice_obj.button_reset_taxes(cr, uid, [last_invoice], context)
        return invoices

    def _progress_invoice_pct(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for project in self.browse(cr, uid, ids):
            res[project.id] = 0.0
            if project.id:
                if project.amount_max == 0:
                    res[project.id] = 0
                else:
                    res[project.id] = 100 * project.ca_invoiced / project.amount_max
        return res

    def default_get(self, cr, uid, fields, context=None):
        res = super(account_analytic_schedule_line, self).default_get(cr, uid, fields, context=context)
        res['cost_account_id'] = 458
        res['tax_code_id'] = 1
        return res

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account', 'Contract', select=True),
        'scheduled_date': fields.date('Geplande Datum', required=True),
        'name': fields.char('Omschrijving', size=64, required=True),
        'amount': fields.float('Bedrag', required=True),
        'cost_account_id': fields.many2one('account.account', 'Grooboekrekening', required=True),
        'tax_code_id': fields.many2one('account.tax', 'Tax Code', required=True),
        'invoice_date': fields.date('Factuur Datum'),
        'invoice_id': fields.many2one('account.invoice', 'Factuur', select=True),
        'amount_max': fields.related('analytic_account_id', 'est_total', type='float', relation='account.analytic.account', string='Verwacht Bedrag', readonly=True),
        'total_sched_amount': fields.related('analytic_account_id', 'total_sched_amount', type='float', relation='account.analytic.account', string='Gepland Bedrag', readonly=True),
        'ca_invoiced': fields.related('analytic_account_id', 'invoiced_total', type='float', relation='account.analytic.account', string='Gefactureerd Bedrag', readonly=True),
        'remaining_ca': fields.related('analytic_account_id', 'remaining_total', type='float', relation='account.analytic.account', string='Saldo', readonly=True),
        'progress_invoice_pct': fields.function(_progress_invoice_pct, string='% Gefactureerd', type='float'),
    }

account_analytic_schedule_line()

class contract_products(osv.osv):
    _name = 'contract.products'

    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account', 'Contract', select=True),
        'product_id': fields.many2one('product.product', 'Product', select=True),
        'qty_contract': fields.float('Aantal'),
        'unit_price': fields.float('Prijs'),
    }

    def onchange_product(self, cr, uid, ids, product_id, context=None):
        res = {}
        sql_stat = 'select list_price from product_product, product_template where product_product.id = %d and product_template.id = product_tmpl_id' % (product_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            if sql_res['list_price']:
                res['unit_price'] = sql_res['list_price']
        return {'value':res}

contract_products()

class account_analytic_account(osv.osv):
    _inherit = 'account.analytic.account'

    _columns = {
        'invoice_schedule': fields.boolean('Facturatieschema'),
        'total_sched_amount': fields.float('Gepland Bedrag'),
        'total_yearly_amount': fields.float('Jaarlijks Bedrag'),
        'invoice_schedule_line_ids': fields.one2many('account.analytic.schedule.line', 'analytic_account_id', 'Lijnen Facturatieschema'),
        'contract_type_id': fields.many2one('contract.type', 'Contract Type', select=True),
        'signature_customer_id': fields.many2one('res.partner', 'Ondergetekende Klant', select=True),
        'address_contract': fields.char('Plaatsadres'),
        'product_ids': fields.one2many('contract.products', 'analytic_account_id', 'Producten'),
        'contract_pct': fields.float('Contract percentage'),
        'years': fields.integer('Aantal jaren'),
        'date_first_invoice': fields.date('Datum 1ste factuur'),
    }

    _defaults = {
        'code': None,
    }

    def create(self, cr, uid, vals, context=None):
        seq_id = None
        if 'contract_type_id' in vals:
            type_id = self.pool.get('contract.type').search(cr, uid, [('id','=',vals['contract_type_id'])])
            for type in self.pool.get('contract.type').browse(cr, uid, type_id, context=context):
                if type.type == 'contract':
                    name = 'Contracten'
                else:
                    name = 'Projecten'
                seq_id = self.pool.get('ir.sequence').search(cr, uid, [('name','=',name)])
        if seq_id:
            vals['code'] = self.pool.get('ir.sequence').next_by_id(cr, uid, seq_id, context)
        else:
            vals['code'] = self.pool.get('ir.sequence').next_by_id(cr, uid, 1, context)

        return super(account_analytic_account, self).create(cr, uid, vals, context=context)

    def onchange_contract_type(self, cr, uid, ids, contract_type_id, context=None):
        res = {}
        sql_stat = 'select years from contract_type where id = %d' % (contract_type_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            if sql_res['years']:
                res['years'] = sql_res['years']
        return {'value':res}

    def recalc_amount(self, cr, uid, ids, context=None):
        for line in self.pool.get('account.analytic.account').browse(cr, uid, ids, context=context):
            total_amount = 0.00
            for prod in line.product_ids:
                total_amount += prod.unit_price * prod.qty_contract
            yearly_amount = round((total_amount * line.contract_pct / 100), 2)
            amount_contract = yearly_amount * line.years

        self.write(cr, uid, ids, {'total_sched_amount': amount_contract, 'total_yearly_amount': yearly_amount}, context=context)
        return True

    def create_invoice_schedule(self, cr, uid, ids, context=None):
        for line in self.pool.get('account.analytic.account').browse(cr, uid, ids, context=context):
            if not line.invoice_schedule_line_ids:
                if line.date_first_invoice:
                    sched_obj = self.pool.get('account.analytic.schedule.line')
                    analytic_account_id = line.id
                    name = line.name
                    amount = line.total_yearly_amount
                    cost_account_id = line.contract_type_id.cost_account_id.id
                    tax_code_id = line.contract_type_id.tax_code_id.id
                    scheduled_date = line.date_first_invoice
                    sched = datetime.strptime(scheduled_date, "%Y-%m-%d").date()

                    year = 0
                    total_amount = 0
                    while year < line.years:
                        print 'SCHED:', scheduled_date
                        stat_id = sched_obj.create(cr, uid, {
                            'analytic_account_id': analytic_account_id,
                            'scheduled_date': sched,
                            'name': name,
                            'amount': amount,
                            'cost_account_id': cost_account_id,
                            'tax_code_id': tax_code_id,
                        }, context=context)
                        year += 1
                        sched = sched + relativedelta(years=1)
                        total_amount += amount

                    self.write(cr, uid, ids, {'fix_price_invoices': True, 'amount_max': total_amount}, context=context)
        return True

account_analytic_account()

class contract_make_invoice(osv.osv_memory):
    _name = "contract.make.invoice"
    _description = "Contract Make Invoice"

    def make_invoices(self, cr, uid, ids, context=None):
        contract_obj = self.pool.get('account.analytic.schedule.line')
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        newinv = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        contract_obj.action_invoice_create(cr, uid, context.get(('active_ids'), []), date_invoice = data['invoice_date'])

        for o in contract_obj.browse(cr, uid, context.get(('active_ids'), []), context=context):
            newinv.append(o.invoice_id.id)

        result = mod_obj.get_object_reference(cr, uid, 'account', 'action_invoice_tree1')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['domain'] = "[('id','in', ["+','.join(map(str,newinv))+"])]"

        return result

    _columns = {
        'invoice_date': fields.date('Factuurdatum'),
    }

contract_make_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:# -*- coding: utf-8 -*-

