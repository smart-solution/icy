#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
from openerp import tools

class crm_case_categ(osv.osv):
    _name = 'crm.case.categ'
    _inherit = 'crm.case.categ'

#     def _get_image(self, cr, uid, ids, name, args, context=None):
#         result = dict.fromkeys(ids, False)
#         for obj in self.browse(cr, uid, ids, context=context):
#             result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
#         return result
# 
#     def _set_image(self, cr, uid, id, name, value, args, context=None):
#         return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _columns = {
        'image': fields.binary("Image",
            help="This field holds the image used as image for the product, limited to 1024x1024px."),

#         'image': fields.function(_get_image, fnct_inv=_set_image,
#             string="Small-sized image", type="binary", multi="_get_image",
#             store={
#                 'asset.asset': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
#             },
#             help="Small-sized image of the asset. It is automatically "\
#                  "resized as a 64x64px image, with aspect ratio preserved. "\
#                  "Use this field anywhere a small image is required."),
#         'active': fields.boolean('Active'),
    }

#     _defaults = {
#         'active': True,
#     }
        
crm_case_categ()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

