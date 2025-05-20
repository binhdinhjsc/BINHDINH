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


class icsc_lt_chitiet_sanpham(osv.osv):
    _name = 'icsc.lt.chitiet.sanpham'    
    _columns = {       
        'kehoach_id':  fields.many2one("icsc.hopdong.vanchuyen.giacuoc.kehoach", 'Kế hoạch', ondelete="cascade"),     
        'sale_id': fields.many2one("sale.order", 'Lệnh xuất hàng',),     
        'line_ids' : fields.many2many('sale.order.line','kehoach_xuathang_rel',id1='order_line_id', id2='chitiet_kehoach_id',
                                      string='Danh sách sản phẩm đưa vào kế hoạch',
                                      domain="[('order_id','=', sale_id)]"),      
   
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
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')          
        vals= []
        kehoach_obj = kehoach_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_lt_chitiet_sanpham, self).default_get(cr, uid, fields, context=context) 
        if kehoach_obj.id:
            kehoach_id=kehoach_obj.id
            sale_id=kehoach_obj.sale_id.id
            for line in kehoach_obj.sale_id.order_line:
                if line.state !='cancel':
                    vals.append(line.id)
                
            if 'sale_id' in fields:
                res.update({'sale_id': sale_id})  
            if 'kehoach_id' in fields:
                res.update({'kehoach_id': kehoach_id})  
            if 'line_ids' in fields:
                res.update({'line_ids': vals})  
            
     
        return res
    def tao_kehoach_vanchuyen(self, cr, uid, ids,  context=None):
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.chitiet') 
        kehoach_diadiem=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        
        for data in self.browse(cr, uid, ids, context):
            kehoach_id=data.kehoach_id.id
            kehoach_name=data.kehoach_id.name
            is_parent=data.kehoach_id.parent_id
            ke_hoach_cha=data.kehoach_id.kehoach_cha.id
            trung_chuyen=data.kehoach_id.trung_chuyen
            sale_id=data.kehoach_id.sale_id.id
            # NEU LA CO TRUNG CHUYEN VA LA KE HOACH CHA
            #if (trung_chuyen == False) and (is_parent==False) and (ke_hoach_cha==False):
            count_cha=0
            # KIEM TRA XEM KE HOACH NAY LA KE HOACH CHA THU MAY CUA LXH
            query_kiemtra1="""select * from icsc_hopdong_vanchuyen_giacuoc_kehoach
            where sale_id= """+str(sale_id)+""" and ((coalesce(trung_chuyen,False)=False  and coalesce(parent_id,False)=False) or (coalesce(trung_chuyen,False)=True  and coalesce(parent_id,False)=True))
             and coalesce(kehoach_cha,0)=0 order by id asc limit 1"""
            cr.execute(query_kiemtra1)
            for item_kiemtra1 in cr.dictfetchall():
                cha_id=item_kiemtra1['id']
                if kehoach_id==cha_id:
                    count_cha +=1
            # NEU LA CHA 1
            if count_cha==1:
                for line in data.line_ids:
                    kl_vc_kehoach=line.product_uom_qty
                    kl_vc_dukien=line.product_uom_qty
                    kl_can_vanchuyen=line.product_uom_qty
                    count=0
                    query_check="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                                 where sale_order_line= """+str(line.id)+""" and kehoach_id= """+str(kehoach_id)
                    cr.execute(query_check)
                    for check in cr.dictfetchall():
                        count =check['count']
                    if count==0:
                        kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                             'kl_vc_dukien':kl_vc_dukien,
                                             'kehoach_id':kehoach_id,
                                             'dia_chi_giao':line.dia_chi_giao.id,                                             
                                             'kl_can_vanchuyen':kl_can_vanchuyen,
                                             'kl_vc_kehoach':kl_vc_kehoach,
                                             'sale_order_line':line.id,
                                             }, context=context)
            else:
                cha_truoc=False
                query_kiemtra2="""select * from icsc_hopdong_vanchuyen_giacuoc_kehoach
                where sale_id= """+str(sale_id)+""" and ((coalesce(trung_chuyen,False)=False  and coalesce(parent_id,False)=False) or (coalesce(trung_chuyen,False)=True  and coalesce(parent_id,False)=True))
             and coalesce(kehoach_cha,0)=0  and id < """+str(kehoach_id)+""" order by id desc limit 1"""
                cr.execute(query_kiemtra2)
                for item_kiemtra2 in cr.dictfetchall(): 
                    cha_truoc= item_kiemtra2['id']
                    #kehoachcha_obj=kehoach_diadiem.browse(cr, uid, cha_truoc, context)
                    #kl_can_vanchuyen=kehoachcha_obj.kl_vc_conlai
                if cha_truoc:
                    for line in data.line_ids:
                        # KIEM TRA XEM TRONG KE HOACH CHA TRUOC DO DA GIAO SAN PHAM NAY HAY CHUA?
                        # NEU DA GIAO ROI THI LAY SO LUONG CON LAI
                        # NEU KHONG SE LAY SO LUONG TREN DON HANG
                        sale_order_line=line.id
                        count2=0
                        query_check2="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                                     where sale_order_line= """+str(sale_order_line)+""" and kehoach_id= """+str(kehoach_id)
                        cr.execute(query_check2)
                        for check2 in cr.dictfetchall():
                            count2 =check2['count']
                        kl_vc_kehoach=line.product_uom_qty
                        kl_vc_dukien=line.product_uom_qty
                        kl_can_vanchuyen=line.product_uom_qty
                        dia_chi_giao=line.dia_chi_giao.id
