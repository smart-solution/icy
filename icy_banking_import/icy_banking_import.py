#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
# 
##############################################################################
import base64
from datetime import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from md5 import md5
import csv

import logging

_logger = logging.getLogger(__name__)

class account_bank_statement(osv.osv):
    _inherit = 'account.bank.statement'
    
    _columns = {
        'fys_file_id': fields.many2one('account.coda.fys.file', 'Fys. File', select=True),
               }
    
    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context):
            if this.fys_file_id:
                this.fys_file_id.write(
                        {'filename': this.fys_file_id.id,
                        })
                this.fys_file_id.refresh()
        return super(account_bank_statement, self).unlink(
                cr, uid, ids, context=context)
    
account_bank_statement()
    
class account_bank_statement_line(osv.osv):
    _inherit = 'account.bank.statement.line'

    def create(self, cr, uid, vals, context=None):
        coda_id = 0
        

        res = super(account_bank_statement_line, self).create(cr, uid, vals, context=context)
        return res

    _columns = {
# 1 line added for NP transaction code improvement
        'transaction_code': fields.char('Trans.Code', size=8),
        'structcomm_flag': fields.boolean('OGM Gebruikt'),
        'structcomm_message': fields.char('OGM Bericht'),
        'name_zonder_adres': fields.char('name zonder adres', size=128),
        'move_flag': fields.boolean('Move found'),
                }

account_bank_statement_line()

class account_coda_fys_file(osv.osv):
    _name = 'account.coda.fys.file'
    _description = 'Coda Fysical File'

    _columns = {
        'filename': fields.char('Name', size=128),
        'files_ids': fields.one2many('account.coda.file', 'fys_file_id', 'Coda Files', ondelete='cascade'),
                }

account_coda_fys_file()

class account_ing_import(osv.osv_memory):
    _name = 'account.ing.import'

    _columns = {
        'ing_data': fields.binary('ING File', required=True),
        'ing_fname': fields.char('ING Filename', size=128, required=True),
        'note': fields.text('Log'),
    }

    def _get_default_tmp_account(self, cr, uid, context):
        user = self.pool.get('res.users').browse(cr, uid, uid) 
        tmp_accounts = self.pool.get('account.account').search(cr, uid, [('code', '=', '499010'),('company_id','=',user.company_id.id)])
        if tmp_accounts and len(tmp_accounts) > 0:
            tmp_account_id = tmp_accounts[0]
        else:
            tmp_account_id = False
        return tmp_account_id
    
    def ing_parsing(self, cr, uid, ids, context=None, batch=False, codafile=None, codafilename=None):
        obj = self.browse(cr, uid, ids)[0]
        print 'OBJ:',obj

        fname = '/tmp/csv_temp_' + datetime.today().strftime('%Y%m%d%H%M%S') + '.csv'
        fp = open(fname,'w+')
        fp.write(base64.decodestring(obj.ing_data))
        fp.close()
        fp = open(fname,'rU')
        reader = csv.reader(fp, delimiter=",", quotechar='"')

        journal_obj = self.pool.get('account.journal')
        stat_obj = self.pool.get('account.bank.statement')
        stat_line_obj = self.pool.get('account.bank.statement.line')
        partner_obj = self.pool.get('res.partner.bank')
        invoice_obj = self.pool.get('account.invoice')

        linenum = 0
        balance_end_real = 0.00
        stat_id = None

        for row in reader:
            linenum = linenum + 1
            print linenum, ' ', row
            if linenum == 1:
                continue

            txn_date = row[0][4:6] + '-' + row[0][6:8] + '-' + row[0][0:4] 
            print txn_date
            txn_partner = row[1]
            icy_bank = row[2]
#            if len(row[3]) > 0:
            txn_bank = row[3]
#            else:
#                txn_bank = row[2]
            txn_code = row[4]
            txn_type = row[5]
            if txn_type == 'Af':
                txn_amount = float(row[6].replace(',','.')) * -1
            else:
                txn_amount = float(row[6].replace(',','.'))
            txn_description = row[8]
            txn_currency1 = 'EUR'

            if linenum == 2:
                cr.execute("select id from res_partner_bank where replace(replace(acc_number,' ',''),'-','') like %s", ('%' + icy_bank + '%',))
                bank_ids = [id[0] for id in cr.fetchall()]
                bank_ids = partner_obj.search(cr, uid, [('id', 'in', bank_ids)])
                journal_id = None
                bank_account = None
                if bank_ids and len(bank_ids) > 0:
                    bank_accs = partner_obj.browse(cr, uid, bank_ids)
                    for bank_acc in bank_accs:
                        if bank_acc.journal_id.id and ((bank_acc.journal_id.currency.id and bank_acc.journal_id.currency.name == txn_currency1) or (not bank_acc.journal_id.currency.id and bank_acc.journal_id.company_id.currency_id.name == txn_currency1)):
                            journal_id = bank_acc.journal_id.id
                            bank_account = bank_acc
                            break
                if not bank_account:
                    raise osv.except_osv(_('Error') + ' R1004', _("No matching Bank Account (with Account Journal) found.\n\nPlease set-up a Bank Account with as Account Number '%s' and as Currency '%s' and an Account Journal.") % (icy_bank, txn_currency1))
            
                journal = journal_obj.browse(cr, uid, journal_id)
                period_id = self.pool.get('account.period').search(cr, uid, [('company_id', '=', journal.company_id.id), ('date_start', '<=', txn_date), ('date_stop', '>=', txn_date)])
                if not period_id:
                    raise osv.except_osv(_('Error') + 'R0002', _("The CODA Statement New Balance date doesn't fall within a defined Accounting Period! Please create the Accounting Period for date %s for the company %s.") % (txn_date, journal.company_id.name))

