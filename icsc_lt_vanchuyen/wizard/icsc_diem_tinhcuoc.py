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

class icsc_diem_tinhcuoc(osv.osv):
    _name = 'icsc.diem.tinhcuoc'
    _description = 'Load diem tinh cuoc'
    _columns = {    
        'kehoach_id' : fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển', ondelete="cascade"),     
        'congty_vc': fields.many2one('res.partner', 'Tên nhà vận chuyển',domain=[('check','=',True),('supplier','=',True)]),
        'so_khvc': fields.many2one('icsc.hopdong.vanchuyen','Số HĐVC',domain="[('check','=',True),('congty_vc','=',congty_vc)]")  ,
        'line_ids' : fields.one2many('icsc.diem.tinhcuoc.line','parent_id','Chi tiết' ),
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
        picking_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')     
        vals= []
        picking_obj = picking_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_diem_tinhcuoc, self).default_get(cr, uid, fields, context=context) 
        if picking_obj.id:
            kehoach_id=picking_obj.id
            so_khvc=picking_obj.so_khvc
            a=picking_obj.so_khvc.chitiet_banggia
            if a is None:
                raise osv.except_osv(_('Lỗi!'), _('Chưa có 1 Hợp đồng vận chuyển nào được chọn trên KHVC. Vui lòng chọn 1 HĐVC trước khi sử dụng tính năng này!'))   
            for line in picking_obj.so_khvc.chitiet_banggia:
                check=False
                now=datetime.now().strftime('%Y-%m-%d')
                todays_date = datetime.strptime(str(now), '%Y-%m-%d')                         
                ngay_hieuluc=datetime.strptime(line.ngay_hieu_luc,'%Y-%m-%d')                  
                if line.ngay_hieu_luc and line.ngay_het_hieu_luc:  
                    
                    ngay_kethuc=datetime.strptime(line.ngay_het_hieu_luc,'%Y-%m-%d')
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                        check=True
                if line.ngay_hieu_luc and not line.ngay_het_hieu_luc:
                    
                    if todays_date >=ngay_hieuluc:   
                        check=True
                if check:
                    vals.append({'tu_diem':line.tu_diem.id,
                                 'den_diem': line.den_diem.id, 
                                 'banggia_id': line.banggia_id.id,
                                 'so_quyet_dinh':line.so_quyet_dinh.id,
                                 'ngay_hieu_luc':line.ngay_hieu_luc,
                                 'ngay_het_hieu_luc':line.ngay_het_hieu_luc,
                                 'gia_id':line.id,
                                 
                               
                                 })
            if 'kehoach_id' in fields:
                res.update({'kehoach_id': kehoach_id})            
            if 'line_ids' in fields:
                res.update({'line_ids': vals})             
            if 'congty_vc' in fields:
                res.update({'congty_vc': picking_obj.congty_vc.id})                
            if 'so_khvc' in fields:
                res.update({'so_khvc': picking_obj.so_khvc.id})
        return res
  
    def xac_nhan(self, cr, uid, ids,  context=None):
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach') 
        phieuvc_pool=self.pool.get('icsc.phieu.vanchuyen')
        kh_update=self.pool.get('icsc.kehoach.update')
        cuoc_tu_diem=False
        cuoc_den_diem=False
        for data in self.browse(cr, uid, ids, context): 
            # lay id ke hoach, xac dinh cac con cua no
            for line in data.line_ids:
                if line.check:
                    cuoc_tu_diem=line.tu_diem.id
                    cuoc_den_diem=line.den_diem.id
                    # xet trung chuyen                         
            
            if cuoc_tu_diem and cuoc_den_diem:
                # lay tat ca phieu van chuyen cua KHVC
                for phieu in data.kehoach_id.phieuvc_lines:
                    pvc_id=phieu.id
                    phieuvc_pool.write(cr, uid, [pvc_id], {'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem}, context=context)
                kehoach_id=data.kehoach_id.id       
                kehoach_pool.write(cr, uid, [kehoach_id], {'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem}, context=context)
                # ghi lich su sua doi KHVC
#                 if data.kehoach_id.state !='draft':
#                     # ghi lich su
#                     kh_update.create(cr, uid, {
#                                             'ngay_capnhat':time.strftime('%Y-%m-%d'),
#                                              'cuoc_den_diem':cuoc_den_diem,
#                                              'cuoc_tu_diem':cuoc_tu_diem,
#                                             
#                                              'kehoach_id' :kehoach_id,  
#                                              'user_id':uid,  
#                                              'line_ids':[]                                                                              
#                                             
#                                              }, context=context)
                    
        return {'type': 'ir.actions.act_window_close'}
    
icsc_diem_tinhcuoc()
class icsc_diem_tinhcuoc_line(osv.osv):
    _name = 'icsc.diem.tinhcuoc.line'
    _description = 'chi tiet bang gia'
    _columns = {
        'parent_id' : fields.many2one('icsc.diem.tinhcuoc', 'Cập nhật'),
        'gia_id': fields.many2one('icsc.hopdong.vanchuyen.chitietbanggia', 'Chi tiết bảng giá', ondelete="cascade"),
        'tu_diem': fields.many2one('res.country.diadiem', 'Vận chuyển từ điểm',domain="[('van_chuyen','=',True)]" , ondelete="cascade" ),
        'den_diem': fields.many2one('res.country.diadiem', 'Vận chuyển đến điểm',domain="[('van_chuyen','=',True)]" , ondelete="cascade"),
        'banggia_id': fields.many2one('icsc.hopdong.vanchuyen.giacuoc', 'Tên bảng giá', ondelete="cascade"),
        'gia_chua_thue': fields.float('Giá chưa thuế'),
        'tax_id': fields.many2one('account.tax', 'Thuế', ondelete='cascade'),
        'gia_co_thue': fields.float('Giá có thuế'),
        'ma_vung': fields.char('Mã vùng', size=500 )  ,
        'so_quyet_dinh': fields.many2one('icsc.quyetdinh.giacuoc.vanchuyen','Số quyết định', ondelete="cascade"),
        'ngay_hieu_luc': fields.date('Ngày hiệu lực'),
        'ngay_het_hieu_luc': fields.date('Ngày hết hiệu lực'),
        'check': fields.boolean('Chọn'),
        }
icsc_diem_tinhcuoc_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
