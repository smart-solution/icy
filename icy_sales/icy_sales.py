#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
from datetime import datetime, date, time
from dateutil import parser

class sale_order_texts(osv.osv):
    _name = 'sale.order.texts'
    _description = 'Teksten Verkooporder'

    _columns = { 
        'name': fields.char('Name', size=32, required=True, select=True, searchable=True),
        'note': fields.text('Tekst'),
    }

sale_order_texts()

class sale_order_type(osv.osv):
    _name = 'sale.order.type'
    _description = 'Type Verkooporder'

    _columns = { 
        'name': fields.char('Name', size=32, required=True, select=True, searchable=True),
        'note': fields.text('Tekst'),
        'cc_quotation': fields.boolean('Control Center Offerte'),
    }

sale_order_type()

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'lead': fields.boolean('Lead'),
        'prospect': fields.boolean('Prospect'),
        'mailing_allowed': fields.boolean('Mailing'),
		'discount_ids': fields.one2many('res.partner.discount', 'partner_id', 'Kortingen'),
		'sales_quotation_ids': fields.one2many('sale.order', 'partner_id', 'Verkoopoffertes', select=True, domain=['|',('state','=','draft'),('state','=','cancel')]),
		'sales_order_ids': fields.one2many('sale.order', 'partner_id', 'Verkooporders', select=True, domain=[('state','!=','draft'),('state','!=','cancel')]),
		'sales_invoice_ids': fields.one2many('account.invoice', 'partner_id', 'Verkoopfacturen', select=True, domain=[('type','=','out_invoice')]),
		'icy_task_ids': fields.one2many('project.task', 'partner_id', 'Taken', select=True),
        'delivery_note_signature': fields.boolean('Handtekening Pakbon'),
        'sale_order_text_id': fields.many2one('sale.order.texts', 'Tekst Verkooporder', select=True),
        'sale_order_contact_id': fields.many2one('res.partner', 'Contact Verkooporder', select=True),
		'stock_picking_ids': fields.one2many('stock.picking', 'partner_id', 'Leveringen', select=True),
    }

res_partner()

