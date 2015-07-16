# -*- coding: utf-8 -*-
###############################################
from osv import fields,osv
from tools.sql import drop_view_if_exists

class res_partner_history(osv.osv):
    _name = "res_partner_history"
    _description = "Partner History"
    _auto = False

    _columns = {
	'date': fields.datetime('Datum', readonly=True),
	'partner_id': fields.many2one('res.partner', 'Partner', select=True, readonly=True),
	'partner_name': fields.char('Partnernaam', select=True, readonly=True),
	'id': fields.integer('ID'),
	'description': fields.char('Omschrijving', readonly=True),
	'reference': fields.text('Referentie', readonly=True),
	'user_id': fields.many2one('res.users', 'Gebruiker', select=True, readonly=True),
	'type': fields.char('Type', readonly=True),
	'amount': fields.float('Bedrag', readonly=True),
	'state': fields.char('Status', readonly=True),
	'sale_order_id': fields.many2one('sale.order', 'Verkooporder', select=True, readonly=True),
	'purchase_order_id': fields.many2one('purchase.order', 'Inkooporder', select=True, readonly=True),
	'stock_picking_id': fields.many2one('stock.picking', 'Pakbon', select=True, readonly=True),
	'account_invoice_id': fields.many2one('account.invoice', 'Factuur', select=True, readonly=True),
	'crm_helpdesk_id': fields.many2one('crm.helpdesk', 'Service Call', select=True, readonly=True),
	'payment_order_id': fields.many2one('payment.line', 'Betaling', select=True, readonly=True),
	'crm_meeting_id': fields.many2one('crm.meeting', 'Afspraak', select=True, readonly=True),
	'crm_phonecall_id': fields.many2one('crm.phonecall', 'Telefoon', select=True, readonly=True),
	'crm_lead_id': fields.many2one('crm.lead', 'Verkoopkans', select=True, readonly=True),
	'task_id': fields.many2one('project.task', 'Taak', select=True, readonly=True),
	'message_id': fields.many2one('mail.message', 'Bericht', select=True, readonly=True),
	'customer':fields.boolean('Klant'),
	'supplier':fields.boolean('Leverancier'),
	'consumer':fields.boolean('Consumer'),
    }

    _order = 'date desc'

    def init(self, cr):
        drop_view_if_exists(cr, 'res_partner_history')

