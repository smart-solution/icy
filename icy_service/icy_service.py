#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
import datetime
from datetime import timedelta
from datetime import date

class crm_case_section(osv.osv):
    _name = 'crm.case.section'
    _inherit = 'crm.case.section'

    _columns = {
        'helpdesk_category': fields.boolean('Helpdesk Categorie'),
		'incoming_via_id': fields.many2one('res.partner', 'Binnengekomen Via', select=True),
		'start_email_template_id': fields.many2one('email.template', 'Start Email Template', select=True),
		'end_email_template_id': fields.many2one('email.template', 'Eind Email Template', select=True),
    }

crm_case_section()

class crm_case_categ(osv.osv):
    _name = 'crm.case.categ'
    _inherit = 'crm.case.categ'

    _columns = {
        'probleem': fields.boolean('Probleem'),
        'uitleg': fields.boolean('Uitleg'),
        'reparatie': fields.boolean('Reparatie'),
        'algemeen': fields.boolean('Algemeen'),
        'klacht': fields.boolean('Klacht'),
        'logistiek': fields.boolean('Logistiek'),
        'omruil': fields.boolean('Omruil'),
        'toesturen': fields.boolean('Toesturen'),
        'product_ids': fields.many2many('product.product', 'product_case_categ_rel', 'case_categ_id', 'product_id', 'Producten'),
        'email_template_ids': fields.many2many('email.template', 'mail_template_case_categ_rel', 'case_categ_id', 'email_template_id', 'Email Templates'),
        'active': fields.boolean('Actief'),
        'notes': fields.text('Omschrijving'),
    }

    _defaults = {
        'active': True,
    }

crm_case_categ()

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    _columns = {
        'case_categ_ids': fields.many2many('crm.case.categ', 'product_case_categ_rel', 'product_id', 'case_categ_id', 'Helpdesk Categorieën'),
    }

product_product()

