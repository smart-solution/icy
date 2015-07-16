#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields

class survey(osv.osv):
    _name = 'survey'
    _inherit = 'survey'

    def create(self, cr, uid, vals, context=None):
        vals['max_response_limit'] = 999999
        vals['response_user'] = 999999
        return super(survey, self).create(cr, uid, vals, context=context)

    _columns = {
        'used_for_sales': fields.boolean('Used For Sales'),
    }

survey()

class survey_response(osv.osv):
    _name = 'survey.response'
    _inherit = 'survey.response'

    _defaults = {
        'partner_id': lambda self,cr,uid,context:context.get('partner_id',False),
        'lead_id': lambda self,cr,uid,context:context.get('lead_id',False),
    }

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', select=True),
        'lead_id': fields.many2one('crm.lead', 'Lead/Opportunity', select=True),
    }

survey_response()

class survey_name_wiz(osv.osv):
    _name = 'survey.name.wiz'
    _inherit = 'survey.name.wiz'

    _defaults = {
        'partner_id': lambda self,cr,uid,context:context.get('partner_id',False),
        'lead_id': lambda self,cr,uid,context:context.get('lead_id',False),
    }

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', select=True),
        'lead_id': fields.many2one('crm.lead', 'Lead/Opportunity', select=True),
    }

survey_name_wiz()

class survey_question_wiz(osv.osv):
    _name = 'survey.question.wiz'
    _inherit = 'survey.question.wiz'

    _defaults = {
        'partner_id': lambda self,cr,uid,context:context.get('partner_id',False),
        'lead_id': lambda self,cr,uid,context:context.get('lead_id',False),
    }

    def action_next(self, cr, uid, ids, context=None):
        sql_stat = "select response from survey_name_wiz where id = %d" % context.get('sur_name_id',False)
        cr.execute(sql_stat)
        for sql_res in cr.dictfetchall():
            resp_id = int(sql_res['response'])
            if context.has_key('partner_id'):
                self.pool.get('survey.response').write(cr, uid, resp_id, {'partner_id':context.get('partner_id',False)})
            if context.has_key('lead_id'):
                self.pool.get('survey.response').write(cr, uid, resp_id, {'lead_id':context.get('lead_id',False)})

        return super(survey_question_wiz, self).action_next(cr, uid, ids, context=context)

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', select=True),
        'lead_id': fields.many2one('crm.lead', 'Lead/Opportunity', select=True),
    }

survey_question_wiz()

class survey_name_wiz(osv.osv):
    _name = 'survey.name.wiz'
    _inherit = 'survey.name.wiz'

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(survey_name_wiz, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=False)
        if uid != 1:
            survey_obj = self.pool.get('survey')
            line_ids = survey_obj.search(cr, uid, [('used_for_sales','=',True)], context=context)
            domain = str([('id', 'in', line_ids)])
            doc = etree.XML(res['arch'])
            nodes = doc.xpath("//field[@name='survey_id']")
            for node in nodes:
                node.set('domain', domain)
            res['arch'] = etree.tostring(doc)
        return res

survey_name_wiz()

class crm_lead(osv.osv):
    _inherit = "crm.lead"

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

            print 'IDS:',ids
            print 'CONTEXT:',context

            lead = self.browse(cr, uid, ids, context=context)
            lead_id = lead.id

            context.update({'lead_id': lead.id})
            if lead.partner_id:
                context.update({'partner_id': lead.partner_id.id})

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

    _columns = {'survey_ids' : fields.one2many('survey.response', 'lead_id', 'Checklists'),
	}

crm_lead()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