#                balance_start_check_date = txn_date
#                cr.execute('SELECT balance_end_real \
#                    FROM account_bank_statement \
#                    WHERE journal_id = %s and date <= %s \
#                    ORDER BY date DESC,id DESC LIMIT 1', (journal_id, balance_start_check_date))
#                res = cr.fetchone()
#                balance_start_check = res and res[0]
#                if balance_start_check == None:
#                    if journal.default_debit_account_id and (journal.default_credit_account_id == journal.default_debit_account_id):
#                        balance_start_check = journal.default_debit_account_id.balance
#                    else:
#                        raise osv.except_osv(_('Error'), _("Configuration Error in journal %s!\nPlease verify the Default Debit and Credit Account settings.") % journal.name)
#                if balance_start_check != txn_amount_init:
#                    coda_note = _("The SNS Statement Starting Balance (%.2f) does not correspond with the previous Closing Balance (%.2f) in journal %s!") % (txn_amount_init, balance_start_check, journal.name)

                stmt_nbr = self.pool.get('ir.sequence').next_by_id(cr, uid, journal.sequence_id.id, context)

                txn_amount_init = 0.00

                stat_id = stat_obj.create(cr, uid, {
                    'balance_start': txn_amount_init,
                    'journal_id': journal_id,
                    'period_id': period_id[0],
                    'date': txn_date,
                    'user_id': uid,
                    'name': stmt_nbr,
#                    'closing_date': cfile.t8_end_date,
#                    'balance_end': ,
                    'company_id': journal.company_id.id,
#                     'state': ,
#                    'balance_end_real': cfile.t8_end_balance,
#                    'coda_note': coda_note,
                }, context=context)

#                balance_end_real = float(txn_amount_init)

            ref = linenum
            type = 'normal'
            partner = None
            partner_id = None
            invoice_id = None
            transaction_type = 'general'
            name = txn_description.replace("-", "\n")

#            balance_end_real += float(txn_amount)

            tmp_accounts = self.pool.get('account.account').search(cr, uid, [('code', '=', '999000'),('company_id','=',journal.company_id.id)])
            if tmp_accounts and len(tmp_accounts) > 0:
                account = tmp_accounts[0]
            else:
                tmp_account_id = False

            cr.execute("select id from res_partner_bank where replace(replace(acc_number,' ',''),'-','') like %s", ('%' + txn_bank + '%',))
            bank_ids = [id[0] for id in cr.fetchall()]
            ids = partner_obj.search(cr, uid, [('id', 'in', bank_ids)])
            if ids and len(ids) == 1:
                partner = partner_obj.browse(cr, uid, ids[0], context=context).partner_id
                if not(partner_id):
                    partner_id = partner.id
                    if partner.customer and not (partner.supplier):
                        account = partner.property_account_receivable.id
                        transaction_type = 'customer'
                    elif partner.supplier and not (partner.customer):
                        account = partner.property_account_payable.id
                        transaction_type = 'supplier'

#            txn_desc_upper = txn_description.upper()
#            pos = txn_desc_upper.find('SAJ/')
#            posend = pos + 13
#            invnbr = txn_desc_upper[pos:posend]

#            if not partner_id:
#                ids = invoice_obj.search(cr, uid, [('number', '=', invnbr)])
#                if ids and len(ids) == 1:
#                    partner = invoice_obj.browse(cr, uid, ids[0], context=context).partner_id
#                    if not(partner_id):
#                        partner_id = partner.id
#                        if partner.customer and not (partner.supplier):
#                            account = partner.property_account_receivable.id
#                            transaction_type = 'customer'
#                        elif partner.supplier and not (partner.customer):
#                            account = partner.property_account_payable.id
#                            transaction_type = 'supplier'

            stat_line_id = stat_line_obj.create(cr, uid, {
                'ref': ref,
                'statement_id': stat_id,
                'sequence': linenum,
                'type': transaction_type,
                'company_id': journal.company_id.id,
                'note': name,
                'journal_id': journal_id,
                'amount': txn_amount,
                'date': txn_date,
                'partner_id': partner_id,
                'account_id': account,
                'voucher_id': None,
                'state': 'draft',
                'name': name,
            }, context=context)
   
