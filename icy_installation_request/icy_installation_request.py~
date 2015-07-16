#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
import datetime
from datetime import timedelta
from datetime import date

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'installer': fields.boolean('Installateur'),
    }

res_partner()

class crm_software_version(osv.osv):
    _name = 'crm.software.version'

    _columns = {
        'case_section_id': fields.many2one('crm.case.section', 'Type thermostaat', required=True, select=True),
        'name': fields.char('Software versie', required=True),
    }

crm_software_version()

class crm_case_section(osv.osv):
    _inherit = 'crm.case.section'

    _columns = {
        'software_ids': fields.one2many('crm.software.version', 'case_section_id', 'Software versies'),
    }

crm_case_section()

class crm_installation_request(osv.osv):
    _name = 'crm.installation.request'
    _inherit = ['mail.thread']

    _columns = {
		'partner_id': fields.many2one('res.partner', 'Relatie', required=True, select=True),
        'cust_zip': fields.char('Postcode'),
		'zip_id': fields.many2one('res.country.city', 'Postcodetabel'),
		'street_id': fields.many2one('res.country.city.street', 'Straattabel'),
		'street_nbr': fields.char('Huisnummer', size=16),
        'phone': fields.char('Telefoon'),
        'mobile': fields.char('Mobiel'),
        'email': fields.char('E-mail'),
        'name': fields.char('ID'),
        'user_id': fields.many2one('res.users', 'Gebruiker', required=True, select=True),
        'state': fields.selection([
            ('new', 'Nieuw'),
            ('in_progress', 'In Behandeling'),
            ('problem', 'Probleem'),
            ('done', 'Ingepland'),
            ('cancel', 'Geannuleerd'),
            ], 'Status', readonly=True, track_visibility='onchange', select=True),
        'case_section_id': fields.many2one('crm.case.section', 'Type thermostaat', required=True, select=True),
        'software_version_id': fields.many2one('crm.software.version', 'Software versie', select=True),
        'connected_to': fields.text('Aangesloten op'),
        'problem': fields.text('Probleem'),
        'installer_id': fields.many2one('res.partner', 'Installateur', select=True),
        'request_date': fields.date('Aanvraagdatum'),
        'installation_date': fields.date('Geplande installatiedatum'),
        'first_name': fields.char('Voornaam', len=24),
        'middle_name': fields.char('Tussenvoegsel(s)', len=24),
        'last_name': fields.char('Achternaam', len=24),
        'one': fields.integer('Een'),
        'color': fields.integer('Color Index'),
        'create_partner': fields.boolean('Relatie aanmaken'),
        'address': fields.char('Adres'),
    }

    _defaults = {
        'request_date': fields.date.context_today,
        'user_id': lambda obj, cr, uid, context: uid,
#        'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'crm.installation.request'),
        'state': 'new',
        'one': 1,
        'color': 0,
    }

    _order = 'id desc'

    def onchange_street_id(self, cr, uid, ids, cust_zip, zip_id, street_id, street_nbr, context=None):
        res = {}
        zip = zip_id
        street = street_id
        nbr = street_nbr
        partner_id = None

        if cust_zip:
            sql_stat = "select res_country_city_street.id as street_id, city_id, res_country_city_street.zip, res_country_city_street.name as street_name, res_country_city.name as city_name from res_country_city_street, res_country_city where replace(res_country_city_street.zip, ' ', '') = upper(replace('%s', ' ', '')) and city_id = res_country_city.id" % (cust_zip, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['street_id']:
                res['street_id'] = sql_res['street_id']
                res['zip_id'] = sql_res['city_id']
                res['cust_zip'] = sql_res['zip']
                address = sql_res['street_name']
                if street_nbr:
                    address = address + ' ' + street_nbr
                address = address + ', ' + sql_res['zip'] + ' ' + sql_res['city_name']
                res['address'] = address

        if zip_id and street_nbr:
            sql_stat = "select id as partner_id from res_partner where zip_id = %d and trim(street_nbr) = trim('%s')" % (zip_id, street_nbr, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res:
                if sql_res['partner_id']:
                    res['partner_id'] = sql_res['partner_id']
                else:
                    res['partner_id'] = None
            else:
                res['partner_id'] = None

        return {'value':res}

    def icy_onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        res = {}
        if partner_id:
            partner_obj = self.pool.get('res.partner')
            partner = partner_obj.browse(cr, uid, partner_id, context=context)
            res['phone'] = partner.phone
            res['email'] = partner.email
            res['mobile'] = partner.mobile
            res['zip_id'] = partner.zip_id.id
            res['street_id'] = partner.street_id.id
            res['street_nbr'] = partner.street_nbr
            res['cust_zip'] = partner.zip
        else:
            res['cust_phone'] = None
            res['email'] = None
            res['mobile'] = None
        return {'value':res}

    def button_in_progress(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'in_progress'}, context=context)
        return True

    def button_problem(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'problem'}, context=context)
        return True

    def button_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'done'}, context=context)
        return True

    def button_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True

    def button_reset(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'new'}, context=context)
        return True

    def onchange_create_partner(self, cr, uid, ids, partner_id, phone, email, mobile, zip_id, street_id, street_nbr, first_name, middle_name, last_name, context=None):
        res = {}
        if not partner_id:
            obj_partner = self.pool.get('res.partner')

            vals_partner = {}
            cust_name = ''
            if first_name:
                cust_name = first_name
            if middle_name:
                if cust_name == '':
                    cust_name = middle_name
                else:
                    cust_name = cust_name + ' ' + middle_name
            if last_name:
                if cust_name == '':
                    cust_name = last_name
                else:
                    cust_name = cust_name + ' ' + last_name

            vals_partner['name'] = cust_name
            vals_partner['lang'] = "nl_NL"
            vals_partner['company_id'] = 1
            vals_partner['use_parent_address'] = False
            vals_partner['active'] = True

            sql_stat = "select res_country_city_street.name as cust_street, res_country_city.name as cust_city, res_country_city.zip as cust_zip from res_country_city_street, res_country_city where res_country_city_street.id = %d and city_id = res_country_city.id" % (street_id, )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['cust_street']:
                cust_street = sql_res['cust_street']
                cust_zip = sql_res['cust_zip']
                cust_city = sql_res['cust_city']

            if street_nbr:
                vals_partner['street'] = cust_street + ' ' + street_nbr
            else:
                vals_partner['street'] = cust_street
            vals_partner['supplier'] = False
            vals_partner['city'] = cust_city
            vals_partner['zip'] = cust_zip
            vals_partner['employee'] = False
            vals_partner['installer'] = False
            vals_partner['type'] = "contact"
            vals_partner['email'] = email
            vals_partner['phone'] = phone
            vals_partner['mobile'] = mobile
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
 
            partner_id = obj_partner.create(cr, uid, vals=vals_partner, context=context)
            res['partner_id'] = partner_id
        return {'value':res}

    def create(self, cr, uid, vals, context=None):
        vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'crm.installation.request')
        if 'cust_zip' in vals and vals['cust_zip']:
            sql_stat = "select res_country_city_street.id as street_id, city_id, res_country_city_street.zip, res_country_city_street.name as street_name, res_country_city.name as city_name from res_country_city_street, res_country_city where replace(res_country_city_street.zip, ' ', '') = upper(replace('%s', ' ', '')) and city_id = res_country_city.id" % (vals['cust_zip'], )
            cr.execute(sql_stat)
            sql_res = cr.dictfetchone()
            if sql_res and sql_res['street_id']:
                address = sql_res['street_name']
                if 'street_nbr' in vals and vals['street_nbr']:
                    address = address + ' ' + vals['street_nbr']
                address = address + ', ' + sql_res['zip'] + ' ' + sql_res['city_name']
                vals['address'] = address

        return super(crm_installation_request, self).create(cr, uid, vals, context=context)

crm_installation_request()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

