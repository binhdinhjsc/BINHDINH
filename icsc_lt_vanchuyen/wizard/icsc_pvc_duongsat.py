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

class icsc_pvc_duongsat(osv.osv):
    _name = 'icsc.pvc.duongsat'
    _description = 'PVC'
    _columns = {
        'name': fields.char('Tên',size=256), 
        'user_id' : fields.many2one('res.users', 'Người cập nhật'),  
        'phieu_vc' : fields.many2one('icsc.phieu.vanchuyen.duongsat', 'Phiếu vận chuyển'),             
        'line_ids' : fields.one2many('icsc.pvc.duongsat.line','parent_id','Chi tiết kế hoạch' ),      
        'congty_vc': fields.many2one('res.partner', 'Đơn vị vận chuyển', ondelete="cascade"),
         'hopdong_vanchuyen': fields.many2one('icsc.hopdong.vanchuyen','Hợp đồng vận chuyển', ondelete="cascade")  ,
        
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
        picking_pool = self.pool.get('icsc.phieu.vanchuyen.duongsat')     
        vals= []
        picking_obj = picking_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_pvc_duongsat, self).default_get(cr, uid, fields, context=context) 
        if picking_obj.id:
            phieu_vc=picking_obj.id
            congty_vc=picking_obj.congty_vc.id
            hopdong_vanchuyen=picking_obj.hopdong_vanchuyen.id
            query="""
           select id,name,khach_hang,sale_id,cuoc_tu_diem,cuoc_den_diem,
                sum(LanNC) as lannc, sum(LanNPK) as lannpk, sum(LanSupe) as lansupe,
                sum(Axit) as axit, sum(SPkhac) as spkhac
          from
          (
              select distinct B.*, A.khach_hang,A.sale_id,A.cuoc_tu_diem,A.cuoc_den_diem
                        from
                         (select kh.id,kh.name,kh.khach_hang,kh.sale_id,kh.cuoc_tu_diem,kh.cuoc_den_diem
                           from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                           left join icsc_hopdong_vanchuyen_chitiet ct on kh.id=ct.kehoach_id
                           where ct.kl_vc_conlai>0 and
                           kh.so_khvc= """+str(hopdong_vanchuyen)+"""                           
                           and kh.state not in ('cancel') 
                           )A
                          left join
                          (
                              select kh.id,kh.name ,sum(ct.kl_vc_conlai) as LanNC, 0 as LanNPK,0 as LanSupe, 0 as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '40' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                        
                            union all 
                            
                              select kh.id,kh.name ,0 as LanNC,sum(ct.kl_vc_conlai) as LanNPK,0 as LanSupe, 0 as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '20' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                            union all 
                              select kh.id,kh.name ,0 as LanNC, 0 as LanNPK, sum(ct.kl_vc_conlai) as LanSupe,0 as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '10' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                             union all
                              select kh.id,kh.name ,0 as LanNC, 0 as LanNPK, 0 as LanSupe,sum(ct.kl_vc_conlai) as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '30' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                              union all 
                                
                               select kh.id,kh.name ,0 as LanNC, 0 as LanNPK, 0 as LanSupe,0 as Axit,sum(ct.kl_vc_conlai) as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '80' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                          )B on A.id=B.id 
                    )C
                    group by id,name,khach_hang,sale_id,cuoc_tu_diem,cuoc_den_diem
                    
                    order by name asc"""
            if congty_vc:
                query="""  select id,name,khach_hang,sale_id,cuoc_tu_diem,cuoc_den_diem,
                sum(LanNC) as lannc, sum(LanNPK) as lannpk, sum(LanSupe) as lansupe,
                sum(Axit) as axit, sum(SPkhac) as spkhac
                  from
                  (
                     
                        select distinct B.*, A.khach_hang,A.sale_id,A.cuoc_tu_diem ,A.cuoc_den_diem
                        from
                         (select kh.id,kh.name, kh.khach_hang,kh.sale_id,kh.cuoc_tu_diem,kh.cuoc_den_diem
                           from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                           left join icsc_hopdong_vanchuyen_chitiet ct on kh.id=ct.kehoach_id
                           where ct.kl_vc_conlai>0 and
                           kh.so_khvc= """+str(hopdong_vanchuyen)+""" 
                           and kh.congty_vc= """+str(congty_vc)+""" 
                           and kh.state not in ('cancel') 
                           )A
                          left join
                          (
                              select kh.id,kh.name ,sum(ct.kl_vc_conlai) as LanNC, 0 as LanNPK,0 as LanSupe, 0 as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '40' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                        
                            union all 
                            
                              select kh.id,kh.name ,0 as LanNC,sum(ct.kl_vc_conlai) as LanNPK,0 as LanSupe, 0 as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '20' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                            union all 
                              select kh.id,kh.name ,0 as LanNC, 0 as LanNPK, sum(ct.kl_vc_conlai) as LanSupe,0 as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '10' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                             union all
                              select kh.id,kh.name ,0 as LanNC, 0 as LanNPK, 0 as LanSupe,sum(ct.kl_vc_conlai) as Axit,0 as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '30' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                              union all 
                                
                               select kh.id,kh.name ,0 as LanNC, 0 as LanNPK, 0 as LanSupe,0 as Axit,sum(ct.kl_vc_conlai) as SPkhac
                                from icsc_hopdong_vanchuyen_giacuoc_kehoach kh
                                left join icsc_hopdong_vanchuyen_chitiet ct on kh.id= ct.kehoach_id
                                join product_product p on p.id = ct.product_id
                                left join product_template pt on p.product_tmpl_id = pt.id  
                                left join product_category pc on pt.categ_id = pc.id
                                where left(pc.code, 2) = '80' and (coalesce(kh.trung_chuyen,False)=False
                                or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_1') 
                                 or (coalesce(kh.trung_chuyen,False)=True and kh.chang_khvc like 'chang_2'))
                                group by kh.id
                          )B on A.id=B.id 
                   )C
                    group by id,name,khach_hang,sale_id,cuoc_tu_diem,cuoc_den_diem
                     order by name asc"""
            cr.execute(query)    
            for item in cr.dictfetchall():
                kehoach_id=item['id']  
                if kehoach_id:               
                    vals.append({'khach_hang':item['khach_hang'] or False,
                                 'sale_id': item['sale_id'] or False, 
                                 'cuoc_tu_diem': item['cuoc_tu_diem'] or False,
                                 'cuoc_den_diem':item['cuoc_den_diem'] or False,
                                 'kehoach_id':kehoach_id,
                                 'check':False, 
                                 'kl_lan':item['lansupe'] or 0,
                                 'kl_lannc':item['lannc'] or 0,
                                 'kl_npk':item['lannpk'] or 0,
                                 'kl_axit':item['axit'] or 0,
                                 'kl_spkhac':item['spkhac'] or 0,
                                                        
                                 })
            if 'phieu_vc' in fields:
                res.update({'phieu_vc': phieu_vc}) 
            if 'congty_vc' in fields:
                res.update({'congty_vc': congty_vc}) 
            if 'hopdong_vanchuyen' in fields:
                res.update({'hopdong_vanchuyen': hopdong_vanchuyen})  
            if 'name' in fields:
                res.update({'name': 'Chọn Kế hoạch vận chuyển'})   
                     
            if 'line_ids' in fields:
                res.update({'line_ids': vals})                  
            if 'user_id' in fields:
                res.update({'user_id': uid}) 
        return res
    def action_update(self, cr, uid, ids,  context=None):
        kehoach_pool = self.pool.get('icsc.phieu.vanchuyen.duongsat') 
        #chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        cuoc_tu_diem=cuoc_den_diem=False
        for data in self.browse(cr, uid, ids, context): 
            # lay id ke hoach, xac dinh cac con cua no
            
            phieu_vc=data.phieu_vc.id
            for line in data.line_ids:
                khvc=line.kehoach_id
                if line.check:
                    kehoach_id=khvc.id  
                    if line.cuoc_tu_diem:    
                        cuoc_tu_diem=line.cuoc_tu_diem.id or False
                    if line.cuoc_den_diem:  
                        cuoc_den_diem=line.cuoc_den_diem.id or False
                    donvi_nhanhang=khvc.donvi_nhanhang.id
                    if khvc.la_khach_hang:
                        if khvc.kehoach_cha:
                            dv=khvc.kehoach_cha
                            if dv:
                                donvi_nhanhang=dv.khach_hang.id
                    if khvc.trung_chuyen==False:
                        donvi_nhanhang=khvc.order_partner_id.id 
                    phuongtien_vc=khvc.phuongthuc_vc  
                    # lxh_id=kehoach_vanchuyen_object.sale_id.id
                    kh_cha=False  
                    if  khvc.kehoach_cha:
                        khach_hang=khvc.kehoach_cha.khach_hang.id  
                        kh_cha=khvc.kehoach_cha.id
                    else:
                        khach_hang=khvc.khach_hang.id                        
            #         ngay_vc=kehoach_vanchuyen_object.ngay_tao
                    kiem_soat=khvc.kiem_soat.id
                    chiphi_denxa=0
                    tinh_denxa=khvc.tinh_denxa
                    trung_chuyen=khvc.trung_chuyen 
                    lxh_id=khvc.sale_id.id                                   
                    kehoach_pool.write(cr, uid, [phieu_vc], {'kehoach_vanchuyen':kehoach_id,
                                                            
                                                              'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem,
                                                              'donvi_nhanhang':donvi_nhanhang,
                                                              'phuongtien_vc':phuongtien_vc,'khach_hang':khach_hang,
                                    #                           'ngay_vc':ngay_vc,
                                                              'kiem_soat':kiem_soat,
                                                             # 'tinh_denxa':tinh_denxa,
                                                             # 'chiphi_denxa':chiphi_denxa,
                                                              'trung_chuyen':trung_chuyen,
                                                              'cha_id':kh_cha,
                                                              'sale_id':lxh_id}, context=context)
                    break
        return {'type': 'ir.actions.act_window_close'}
