#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields

class product_template(osv.osv):
    _inherit = 'product.template'

    _columns = {
        'unique_name': fields.char('Unique Name', size=256, translate=True),
    }

product_template()

class product_product(osv.osv):
    _inherit = 'product.product'

#    def name_get(self, cr, uid, ids, context=None):
#        if not ids:
#            return []
#        res = []
#        for r in self.read(cr, uid, ids, ['id', 'icy_value', 'icy_package', 'icy_smd_tht', 'name_template'], context):
#            if r['name_template']:
#                aux = r['name_template']
#            else:
#                aux = _(r['id'])  
#
#            aux +=  " ("
#            if r['icy_value']:
#                aux += _(r['icy_value']) 
#            if r['icy_package']:
#                aux +=  ' - '
#                aux += _(r['icy_package']) 
#            if r['icy_smd_tht']:
#                aux +=  ' - '
#                aux += _(r['icy_smd_tht']) 
#            aux += ')'
#
#            res.append((r['id'], aux)) 
#
#        return res

    _columns = {
        'unique_name': fields.char('Unique Name', size=256, translate=True),
        'icy_value': fields.char('Value', size=256, translate=True, select=True),
        'icy_package': fields.char('Package', size=64, translate=True, select=True),
        'icy_smd_tht': fields.char('SMD/THT', size=16, translate=True, select=True),
        'product_description_sale': fields.text('Productomschrijving Offerte', translate=True),
        'description_pricelist': fields.text('Prijslijst Tekst', translate=True),
        'description_email': fields.text('Email Tekst', translate=True),
        'description_phone': fields.text('Telefoon Tekst', translate=True),
        'description_sale_cc': fields.text('Productomschrijving CC Offerte', translate=True),
    }

product_template()

class product_product(osv.osv):
    _inherit = 'product.product'

    _columns = {
        'dtl_description': fields.char('Dtl. Description', size=128, translate=True),
    }

product_product()

class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'

    _columns = {
        'dtl_description': fields.char('Dtl. Description', size=128, translate=True),
        'icy_value': fields.related('product_id', 'icy_value', type='char', relation='product.product', string='Value', readonly=True),
        'icy_package': fields.related('product_id', 'icy_package', type='char', relation='product.product', string='Package', readonly=True),
        'icy_smd_tht': fields.related('product_id', 'icy_smd_tht', type='char', relation='product.product', string='SMD/THT', readonly=True),
    }

mrp_bom()

class product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'

    _columns = {
        'manufacturer': fields.char('Manufacturer', size=64),
        'manufacturer_part_nbr': fields.char('Manufacturer Part No.', size=64),
        'manufacturer_priority': fields.integer('Manufacturer Prioriteit'),
    }

product_supplierinfo()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

