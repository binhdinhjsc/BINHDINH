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


class icsc_lt_chang1(osv.osv):
    _name = 'icsc.lt.chang1'    
    _columns = {       
        'kehoach_id':  fields.many2one("icsc.hopdong.vanchuyen.giacuoc.kehoach", 'Kế hoạch vận chuyển', ondelete="cascade"),    
        'line_ids' : fields.one2many('icsc.lt.chang1.chitiet','kehoach_id','Chi tiết'),      
        
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
        phieu_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')          
        vals= []
        record_id = context and context.get('active_id', False) or False
        phieu_obj = phieu_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_lt_chang1, self).default_get(cr, uid, fields, context=context) 
        if phieu_obj.id:
            kehoach_id=phieu_obj.id          
            if 'kehoach_id' in fields:
                res.update({'kehoach_id': kehoach_id}) 
             
            return_history = self.get_return_history(cr, uid, phieu_obj.kehoach_cha.id, context)
           
            for line in phieu_obj.kehoach_cha.chitiet_kh:
                # tinh con lai LXH
                #lxk_line_id=line.sale_order_line.id
                #query=""""""
                # end
                qty = line.kl_vc_kehoach - return_history.get(line.id, 0)
                if qty > 0:
                    vals.append({'sale_order_line':line.sale_order_line.id,
                                 'kl_vc_dukien':line.kl_vc_kehoach,
                                 'kl_can_vanchuyen':qty,
                                 'kl_vc_conlai': line.sale_order_line.ton_khvc,
                                 'product_id': line.product_id.id, 
                                 'kl_vc_kehoach': qty,
                                 'chitiet_phieu_id':line.id,
                                 'dia_chi_giao':line.dia_chi_giao.id})
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
        pick_obj = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        pick = pick_obj.browse(cr, uid, pick_id, context=context)
        return_history = {}
        for m  in pick.chitiet_kh:            
            return_history[m.id] = 0
                           
            cr.execute("""select coalesce(sum(ct.kl_vc_kehoach),0) as kl_vc_kehoach
                from  icsc_hopdong_vanchuyen_chitiet ct
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                where kh.chang_khvc!='chang_2' and ct.cha_id= """+str(m.id)) 
            for item in cr.dictfetchall():                             
                return_history[m.id] +=  item['kl_vc_kehoach']
        return return_history
#         return_history[pick.id] = 0
#         cr.execute("""select coalesce(sum(kl_vc_kehoach),0) as kl_vc_kehoach
#                     from  icsc_hopdong_vanchuyen_chitiet
#                     where cha_id= """+str(pick.id)) 
#         for item in cr.dictfetchall():                             
#             return_history[pick.id] +=  item['kl_vc_kehoach']
#         return return_history
    def tao_phieu(self, cr, uid, ids, context=None):       
        if context is None:
            context = {} 
        phieu_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')     
        chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')    
        vals= []
        record_id = context and context.get('active_id', False) or False
        phieu_obj = phieu_pool.browse(cr, uid, context.get('active_id', False))      
        #record_id = context and context.get('active_id', False) or False         
        for data in self.browse(cr, uid,ids , context):
            for line in data.line_ids:  
                cha=line.chitiet_phieu_id.id
                kh=phieu_obj.id
                check=0
                cr.execute("""select count(*) as sl from icsc_hopdong_vanchuyen_chitiet
                                where cha_id= """+str(cha)+""" and kehoach_id= """+str(kh))  
                for check_item in cr.dictfetchall():
                    check= check_item['sl']
                if check==0:         
                    chitiet_pool.create(cr, uid, {
                                               'cha_id': cha,                                                                                                           
                                               'product_id': line.product_id.id,
                                               'sale_order_line':line.sale_order_line.id,                                               
                                               'kl_vc_dukien':line.chitiet_phieu_id.kl_vc_kehoach,
                                               'kl_vc_kehoach':line.kl_vc_kehoach,
                                               'kl_can_vanchuyen':line.kl_vc_kehoach,
                                               'kehoach_id':phieu_obj.id,
                                               'dia_chi_giao':line.dia_chi_giao.id,
                                               }, context=context)                
        return {'type': 'ir.actions.act_window_close'}

icsc_lt_chang1()
class icsc_lt_chang1_chitiet(osv.osv):
    _name = 'icsc.lt.chang1.chitiet'    
    _columns = {       
        'kehoach_id':  fields.many2one("icsc.lt.chang1", 'KH vận chuyển', ondelete="cascade"),    
        'chitiet_phieu_id':  fields.many2one("icsc.hopdong.vanchuyen.chitiet", 'Phiếu chi tiết vận chuyển', ondelete="cascade"),
        'product_id': fields.many2one('product.product', 'Sản phẩm', ondelete='cascade'),        
        'kl_vc_dukien': fields.float('KL/cha'),
        'kl_vc_kehoach': fields.float('KL/con'),       
        'kl_can_vanchuyen': fields.float('KL còn lại/cha'),         
        'sale_order_line': fields.many2one('sale.order.line', 'Chi tiết LXH', ondelete='cascade'),                
        'kl_vc_conlai': fields.float('KL còn lại/LXH'),       
        'kl_dangvc_dukien': fields.float('KL đang VC/cha'),
        'dia_chi_giao':fields.many2one('res.partner', 'Địa chỉ giao hàng',domain="[('parent_other_id','=',parent.khach_hang)]", ondelete="cascade"),
    } 
icsc_lt_chang1_chitiet () 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