#	cr.execute("""
#CREATE OR REPLACE FUNCTION strip_tags(text)
#  RETURNS text AS
#$BODY$
#    SELECT regexp_replace(regexp_replace($1, E'(?x)<[^>]*?(\s alt \s* = \s* ([\'"]) ([^>]*?) \2) [^>]*? >', E'\3'), E'(?x)(< [^>]*? >)', '', 'g')
#$BODY$
#  LANGUAGE sql VOLATILE
#  COST 100;
#ALTER FUNCTION strip_tags(text)
#  OWNER TO postgres;
#""")

        cr.execute("""create or replace view res_partner_history
as
select  (1000000 + sale_order.id) as id,
        partner_id,
	res_partner.name as partner_name,
	sale_order.name as description,
	client_order_ref as reference,
	sale_order.create_uid as user_id,
	date_order::date as date,
	'Verkooporder' as type,
	amount_total as amount,
	case when state = 'done' then 'Uitgevoerd'
	     when state = 'sent' then 'Verzonden'
	     when state = 'manual' then 'Handmatig'
	     when state = 'invoice_except' then 'Probleem'
	     when state = 'draft' then 'Verkoopofferte'
	     when state = 'progress' then 'In Uitvoering'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	sale_order.id as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from sale_order
join res_partner on (res_partner.id = partner_id)
union
select  (2000000 + purchase_order.id) as id,
        partner_id,
	res_partner.name as partner_name,
	purchase_order.name as description,
	partner_ref as reference,
	purchase_order.create_uid as user_id,
	date_order::date as date,
	'Inkooporder' as type,
	amount_total as amount,
	case when state = 'approved' then 'Inkooporder'
	     when state = 'draft' then 'Inkoopofferte'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	purchase_order.id as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from purchase_order
join res_partner on (res_partner.id = partner_id)
union
select  (3000000 + stock_picking.id) as id,
        partner_id,
	res_partner.name as partner_name,
	stock_picking.name as description,
	origin as reference,
	stock_picking.create_uid as user_id,
	stock_picking.date::date as date,
	case when stock_picking.type = 'in' then 'Ontvangst' else 'Levering' end as type,
	NULL::float as amount,
	case when state = 'done' then 'Uitgevoerd'
	     when state = 'assigned' then 'In Voorbereiding'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	sale_id as sale_order_id,
	purchase_id as purchase_order_id,
	stock_picking.id as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from stock_picking
join res_partner on (res_partner.id = partner_id)
union
select  (4000000 + account_invoice.id) as id,
        partner_id,
	res_partner.name as partner_name,
	number as description,
	origin as reference,
	account_invoice.create_uid as user_id,
	date_invoice::date as date,
	case when account_invoice.type = 'in_invoice' then 'Leverancierfactuur'
	     when account_invoice.type = 'in_refund' then 'Leverancierkredietnota'
	     when account_invoice.type = 'out_invoice' then 'Klantfactuur'
	     when account_invoice.type = 'out_refund' then 'Klantkredietnota'
	     else 'Ongekend' end as type,
	amount_total as amount,
	case when state = 'open' then 'Open'
	     when state = 'paid' then 'Betaald'
	     when state = 'draft' then 'In Voorbereiding'
	     when state = 'proforma2' then 'Pro Forma'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	account_invoice.id as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from account_invoice
join res_partner on (res_partner.id = partner_id)
union
select  (5000000 + crm_helpdesk.id) as id,
        partner_id,
	res_partner.name as partner_name,
	cast(crm_helpdesk.id as text) as description,
	crm_helpdesk.name as reference,
	crm_helpdesk.create_uid as user_id,
	crm_helpdesk.date::date as date,
	'Servicecall' as type,
	NULL::float as amount,
	case when state = 'done' then 'Afgesloten'
	     when state = 'open' then 'Open'
	     when state = 'draft' then 'In Voorbereiding'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	crm_helpdesk.id as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from crm_helpdesk
join res_partner on (res_partner.id = partner_id)
union
select  (6000000 + payment_line.id) as id,
        partner_id,
	res_partner.name as partner_name,
	payment_order.reference as description,
	communication as reference,
	payment_order.user_id,
	payment_line.date::date as date,
	'Betaling' as type,
	amount_currency as amount,
	case when payment_order.state = 'done' then 'Afgesloten'
	     when payment_order.state = 'open' then 'Open'
	     when payment_order.state = 'draft' then 'In Voorbereiding'
	     when payment_order.state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	payment_line.id as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from payment_line
join payment_order on (order_id = payment_order.id)
join res_partner on (res_partner.id = partner_id)
union
select  (7000000 + crm_meeting.id) as id,
        partner_id,
	res_partner.name as partner_name,
	crm_meeting.name as description,
	location as reference,
	crm_meeting.user_id,
	crm_meeting.date::date as date,
	'Afspraak' as type,
	NULL::float as amount,
	case when state = 'done' then 'Afgesloten'
	     when state = 'open' then 'Open'
	     when state = 'draft' then 'In Voorbereiding'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	crm_meeting.id as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from crm_meeting
join crm_meeting_partner_rel on (meeting_id = crm_meeting.id)
join res_partner on (res_partner.id = partner_id)
union
select  (8000000 + crm_phonecall.id) as id,
        partner_id,
	res_partner.name as partner_name,
	crm_phonecall.name as description,
	description as reference,
	crm_phonecall.user_id,
	crm_phonecall.date::date as date,
	'Telefoon' as type,
	NULL::float as amount,
	case when state = 'done' then 'Afgesloten'
	     when state = 'open' then 'Open'
	     when state = 'draft' then 'In Voorbereiding'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	crm_phonecall.id as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from crm_phonecall
join res_partner on (res_partner.id = partner_id)
union
select  (9000000 + crm_lead.id) as id,
        partner_id,
	res_partner.name as partner_name,
	crm_lead.name as description,
	description as reference,
	crm_lead.user_id,
	date_open::date as date,
	'Verkoopkans' as type,
	NULL::float as amount,
	case when state = 'done' then 'Afgesloten'
	     when state = 'open' then 'Open'
	     when state = 'draft' then 'In Voorbereiding'
	     when state = 'cancel' then 'Geannuleerd'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	crm_lead.id as crm_lead_id,
	NULL::integer as task_id,
	NULL::integer as message_id,
	customer,
	supplier,
	consumer
from crm_lead
join res_partner on (res_partner.id = partner_id)
union
select  (11000000 + mail_message.id) as id,
        res_id as partner_id,
	res_partner.name as partner_name,
	record_name as description,
	strip_tags(body) as reference,
	mail_message.create_uid as user_id,
	mail_message.date::date as date,
	'Bericht' as type,
	NULL::float as amount,
	case when mail_message.type = 'notification' then 'Bericht'
	     when mail_message.type = 'comment' then 'Commentaar'
	     else 'Ongekend' end as state,
	NULL::integer as sale_order_id,
	NULL::integer as purchase_order_id,
	NULL::integer as stock_picking_id,
	NULL::integer as account_invoice_id,
	NULL::integer as crm_helpdesk_id,
	NULL::integer as payment_order_id,
	NULL::integer as crm_meeting_id,
	NULL::integer as crm_phonecall_id,
	NULL::integer as crm_lead_id,
	NULL::integer as task_id,
	mail_message.id as message_id,
	customer,
	supplier,
	consumer
from mail_message
join res_partner on (res_partner.id = res_id)
where model = 'res.partner'

order by partner_id, date desc, id desc;""")

res_partner_history()

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
	'partner_history_ids': fields.one2many('res.partner.history', 'partner_id', 'Geschiedenis'),
    }

res_partner()