#        if stat_id:
#            stat_obj.write(cr, uid, [stat_id], {'balance_end_real': balance_end_real}, context=context)

        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'action_bank_statement_tree')
        action = self.pool.get(model).browse(cr, uid, action_id, context=context)
        return {
            'name': action.name,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'res_model': action.res_model,
            'domain': action.domain,
            'context': action.context,
            'type': 'ir.actions.act_window',
            'search_view_id': action.search_view_id.id,
            'views': [(v.view_id.id, v.view_mode) for v in action.view_ids]
        }

        return True

account_ing_import()

class account_sns_import(osv.osv_memory):
    _name = 'account.sns.import'

    _columns = {
        'sns_data': fields.binary('SNS File', required=True),
        'sns_fname': fields.char('SNS Filename', size=128, required=True),
        'note': fields.text('Log'),
    }

    def _get_default_tmp_account(self, cr, uid, context):
        user = self.pool.get('res.users').browse(cr, uid, uid) 
        tmp_accounts = self.pool.get('account.account').search(cr, uid, [('code', '=', '499010'),('company_id','=',user.company_id.id)])
        if tmp_accounts and len(tmp_accounts) > 0:
            tmp_account_id = tmp_accounts[0]
        else:
            tmp_account_id = False
        return tmp_account_id
    
    def sns_parsing(self, cr, uid, ids, context=None, batch=False, snsfile=None, snsfilename=None):
        obj = self.browse(cr, uid, ids)[0]
        print 'OBJ:',obj

        fname = '/tmp/csv_temp_' + datetime.today().strftime('%Y%m%d%H%M%S') + '.csv'
        fp = open(fname,'w+')
        fp.write(base64.decodestring(obj.sns_data))
        fp.close()
        fp = open(fname,'rU')
        reader = csv.reader(fp, delimiter=";", quotechar='"')

        journal_obj = self.pool.get('account.journal')
        stat_obj = self.pool.get('account.bank.statement')
        stat_line_obj = self.pool.get('account.bank.statement.line')
        partner_obj = self.pool.get('res.partner.bank')
        invoice_obj = self.pool.get('account.invoice')

        linenum = 0
        balance_end_real = 0.00
        stat_id = None

        for row in reader:
            linenum = linenum + 1

            txn_date = (row[0].split('-'))[2] + '-' + (row[0].split('-'))[1] + '-' + (row[0].split('-'))[0] 
            icy_bank = row[1]
            txn_bank = row[2]
            txn_partner = row[3]
            txn_currency1 = row[7]
            txn_amount_init = row[8]
            txn_currency2 = row[9]
            txn_amount = row[10]
            txn_description = row[17]

            if linenum == 1:
                cr.execute("select id from res_partner_bank where replace(replace(acc_number,' ',''),'-','') like %s", ('%' + icy_bank + '%',))
                bank_ids = [id[0] for id in cr.fetchall()]
                bank_ids = partner_obj.search(cr, uid, [('id', 'in', bank_ids)])
                journal_id = None
                bank_account = None
                if bank_ids and len(bank_ids) > 0:
                    bank_accs = partner_obj.browse(cr, uid, bank_ids)
                    for bank_acc in bank_accs:
                        if bank_acc.journal_id.id and ((bank_acc.journal_id.currency.id and bank_acc.journal_id.currency.name == txn_currency1) or (not bank_acc.journal_id.currency.id and bank_acc.journal_id.company_id.currency_id.name == txn_currency1)):
                            journal_id = bank_acc.journal_id.id
                            bank_account = bank_acc
                            break
                if not bank_account:
                    raise osv.except_osv(_('Error') + ' R1004', _("No matching Bank Account (with Account Journal) found.\n\nPlease set-up a Bank Account with as Account Number '%s' and as Currency '%s' and an Account Journal.") % (icy_bank, txn_currency1))
            
                journal = journal_obj.browse(cr, uid, journal_id)
                period_id = self.pool.get('account.period').search(cr, uid, [('company_id', '=', journal.company_id.id), ('date_start', '<=', txn_date), ('date_stop', '>=', txn_date)])
                if not period_id:
                    raise osv.except_osv(_('Error') + 'R0002', _("The CODA Statement New Balance date doesn't fall within a defined Accounting Period! Please create the Accounting Period for date %s for the company %s.") % (txn_date, journal.company_id.name))

