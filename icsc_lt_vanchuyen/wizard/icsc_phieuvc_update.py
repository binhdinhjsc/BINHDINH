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

class icsc_phieuvc_update(osv.osv):
    _name = 'icsc.phieuvc.update'
    _description = 'Sua doi KHVC'
    _columns = {
        'phuongtien_vc': fields.selection([             
            ('duongbo', 'Đường bộ'),          
            ('duongthuy', 'Đường thủy + Đường bộ'),   
            ('duongsat_chuyentuyen', 'Đường sắt + Đường bộ'),     
            ('duongsat_thongthuong', 'Đường sắt'),                    
            ], 'Phương thức vận chuyển', ),  
        'phieu_id' : fields.many2one('icsc.phieu.vanchuyen', 'Phiếu vận chuyển', ondelete="cascade"),
        'bang_kiem_soat_cu': fields.char('Bảng kiểm soát/Số toa ban đầu')  , 
        'bang_kiem_soat': fields.char('Bảng kiểm soát/Số toa mới')  , 
        'name': fields.char('Số phiếu',size=500,required=True)  , 
        'ngay_capnhat': fields.date('Ngày cập nhật'),     
         'user_id' : fields.many2one('res.users', 'Người cập nhật', ondelete="cascade"),  
        'cuoc_tu_diem': fields.many2one('res.country.diadiem', 
                                      'Tính cước từ điểm',domain="[('van_chuyen','=',True)]" , 
                                    ),
        'cuoc_den_diem': fields.many2one('res.country.diadiem', 
                                       'Tính cước đến điểm', domain="[('van_chuyen','=',True)]" ,
                                      
                                       ),    
        'congty_vc': fields.many2one('res.partner', 'Tên nhà vận chuyển',
                                    domain=[('check','=',True),('supplier','=',True)]),
        'lai_xe': fields.many2one('res.partner', 'Lái xe',domain="['|',('parent_id','=',congty_vc),('parent_uyquyen_id','=',congty_vc),('check','=',True)]"),
        'line_ids' : fields.one2many('icsc.phieuvc.update.line','parent_id','Chi tiết PVC' ),      
        'ngay_vc': fields.date('Ngày vận chuyển',required=True,)  , 
        'dai_dien': fields.many2one('res.partner', 'Người đại diện',domain="['|',('parent_id','=',congty_vc),('parent_uyquyen_id','=',congty_vc),('check','=',True)]"),   
        'kiem_soat': fields.many2one('res.country.tramkiemsoat',
                                    'Trạm kiểm soát',),
        'giam_sat_kho': fields.many2one('icsc.giamsatkho',
                                    'Giám sát kho',),
        
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
        picking_pool = self.pool.get('icsc.phieu.vanchuyen')     
        vals= []        
        picking_obj = picking_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_phieuvc_update, self).default_get(cr, uid, fields, context=context) 
        if picking_obj.id:
            phieu_id=picking_obj.id 
            
            if picking_obj.kiem_soat: 
                if 'kiem_soat' in fields:                
                    res.update({'kiem_soat':picking_obj.kiem_soat.id})
            if picking_obj.giam_sat_kho: 
                if 'giam_sat_kho' in fields:                
                    res.update({'giam_sat_kho':picking_obj.giam_sat_kho.id})
            if 'phuongtien_vc' in  fields:
                res.update({'phuongtien_vc': picking_obj.phuongtien_vc})   
            if 'name' in  fields:
                res.update({'name': picking_obj.name})          
            if 'congty_vc' in fields:
                res.update({'congty_vc': picking_obj.congty_vc.id}) 
            if 'ngay_vc' in fields:
                res.update({'ngay_vc': picking_obj.ngay_vc})  
            if 'lai_xe' in fields:
                res.update({'lai_xe': picking_obj.lai_xe.id})  
            if 'phieu_id' in fields:
                res.update({'phieu_id': phieu_id})           
            if 'bang_kiem_soat_cu' in fields:
                res.update({'bang_kiem_soat_cu': picking_obj.bang_kiem_soat})   
            if 'bang_kiem_soat' in fields:
                #pxk_id=picking_obj.phieu_xuat
                #if pxk_id:
                res.update({'bang_kiem_soat': picking_obj.bang_kiem_soat})       
            if 'ngay_capnhat' in fields:
                res.update({'ngay_capnhat': time.strftime('%Y-%m-%d')})
            if 'user_id' in fields:
                res.update({'user_id': uid}) 
            if 'cuoc_tu_diem' in fields:
                res.update({'cuoc_tu_diem': picking_obj.cuoc_tu_diem.id}) 
            if 'cuoc_den_diem' in fields:
                res.update({'cuoc_den_diem': picking_obj.cuoc_den_diem.id}) 
            if 'dai_dien' in fields:
                res.update({'dai_dien': picking_obj.dai_dien.id}) 
            phuongtien_vc=picking_obj.phuongtien_vc
            if phuongtien_vc in ('duongsat_thongthuong'):
                for line in picking_obj.chitiet_vc:
                    vals.append({'product_id':line.product_id.id,                             
                                 'name': line.name.id,
                                 'kl_vc':line.kl_vc,
                                 'diem_den':line.diem_den.id,
                                 'thanh_tien':line.thanh_tien,   
                                 'chitiet_id_ds':line.id, 
                                 'thue_id':line.thue_id.id, 
                                 'duongsat':True,                                
                                 })
            else:
                for line in picking_obj.chitiet_vc:
                    vals.append({'product_id':line.product_id.id,                             
                                 'name': line.name.id,
                                 'kl_vc':line.kl_vc,
                                 'diem_den':line.diem_den.id,
                                 'thanh_tien':line.thanh_tien,   
                                 'chitiet_id':line.id, 
                                 'thue_id':line.thue_id.id,  
                                                
                                 })
            if 'line_ids' in fields:
                res.update({'line_ids': vals}) 
        return res
    def action_correct_delivery(self, cr, uid, ids,  context=None):
        chitiet_pool = self.pool.get('icsc.phieu.vanchuyen.chitiet')   
        chitiet_pool_ds = self.pool.get('icsc.phieu.vanchuyen.chitiet.duongsat')
        kehoach_pool = self.pool.get('icsc.phieu.vanchuyen')  
        chitiet_kh=self.pool.get('icsc.hopdong.vanchuyen.chitiet')   
        for data in self.browse(cr, uid, ids, context): 
            # lay id ke hoach, xac dinh cac con cua no
            phuongtien_vc=data.phieu_id.phuongtien_vc
            bang_kiem_soat=data.bang_kiem_soat
            lai_xe=data.lai_xe.id
            giay_phep=data.lai_xe.giayphep_laixe
            ngay_vc=data.ngay_vc
            kiem_soat=False
            if data.kiem_soat:
                kiem_soat = data.kiem_soat.id
            giam_sat_kho = False
            if data.giam_sat_kho:
                giam_sat_kho = data.giam_sat_kho.id
            if phuongtien_vc not in ('duongsat_thongthuong'):
                kehoach_pool.write(cr, uid, [data.phieu_id.id], {'kiem_soat':kiem_soat,
                                                                 'giam_sat_kho':giam_sat_kho,
                                                                 'name':data.name,
                                                                 'dai_dien':data.dai_dien.id,
                                                                 'ngay_vc':ngay_vc,
                                                                 'giayphep_laixe':giay_phep,
                                                                 'bang_kiem_soat':bang_kiem_soat,
                                                                 'lai_xe':lai_xe,
                                                                 'cuoc_tu_diem':data.cuoc_tu_diem.id,
                                                                 'cuoc_den_diem':data.cuoc_den_diem.id}, context=context)
            else:
                kehoach_pool.write(cr, uid, [data.phieu_id.id], {'name':data.name ,'ngay_vc':ngay_vc,'giayphep_laixe':giay_phep,'bang_kiem_soat':bang_kiem_soat,'lai_xe':lai_xe,'cuoc_tu_diem':data.cuoc_tu_diem.id,'cuoc_den_diem':data.cuoc_den_diem.id}, context=context)
            for line in data.line_ids:
                thanh_tien=line.thanh_tien 
                chitiet_id=line.chitiet_id.id
                try:
                    gia_chua_thue=thanh_tien/(1+line.thue_id.amount)
                except:
                    gia_chua_thue=thanh_tien/(1+0.1)
                
                if phuongtien_vc in ('duongsat_thongthuong'):                    
                    # so cu
                    kv_vc_old=line.chitiet_id_ds.kl_vc
                    kl_vc_new=line.kl_vc
                    if kl_vc_new < 0:
                        raise osv.except_osv(_("Thông báo!"), _("Khối lượng vận chuyển trên phiếu phải >= 0"))
                    chenh_lech=kl_vc_new - kv_vc_old
                    #sua kl tuong ung tren KHVC
                    CT_KHVC=line.name.id
                    kl_vc_kehoach=line.name.kl_vc_kehoach
                    saukhi_sua=kl_vc_kehoach + chenh_lech
                    #chitiet_kh.write(cr, uid, [CT_KHVC],{'kl_vc_kehoach':saukhi_sua})
                    chitiet_pool_ds.write(cr, uid, [line.chitiet_id_ds.id], {'kl_vc':line.kl_vc,'thanh_tien':thanh_tien,'gia_chua_thue':gia_chua_thue}, context=context)
                    
                else:
                    chitiet_pool.write(cr, uid, [chitiet_id], {'thanh_tien':thanh_tien,'gia_chua_thue':gia_chua_thue}, context=context)
        return {'type': 'ir.actions.act_window_close'}
    