icsc_pvc_duongsat()  
class icsc_pvc_duongsat_line(osv.osv):
    _name = 'icsc.pvc.duongsat.line'
    _description = 'pvc duong sat'
    _columns = {
        'kehoach_id' : fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển', ondelete="cascade"),
        'tu_diem': fields.many2one('res.partner', 'VC từ điểm', ondelete="cascade" ),
        'den_diem': fields.many2one('res.partner', 'VC đến điểm', ondelete="cascade" ),
        'cuoc_tu_diem': fields.many2one('res.country.diadiem', 'Tính cước từ điểm', ondelete="cascade" ),
        'cuoc_den_diem': fields.many2one('res.country.diadiem', 'Tính cước đến điểm', ondelete="cascade"),
        'parent_id' : fields.many2one('icsc.pvc.duongsat', 'Cập nhật', ondelete="cascade"),       
        'check': fields.boolean('Chọn'),    
        'kl_lan': fields.float('Lân còn lại'),
         'kl_lannc': fields.float('Lân NC còn lại'),
        'kl_npk': fields.float('NPK còn lại'),
        'kl_axit': fields.float('Axit còn lại'),
        'kl_spkhac': fields.float("SP khác còn lại"),        
        'sale_id': fields.many2one('sale.order', 'LXH',domain=[('loai_lenh_vc','=','vanchuyen'),('state','in',('sent','waiting_date'))]),
       'khach_hang': fields.many2one('res.partner', 'Khách hàng',domain=[('check','=',True),('customer','=',True)] ),
        }
icsc_pvc_duongsat_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