#                balance_start_check_date = txn_date
#                cr.execute('SELECT balance_end_real \
#                    FROM account_bank_statement \
#                    WHERE journal_id = %s and date <= %s \
#                    ORDER BY date DESC,id DESC LIMIT 1', (journal_id, balance_start_check_date))
#                res = cr.fetchone()
#                balance_start_check = res and res[0]
#                if balance_start_check == None:
#                    if journal.default_debit_account_id and (journal.default_credit_account_id == journal.default_debit_account_id):
#                        balance_start_check = journal.default_debit_account_id.balance
#                    else:
#                        raise osv.except_osv(_('Error'), _("Configuration Error in journal %s!\nPlease verify the Default Debit and Credit Account settings.") % journal.name)
#                if balance_start_check != txn_amount_init:
#                    coda_note = _("The SNS Statement Starting Balance (%.2f) does not correspond with the previous Closing Balance (%.2f) in journal %s!") % (txn_amount_init, balance_start_check, journal.name)

                stmt_nbr = self.pool.get('ir.sequence').next_by_id(cr, uid, journal.sequence_id.id, context)

                stat_id = stat_obj.create(cr, uid, {
                    'balance_start': txn_amount_init,
                    'journal_id': journal_id,
                    'period_id': period_id[0],
                    'date': txn_date,
                    'user_id': uid,
                    'name': stmt_nbr,
#                    'closing_date': cfile.t8_end_date,
#                    'balance_end': ,
                    'company_id': journal.company_id.id,
#                     'state': ,
#                    'balance_end_real': cfile.t8_end_balance,
#                    'coda_note': coda_note,
                }, context=context)

                balance_end_real = float(txn_amount_init)

            ref = linenum
            type = 'normal'
            partner = None
            partner_id = None
            invoice_id = None
            transaction_type = 'general'
            name = txn_description.replace("-", "\n")

            balance_end_real += float(txn_amount)

            tmp_accounts = self.pool.get('account.account').search(cr, uid, [('code', '=', '999000'),('company_id','=',journal.company_id.id)])
            if tmp_accounts and len(tmp_accounts) > 0:
                account = tmp_accounts[0]
            else:
                tmp_account_id = False

            cr.execute("select id from res_partner_bank where replace(replace(acc_number,' ',''),'-','') like %s", ('%' + txn_bank + '%',))
            bank_ids = [id[0] for id in cr.fetchall()]
            ids = partner_obj.search(cr, uid, [('id', 'in', bank_ids)])
            if ids and len(ids) == 1:
                partner = partner_obj.browse(cr, uid, ids[0], context=context).partner_id
                if not(partner_id):
                    partner_id = partner.id
                    if partner.customer and not (partner.supplier):
                        account = partner.property_account_receivable.id
                        transaction_type = 'customer'
                    elif partner.supplier and not (partner.customer):
                        account = partner.property_account_payable.id
                        transaction_type = 'supplier'

            txn_desc_upper = txn_description.upper()
            pos = txn_desc_upper.find('SAJ/')
            posend = pos + 13
            invnbr = txn_desc_upper[pos:posend]

            if not partner_id:
                ids = invoice_obj.search(cr, uid, [('number', '=', invnbr)])
                if ids and len(ids) == 1:
                    partner = invoice_obj.browse(cr, uid, ids[0], context=context).partner_id
                    if not(partner_id):
                        partner_id = partner.id
                        if partner.customer and not (partner.supplier):
                            account = partner.property_account_receivable.id
                            transaction_type = 'customer'
                        elif partner.supplier and not (partner.customer):
                            account = partner.property_account_payable.id
                            transaction_type = 'supplier'

            stat_line_id = stat_line_obj.create(cr, uid, {
                'ref': ref,
                'statement_id': stat_id,
                'sequence': linenum,
                'type': transaction_type,
                'company_id': journal.company_id.id,
                'note': name,
                'journal_id': journal_id,
                'amount': txn_amount,
                'date': txn_date,
                'partner_id': partner_id,
                'account_id': account,
                'voucher_id': None,
                'state': 'draft',
                'name': name,
            }, context=context)
   
        if stat_id:
            stat_obj.write(cr, uid, [stat_id], {'balance_end_real': balance_end_real}, context=context)

        model, action_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'action_bank_statement_tree')
        action = self.pool.get(model).browse(cr, uid, action_id, context=context)
        return {
            'name': action.name,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'res_model': action.res_model,
            'domain': action.domain,
            'context': action.context,
            'type': 'ir.actions.act_window',
            'search_view_id': action.search_view_id.id,
            'views': [(v.view_id.id, v.view_mode) for v in action.view_ids]
        }

        return True

account_sns_import()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:# -*- coding: utf-8 -*-

