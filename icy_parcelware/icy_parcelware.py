#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################
import base64

from openerp.osv import osv, fields

class export_parcelware(osv.osv_memory):
    """ Export parcelware """
    _name = "export.parcelware"
    _description = "Export parcelware"

    def _get_file_name(self, cr, uid, context=None):
        print "DEFAULT CONTEXT:",context
        if context.get('active_id', False):
            return 'parcelware.csv'
        return ''
    
    def _get_file_data(self, cr, uid, context=None):
        if context.get('file_save', False):
            return base64.encodestring(context['file_save'].encode('utf8'))
        return ''
    
    _columns = {
	'filename_field': fields.char('File Name', size=32),
        'msg': fields.text('File created', size=64, readonly=True),
        'file_save': fields.binary('Save File'),
    }

    _defaults = {
        'msg': 'Save the File.',
        'file_save': _get_file_data,
        'filename_field': _get_file_name,
    }
    
    def create_file(self, cr, uid, ids, context=None):
        obj_stock_picking = self.pool.get('stock.picking')
        mod_obj = self.pool.get('ir.model.data')

        sp = obj_stock_picking.browse(cr, uid, context['active_id'])

        if context is None:
            context = {}

        print "CONTEXT:",context

        data_of_file = """id;contents;date;initials;last_name;email;street;house_number;house_number_addition;zip_code;city;land;afz;ord""" 
        count_lines = 0
        for lines in sp.move_lines:
            zipc = lines.partner_id.zip.replace(' ','')
            if lines.partner_id.first_name:
                initial = lines.partner_id.first_name[0:1]
            else:
                initial = ''
            if lines.partner_id.last_name:
                lastn = lines.partner_id.last_name
            else:
                lastn = ''
            if lines.partner_id.email:
                email = lines.partner_id.email
            else:
                email = ''
            if lines.partner_id.street:
                str = lines.partner_id.street
            else:
                str = ''
            if lines.partner_id.street_nbr:
                hn = lines.partner_id.street_nbr.replace(' ','')
                str = str.replace(hn,'')
            else:
                hn = ''
            if lines.partner_id.street_bus:
                hna = lines.partner_id.street_bus
            else:
                hna= ''
            if lines.partner_id.country_id.code:
                lnd = lines.partner_id.country_id.code
            else:
                lnd = ''
            afz = '3'
            ord = ''
            if lines.sale_line_id:
                afz = '2'
                ord = lines.sale_line_id.order_id.name
            if lines.helpdesk_id:
                afz = '1'
            lines_data = {
                          'id': lines.id,
                          'dat': sp.date_done,
                          'aant': lines.product_qty,
                          'product': lines.product_id.name,
                          'initial': initial,
                          'lastn': lastn,
                          'email': email,
                          'str': str,
                          'hn': hn,
                          'hna': hna,
                          'zip': zipc,
                          'city': lines.partner_id.city,
                          'lnd': lnd,
                          'afz': afz,
                          'ord': ord,
                         }
            data_of_file += '\n%(id)s;%(aant)s*%(product)s;%(dat)s;%(initial)s;%(lastn)s;%(email)s;%(str)s;%(hn)s;%(hna)s;%(zip)s;%(city)s;%(lnd)s;%(afz)s;%(ord)s' % (lines_data)
        model_data_ids = mod_obj.search(cr, uid, [('model', '=', 'ir.ui.view'), ('name', '=', 'view_parcelware_save')], context=context)
        resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'], context=context)[0]['res_id']
        context['file_save'] = data_of_file
        return {
            'name': 'Save parcelware file',
            'context': context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'export.parcelware',
            'views': [(resource_id, 'form')],
            'view_id': 'view_parcelware_save',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

export_parcelware()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

