#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
import datetime
from datetime import timedelta
from datetime import date
from time import mktime, strptime

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'

    def _running_availability(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            res[move.id] = 0.00
            if move.id:
                if move.product_id:
                    if move.product_id.move_ids:
                        qty_mv = 0.00
                        for m in move.product_id.move_ids:
                            if m.valid_shortage: # and m.state in ('confirmed','waiting','assigned','draft'):
#                                if m.date_expected <= move.date_expected:
                                if m.date <= move.date:
                                    if m.location_id.usage == 'internal':
                                        qty_mv = qty_mv - m.product_qty
                                    if m.location_dest_id.usage == 'internal':
                                        qty_mv = qty_mv + m.product_qty
                        res[move.id] = move.product_id.qty_available + qty_mv
        return res

    def _product_shortage(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            res[move.id] = False
            if move.id:
                if move.running_availability < 0.00:
                    res[move.id] = True
        return res

    def _minimum_stock(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            if move.id and move.product_id:
                minqty = 0.00
                res[move.id] = move.product_id.minimum_stock
        return res

    def _valid_shortage(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            if move.id and move.product_id:
                sel = False
                if move.state in ('confirmed','waiting','assigned','draft'):
                    if move.location_id.usage == 'internal' or move.location_dest_id.usage == 'internal':
                        if move.location_id.usage == 'view' or move.location_dest_id.usage == 'view':
                            sel = False
                        else:
                            sel = True
                res[move.id] = sel
        return res

    def _disp_partner(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            if move.id and move.partner_id:
                res[move.id] = move.partner_id.id
        return res

    def _disp_source_location(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            if move.id and move.location_id:
                res[move.id] = move.location_id.name
        return res

    def _disp_dest_location(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for move in self.browse(cr, uid, ids):
            if move.id and move.location_dest_id:
                res[move.id] = move.location_dest_id.name
        return res

    _columns = {
		'product_shortage': fields.function(_product_shortage, string='Shortage', type='boolean', select=True),
		'running_availability': fields.function(_running_availability, string='Running Availability', type='float'),
		'minimum_stock': fields.function(_minimum_stock, string='Sum Min.Stock Rules', type='float',select=True,store=True),
		'valid_shortage': fields.function(_valid_shortage, string='Selected for Shortage', type='boolean',select=True,store=True),
        'disp_partner_id': fields.function(_disp_partner, type='many2one', relation="res.partner", string='Partner', select=True),
        'disp_source_location': fields.function(_disp_source_location, type='char', string='Source Location', select=True),
        'disp_dest_location': fields.function(_disp_dest_location, type='char', string='Destination Location', select=True),
    }

    _order = 'date desc, id desc'

stock_move()

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    def _product_shortage(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for product in self.browse(cr, uid, ids):
            res[product.id] = False
            if product.id:
                minqty = 0.00
                if product.orderpoint_ids:
                    for op_ids in product.orderpoint_ids:
                        minqty = minqty + op_ids.product_min_qty
                if product.move_ids:
                    for move_ids in product.move_ids:
                        if move_ids.valid_shortage:
#                            if move_ids.running_availability < product.minimum_stock:
                            if move_ids.running_availability < minqty:
                                res[product.id] = True
                else:
                    if minqty > (product.virtual_available + product.qty_draft_wo + product.qty_draft_po + product.qty_po_req):
                        res[product.id] = True
        return res

    def _minimum_stock(self, cr, uid, ids, name, arg, context=None):
        res = {}
        minqty = 0.00
        for product in self.browse(cr, uid, ids):
            res[product.id] = False
            if product.id:
                minqty = 0.00
                if product.orderpoint_ids:
                    for op_ids in product.orderpoint_ids:
                        minqty = minqty + op_ids.product_min_qty
        res[product.id] = minqty
        return res

    def _calc_main_supplier(self, cr, uid, ids, fields, arg, context=None):
        result = {}
        for product in self.browse(cr, uid, ids, context=context):
            main_supplier = self._get_main_product_supplier(cr, uid, product, context=context)
            result[product.id] = main_supplier and main_supplier.name.id or False
        return result

    def _qty_draft_po(self, cr, uid, ids, name, arg, context=None):
        res = {}
        qty = 0.00
        for product in self.browse(cr, uid, ids, context=context):
            qty = 0.00
            sql_stat = "select sum(purchase_order_line.product_qty) as qty from purchase_order_line, purchase_order where purchase_order_line.product_id =  %d and order_id = purchase_order.id and purchase_order.state = 'draft' and (purchase_order.origin = '' or purchase_order.origin IS NULL)" % (product, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['qty']:
                    qty = sql_res['qty']
            res[product.id] = qty
        return res

    def _qty_po_req(self, cr, uid, ids, name, arg, context=None):
        res = {}
        qty = 0.00
        for product in self.browse(cr, uid, ids, context=context):
            qty = 0.00
            sql_stat = "select sum(product_qty) as qty from purchase_requisition_line, purchase_requisition where product_id =  %d and requisition_id = purchase_requisition.id and purchase_requisition.state = 'draft'" % (product, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['qty']:
                    qty = sql_res['qty']
            res[product.id] = qty
        return res

    def _qty_draft_wo(self, cr, uid, ids, name, arg, context=None):
        res = {}
        qty = 0.00
        for product in self.browse(cr, uid, ids, context=context):
            qty = 0.00
            sql_stat = "select sum(product_qty) as qty from mrp_production where product_id =  %d and state = 'draft'" % (product, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['qty']:
                    qty = sql_res['qty']
            res[product.id] = qty
        return res

    _columns = {
		'product_shortage': fields.function(_product_shortage, string='Shortage', type='boolean', select=True, store=True),
		'move_ids': fields.one2many('stock.move', 'product_id', 'Stock Moves', select=True, domain=[('valid_shortage','=',True)]),
        'seller_purchase_order_ids': fields.related('seller_id', 'purchase_order_ids', type="one2many", obj="purchase.order", domain=[('state','=','draft')]),
        'manufacturing_order_ids': fields.one2many('mrp.production', 'product_id', 'Manufacturing Orders', select=True),
        'purchase_order_line_ids': fields.one2many('purchase.order.line', 'product_id', 'Purchase Orders', select=True, domain=[('state','=','draft')]),
		'minimum_stock': fields.function(_minimum_stock, string='Sum Min.Stock Rules', type='float', select=True, store=True),
        'main_supplier_id': fields.function(_calc_main_supplier, type='many2one', relation="res.partner", string='Main Supplier', select=True, store=True),
		'qty_draft_wo': fields.function(_qty_draft_wo, string='Qty. Draft WO', type='float', select=True),
		'qty_draft_po': fields.function(_qty_draft_po, string='Qty. Draft PO', type='float', select=True),
		'qty_po_req': fields.function(_qty_po_req, string='Qty. PO Req.', type='float', select=True),
        'default_order_qty': fields.float('Default order qty.'),
        'multiple_order_qty': fields.float('Multiple order qty.'),
        'qty_to_order': fields.float('Qty to order'),
        'date_to_order': fields.date('Date to order'),
        'purchase_requisition_ids': fields.one2many('purchase.requisition', 'line_product_id', 'Purchase Requisitions', domain=[('state','=','open')]),
        'all_partner_id': fields.many2one('res.partner', 'All Partners', select=True),
    }

    def create_wo(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product').browse(cr, uid, ids)
        for product in product_obj:
            bom_id = 0
            sql_stat = "select id from mrp_bom where product_id = %d and type = 'normal'" % (product.id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['id']:
                    bom_id = sql_res['id']

            pr = self.pool.get('mrp.production')
            pr_id = pr.create(cr, uid, {
                'product_uos_qty': 0.00,
                'product_uom': product.product_tmpl_id.uom_id.id,
                'product_qty': product.qty_to_order,
                'product_id': product.id,
                'user_id': uid,
                'location_src_id': 13, #product.product_tmpl_id.property_mrp_location,
                'date_planned': product.date_to_order + ' 0:00:00',
                'cycle_total': 0.00,
                'company_id': 1,
#                'priority': 1,
                'state': 'draft',
                'hour_total': 0.00,
                'location_dest_id': 13, #product.product_tmpl_id.property_mrp_location,
                'bom_id': bom_id,
                'allow_reorder': False
            },context=context)
            product_obj2 = self.pool.get('product.product')
            product_ids = product_obj2.search(cr, uid, [('id','=',product.id)], context=context)
            for product2 in product_ids:
                product_obj2.write(cr, uid, product2, {'product_shortage': False})
            return True

    def create_pr(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product').browse(cr, uid, ids)
        for product in product_obj:
            seq_id = self.pool.get('ir.sequence').search(cr, uid, [('code','=','purchase.order.requisition')])
            seqnbr = self.pool.get('ir.sequence').next_by_id(cr, uid, seq_id, context)
            pr = self.pool.get('purchase.requisition')
            pr_id = pr.create(cr, uid, {
                'origin': '[' + product.default_code + '] ' + product.name_template,
                'exclusive': 'exclusive',
                'user_id': uid,
                'message_follower_ids': False,
                'date_end': False,
                'date_start': product.date_to_order,
                'company_id': 1,
                'warehouse_id': 1,
                'state': 'draft',
                'line_ids':  [[0, False, {'product_uom_id': product.product_tmpl_id.uom_id.id, 'product_id': product.id, 'product_qty': product.qty_to_order, 'name': product.name_template}]],
                'message_ids': False,
                'description': False, 
                'name': seqnbr
            },context=context)
            product_obj2 = self.pool.get('product.product')
            product_ids = product_obj2.search(cr, uid, [('id','=',product.id)], context=context)
            for product2 in product_ids:
                product_obj2.write(cr, uid, product2, {'product_shortage': False})
            return True

    def create_pol(self, cr, uid, ids, context=None):
        product_obj = self.pool.get('product.product').browse(cr, uid, ids)
        for product in product_obj:
            if product.all_partner_id:
                partner_selected = product.all_partner_id.id
            else:
                partner_selected = product.main_supplier_id.id

            order_id = 0
            sql_stat = "select id from purchase_order where purchase_order.partner_id = %d and state = 'draft' order by date_order desc limit 1" % (partner_selected, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['id']:
                    order_id = sql_res['id']
            
            setup_cost = 0
            unit_price = 0
            sql_stat = "select price from product_supplierinfo, pricelist_partnerinfo where product_supplierinfo.name =  %d and product_id = %d and product_supplierinfo.id = suppinfo_id order by pricelist_partnerinfo.min_quantity asc limit 1" % (partner_selected, product.product_tmpl_id.id)
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['price']:
                    unit_price = sql_res['price']

            if order_id == 0:
                po = self.pool.get('purchase.order')
                po_id = po.create(cr, uid, {
                    'shipped': False,
                    'warehouse_id': 1,
                    'date_order': date.today(),
                    'location_id': 12,
#                    'fiscal_position': product.main_supplier_id.fiscal_position,
                    'amount_untaxed': 0.00,
                    'partner_id': partner_selected,
                    'company_id': 1,
                    'amount_tax': 0.00,
                    'invoice_method': 'picking',
                    'state': 'draft',
                    'pricelist_id': 2,
                    'amount_total': 0.00,  
                    'journal_id': 2,
                    'accept_amount': False,
#                    'payment_term_id': product.main_supplier_id.payment_term_id.id
                },context=context)
                order_id = po_id

            if order_id != 0:
                pr = self.pool.get('purchase.order.line')
                pr_id = pr.create(cr, uid, {
                    'product_id': product.id,
                    'product_uom': product.product_tmpl_id.uom_id.id,
                    'date_planned': product.date_to_order,
                    'order_id': order_id, 
                    'name': '[' + product.default_code + '] ' + product.name_template,
                    'price_unit': unit_price,
                    'product_qty': product.qty_to_order,
                    'supplier_uom_id': product.product_tmpl_id.uom_id.id,
                    'discount': 0,
                    'account_analytic_id': False,
                    'taxes_id': [[6, False, [14]]],
                    'description': False, 
                },context=context)

            product_obj2 = self.pool.get('product.product')
            product_ids = product_obj2.search(cr, uid, [('id','=',product.id)], context=context)
            for product2 in product_ids:
                product_obj2.write(cr, uid, product2, {'product_shortage': False})
            return True

product_product()

class product_shortage_compute_all(osv.osv_memory):
    _name = 'product.shortage.compute.all'

    _columns = {
    }

    def recalc_shortage(self, cr, uid, ids, context=None):
        print 'START CALCULATE SHORTAGE'
        result = {}
        product_obj = self.pool.get('product.product')
        product_ids = product_obj.search(cr, uid, [('active','=',True)], context=context)

        print 'DATE TO ORDER'
#        for product_id in product_ids:
        for product in product_obj.browse(cr, uid, product_ids):
#            print 'PRODUCT: ', product.default_code, ' - ', product.name_template

            nbrdays = 0
            if product.product_tmpl_id.supply_method == 'buy':
                nbrdays = product.seller_delay or 0
            else:
                nbrdays = product.product_tmpl_id.produce_delay or 0

            qty_to_order = 0.00
#            if product.product_shortage:
            qty_to_shortage = 0.00
            default_order_qty = 0.00
            qty_shortage = product.minimum_stock - (product.virtual_available + product.qty_draft_wo + product.qty_draft_po + product.qty_po_req)
            if qty_shortage < product.default_order_qty:
                qty_to_order = product.default_order_qty
            else:
                if product.default_order_qty == 0.00:
                    if product.multiple_order_qty == 0.00:
                        default_order_qty = 1.00
                    else:
                        default_order_qty = product.multiple_order_qty
                else:
                    default_order_qty = product.default_order_qty
                if product.multiple_order_qty == 0.00:
                    qty_to_order = qty_shortage
                else:
                    qty_to_order = default_order_qty
                    while qty_to_order <= qty_shortage:
                        qty_to_order = qty_to_order + product.multiple_order_qty
            if qty_to_order < 0:
                qty_to_order == 0.00

            product_obj.write(cr, uid, product.id, {'date_to_order': date.today()+timedelta(days=nbrdays), 'qty_to_order': qty_to_order})

        print 'END CALCULATE SHORTAGE'
        return result

#        print 'MINIMUM STOCK'
#        product_obj._minimum_stock(cr, uid, product_ids, name=None, arg=None, context=context)
#        for product in product_ids:
#            product_obj.write(cr, uid, product, {'active': True})
#        print 'SHORTAGE'
#        product_obj._product_shortage(cr, uid, product_ids, name=None, arg=None, context=context)
#        for product in product_ids:
#            product_obj.write(cr, uid, product, {'active': True})
#        print 'MAIN SUPPLIER'
#        product_obj._calc_main_supplier(cr, uid, product_ids, fields=None, arg=None, context=context)
#        for product in product_ids:
#            product_obj.write(cr, uid, product, {'active': True})


product_shortage_compute_all()

class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'

    def _qty_available(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for bom in self.browse(cr, uid, ids):
            res[bom.id] = False
            res[bom.id] = bom.product_id.qty_available
        return res

    def _qty_virtual(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for bom in self.browse(cr, uid, ids):
            res[bom.id] = False
            res[bom.id] = bom.product_id.virtual_available
        return res

    _columns = {
		'qty_available': fields.function(_qty_available, string='Qty. Available', type='float', select=True),
		'qty_virtual': fields.function(_qty_virtual, string='Virtual Available', type='float', select=True),
    }

mrp_bom()

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

#    def default_get(self, cr, uid, fields, context=None):
#        data = super(purchase_order, self).default_get(cr, uid, fields, context)
#        return data

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        return super(purchase_order, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)

    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        #result =  super(purchase_order, self).read(cr, uid, ids, fields=fields, context=context, load=load)
        if context and 'default_product_id' in context and context['default_product_id']:
            self.write(cr, uid, ids, {'product_id':context['default_product_id']})
#            self.write(cr, uid, ids, {'product_id':context['default_product_id'], 'product_qty':context['default_product_qty'], 'supplier_qty': context['default_supplier_qty'], })
        #return result
        return super(purchase_order, self).read(cr, uid, ids, fields=fields, context=context, load=load)

    _columns = {
        'product_id': fields.many2one('product.product', 'Product', select=True),
#        'product_qty': fields.float('Order qty'),
#        'supplier_qty': fields.float('Supplier qty'),
    }

purchase_order()

class product_supplierinfo(osv.osv):
    _name = 'product.supplierinfo'
    _inherit = 'product.supplierinfo'

    _columns = {
		'supplier_lead_time': fields.integer('Supplier lead time'),
    }

product_supplierinfo()

class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'

    def create(self, cr, uid, vals, context=None):
        return super(purchase_order_line, self).create(cr, uid, vals, context=context)

purchase_order_line()

class purchase_requisition(osv.osv):
    _inherit = 'purchase.requisition'

    def _line_product(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            res[po.id] = 0
            if po.id and po.line_ids:
                line_count = 0
                for line in po.line_ids:
                    line_count = line_count + 1
                    if line_count == 1:
                        res[po.id] = line.product_id.id
                    else:
                        res = {}
            else:
                res = {}
        return res

    def _line_product_qty(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for po in self.browse(cr, uid, ids):
            res[po.id] = 0.00
            if po.id and po.line_ids:
                line_count = 0
                for line in po.line_ids:
                    line_count = line_count + 1
                    if line_count == 1:
                        res[po.id] = line.product_qty
                    else:
                        res = {}
            else:
                res = {}
        return res

    _columns = {
   	    'line_product_id': fields.function(_line_product, string='Product', type='many2one', relation='product.product', select=True, store=True),
        'line_product_qty': fields.function(_line_product_qty, string='Qty.', type='float', store=True),
    }

purchase_requisition()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