class crm_helpdesk(osv.osv):
    _name = 'crm.helpdesk'
    _inherit = 'crm.helpdesk'

    def onchange_incoming_via(self, cr, uid, ids, incoming_via_id, context=None):
        res = {}
        if incoming_via_id:
            sql_stat = "select id from crm_case_section where incoming_via_id = %d" % (incoming_via_id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['id']:
                res['section_id'] = sql_res['id']
        return {'value':res}

    def onchange_email_template(self, cr, uid, ids, email_template_id, email_template2_id, email_template3_id, email_template4_id, email_template5_id, gender, partner_id, section_id, context=None):
        res = {}
        email_body = ''
        if gender == 'm':
            email_body = 'Geachte heer'
        else:
            if gender == 'f':
                email_body = 'Geachte mevrouw'
            else:
                email_body = 'Geachte'
        if partner_id:
            partner_obj = self.pool.get('res.partner')
            partner = partner_obj.browse(cr, uid, partner_id, context=context)
            email_body = email_body + ' ' + partner.name + ','
        else:
            email_body = email_body + ','

        if section_id:
            section_obj = self.pool.get('crm.case.section')
            section = section_obj.browse(cr, uid, section_id, context=context)
            if section.start_email_template_id.email_body:
                email_body = email_body + section.start_email_template_id.email_body

        if email_template_id:
            mail_obj = self.pool.get('email.template')
            mail = mail_obj.browse(cr, uid, email_template_id, context=context)
            if mail.email_body:
                email_body = email_body + mail.email_body
        if email_template2_id:
            mail_obj = self.pool.get('email.template')
            mail = mail_obj.browse(cr, uid, email_template2_id, context=context)
            if mail.email_body:
                email_body = email_body + mail.email_body 
        if email_template3_id:
            mail_obj = self.pool.get('email.template')
            mail = mail_obj.browse(cr, uid, email_template3_id, context=context)
            if mail.email_body:
                email_body = email_body + mail.email_body 
        if email_template4_id:
            mail_obj = self.pool.get('email.template')
            mail = mail_obj.browse(cr, uid, email_template4_id, context=context)
            if mail.email_body:
                email_body = email_body + mail.email_body 
        if email_template5_id:
            mail_obj = self.pool.get('email.template')
            mail = mail_obj.browse(cr, uid, email_template5_id, context=context)
            if mail.email_body:
                email_body = email_body + mail.email_body
        
        if section_id:
            section_obj = self.pool.get('crm.case.section')
            section = section_obj.browse(cr, uid, section_id, context=context)
            if section.end_email_template_id.email_body:
                email_body = email_body + section.end_email_template_id.email_body

        if uid:
            user_obj = self.pool.get('res.users')
            user = user_obj.browse(cr, uid, uid, context=context)
            if user.partner_id:
                if user.partner_id.name:
                    email_body = email_body.replace('[user]', user.partner_id.name)

        res['email_body'] = email_body
        return {'value':res}

    def onchange_categ_id(self, cr, uid, ids, categ_id, context=None):
        res = {}
        categ_obj = self.pool.get('crm.case.categ')
        categ = categ_obj.browse(cr, uid, categ_id, context=context)
        print 'CATEG:',categ.name
        res['name'] = categ.name
        res['omruil'] = False
        res['toesturen'] = False
        if categ.omruil:
            res['omruil'] = True
            product_ids = []
            for product in categ.product_ids:
                product_ids.append(product.id)
            res['product_ids'] = product_ids
        if categ.toesturen:
            res['toesturen'] = True
            product_ids = []
            for product in categ.product_ids:
                product_ids.append(product.id)
            res['product_ids_send'] = product_ids
        template_ids = []
        for template in categ.email_template_ids:
            template_ids.append(template.id)
        res['email_template_ids'] = template_ids
        return {'value':res}

    def onchange_categ2_id(self, cr, uid, ids, categ_id, context=None):
        res = {}
        categ_obj = self.pool.get('crm.case.categ')
        categ = categ_obj.browse(cr, uid, categ_id, context=context)
        template_ids = []
        for template in categ.email_template_ids:
            template_ids.append(template.id)
        res['email_template2_ids'] = template_ids
        return {'value':res}

    def onchange_categ3_id(self, cr, uid, ids, categ_id, context=None):
        res = {}
        categ_obj = self.pool.get('crm.case.categ')
        categ = categ_obj.browse(cr, uid, categ_id, context=context)
        template_ids = []
        for template in categ.email_template_ids:
            template_ids.append(template.id)
        res['email_template3_ids'] = template_ids
        return {'value':res}

    def onchange_categ4_id(self, cr, uid, ids, categ_id, context=None):
        res = {}
        categ_obj = self.pool.get('crm.case.categ')
        categ = categ_obj.browse(cr, uid, categ_id, context=context)
        template_ids = []
        for template in categ.email_template_ids:
            template_ids.append(template.id)
        res['email_template4_ids'] = template_ids
        return {'value':res}

    def onchange_categ5_id(self, cr, uid, ids, categ_id, context=None):
        res = {}
        categ_obj = self.pool.get('crm.case.categ')
        categ = categ_obj.browse(cr, uid, categ_id, context=context)
        template_ids = []
        for template in categ.email_template_ids:
            template_ids.append(template.id)
        res['email_template5_ids'] = template_ids
        return {'value':res}

    def icy_onchange_partner_id(self, cr, uid, ids, partner_id, email_from, context=None):
        res = {}
        if partner_id:
            print 'PARTNER_ID:',partner_id
            partner_obj = self.pool.get('res.partner')
            partner = partner_obj.browse(cr, uid, partner_id, context=context)
            if partner.street:
                res['address'] = partner.street + " " + partner.street_nbr + ", " + partner.zip + " " + partner.city
            if partner.email:
                res['address'] = res['address'] + " - " + partner.email
            print 'NBR:',partner.street_nbr
            print 'ADDRESS:',res['address']
            res['cust_city'] = partner.city
            res['cust_zip'] = partner.zip
            res['street'] = partner.street
            res['cust_street'] = partner.street
            res['street_nbr'] = partner.street_nbr
            res['cust_phone'] = partner.phone
            res['email_from'] = partner.email
            res['cust_email'] = partner.email
            history_ids = []
            history_found = False
            for helpdesk in partner.helpdesk_ids:
                history_ids.append(helpdesk.id)
                history_found = True
            res['service_call_history_ids'] = history_ids
            res['history_found'] = history_found
        else:
            res['address'] = ""
            res['email_from'] = ""
        if partner_id:
            sql_stat = "select received_via_id from crm_helpdesk where partner_id = %d order by id desc limit 1" % (partner_id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['received_via_id']:
                res['received_via_id'] = sql_res['received_via_id']
        return {'value':res}

    def onchange_zip(self, cr, uid, ids, cust_zip, context=None):
        res = {}
        if cust_zip:
            sql_stat = "select id as street_id, name, city_id, zip from res_country_city_street where replace(zip, ' ', '') = upper(replace('%s', ' ', ''))" % (cust_zip, )
            print sql_stat
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['street_id']:
                res['street_id'] = sql_res['street_id']
                res['zip_id'] = sql_res['city_id']
                res['cust_zip'] = sql_res['zip']
                res['cust_street'] = sql_res['name']
                city_obj = self.pool.get('res.country.city')
                city = city_obj.browse(cr, uid, sql_res['city_id'], context=context)
                res['cust_city'] = city.name
#                res['cust_zip'] = cust_zip[0:4] + " " + cust_zip[4:]
                res['address'] = sql_res['name'] + ", " + city.name

        return {'value':res}

    def onchange_fml_name(self, cr, uid, ids, first_name, middle_name, last_name, context=None):
        res = {}
        name = ''
        if first_name and first_name != '':
            name = first_name
        if middle_name and middle_name != '':
            if name == '':
                name = middle_name
            else:
                name = name + ' ' + middle_name
        if last_name and last_name != '':
            if name == '':
                name = last_name
            else:
                name = name + ' ' + last_name
        res['cust_name'] = name
        return {'value':res}

    def onchange_street_id(self, cr, uid, ids, zip_id, street_id, street_nbr, street, cust_zip, cust_city, context=None):
        res = {}   
        sql_stat = "select id as partner_id, name, street, zip, city, first_name, last_name, middle_name from res_partner where trim(zip) =  trim('%s') and trim(street_nbr) = trim('%s')" % (cust_zip, street_nbr, )
        print sql_stat
        partner_id = 0
        cr.execute(sql_stat)
        sql_res = cr.dictfetchone()
        if sql_res:
            if sql_res['partner_id']:
                res['partner_id'] = sql_res['partner_id']
                partner_id = sql_res['partner_id']
                res['cust_name'] = sql_res['name']
                res['cust_street'] = sql_res['street']
                res['cust_zip'] = sql_res['zip']
                res['cust_city'] = sql_res['city']
                res['address'] = sql_res['street'] + ", " + sql_res['zip'] + " " + sql_res['city']
                res['cust_name'] = sql_res['name']
                res['first_name'] = sql_res['first_name']
                res['last_name'] = sql_res['last_name']
                res['middle_name'] = sql_res['middle_name']
        if not sql_res:
            address = ''
            if street and street != '':
                address = street
            if street_nbr and street_nbr != '':
                if address == '':
                    address = street_nbr
                else:
                    address = address + ' ' + street_nbr
            if cust_zip and cust_zip != '':
                if address == '':
                    address = cust_zip
                else:
                    address = address + ', ' + cust_zip
            if cust_city and cust_city != '':
                if address == '':
                    address = cust_city
                else:
                    address = address + ' ' + cust_city
            res['address'] = address
        if partner_id != 0:
            sql_stat = "select received_via_id from crm_helpdesk where partner_id = %d order by id desc limit 1" % (partner_id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['received_via_id']:
                res['received_via_id'] = sql_res['received_via_id']

        return {'value':res}

    def onchange_create_partner(self, cr, uid, ids, partner_id, cust_name, cust_street, cust_zip, cust_city, cust_phone, cust_email, zip_id, street_id, street_nbr, first_name, middle_name, last_name, via_essent, context=None):
        res = {}
        if not partner_id:
            print "BUTTON CREATE PARTNER"
            obj_partner = self.pool.get('res.partner')

            vals_partner = {}
            vals_partner['name'] = cust_name
            vals_partner['lang'] = "nl_NL"
            vals_partner['company_id'] = 1
            vals_partner['use_parent_address'] = False
            vals_partner['active'] = True
            vals_partner['street'] = cust_street + ' ' + street_nbr
            vals_partner['supplier'] = False
            vals_partner['city'] = cust_city
            vals_partner['zip'] = cust_zip
            vals_partner['employee'] = False
            vals_partner['type'] = "contact"
            vals_partner['email'] = cust_email
            vals_partner['phone'] = cust_phone
            vals_partner['customer'] = False
            vals_partner['is_company'] = False
            vals_partner['notification_email_send'] = "comment"
            vals_partner['opt_out'] = False
            vals_partner['display_name'] = cust_name
            vals_partner['purchase_warn'] = "no-message"
            vals_partner['sale_warn'] = "no-message"
            vals_partner['invoice_warn'] = "no-message"
            vals_partner['picking-warn'] = "no-message"
            vals_partner['received_via'] = False
            vals_partner['consumer'] = True
            vals_partner['subcontractor'] = False
            vals_partner['zip_id'] = zip_id
            vals_partner['street_id'] = street_id
            vals_partner['street_nbr'] = street_nbr
            vals_partner['first_name'] = first_name
            vals_partner['middle_name'] = middle_name
            vals_partner['last_name'] = last_name
            vals_partner['via_essent'] = via_essent
 
            partner_id = obj_partner.create(cr, uid, vals=vals_partner, context=context)
            res['partner_id'] = partner_id
        return {'value':res}

    _defaults = {
        'omruil_retour_date': (date.today() + timedelta(days=21)).strftime('%Y-%m-%d')
    }

    _columns = {
		'stock_move_ids': fields.one2many('stock.move', 'helpdesk_id', 'Stock Moves'),
		'received_via_id': fields.many2one('res.partner', 'Aangeschaft Bij', select=True),
		'serial_nbr1': fields.many2one('stock.production.lot', 'Serienummer 1', select=True),
		'serial_nbr2': fields.many2one('stock.production.lot', 'Serienummer 2', select=True),
        'additional_sns': fields.boolean('Meer Serienummers'),
        'serial_nbr_ids': fields.many2many('stock.production.lot', 'helpdesk_serial_nbr_rel', 'serial_nbr_id', 'helpdesk_id', 'Serienummers'),
		'product_id': fields.many2one('product.product', 'Omruil', select=True),
		'product_id_send': fields.many2one('product.product', 'Toesturen', select=True),
        'address': fields.char('Adres', len=124, readonly=True, store=True),
		'incoming_via_id': fields.many2one('res.partner', 'Binnengekomen Via', select=True),
		'categ2_id': fields.many2one('crm.case.categ', 'Service Categorie 2', select=True, domain="['|',('section_id','=',False),('section_id','=',section_id),('object_id.model', '=', 'crm.helpdesk')]"),
		'categ3_id': fields.many2one('crm.case.categ', 'Service Categorie 3', select=True, domain="['|',('section_id','=',False),('section_id','=',section_id),('object_id.model', '=', 'crm.helpdesk')]"),
		'categ4_id': fields.many2one('crm.case.categ', 'Service Categorie 4', select=True, domain="['|',('section_id','=',False),('section_id','=',section_id),('object_id.model', '=', 'crm.helpdesk')]"),
		'categ5_id': fields.many2one('crm.case.categ', 'Service Categorie 5', select=True, domain="['|',('section_id','=',False),('section_id','=',section_id),('object_id.model', '=', 'crm.helpdesk')]"),
		'task_user': fields.many2one('res.users', 'Taak Voor', select=True),
        'task_date': fields.date('Einddatum'),
        'task_description': fields.char('Actieomschrijving', len=124),
        'omruil': fields.boolean('Omruil'),
        'toesturen': fields.boolean('Toesturen'),
        'call_transfer': fields.boolean('Doorverbinden'),
        'call_transfer_user_id': fields.many2one('res.users', 'Doorverbinden Naar', select=True),
		'email_template_id': fields.many2one('email.template', 'Email Template', select=True),
		'email_template2_id': fields.many2one('email.template', 'Email Template 2', select=True),
		'email_template3_id': fields.many2one('email.template', 'Email Template 3', select=True),
		'email_template4_id': fields.many2one('email.template', 'Email Template 4', select=True),
		'email_template5_id': fields.many2one('email.template', 'Email Template 5', select=True),
        'omruil_retour_date': fields.date('Omruil Retour Datum'),
        'product_ids': fields.related('categ_id', 'product_ids', type="many2many", obj="product.product"),
        'product_ids_send': fields.related('categ_id', 'product_ids', type="many2many", obj="product.product"),
        'email_template_ids': fields.related('categ_id', 'email_template_ids', type="many2many", obj="email.template"),
        'email_template2_ids': fields.related('categ2_id', 'email_template_ids', type="many2many", obj="email.template"),
        'email_template3_ids': fields.related('categ3_id', 'email_template_ids', type="many2many", obj="email.template"),
        'email_template4_ids': fields.related('categ4_id', 'email_template_ids', type="many2many", obj="email.template"),
        'email_template5_ids': fields.related('categ5_id', 'email_template_ids', type="many2many", obj="email.template"),
		'zip_id': fields.many2one('res.country.city', 'Postcode'),
		'street_id': fields.many2one('res.country.city.street', 'Straat'),
		'street_nbr': fields.char('Huisnummer', size=16),
        'cust_name': fields.char('Relatienaam', len=124),
        'cust_street': fields.char('Straat', len=124),
        'cust_zip': fields.char('Postcode', len=24),
        'cust_city': fields.char('Plaats', len=124),
        'cust_phone': fields.char('Telefoon', len=24),
        'cust_email': fields.char('Email', len=124),
        'create_partner': fields.boolean('Relatie Aanmaken'),
        'first_name': fields.char('Voornaam', len=24),
        'middle_name': fields.char('Tussenvoegsel(s)', len=24),
        'last_name': fields.char('Achternaam', len=24),
        'essent_ref': fields.char('Essent Klantnummer', len=24),
        'gender': fields.selection([('m','Man'),('f','Vrouw')], string='Geslacht', size=1),
        'email_body': fields.html('Email Tekst'),
        'service_call_history_ids': fields.related('partner_id', 'helpdesk_ids', type="many2many", obj="crm.helpdesk"),
        'history_found': fields.boolean('Historie Gevonden'),
		'child_ids': fields.one2many('crm.helpdesk', 'parent_id', 'Vervolgcalls'),
		'parent_id': fields.many2one('crm.helpdesk', 'Originele Call', select=True),
        'username_portal': fields.char('Gebruikersnaam Portal', len=64),
		'icy_task_ids': fields.one2many('project.task', 'helpdesk_id', 'Taken en Terugbelverzoeken', select=True),
		'notes': fields.text('''Nota's'''),
		'brandtype': fields.char('Merk en type ketel', len=128),
        'via_essent': fields.boolean('Via Essent'),
    }

    def create(self, cr, uid, vals, context=None):
        if 'partner_id' in vals and vals['partner_id']:
            sql_stat = "select street, zip, city, street_nbr from res_partner where id = %d" % (vals['partner_id'], )
            print sql_stat
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                address = ''
                if sql_res['street'] != '':
                    address = sql_res['street']
                if sql_res['street_nbr'] != '':
                    if address == '':
                        address = sql_res['street_nbr']
                    else:
                        address = address + ' ' + sql_res['street_nbr']
                if sql_res['zip'] != '':
                    if address == '':
                        address = sql_res['zip']
                    else:
                        address = address + ', ' + sql_res['zip']
                if sql_res['city'] != '':
                    if address == '':
                        address = sql_res['city']
                    else:
                        address = address + ' ' + sql_res['city']
                vals['address'] = address

        res = super(crm_helpdesk, self).create(cr, uid, vals, context=context)
        prc = self.browse(cr, uid, res)
        if prc.omruil:
            if prc.partner_id:
# SHIPMENT VOOR OMRUIL
                picking = self.pool.get('stock.picking')
                picking_id = picking.create(cr, uid, {
                    'origin': 'Service Omruil',
                    'min_date': date.today().strftime('%Y-%m-%d'),
                    'max_date': date.today().strftime('%Y-%m-%d'),
                    'date': date.today().strftime('%Y-%m-%d'),
                    'user_id': prc.user_id.id,
                    'partner_id': prc.partner_id.id,
                    'company_id': prc.company_id.id,
                    'move_type': 'direct',
                    'stock_journal_id': 1,
                    'invoice_state': '2binvoiced',
                    'stage': 'draft', 
                    'auto_picking': False, 
                    'type': 'out', 
                    'helpdesk_id': prc.id,
                },context=context)
#                for product_omruil in prc.product_ids:
                if prc.product_id:
                    move = self.pool.get('stock.move')
                    move_id = move.create(cr, uid, {
                        'origin': 'Service Omruil',
                        'product_uos_qty': 1,
                        'product_qty': 1,
                        'product_uom': 1,
                        'product_uos': 1,
                        'date_expected': date.today().strftime('%Y-%m-%d'),
                        'date': date.today().strftime('%Y-%m-%d'),
                        'price_unit': prc.product_id.list_price, #product_omruil.list_price,
                        'name': prc.product_id.name_template, #product_omruil.name_template,
                        'product_id': prc.product_id.id, #product_omruil.id,
                        'partner_id': prc.partner_id.id,
                        'company_id': prc.company_id.id,
                        'helpdesk_id': prc.id,
                        'location_id': 12,
                        'location_dest_id': 9,
                        'picking_id': picking_id,
                        'auto_validate': False, 
                        'cancel_cascade': False, 
                        'valid_shortage': False, 
                    },context=context)
# RECEIPT VOOR OMRUIL
                picking = self.pool.get('stock.picking')
                picking_id = picking.create(cr, uid, {
                    'origin': 'Service Omruil',
                    'min_date': prc.omruil_retour_date,
                    'max_date': prc.omruil_retour_date,
                    'date': prc.omruil_retour_date,
                    'user_id': prc.user_id.id,
                    'partner_id': prc.partner_id.id,
                    'company_id': prc.company_id.id,
                    'move_type': 'direct',
                    'stock_journal_id': 1,
                    'invoice_state': 'none',
                    'stage': 'draft', 
                    'auto_picking': False, 
                    'type': 'in', 
                    'helpdesk_id': prc.id,
                },context=context)
#                for product_omruil in prc.product_ids:
                if prc.product_id:
                    move = self.pool.get('stock.move')
                    move_id = move.create(cr, uid, {
                        'origin': 'Service Omruil',
                        'product_uos_qty': 1,
                        'product_qty': 1,
                        'product_uom': 1,
                        'product_uos': 1,
                        'date_expected': prc.omruil_retour_date,
                        'date': prc.omruil_retour_date,
                        'price_unit': prc.product_id.list_price, #product_omruil.list_price,
                        'name': prc.product_id.name_template, #product_omruil.name_template,
                        'product_id': prc.product_id.id, #product_omruil.id,
                        'partner_id': prc.partner_id.id,
                        'company_id': prc.company_id.id,
                        'helpdesk_id': prc.id,
                        'location_id': 9,
                        'location_dest_id': 12,
                        'picking_id': picking_id,
                        'auto_validate': False, 
                        'cancel_cascade': False, 
                        'valid_shortage': False, 
                    },context=context)
        if prc.toesturen:
            if prc.partner_id:
# SHIPMENT VOOR TOESTUREN
                picking = self.pool.get('stock.picking')
                picking_id = picking.create(cr, uid, {
                    'origin': 'Service Toesturen',
                    'min_date': date.today().strftime('%Y-%m-%d'),
                    'max_date': date.today().strftime('%Y-%m-%d'),
                    'date': date.today().strftime('%Y-%m-%d'),
                    'user_id': prc.user_id.id,
                    'partner_id': prc.partner_id.id,
                    'company_id': prc.company_id.id,
                    'move_type': 'direct',
                    'stock_journal_id': 1,
                    'invoice_state': '2binvoiced',
                    'stage': 'draft', 
                    'auto_picking': False, 
                    'type': 'out', 
                },context=context)
#                for product_toesturen in prc.product_ids_send:
                if prc.product_id_send:
                    move = self.pool.get('stock.move')
                    move_id = move.create(cr, uid, {
                        'origin': 'Service Toesturen',
                        'product_uos_qty': 1,
                        'product_qty': 1,
                        'product_uom': 1,
                        'product_uos': 1,
                        'date_expected': date.today().strftime('%Y-%m-%d'),
                        'date': date.today().strftime('%Y-%m-%d'),
                        'price_unit': prc.product_id_send.list_price, #product_toesturen.list_price,
                        'name': prc.product_id_send.name_template, #product_toesturen.name_template,
                        'product_id': prc.product_id_send.id, #product_toesturen.id,
                        'partner_id': prc.partner_id.id,
                        'company_id': prc.company_id.id,
                        'helpdesk_id': prc.id,
                        'location_id': 12,
                        'location_dest_id': 9,
                        'picking_id': picking_id,
                        'auto_validate': False, 
                        'cancel_cascade': False, 
                        'valid_shortage': False, 
                    },context=context)
        return res

crm_helpdesk()

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'

    _columns = {
		'helpdesk_id': fields.many2one('crm.helpdesk', 'Helpdesk Call', select=True),
    }

stock_move()

class email_template(osv.osv):
    _name = 'email.template'
    _inherit = 'email.template'

    _columns = {
        'email_body': fields.html('Email Tekst'),
    }

email_template()

class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(res_partner,self).name_get(cr, uid, ids, context=context)
        res2 = []
        for partner_id, name in res:
            record = self.read(cr, uid, partner_id, ['city','zip'], context=context)
            if record['city']:
                city = record['city']
            else:
                city = ''
            if record['zip']:
                zip = record['zip']
            else:
                zip = ''
            new_name = name + ' - [' + zip + ' ' + city + ']'
            res2.append((partner_id, new_name))
        return res2

    def onchange_zip(self, cr, uid, ids, cust_zip, context=None):
        res = {}
        if cust_zip:
            sql_stat = "select id as street_id, name, city_id, zip from res_country_city_street where replace(zip, ' ', '') = upper(replace('%s', ' ', ''))" % (cust_zip, )
            print sql_stat
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['street_id']:
                res['street_id'] = sql_res['street_id']
                res['zip_id'] = sql_res['city_id']
                res['street'] = sql_res['name']
                city_obj = self.pool.get('res.country.city')
                city = city_obj.browse(cr, uid, sql_res['city_id'], context=context)
                res['city'] = city.name

        return {'value':res}

    _columns = {
		'helpdesk_ids': fields.one2many('crm.helpdesk', 'partner_id', ''),
		'received_via': fields.boolean('Aangeschaft Via'),
		'consumer': fields.boolean('Consument'),
		'incoming_service_call': fields.boolean('Binnenkomende Helpdesk Call'),
        'first_name': fields.char('Voornaam', len=24),
        'middle_name': fields.char('Tussenvoegsel(s)', len=24),
        'last_name': fields.char('Achternaam', len=24),
        'essent_ref': fields.char('Essent Klantnummer', len=24),
        'gender': fields.selection([('m','Man'),('f','Vrouw')], string='Geslacht', size=1),
		'via_essent': fields.boolean('Via Essent'),
    }

res_partner()

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    _columns = {
		'helpdesk_retour': fields.boolean('Helpdesk Retour'),
    }

product_product()

class project_task(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'helpdesk_id': fields.many2one('crm.helpdesk', 'Helpdesk Call', select=True),
        'user_name': fields.related('user_id', 'name', type='many2one', relation='res.users', string='Gebruiker', readonly=True),
    }

project_task()

class res_users(osv.osv):
    _inherit = 'res.users'

    _columns = {
        'salesrep': fields.boolean('Account manager'),
    }

res_users()

class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    _columns = {
        'helpdesk_id': fields.many2one('crm.helpdesk', 'Helpdesk Call', select=True),
    }

stock_picking()

class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'

    _columns = {
        'helpdesk_id': fields.many2one('crm.helpdesk', 'Helpdesk Call', select=True),
    }

stock_picking_out()

class stock_picking_in(osv.osv):
    _inherit = 'stock.picking.in'

    _columns = {
        'helpdesk_id': fields.many2one('crm.helpdesk', 'Helpdesk Call', select=True),
    }

stock_picking_in()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

