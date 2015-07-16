#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields

class crm_lead(osv.osv):
    _inherit = 'crm.lead'

    _columns = {
		'icy_task_ids': fields.one2many('project.task', 'icy_lead_id', 'Taken', select=True),
    }

crm_lead

class project_task(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'icy_lead_id': fields.many2one('crm.lead', 'Lead', select=True),
    }

project_task()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