icsc_phieuvc_update()

class icsc_phieuvc_update_line(osv.osv):
    _name = 'icsc.phieuvc.update.line'
    _description = 'Sua doi PVC'
    _columns = {
        'chitiet_id_ds':fields.many2one('icsc.phieu.vanchuyen.chitiet.duongsat','Chi tiết', ondelete="cascade"),
        'chitiet_id':fields.many2one('icsc.phieu.vanchuyen.chitiet','Chi tiết', ondelete="cascade"),
        'name': fields.many2one('icsc.hopdong.vanchuyen.chitiet', 'Chi tiết KHVC', ondelete="cascade" ), 
        'product_id': fields.many2one('product.product', 'Tên vật tư', ondelete='cascade'),  
        'kl_vc': fields.float('KL vận chuyển/tấn'),    
        'diem_den': fields.many2one('res.country.diadiem', 'Chi tiết điểm đến',domain="[('van_chuyen','=',True)]" ),  
        'thanh_tien': fields.float('Thành tiền'),        
        'parent_id' : fields.many2one('icsc.phieuvc.update', 'Cập nhật'),
        'thue_id': fields.many2one('account.tax','Thuế'),
        'duongsat': fields.boolean('Đường sắt'),                    
    }
    _defaults={'duongsat':False}
icsc_phieuvc_update_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