#                         query_kiemtra_sanpham_cha1="""select line.id as line from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
#                         left join icsc_hopdong_vanchuyen_chitiet line on line.kehoach_id=kh.id
#                         where  ((coalesce(trung_chuyen,False)=False  and coalesce(parent_id,False)=False) or (coalesce(trung_chuyen,False)=True  and coalesce(parent_id,False)=True))
#                          and coalesce(kehoach_cha,0)=0 and 
#                           line.sale_order_line= """+str(sale_order_line)+""" order by line.id asc"""
#                         cr.execute(query_kiemtra_sanpham_cha1)
#                         for item_kiemtra_sanpham_cha1 in cr.dictfetchall(): 
#                             chitiet_chatruoc=item_kiemtra_sanpham_cha1['line']
#                             chitiet_chatruoc_obj=kehoach_pool.browse(cr, uid, chitiet_chatruoc, context)
#                             kl_can_vanchuyen=chitiet_chatruoc_obj.kl_can_vanchuyen - chitiet_chatruoc_obj.kl_vc_kehoach
#                             kl_vc_kehoach=kl_can_vanchuyen
                        kl_vc_kehoach=line.ton_khvc
                        
                        if kl_can_vanchuyen>0 and kl_vc_kehoach>0:
                            if count2==0:
                                kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                                 'kl_vc_dukien':kl_vc_dukien,
                                                 'kehoach_id':kehoach_id,
                                                 'dia_chi_giao':dia_chi_giao,                                             
                                                 'kl_can_vanchuyen':kl_can_vanchuyen,
                                                 'kl_vc_kehoach':kl_vc_kehoach,
                                                 'sale_order_line':sale_order_line,
                                                 }, context=context)
            kehoach_diadiem.write(cr, uid, [kehoach_id], {'den_diem': line.dia_chi_giao.id}, context=context)
       
        return {'type': 'ir.actions.act_window_close'}
    def tao_kehoach_vanchuyen1(self, cr, uid, ids,  context=None):
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.chitiet') 
        kehoach_diadiem=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        for data in self.browse(cr, uid, ids, context):
            kehoach_id=data.kehoach_id.id
            kehoach_name=data.kehoach_id.name
            is_parent=data.kehoach_id.parent_id
            ke_hoach_cha=data.kehoach_id.kehoach_cha.id
            trung_chuyen=data.kehoach_id.trung_chuyen
            sale_id=data.kehoach_id.sale_id.id
            # NEU LA CO TRUNG CHUYEN VA LA KE HOACH CHA
            if (trung_chuyen == False) and (is_parent==False) and (ke_hoach_cha==False):
                count_cha=0
                # KIEM TRA XEM KE HOACH NAY LA KE HOACH CHA THU MAY CUA LXH
                query_kiemtra1="""select * from icsc_hopdong_vanchuyen_giacuoc_kehoach
                where sale_id= """+str(sale_id)+""" and trung_chuyen=False  and
                parent_id=False and coalesce(kehoach_cha,0)=0 order by id asc limit 1"""
                cr.execute(query_kiemtra1)
                for item_kiemtra1 in cr.dictfetchall():
                    cha_id=item_kiemtra1['id']
                    if kehoach_id==cha_id:
                        count_cha +=1
                # NEU LA CHA 1
                if count_cha==1:
                    for line in data.line_ids:
                        kl_vc_kehoach=line.product_uom_qty
                        kl_vc_dukien=line.product_uom_qty
                        kl_can_vanchuyen=line.product_uom_qty
                        count=0
                        query_check="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                                     where sale_order_line= """+str(line.id)+""" and kehoach_id= """+str(kehoach_id)
                        cr.execute(query_check)
                        for check in cr.dictfetchall():
                            count =check['count']
                        if count==0:
                            kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                                 'kl_vc_dukien':kl_vc_dukien,
                                                 'kehoach_id':kehoach_id,
                                                 'dia_chi_giao':line.dia_chi_giao.id,                                             
                                                 'kl_can_vanchuyen':kl_can_vanchuyen,
                                                 'kl_vc_kehoach':kl_vc_kehoach,
                                                 'sale_order_line':line.id,
                                                 }, context=context)
                else:
                    cha_truoc=False
                    query_kiemtra2="""select * from icsc_hopdong_vanchuyen_giacuoc_kehoach
                    where sale_id= """+str(sale_id)+""" and trung_chuyen=False  and
                    parent_id=False and coalesce(kehoach_cha,0)=0 and id < """+str(kehoach_id)+""" order by id desc limit 1"""
                    cr.execute(query_kiemtra2)
                    for item_kiemtra2 in cr.dictfetchall(): 
                        cha_truoc= item_kiemtra2['id']
                        #kehoachcha_obj=kehoach_diadiem.browse(cr, uid, cha_truoc, context)
                        #kl_can_vanchuyen=kehoachcha_obj.kl_vc_conlai
                    if cha_truoc:
                        for line in data.line_ids:
                            # KIEM TRA XEM TRONG KE HOACH CHA TRUOC DO DA GIAO SAN PHAM NAY HAY CHUA?
                            # NEU DA GIAO ROI THI LAY SO LUONG CON LAI
                            # NEU KHONG SE LAY SO LUONG TREN DON HANG
                            sale_order_line=line.id
                            count2=0
                            query_check2="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                                         where sale_order_line= """+str(sale_order_line)+""" and kehoach_id= """+str(kehoach_id)
                            cr.execute(query_check2)
                            for check2 in cr.dictfetchall():
                                count2 =check2['count']
                            kl_vc_kehoach=line.product_uom_qty
                            kl_vc_dukien=line.product_uom_qty
                            kl_can_vanchuyen=line.product_uom_qty
                            dia_chi_giao=line.dia_chi_giao.id
                            query_kiemtra_sanpham_cha1="""select line.id as line from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                            left join icsc_hopdong_vanchuyen_chitiet line on line.kehoach_id=kh.id
                            where --trung_chuyen=False and parent_id=False  and 
                             coalesce(kehoach_cha,0)=0 and 
                              line.sale_order_line= """+str(sale_order_line)+""" order by line.id asc"""
                            cr.execute(query_kiemtra_sanpham_cha1)
                            for item_kiemtra_sanpham_cha1 in cr.dictfetchall(): 
                                chitiet_chatruoc=item_kiemtra_sanpham_cha1['line']
                                chitiet_chatruoc_obj=kehoach_pool.browse(cr, uid, chitiet_chatruoc, context)
                                kl_can_vanchuyen=chitiet_chatruoc_obj.kl_vc_conlai
                                kl_vc_kehoach=kl_can_vanchuyen
                            if kl_can_vanchuyen>0:
                                if count2==0:
                                    kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                                     'kl_vc_dukien':kl_vc_dukien,
                                                     'kehoach_id':kehoach_id,
                                                     'dia_chi_giao':dia_chi_giao,                                             
                                                     'kl_can_vanchuyen':kl_can_vanchuyen,
                                                     'kl_vc_kehoach':kl_vc_kehoach,
                                                     'sale_order_line':sale_order_line,
                                                     }, context=context)
                kehoach_diadiem.write(cr, uid, kehoach_id, {'den_diem': line.dia_chi_giao.id}, context=context)
            # NEU LA CO TRUNG CHUYEN VA LA KE HOACH CHA
            if trung_chuyen and is_parent:
                count_cha=0
                # KIEM TRA XEM KE HOACH NAY LA KE HOACH CHA THU MAY CUA LXH
                query_kiemtra1="""select * from icsc_hopdong_vanchuyen_giacuoc_kehoach
                where sale_id= """+str(sale_id)+""" and parent_id=True and trung_chuyen=True order by id asc limit 1"""
                cr.execute(query_kiemtra1)
                for item_kiemtra1 in cr.dictfetchall():
                    cha_id=item_kiemtra1['id']
                    if kehoach_id==cha_id:
                        count_cha +=1
                # NEU LA CHA 1
                if count_cha==1:
                    for line in data.line_ids:
                        kl_vc_kehoach=line.product_uom_qty
                        kl_vc_dukien=line.product_uom_qty
                        kl_can_vanchuyen=line.product_uom_qty
                        count3=0
                        query_check3="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                                     where sale_order_line= """+str(line.id)+""" and kehoach_id= """+str(kehoach_id)
                        cr.execute(query_check3)
                        for check3 in cr.dictfetchall():
                            count3 =check3['count']
                        if count3==0:
                            kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                                 'kl_vc_dukien':kl_vc_dukien,
                                                 'kehoach_id':kehoach_id,
                                                 'dia_chi_giao':line.dia_chi_giao.id,                                             
                                                 'kl_can_vanchuyen':kl_can_vanchuyen,
                                                 'kl_vc_kehoach':kl_vc_kehoach,
                                                 'sale_order_line':line.id,
                                                 }, context=context)
                else:
                    cha_truoc=False
                    query_kiemtra2="""select * from icsc_hopdong_vanchuyen_giacuoc_kehoach
                    where sale_id= """+str(sale_id)+""" and parent_id=True and id < """+str(kehoach_id)+""" and trung_chuyen=True 
                    order by id desc limit 1"""
                    cr.execute(query_kiemtra2)
                    for item_kiemtra2 in cr.dictfetchall(): 
                        cha_truoc= item_kiemtra2['id']
                        #kehoachcha_obj=kehoach_diadiem.browse(cr, uid, cha_truoc, context)
                        #kl_can_vanchuyen=kehoachcha_obj.kl_vc_conlai
                    if cha_truoc:
                        for line in data.line_ids:
                            # KIEM TRA XEM TRONG KE HOACH CHA TRUOC DO DA GIAO SAN PHAM NAY HAY CHUA?
                            # NEU DA GIAO ROI THI LAY SO LUONG CON LAI
                            # NEU KHONG SE LAY SO LUONG TREN DON HANG
                            
                            sale_order_line=line.id
                            count4=0
                            query_check4="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                                         where sale_order_line= """+str(sale_order_line)+""" and kehoach_id= """+str(kehoach_id)
                            cr.execute(query_check4)
                            for check4 in cr.dictfetchall():
                                count4 =check4['count']
                            kl_vc_kehoach=line.product_uom_qty
                            kl_vc_dukien=line.product_uom_qty
                            kl_can_vanchuyen=line.product_uom_qty
                            dia_chi_giao=line.dia_chi_giao.id
                            query_kiemtra_sanpham_cha1="""select line.id as line from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                            left join icsc_hopdong_vanchuyen_chitiet line on line.kehoach_id=kh.id
                            where --parent_id=True and trung_chuyen=True 
                                coalesce(kehoach_cha,0)=0 and 
                            and line.sale_order_line= """+str(sale_order_line)+""" order by line.id asc"""
                            cr.execute(query_kiemtra_sanpham_cha1)
                            for item_kiemtra_sanpham_cha1 in cr.dictfetchall(): 
                                chitiet_chatruoc=item_kiemtra_sanpham_cha1['line']
                                chitiet_chatruoc_obj=kehoach_pool.browse(cr, uid, chitiet_chatruoc, context)
                                kl_can_vanchuyen=chitiet_chatruoc_obj.kl_vc_conlai
                                kl_vc_kehoach=kl_can_vanchuyen
                            if count4==0:
                                kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                                 'kl_vc_dukien':kl_vc_dukien,
                                                 'kehoach_id':kehoach_id,
                                                 'dia_chi_giao':dia_chi_giao,                                             
                                                 'kl_can_vanchuyen':kl_can_vanchuyen,
                                                 'kl_vc_kehoach':kl_vc_kehoach,
                                                 'sale_order_line':sale_order_line,
                                                 }, context=context)                 
                kehoach_diadiem.write(cr, uid, kehoach_id, {'den_diem': line.dia_chi_giao.id}, context=context)
        return {'type': 'ir.actions.act_window_close'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

class icsc_lt_sanpham_ngoaile(osv.osv):
    _name = 'icsc.lt.sanpham.ngoaile'    
    _columns = {       
        'kehoach_id':  fields.many2one("icsc.hopdong.vanchuyen.giacuoc.kehoach", 'Kế hoạch', ondelete="cascade"),     
        'sale_id': fields.many2one("sale.order", 'Lệnh xuất hàng',),     
        'line_ids' : fields.one2many('icsc.lt.chitiet.sanpham.ngoaile','parent_id',
                                    'Danh sách sản phẩm đưa vào kế hoạch',),  
   
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
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')          
        vals= []
        kehoach_obj = kehoach_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_lt_sanpham_ngoaile, self).default_get(cr, uid, fields, context=context) 
        if kehoach_obj.id:
            kehoach_id=kehoach_obj.id
            sale_id=kehoach_obj.sale_id.id
            for line in kehoach_obj.sale_id.order_line:
                if line.state !='cancel':
                    #vals.append(line.id)
                    vals.append({'product_id':line.product_id.id,
                             'dia_chi_giao': line.dia_chi_giao.id, 
                             'sale_line_id':line.id,
                             'product_uom_qty':line.product_uom_qty,
                             'product_uom':line.product_uom.id,
                             'kl_can_vanchuyen':line.ton_khvc,
                             'ton_khvc':line.ton_khvc,
                             })
                
            if 'sale_id' in fields:
                res.update({'sale_id': sale_id})  
            if 'kehoach_id' in fields:
                res.update({'kehoach_id': kehoach_id})  
            if 'line_ids' in fields:
                res.update({'line_ids': vals})  
        return res
    def tao_kehoach_vanchuyen(self, cr, uid, ids,  context=None):
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.chitiet') 
        kehoach_diadiem=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        for data in self.browse(cr, uid, ids, context):
            kehoach_id=data.kehoach_id.id           
            for line in data.line_ids:
                count3=0
                query_check3="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet
                             where sale_order_line= """+str(line.sale_line_id.id)+""" and kehoach_id= """+str(kehoach_id)
                cr.execute(query_check3)
                for check3 in cr.dictfetchall():
                    count3 =check3['count']
                if line.kl_can_vanchuyen > 0 and count3==0:
                    kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                             'kl_vc_dukien':line.kl_can_vanchuyen,
                             'kehoach_id':kehoach_id,
                             'dia_chi_giao':line.dia_chi_giao.id,                                             
                             'kl_can_vanchuyen':line.kl_can_vanchuyen,
                             'kl_vc_kehoach':line.kl_can_vanchuyen,
                             'sale_order_line':line.sale_line_id.id,
                             }, context=context)
            kehoach_diadiem.write(cr, uid, [kehoach_id], {'den_diem': line.dia_chi_giao.id}, context=context)
       
        return {'type': 'ir.actions.act_window_close'}
icsc_lt_sanpham_ngoaile()
class icsc_lt_chitiet_sanpham_ngoaile(osv.osv):
    _name = 'icsc.lt.chitiet.sanpham.ngoaile'    
    _columns = {       
        'sale_line_id': fields.many2one("sale.order.line", 'Chi tiết LXH',),     
        'product_id':fields.many2one("product.product", 'Sản phẩm',),     
        'dia_chi_giao':fields.many2one("res.partner", 'Địa chỉ giao hàng',), 
        'product_uom_qty':fields.float('KL/LXH', digits=(15,2)),
        'product_uom':fields.many2one('product.uom','Đơn vị/LXH'),
        'kl_can_vanchuyen':fields.float('KL cần vận chuyển', digits=(15,2)),
        'ton_khvc':fields.float('KL còn lại/LXH', digits=(15,2)),
        'parent_id':fields.many2one("icsc.lt.sanpham.ngoaile", 'Sản phẩm ngoại lệ',),     
   
    }   
icsc_lt_chitiet_sanpham_ngoaile()