#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class purchase_order_texts(osv.osv):
    _name = 'purchase.order.texts'
    _description = 'Teksten Inkooporder'

    _columns = { 
        'name': fields.char('Name', size=32, required=True, select=True, searchable=True),
        'note': fields.text('Tekst'),
    }

purchase_order_texts()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    def _function_delivery_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                state = 'Geleverd'
                sql_stat = '''select distinct purchase_order.id from purchase_order, purchase_order_line, stock_move where purchase_order.id = purchase_order_line.order_id and purchase_order_line.id = stock_move.purchase_line_id and stock_move.state = 'assigned' and purchase_order.id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    state = 'Open'
                    sql_stat = '''select distinct purchase_order.id from purchase_order, purchase_order_line, stock_move where purchase_order.id = purchase_order_line.order_id and purchase_order_line.id = stock_move.purchase_line_id and stock_move.state = 'done' and purchase_order.id =  %d''' % (po.id, )
                    cr.execute(sql_stat)
                    sql_res = cr.dictfetchone()
                    if sql_res:
                        state = 'Deellevering'
                sql_stat = '''select distinct purchase_order.id from purchase_order where state = 'draft' and purchase_order.id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    state = 'Offerte'
                res[po.id] = state
        return res

    _columns = {
        'delivery_state': fields.function(_function_delivery_state, string='Leverstatus', type='char'),
        'aanleiding': fields.text('Aanleiding'),
        'via_quotation': fields.boolean('Offerte'),
        'incoterm': fields.many2one('stock.incoterms', 'Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions."),
        'purchase_order_text_id': fields.many2one('purchase.order.texts', 'Tekst Inkooporder', select=True),
        'po_text': fields.text('Tekst'),
    }

    def onchange_po_text(self, cr, uid, ids, po_text_id, context=None):
        res = {}
        sql_stat = 'select note from purchase_order_texts where id = %d' % (po_text_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            if sql_res['note']:
                res['po_text'] = sql_res['note']
        return {'value':res}

    def onchange_partner_id(self, cr, uid, ids, partner_id):
        if not partner_id:
            return False

        res = super(purchase_order, self).onchange_partner_id( cr, uid, ids, partner_id)

        sql_stat = '''select purchase_order_text_id, purchase_order_texts.note from res_partner, purchase_order_texts where res_partner.id = %d and res_partner.purchase_order_text_id = purchase_order_texts.id''' % (partner_id, )
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            res['value']['po_text'] = sql_res['note']
            res['value']['purchase_order_text_id'] = sql_res['purchase_order_text_id']

        return res

purchase_order()

class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'

    def _supplier_product_nbr(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                product = ''
                sql_stat = '''select product_code from purchase_order_line, purchase_order, product_product, product_supplierinfo where purchase_order_line.order_id = purchase_order.id and purchase_order_line.product_id = product_product.id and product_product.product_tmpl_id = product_supplierinfo.product_id and product_supplierinfo.name = purchase_order.partner_id and purchase_order_line.id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    print sql_res
                    product = sql_res['product_code']
                res[po.id] = product
        return res

    def _manufacturer_product_nbr(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                product = ''
                sql_stat = '''select manufacturer_part_nbr from purchase_order_line, purchase_order, product_product, product_supplierinfo where purchase_order_line.order_id = purchase_order.id and purchase_order_line.product_id = product_product.id and product_product.product_tmpl_id = product_supplierinfo.product_id and product_supplierinfo.name = purchase_order.partner_id and purchase_order_line.id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    product = sql_res['manufacturer_part_nbr']
                res[po.id] = product
        return res

    def _manufacturer_product(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            if po.id:
                product = ''
                sql_stat = '''select manufacturer from purchase_order_line, purchase_order, product_product, product_supplierinfo where purchase_order_line.order_id = purchase_order.id and purchase_order_line.product_id = product_product.id and product_product.product_tmpl_id = product_supplierinfo.product_id and product_supplierinfo.name = purchase_order.partner_id and purchase_order_line.id =  %d''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    product = sql_res['manufacturer']
                res[po.id] = product
        return res

    _columns = {
        'icy_value': fields.related('product_id', 'icy_value', type='char', string='Value', readonly=True),
        'icy_package': fields.related('product_id', 'icy_package', type='char', string='Package', readonly=True),
        'icy_smd_tht': fields.related('product_id', 'icy_smd_tht', type='char', string='SMD/THT', readonly=True),
        'supplier_product_nbr': fields.function(_supplier_product_nbr, string='Lev.Prod.', type='char'),
        'manufacturer_product_nbr': fields.function(_manufacturer_product_nbr, string='Fabr.Prod.', type='char'),
        'manufacturer_product': fields.function(_manufacturer_product, string='Fabrikant', type='char'),
        'order_state': fields.related('order_id', 'state', type='char', relation='purchase.order', string='Order State', readonly=True),
    }

purchase_order_line()

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    _columns = {
        'pct_underdelivery': fields.integer('% Underdelivery'),
        'pct_overdelivery': fields.integer('% Overdelivery'),
        'subcontractor': fields.boolean('Subcontractor'),
		'purchase_quotation_ids': fields.one2many('purchase.order', 'partner_id', 'Inkoopoffertes', select=True, domain=['|',('state','=','draft'),('state','=','cancel')]),
		'purchase_order_ids': fields.one2many('purchase.order', 'partner_id', 'Inkooporders', select=True, domain=[('state','!=','draft'),('state','!=','cancel')]),
		'purchase_invoice_ids': fields.one2many('account.invoice', 'partner_id', 'Inkoopfacturen', select=True, domain=[('type','=','in_invoice')]),
	    'product_ids': fields.one2many('product.supplierinfo', 'name', 'Product Prices', select=True),
        'purchase_order_text_id': fields.many2one('purchase.order.texts', 'Tekst Inkooporder', select=True),
    }

res_partner()

class product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'

    def _first_price(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line_id in ids:
            res[line_id] = 0.00
            sql_stat = "select price from pricelist_partnerinfo where suppinfo_id = %d order by min_quantity limit 1" % (line_id)
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
	        	res[line_id] = sql_res['price']
        return res

    def _product_ref(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line_id in ids:
            sql_stat = "select default_code from product_supplierinfo, product_product where product_supplierinfo.id = %d and product_id = product_product.id" % (line_id)
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
	        	res[line_id] = sql_res['default_code']
        return res

    _columns = {
	    'first_price': fields.function(_first_price, string='Bedrag Prijslijst', type='float'),
	    'product_ref': fields.function(_product_ref, string='Referentie', type='char'),
    }

product_supplierinfo()

class stock_move_split(osv.osv):
    _name = 'stock.move.split'
    _inherit = 'stock.move.split'

    _columns = {
        'date_expected': fields.date('Date Expected')
    }

stock_move_split()

class stock_move_split_lines(osv.osv):
    _name = 'stock.move.split.lines'
    _inherit = 'stock.move.split.lines'

    _columns = {
        'date_expected': fields.date('Date Expected')
    }

stock_move_split_lines()

####################################################################################################################
# TO BE VERIFIED IF MOVING DATE EXPECTED CAN BE SOLVED ANOTHER WAY THAN COPYING THE CLASS FROM STOCK_MOVE.PY       #
####################################################################################################################
class split_in_production_lot(osv.osv_memory):
    _inherit = "stock.move.split"
    _description = "Split in Serial Numbers"

    def split(self, cr, uid, ids, move_ids, context=None):
        """ To split stock moves into serial numbers

        :param move_ids: the ID or list of IDs of stock move we want to split
        """
        if context is None:
            context = {}
        assert context.get('active_model') == 'stock.move',\
             'Incorrect use of the stock move split wizard'
        inventory_id = context.get('inventory_id', False)
        prodlot_obj = self.pool.get('stock.production.lot')
        inventory_obj = self.pool.get('stock.inventory')
        move_obj = self.pool.get('stock.move')
        new_move = []
        for data in self.browse(cr, uid, ids, context=context):
            for move in move_obj.browse(cr, uid, move_ids, context=context):
                move_qty = move.product_qty
                quantity_rest = move.product_qty
                uos_qty_rest = move.product_uos_qty
                new_move = []
                if data.use_exist:
                    lines = [l for l in data.line_exist_ids if l]
                else:
                    lines = [l for l in data.line_ids if l]
                total_move_qty = 0.0
                for line in lines:
                    quantity = line.quantity
                    date_expected = line.date_expected
                    total_move_qty += quantity
                    if total_move_qty > move_qty:
                        raise osv.except_osv(_('Processing Error!'), _('Serial number quantity %d of %s is larger than available quantity (%d)!') \
                                % (total_move_qty, move.product_id.name, move_qty))
                    if quantity <= 0 or move_qty == 0:
                        continue
                    quantity_rest -= quantity
                    uos_qty = quantity / move_qty * move.product_uos_qty
                    uos_qty_rest = quantity_rest / move_qty * move.product_uos_qty
                    if quantity_rest < 0:
                        quantity_rest = quantity
                        self.pool.get('stock.move').log(cr, uid, move.id, _('Unable to assign all lots to this move!'))
                        return False
                    default_val = {
                        'product_qty': quantity,
                        'product_uos_qty': uos_qty,
                        'state': move.state,
                        'date_expected': date_expected,
                        'date': date_expected,
                    }
                    if quantity_rest > 0:
                        current_move = move_obj.copy(cr, uid, move.id, default_val, context=context)
                        if inventory_id and current_move:
                            inventory_obj.write(cr, uid, inventory_id, {'move_ids': [(4, current_move)]}, context=context)
                        new_move.append(current_move)

                    if quantity_rest == 0:
                        current_move = move.id
                    prodlot_id = False
                    if data.use_exist:
                        prodlot_id = line.prodlot_id.id
                    if not prodlot_id:
                        prodlot_id = prodlot_obj.create(cr, uid, {
                            'name': line.name,
                            'product_id': move.product_id.id},
                        context=context)

                    move_obj.write(cr, uid, [current_move], {'prodlot_id': prodlot_id, 'state':move.state})

                    update_val = {}
                    if quantity_rest > 0:
                        update_val['product_qty'] = quantity_rest
                        update_val['product_uos_qty'] = uos_qty_rest
                        update_val['state'] = move.state
                        move_obj.write(cr, uid, [move.id], update_val)

        return new_move

split_in_production_lot()
####################################################################################################################

class survey(osv.osv):
    _name = 'survey'
    _inherit = 'survey'

    def create(self, cr, uid, vals, context=None):
        vals['max_response_limit'] = 999999
        vals['response_user'] = 999999
        return super(survey, self).create(cr, uid, vals, context=context)

    _columns = {
    }

survey()

class survey_response(osv.osv):
    _name = 'survey.response'
    _inherit = 'survey.response'

    _defaults = {
        'stock_move_id': lambda self,cr,uid,context:context.get('stock_move_id',False),
        'product_id': lambda self,cr,uid,context:context.get('product_id',False),
    }

    _columns = {
        'stock_move_id': fields.many2one('stock.move', 'Stock Move', select=True),
        'product_id': fields.many2one('product.product', 'Product', select=True),
    }

survey_response()

class survey_name_wiz(osv.osv):
    _name = 'survey.name.wiz'
    _inherit = 'survey.name.wiz'

    _defaults = {
        'stock_move_id': lambda self,cr,uid,context:context.get('stock_move_id',False),
        'product_id': lambda self,cr,uid,context:context.get('product_id',False),
    }

    _columns = {
        'stock_move_id': fields.many2one('stock.move', 'Stock Move', select=True),
        'product_id': fields.many2one('product.product', 'Product', select=True),
    }

survey_name_wiz()

class survey_question_wiz(osv.osv):
    _name = 'survey.question.wiz'
    _inherit = 'survey.question.wiz'

    _defaults = {
        'stock_move_id': lambda self,cr,uid,context:context.get('stock_move_id',False),
        'product_id': lambda self,cr,uid,context:context.get('product_id',False),
    }

    def action_next(self, cr, uid, ids, context=None):
        sql_stat = "select response from survey_name_wiz where id = %d" % context.get('sur_name_id',False)
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            resp_id = int(sql_res['response'])
            if context.has_key('product_id'):
                self.pool.get('survey.response').write(cr, uid, resp_id, {'product_id':context.get('product_id',False)})
            if context.has_key('active_model'):
                if context.get('active_model') == 'stock.move':
                    self.pool.get('survey.response').write(cr, uid, resp_id, {'stock_move_id':context.get('active_id',False)})
            if context.has_key('stock_move_id'):
                self.pool.get('survey.response').write(cr, uid, resp_id, {'stock_move_id':context.get('stock_move_id',False)})

        return super(survey_question_wiz, self).action_next(cr, uid, ids, context=context)

    _columns = {
        'stock_move_id': fields.many2one('stock.move', 'Stock Move', select=True),
        'product_id': fields.many2one('product.product', 'Product', select=True),
    }

survey_question_wiz()

class product_product(osv.osv):
    _inherit = "product.product"

    def answer_checklist(self, cr, uid, ids, context=None):
            ir_model_data_obj = self.pool.get('ir.model.data')
            ir_model_data_id = ir_model_data_obj.search(cr, uid,
                [['model', '=', 'ir.ui.view'],
                 ['name', '=', 'view_survey_name']],
                context=context)
            res_id = ir_model_data_obj.read(cr, uid, ir_model_data_id,
                                            fields=['res_id'])[0]['res_id']

            if isinstance(ids, list):
                ids = ids[0]

            product = self.browse(cr, uid, ids, context=context)
            product_id = product.id

            context.update({'product_id': product.id})

            return {
                'name': 'Answer Checklist',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [res_id],
                'res_model': 'survey.name.wiz',
                'context': context,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
            }

    _columns = {'survey_ids' : fields.one2many('survey.response', 'product_id', 'Checklists'),
	}

product_product()

class stock_move(osv.osv):
    _inherit = "stock.move"

    def answer_checklist(self, cr, uid, ids, context=None):
            print'ACSM:',context
            ir_model_data_obj = self.pool.get('ir.model.data')
            ir_model_data_id = ir_model_data_obj.search(cr, uid,
                [['model', '=', 'ir.ui.view'],
                 ['name', '=', 'view_survey_name']],
                context=context)
            res_id = ir_model_data_obj.read(cr, uid, ir_model_data_id,
                                            fields=['res_id'])[0]['res_id']

            if isinstance(ids, list):
                ids = ids[0]

            move = self.browse(cr, uid, ids, context=context)
            print 'MOVE:',move
            product_id = move.product_id.id
            move_id = move.id

            context.update({'product_id': product_id})
            context.update({'stock_move_id': move_id})
            print 'CONTEXT:',context

            return {
                'name': 'Answer Checklist',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [res_id],
                'res_model': 'survey.name.wiz',
                'context': context,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
            }

    def _function_exp_inv_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            amount = 0.00
            if po.id:
                sql_stat = '''select (stock_move.product_qty * purchase_order_line.price_unit) as amount from stock_move, purchase_order_line where stock_move.id = %d and purchase_order_line.id = stock_move.purchase_line_id''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    amount = sql_res['amount']
            res[po.id] = amount
        return res

    _columns = {
        'survey_ids' : fields.one2many('survey.response', 'stock_move_id', 'Checklists'),
        'product_desc': fields.related('product_id', 'name_template', type='char', string='Omschrijving', readonly=True),
        'icy_value': fields.related('product_id', 'icy_value', type='char', string='Value', readonly=True),
        'icy_package': fields.related('product_id', 'icy_package', type='char', string='Package', readonly=True),
        'icy_smd_tht': fields.related('product_id', 'icy_smd_tht', type='char', string='SMD/THT', readonly=True),
        'expected_invoice_amount': fields.function(_function_exp_inv_amount, string='Verwacht factuurbedrag', type='float'),
	}

stock_move()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    def _function_exp_inv_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            amount = 0.00
            if po.id:
                sql_stat = '''select sum(stock_move.product_qty * purchase_order_line.price_unit) as amount from stock_picking, stock_move, purchase_order_line where stock_picking.id = %d and stock_move.picking_id = stock_picking.id and purchase_order_line.id = stock_move.purchase_line_id''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    amount = sql_res['amount']
            res[po.id] = amount
        return res

    _columns = {
        'reason_return': fields.text('Reden retour'),
        'expected_return_date': fields.date('Datum gewenste ontvangst'),
        'expected_invoice_amount': fields.function(_function_exp_inv_amount, string='Verwacht factuurbedrag', type='float'),
    }

stock_picking()

class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'

    _columns = {
        'reason_return': fields.text('Reden retour'),
        'expected_return_date': fields.date('Datum gewenste ontvangst'),
    }

stock_picking_out()

class stock_picking_in(osv.osv):
    _inherit = 'stock.picking.in'

    def _function_exp_inv_amount(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            amount = 0.00
            if po.id:
                sql_stat = '''select sum(stock_move.product_qty * purchase_order_line.price_unit) as amount from stock_picking, stock_move, purchase_order_line where stock_picking.id = %d and stock_move.picking_id = stock_picking.id and purchase_order_line.id = stock_move.purchase_line_id''' % (po.id, )
                cr.execute(sql_stat)
                sql_res = cr.dictfetchone()
                if sql_res:
                    amount = sql_res['amount']
            res[po.id] = amount
        return res

    _columns = {
        'expected_invoice_amount': fields.function(_function_exp_inv_amount, string='Verwacht factuurbedrag', type='float'),
    }

stock_picking_in()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