class sale_order(osv.osv):
    _inherit = 'sale.order'

    def _function_week(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for week in self.browse(cr, uid, ids):
            if week.date_confirm:
                d = parser.parse(week.date_confirm)
                res[week.id] = (d.isocalendar()[0] * 100) + d.isocalendar()[1]
        return res

    def _function_amount_residual(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for so in self.browse(cr, uid, ids):
            amount_residual = so.amount_total
            if so.invoice_ids:
                amount_invoiced = 0.00
                for inv in so.invoice_ids:
                    amount_invoiced = amount_invoiced + inv.amount_total
                if amount_invoiced > amount_residual:
                    amount_residual = 0.00
                else:
                    amount_residual = amount_residual - amount_invoiced
            res[so.id] = amount_residual
        return res

    def _function_invoiced_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for so in self.browse(cr, uid, ids):
            inv_state = ''
            if so.invoiced_rate == 0.00:
                inv_state = 'Geen'
            else:
                if so.invoiced or so.invoiced_rate == 100.00:
                    inv_state = 'Gefactureerd'
                else:
                    inv_state = 'Deelfacturatie (' + str(round(so.invoiced_rate, 0)) + '%)'
            res[so.id] = inv_state
        return res

    _columns = {
        'note_footer': fields.text('Voettekst'),
        'date_expected': fields.date('Leverdatum'),
        'date_callback': fields.date('Nabeldatum'),
        'write_date': fields.datetime('Schrijfdatum'),
        'first_quotation': fields.boolean('Met Offerte'),
        'prepayment_pct': fields.integer('Aanbetaling %'),
        'callback_user_id': fields.many2one('res.users', 'Nabellen door', select=True),
        'exp_decision_rate': fields.selection([('50', '50%'),('75', '75%'),('90', '90%')], 'Slagingspercentage'),
        'exp_decision_date': fields.date('Verwachte Valdatum'),
        'partner_category_id': fields.related('partner_id', 'category_id', type="many2many", obj="res.partner.category"),
        'salesrep_id': fields.related('partner_id','user_id',type="many2one",relation="res.users",string="Account Manager",store=True),
        'contact_id': fields.many2one('res.partner', 'Ter attentie van', select=True),
        'week': fields.function(_function_week, string='Week', type='integer', select=True, store=True),
        'create_uid': fields.many2one('res.users', 'Behandelaar', select=True),
        'so_type_id': fields.many2one('sale.order.type', 'Type Verkooporder', select=True),
        'amount_residual': fields.function(_function_amount_residual, string='Netto saldo', type='float'),
        'cc_product_id': fields.many2one('product.product', 'CC Product', select=True),
        'cc_amount': fields.char('CC Bedrag'),
        'cc_quotation': fields.boolean('CC Offerte'),
#        'delivery_state': fields.function(_function_delivery_state, string='Lev.status', type='char'),
        'invoiced_state': fields.function(_function_invoiced_state, string='Fact.status', type='char', store=True),
    }

#    def create(self, cr, uid, vals, context=None):
#        res = super(sale_order, self).create(cr, uid, vals, context=context)
#        prc = self.browse(cr, uid, res)
#        if prc.user_id:
#            if prc.partner_id and prc.date_callback:
#                task = self.pool.get('project.task')
#                task_id = task.create(cr, uid, {
#                    'date_deadline': prc.date_callback,
#                    'sequence': 1,
#                    'user_id': prc.user_id.id,
#                    'partner_id': prc.partner_id.id,
#                    'sale_order_id': prc.id,
#                    'company_id': prc.company_id.id,
#                    'state': 'open',
#                    'stage_id': 1,
#                    'name': 'Nabellen',
#                    'description': 'Nabellen offerte %s voor klant %s' % (prc.name, prc.partner_id.name), 
#                },context=context)
#        print 'TASK CREATED'
#        return res

    def onchange_so_type(self, cr, uid, ids, so_type_id, context=None):
        res = {}
        sql_stat = 'select cc_quotation from sale_order_type where id = %d' % (so_type_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            if sql_res['cc_quotation']:
                res['cc_quotation'] = True
            else:
                res['cc_quotation'] = False
#                res['cc_product_id'] = None
#                res['cc_amount'] = 0.00
        return {'value':res}

    def onchange_payment_term(self, cr, uid, ids, payment_term, context=None):
        res = {}
        sql_stat = 'select order_policy from account_payment_term where id = %d' % (payment_term, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            res['order_policy'] = sql_res['order_policy']
        return {'value':res}

    def onchange_icy_discount(self, cr, uid, ids, discount1, discount2, context=None):
        res = {}
        discount = 0.00
        if discount1 == 0.00:
            discount = discount2
        else:
            if discount2 == 0.00:
                discount = discount1
            else:
                discount = discount1 + (discount2 * (100 - discount1) / 100)
        res['discount'] = discount
        return {'value':res}

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        if not partner_id:
            return False

        res = super(sale_order, self).onchange_partner_id( cr, uid, ids, partner_id, context=context)

        sql_stat = '''select sale_order_contact_id from res_partner where id = %d''' % (partner_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            res['value']['contact_id'] = sql_res['sale_order_contact_id']

        sql_stat = '''select sale_order_texts.note from res_partner, sale_order_texts where res_partner.id = %d and res_partner.sale_order_text_id = sale_order_texts.id''' % (partner_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            res['value']['note_footer'] = sql_res['note']

        return res

sale_order()

class stock_move(osv.osv):
    _inherit = 'stock.move'

    def create(self, cr, uid, vals, context=None):
        if 'sale_line_id' in vals and vals['sale_line_id']:
            sale_line_obj = self.pool.get('sale.order.line')
            sale_line = sale_line_obj.browse(cr, uid, vals['sale_line_id'])
            if sale_line.date_expected:
                vals.update({'date_expected':sale_line.date_expected})        
            else:
                vals.update({'date_expected':sale_line.order_id.date_expected})  
        return super(stock_move, self).create(cr, uid, vals, context=context)

stock_move()

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def _function_qty_delivered(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for so in self.browse(cr, uid, ids):
            if so.id:
                qty_deliverd = 0.00
                sql_stat = "select sum(case when location_dest_id = 9 then product_qty else (product_qty * -1) end) as qty_delivered from stock_move where sale_line_id = %d and (location_dest_id = 9 or location_id = 9) and state = 'done'" % (so.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    qty_delivered = sql_res['qty_delivered']
                res[so.id] = qty_delivered
        return res

    _columns = {
        'date_expected': fields.date('Leverdatum'),
        'discount1': fields.float('Klantkorting'),
        'discount2': fields.float('Projectkorting'),
        'date_tbd': fields.boolean('N.T.B.'),
		'volume_dscnt_ids': fields.one2many('sale.order.line.volume.dscnt', 'order_line_id', 'Staffelprijzen'),
        'order_state': fields.related('order_id', 'state', type='char', relation='sale.order', string='Orderstatus', readonly=True),
        'qty_delivered': fields.function(_function_qty_delivered, string='Hoev. geleverd', type='float'),
    }

    _defaults = {
        'date_expected': lambda self,cr,uid,context:context.get('date_expected',False),
    }

    def onchange_icy_discount(self, cr, uid, ids, discount1, discount2, context=None):
        res = {}
        discount = 0.00
        if discount1 == 0.00:
            discount = discount2
        else:
            if discount2 == 0.00:
                discount = discount1
            else:
                discount = discount1 + (discount2 * (100 - discount1) / 100)
        res['discount'] = discount
        return {'value':res}

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):

        if not partner_id:
            return False
    	if not product:
	        return False

        res = super(sale_order_line, self).product_id_change( cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, flag, context=context)

        discount1 = 0.00

# partner category
        sql_stat = '''select discount_pct 
from res_partner_discount d, res_partner_res_partner_category_rel pcr 
where d.partner_category_id = pcr.category_id 
  and pcr.partner_id = %d 
  and d.partner_id IS NULL 
  and d.product_id IS NULL 
  and d.product_category_id IS NULL''' % (partner_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# product category
        sql_stat = '''select discount_pct 
from res_partner_discount d, product_product pp, product_template pt 
where d.product_category_id = pt.categ_id 
  and pt.id = pp.product_tmpl_id 
  and pp.id = %d 
  and d.product_id IS NULL 
  and d.partner_id IS NULL 
  and d.partner_category_id IS NULL''' % (product, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# partner
        sql_stat = '''select discount_pct 
from res_partner_discount d
where d.partner_id = %d 
  and d.partner_category_id IS NULL 
  and d.product_id IS NULL 
  and d.product_category_id IS NULL''' % (partner_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# product
        sql_stat = '''select discount_pct 
from res_partner_discount d
where d.product_id = %d 
  and d.partner_category_id IS NULL 
  and d.partner_id IS NULL 
  and d.product_category_id IS NULL''' % (product, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# partner category and product category
        sql_stat = '''select discount_pct 
from res_partner_discount d, res_partner_res_partner_category_rel pcr, product_product pp, product_template pt  
where d.partner_category_id = pcr.category_id 
  and pcr.partner_id = %d 
  and d.product_category_id = pt.categ_id 
  and pt.id = pp.product_tmpl_id 
  and pp.id = %d 
  and d.partner_id IS NULL 
  and d.product_id IS NULL''' % (partner_id, product, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# partner and product category
        sql_stat = '''select discount_pct 
from res_partner_discount d, product_product pp, product_template pt  
where d.partner_id = %d 
  and d.product_category_id = pt.categ_id 
  and pt.id = pp.product_tmpl_id 
  and pp.id = %d 
  and d.partner_category_id IS NULL 
  and d.product_id IS NULL''' % (partner_id, product)
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# partner category and product
        sql_stat = '''select discount_pct 
from res_partner_discount d, res_partner_res_partner_category_rel pcr 
where d.product_id = %d 
  and d.partner_category_id = pcr.category_id 
  and pcr.partner_id = %d 
  and d.partner_id IS NULL 
  and d.product_category_id IS NULL''' % (product, partner_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

# partner and product
        sql_stat = '''select discount_pct 
from res_partner_discount d
where d.partner_id = %d 
  and d.product_id = %d 
  and d.partner_category_id IS NULL 
  and d.product_category_id IS NULL''' % (partner_id, product, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            discount1 = sql_res['discount_pct']

        res['value']['discount1'] = discount1
        return res

sale_order_line()

class sale_order_line_volume_dscnt(osv.osv):
    _name = 'sale.order.line.volume.dscnt'

    _columns = {
        'order_line_id': fields.many2one('sale.order.line', 'Orderlijn', select=True),
        'qty_discount': fields.float('Hoeveelheid'),
        'volume_price': fields.float('Prijs'),
    }

sale_order_line_volume_dscnt()

class project_task(osv.osv):
    _inherit = 'project.task'

    def _function_write_date(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids):
            if task.id:
                sql_stat = '''select write_date from project_task where id =  %d''' % (task.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res['write_date']:
                    res[task.id] = sql_res['write_date']
        return res

    def _function_close_date(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids):
            if task.id:
                sql_stat = '''select write_date, state from project_task where id =  %d''' % (task.id, )
                print sql_stat
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                print sql_res['write_date']
                print sql_res['state']
                if sql_res['state'] != 'done':
                    res[task.id] = ''
                else:
                    if sql_res['write_date']:
                        res[task.id] = sql_res['write_date']
        return res

    def _function_user_name(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids):
            if task.id:
                sql_stat = '''select res_partner.name from project_task, res_users, res_partner where project_task.user_id = res_users.id and res_partner.id = res_users.partner_id and project_task.id =  %d''' % (task.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res['name']:
                    res[task.id] = sql_res['name']
        return res

    _columns = {
        'sale_order_id': fields.many2one('sale.order', 'Offerte/Order', select=True),
        'icy_lead_id': fields.many2one('crm.lead', 'Lead', select=True),
        'icy_close_date': fields.function(_function_close_date, string='Realisatie', type='date'),
        'icy_write_date': fields.function(_function_write_date, string='Gewijzigd', type='date'),
        'icy_user_name': fields.function(_function_user_name, string='Verantwoordelijke', type='char'),
        'context_id': fields.many2one('project.gtd.context', "Taaktype",help="The context place where user has to treat task"),
    }

project_task()

class res_partner_discount(osv.osv):
    _name = 'res.partner.discount'

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', select=True),
        'partner_category_id': fields.many2one('res.partner.category', 'Partner Categorie', select=True),
        'product_id': fields.many2one('product.product', 'Product', select=True),
        'product_category_id': fields.many2one('product.category', 'Product Categorie', select=True),
        'discount_pct': fields.float('Korting', select=True),
    }

res_partner_discount()

class product_product(osv.osv):
    _inherit = 'product.product'

    _columns = {
		'discount_ids': fields.one2many('res.partner.discount', 'product_id', 'Kortingen'),
    }

product_product()

class product_category(osv.osv):
    _inherit = 'product.category'

    _columns = {
		'discount_ids': fields.one2many('res.partner.discount', 'product_category_id', 'Kortingen'),
    }

product_category()

class res_partner_category(osv.osv):
    _inherit = 'res.partner.category'

    _columns = {
		'discount_ids': fields.one2many('res.partner.discount', 'partner_category_id', 'Kortingen'),
        'company_category': fields.boolean('Enkel bedrijven'),
    }

    _defaults = {
        'company_category': True,
    }

res_partner_category()

class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    def onchange_zip_id(self, cr, uid, ids, zip_id, context=None):
        res = {}
        if not zip_id:
            res['street'] = ""
            res['city'] = ""
            res['country_id'] = ""
            res['zip'] = ""
        else:
            city_obj = self.pool.get('res.country.city')
            city = city_obj.browse(cr, uid, zip_id, context=context)
            res['city'] = city.name
            res['country_id'] = city.country_id.id
            res['zip'] = city.zip
        return {'value':res}

    def onchange_street_id(self, cr, uid, ids, zip_id, street_id, street_nbr, street_bus, context=None):
        res = {}
        if not street_id:
            res['street'] = ""
        else:
            street_obj = self.pool.get('res.country.city.street')
            street = street_obj.browse(cr, uid, street_id, context=context)
            if street_nbr and street_bus:
                res['street'] = street.name + ' ' + street_nbr + street_bus
            else:
                if street_nbr:
                    res['street'] = street.name + ' ' + street_nbr
                else:
                    res['street'] = street.name
        return {'value':res}

    _columns = {
		'icy_task_ids': fields.one2many('project.task', 'icy_lead_id', 'Taken', select=True),
		'zip_id': fields.many2one('res.country.city', 'Postcode'),
		'street_id': fields.many2one('res.country.city.street', 'Straat'),
		'street_nbr': fields.char('Huisnummer', size=16),
		'street_bus': fields.char('Bus', size=16),
    }

crm_lead()

class account_payment_term(osv.osv):
    _inherit = 'account.payment.term'

    _columns = {
        'order_policy': fields.selection([('manual', 'Op verzoek'),('picking', 'Bij uitgaande levering'),('prepaid', 'Voor levering')], 'Default maak factuur'),
    }

account_payment_term()

class crm_meeting(osv.osv):
    _inherit = 'crm.meeting'

    def _function_meeting_report_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for meeting in self.browse(cr, uid, ids):
            if meeting.id:
                sql_stat = '''select case 
when date < now() and meeting_report IS NULL then 'To do' 
when date < now() then 'Gereed' 
else ' ' end as state 
from crm_meeting where id =  %d''' % (meeting.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res['state']:
                    res[meeting.id] = sql_res['state']
        return res

    _columns = {
        'meeting_report': fields.text('Bezoekverslag'),
        'meeting_report_state': fields.function(_function_meeting_report_state, string='Status Bezoekverslag', type='char'),
    }

crm_meeting()

class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _function_week(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for week in self.browse(cr, uid, ids):
            if week.date_invoice:
                d = parser.parse(week.date_invoice)
                res[week.id] = (d.isocalendar()[0] * 100) + d.isocalendar()[1]
        return res

    _columns = {
        'week': fields.function(_function_week, string='Week', type='integer', select=True, store=True),
    }

account_invoice()

#class stock_partial_picking(osv.osv_memory):
#    _inherit = "stock.partial.picking"
#
#    def do_partial(self, cr, uid, ids, context=None):
#        print 'DO PARTIAL'
#        res = {}
#        res = super(stock_partial_picking, self).do_partial( cr, uid, ids, context=context)
#
#        domain = None
#        pickings = []
#        for picking in self.browse(cr, uid, ids, context=context):
#            pickings.append(picking.picking_id.backorder_id.id)
#            domain = "['id','in',%d]" % (picking.picking_id.backorder_id.id, )
#
#        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'view_picking_out_tree')
#        action = self.pool.get(model).browse(cr, uid, action_id, context=context)
#        return {
#            'name': action.name,
#            'view_type': ['tree'],
#            'view_mode': 'tree,form,calendar',
#            'res_model': 'stock.picking.out',
#            'domain': domain, #action.domain,
#            'context': "{'default_type': 'out', 'contact_display': 'partner_address'}",
#            'type': 'ir.actions.act_window',
#            'search_view_id': 568,
#            'views': [566]
#        }
#
#stock_partial_picking()

class sale_advance_payment_inv(osv.osv_memory):
    _inherit = 'sale.advance.payment.inv'

    _columns = {
		'picking_id': fields.many2one('stock.picking', 'Uitgaande levering'),
		'sale_id': fields.many2one('sale.order', 'Verkooporder'),
    }

    def onchange_picking_id(self, cr, uid, ids, picking_id, context=None):
        res = {}
        amount = 0.00
        prepaid = 0.00
        if picking_id:
            picking = self.pool.get('stock.picking').browse(cr, uid, picking_id) 
            for move in picking.move_lines:
                if move.sale_line_id:
                    amount_line = move.product_qty * move.sale_line_id.price_unit * ((100.00 - move.sale_line_id.discount) / 100.00)
                    amount = amount + amount_line
                    prepaid = move.sale_line_id.order_id.prepayment_pct
        print 'PREPAID:',prepaid
        print 'AMOUNT:',amount
        amount = amount * ((100.00 - float(prepaid)) / 100.00)
        print 'AMOUNT:',amount
        res['amount'] = amount
        return {'value':res}

sale_advance_payment_inv()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

