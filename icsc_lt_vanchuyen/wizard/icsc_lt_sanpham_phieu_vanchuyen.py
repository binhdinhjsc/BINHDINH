# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp.osv.orm import browse_record, browse_null
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP


class icsc_lt_phieutungphan(osv.osv):
    _name = 'icsc.lt.phieutungphan'    
    _columns = {       
        'phieu_id':  fields.many2one("icsc.phieu.vanchuyen", 'Phiếu vận chuyển', ondelete="cascade"),    
        'line_ids' : fields.one2many('icsc.lt.phieutungphan.chitiet','phieu_id','Chi tiết'),      
        'ngay_lap':fields.date('Ngày tạo')
    }   
    def default_get(self, cr, uid,fields, context=None):
        """ To get default values for the object.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param fields: List of fields for which we want default values
         @param context: A standard dictionary
         @return: A dictionary which of fields with values.
        """
      
        if context is None:
            context = {}
        phieu_pool = self.pool.get('icsc.phieu.vanchuyen')          
        vals= []
        record_id = context and context.get('active_id', False) or False
        phieu_obj = phieu_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_lt_phieutungphan, self).default_get(cr, uid, fields, context=context) 
        if phieu_obj.id:
            phieu_id=phieu_obj.id          
            if 'phieu_id' in fields:
                res.update({'phieu_id': phieu_id})  
            if 'ngay_lap'in fields:
                res.update({'ngay_lap':  time.strftime('%Y-%m-%d')})  
            return_history = self.get_return_history(cr, uid, record_id, context)
            for line in phieu_obj.chitiet_vc:
                qty = line.kl_vc - return_history.get(line.id, 0)
                if qty > 0:
                    vals.append({'product_id': line.product_id.id, 'kl_vc': qty,'chitiet_phieu_id':line.id})
            if 'line_ids' in fields:
                res.update({'line_ids': vals})
                 
        return res
    def get_return_history(self, cr, uid, pick_id, context=None):
        """ 
         Get  return_history.
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param pick_id: Picking id
         @param context: A standard dictionary
         @return: A dictionary which of values.
        """
        pick_obj = self.pool.get('icsc.phieu.vanchuyen')
        pick = pick_obj.browse(cr, uid, pick_id, context=context)
        return_history = {}
        for m  in pick.chitiet_vc:
            
            return_history[m.id] = 0
            for rec in m.history_ids:                 
                return_history[m.id] +=  rec.kl_vc
        return return_history
    def tao_phieu(self, cr, uid, ids, context=None):       
        if context is None:
            context = {} 
        phieu_pool = self.pool.get('icsc.phieu.vanchuyen')     
        chitiet_pool=self.pool.get('icsc.phieu.vanchuyen.chitiet')    
        vals= []
        record_id = context and context.get('active_id', False) or False
        phieu_obj = phieu_pool.browse(cr, uid, context.get('active_id', False))      
        #record_id = context and context.get('active_id', False) or False
        chitiet_capnhat=self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat') 
        for data in self.browse(cr, uid,ids , context):
            for line in data.line_ids:
                product_id=line.product_id.id
                kl_vc=line.kl_vc
                chitiet_phieu_id=line.chitiet_phieu_id.id
                chitiet_capnhat.create(cr, uid, {
                                               'name': chitiet_phieu_id,                                                                                                           
                                               'product_id': product_id,
                                               'phieu_id':phieu_obj.id,                                               
                                               'ngay_capnhat':data.ngay_lap,
                                               'kl_vc':kl_vc,
                                               'thanh_tien':line.chitiet_phieu_id.thanh_tien,
                                               }, context=context)
                chitiet_pool.write(cr, uid, chitiet_phieu_id, {'tung_phan':True,'state':'du_dk_tung_phan',}, context)
        phieu_pool.write(cr, uid, record_id, {'state':'du_dk',}, context)
        #chitiet_pool.write(cr, uid, record_id, {'state':'du_dk_tung_phan',}, context)
#      
#         count=count1=0
#         for phieu_vc in phieu_obj.chitiet_vc:
#             count +=1
#             sum_qty=phieu_vc.kl_vc
#             sum_capnhat=0
#             for line_capnhat in phieu_vc.history_ids:
#                 sum_capnhat +=line_capnhat.kl_vc
#             if sum_qty==sum_capnhat:
#                 count1 +=1
#         if (count==count1):
#             
#                 
          
#         # Update view id in context, lp:702939
#         model_list = {
#                 'out': 'stock.picking.out',
#                 'in': 'stock.picking.in',
#                 'internal': 'stock.picking',
#         }
#         return {
#             'domain': "[('id', 'in', ["+str(new_picking)+"])]",
#             'name': _('Returned Picking'),
#             'view_type':'form',
#             'view_mode':'tree,form',
#             'res_model': model_list.get(new_type, 'stock.picking'),
#             'type':'ir.actions.act_window',
#             'context':context,
#         }
        return {'type': 'ir.actions.act_window_close'}

icsc_lt_phieutungphan()
class icsc_lt_phieutungphan_chitiet(osv.osv):
    _name = 'icsc.lt.phieutungphan.chitiet'    
    _columns = {       
        'phieu_id':  fields.many2one("icsc.lt.phieutungphan", 'Phiếu vận chuyển', ondelete="cascade"),    
        'chitiet_phieu_id':  fields.many2one("icsc.phieu.vanchuyen.chitiet", 'Phiếu chi tiết vận chuyển', ondelete="cascade"),
        'product_id': fields.many2one('product.product', 'Tên vật tư', ondelete='cascade'),  
        'kl_vc': fields.float('KL vận chuyển/tấn'),       
      
    } 
icsc_lt_phieutungphan_chitiet () 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
