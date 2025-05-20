# -*- coding: utf-8 -*-
##############################################################################
#    
#    VNC Developments (India) Pvt. Ltd.
#    Copyright (C) 2004-TODAY VNC (<http://www.vnc.biz>).
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
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import datetime 
import time
import math
import sys
from datetime import date
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

_TASK_STATE = [('vanchuyen', 'Vận chuyển'),('khongvanchuyen', 'Không vận chuyển')]

def rounding(f, r):
    if not r:
        return f
    return round(f / r) * r
class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    _order = 'id desc'
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}   
        kh_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')     
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'ngay_giao': False,
                'loai_lenh_vc':False,
                'tong_khoiluong':0,
                'donvi_vanchuyen':False,
                'ma_vung':False,              
            } 
            loai_lenh_vc=False       
            if order.sale_id:
                loai_lenh_vc=order.sale_id.loai_lenh_vc
            val=0  
            string=matinh=''  
            if order.state=='done':
                partner_id=order.partner_id.ma_quanly
                left_code_kh=''
                if partner_id:
                    left_code_kh=partner_id+'-'
                string +=left_code_kh     
            for line in order.move_lines:
                if line.doitac_giaohang:
                    matinh=line.doitac_giaohang.state_id.code
                if line.state!='cancel':
                    val+= line.product_qty  
            if matinh:
                string +=matinh         
            nha_vc=order.partner_id.id
            if order.kehoach_vanchuyen_id:                
                if order.kehoach_vanchuyen_id.parent_id: 
                    kehoach=order.kehoach_vanchuyen_id.id            
                    kh_ids = kh_pool.search(cr, uid, [('kehoach_cha','=',kehoach)], limit=1, context=context)    
                    if kh_ids:
                        kh_obj = kh_pool.browse(cr, uid, kh_ids[0], context=context)                   
                        nha_vc=kh_obj.congty_vc and kh_obj.congty_vc.id or False
                else:
                    nha_vc=order.kehoach_vanchuyen_id.congty_vc.id                
            res[order.id]['tong_khoiluong']= val
            res[order.id]['loai_lenh_vc']= loai_lenh_vc 
            res[order.id]['ngay_giao']= order.date_done
            res[order.id]['donvi_vanchuyen']= nha_vc       
            res[order.id]['ma_vung']= string                 
        return res
    def _loai_lenh_vc(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = False
            loai_lenh_vc=task.loai_lenh_vc
            if loai_lenh_vc=='vanchuyen':
                res[task.id] ='Vận chuyển'
            if loai_lenh_vc=='khongvanchuyen':
                res[task.id] ='Không vận chuyển'
        return res
    def _kehoach_cha(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        kh_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = False
            nha_vc=False
            kh=task.kehoach_vanchuyen_id
            if kh:                
                if task.kehoach_vanchuyen_id.parent_id: 
                    kehoach=task.kehoach_vanchuyen_id.id    
                    kh_ids = kh_pool.search(cr, uid, [('kehoach_cha','=',kehoach)], limit=1, context=context)    
                    if kh_ids:
                        kh_obj = kh_pool.browse(cr, uid, kh_ids[0], context=context)                   
                        nha_vc=kh_obj.congty_vc and kh_obj.congty_vc.id or False
                else:
                    nha_vc=task.kehoach_vanchuyen_id.congty_vc.id
            else:
                nha_vc=task.partner_id.id
            res[task.id] =nha_vc           
        return res
   
    def _update_name(self, cr, uid, ids, name, args, context=None):
        res = {}        
        kq=False   
        
        table_name = 'stock_picking'     
        for stock in self.browse(cr, uid, ids, context=context): 
            type=stock.loai_xuatkho
            code =  'stock.picking.' + type
            if stock.state in ('done') and stock.type=='out':
                dem = 1
                if type=='thongthuong':                
                    query = """ select left(name,3) as name,id,ROW_NUMBER() over (order by id) as STT
                                from stock_picking where name = '"""+ str(stock.name) +"""'
                                order by id
                            """ 
                else:                                 
                    query = """ select left(name,4) as name,id,ROW_NUMBER() over (order by id) as STT
                                from stock_picking where name = '"""+ str(stock.name) +"""'
                                order by id
                            """ 
                cr.execute(query)
                for item in cr.dictfetchall():
                    name = item['name']
                    sale_id = item['id']
                    stt = item['stt']
                    if stt > 1:
                        tenmoi = self.pool.get('sequence.custormize.pickingout').get_names(cr, uid, code, table_name, type, dem)
                        check_trung = self.pool.get('stock.picking').search(cr, uid, [('name', '=', tenmoi),('id', '!=', stock.id)])
                        if check_trung:
                            return res
                        kq = self.write(cr,uid,[sale_id],{'name':tenmoi})
                        dem += 1
            res[stock.id] = kq
        return res
    
    def _get_tongkhoiluong(self, cr, uid, ids, name=None, args=None, context=None):
        res={}        
        if context is None:
            context = {}        
        for order in self.browse(cr, uid, ids, context):  
            val=0        
            for line in order.move_lines:
                if line.state!='cancel':
                    val+=line.product_qty
            res[order.id]=val            
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[line.picking_id.id] = True
        return result.keys()
    
    def _get_khvc(self, cr, uid, ids,context=None):
        result = {}
        for line in self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, ids, context=context):
            for pk in line.xuatkho_lines:
                result[pk.id] = True
        return result.keys()
    
    _columns = {   
               'tong_khoiluong_tmp': fields.function(_get_tongkhoiluong,type='float',string='Tổng KL', digits=(15,3)), 
               'tong_khoiluong': fields.function(_amount_all,type='float',string='Tổng KL',digits=(15,3),
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['name','date_done','sale_id','state','bang_kiem_soat','move_lines','origin','invoice_state','mistake_delivery'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['name','date_done','sale_id','state','bang_kiem_soat','move_lines','origin','invoice_state','mistake_delivery'], 10),
                        'stock.move': (_get_order, ['product_qty','state','product_uos_qty','picking_id'], 10),
                    }, multi="sums",help="Tổng KL"),
               'auto_update_name':  fields.function(_update_name, type='boolean', string='Tự động cập nhập tên trùng'),
               'loai_lenh_vc_ht': fields.function(_loai_lenh_vc, string='Loại đơn hàng',type="char",size=256),
               'ngay_giao': fields.function(_amount_all,type='date', string='Ngày giao',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state','move_lines'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state','move_lines'], 10),
                       
                    }, multi="all",help="KL còn lại"),
               'loai_lenh_vc': fields.function(_amount_all,type='selection', selection=_TASK_STATE,string='Loại đơn hàng',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                       
                    }, multi="all",help="Loại đơn hàng"),
                
                'donvi_vanchuyen': fields.function(_amount_all,type='many2one', relation='res.partner',string='Đơn vị vận chuyển',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines','don_vi_vc','kehoach_vanchuyen_id','partner_id'], 10),
                        #'stock.move': (_get_order, ['product_qty','state','product_uos_qty','picking_id','doitac_giaohang'], 10),
                        'icsc.hopdong.vanchuyen.giacuoc.kehoach': (_get_khvc, ['parent_id','state','kehoach_cha','xuatkho_lines','congty_vc'], 10),
                    }, multi="all"),
                
                'ma_vung': fields.function(_amount_all,type='char', string='Mã Vùng',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines','don_vi_vc','kehoach_vanchuyen_id','partner_id'], 10),
                        'stock.move': (_get_order, ['picking_id','doitac_giaohang'], 10),
                        'icsc.hopdong.vanchuyen.giacuoc.kehoach': (_get_khvc, ['parent_id','state','kehoach_cha','xuatkho_lines','congty_vc'], 10),
                    }, multi="all"),
                
                'so_theo_doi_vc': fields.char( 'Sổ theo dõi vận chuyển', size=564, states={'done': [('readonly', True)]}),
                'doitac_giaohang':fields.many2one('res.partner', 'Đối tác nhận hàng',domain=[('check','=',True),('supplier','=',True)], states={'done': [('readonly', True)]}),
                #'ma_vung': fields.char( 'Mã vùng', size=500, states={'done': [('readonly', True)]}),
                'don_vi_vc': fields.function(_kehoach_cha, string='Tên đơn vị vận chuyển',type="many2one",relation="res.partner", track_visibility='onchange', states={'done': [('readonly', True)]}),
                'kehoach_vanchuyen_id':fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển số', states={'done': [('readonly', True)]}),
                'khoxuat_id':fields.many2one('res.partner', 'Kho xuất',domain=[('kho','=',True)], states={'done': [('readonly', True)]}),
                'bang_kiem_soat': fields.char( 'Bảng kiểm soát/số toa', size=1000,states={'done': [('readonly', True)]}),
                'loai_vanchuyen': fields.selection([  
                              ('diennuoc', ''),  
                              ('oto', 'Ô tô (Đường sắt – ô tô; đường thủy – ô tô, kho – ô tô)'),             
                            ('nhan_tai_ga', 'Nhận tại ga (cảng, kho ngoài)'),
                            ], 'Hình thức vận chuyển',track_visibility='onchange',), 
                 'hoa_don_id':fields.many2one('account.invoice', 'Số hóa đơn', states={'done': [('readonly', True)]}),
                 #'donvi_vanchuyen':fields.many2one('res.partner', 'Tên đơn vị vận chuyển', states={'done': [('readonly', True)]}),
                 'daidien_muahang':fields.many2one('res.partner', 'Người đại diện mua hàng',domain="['|',('parent_id','=',partner_id),('parent_uyquyen_id','=',partner_id),('check','=',True)]", states={'done': [('readonly', True)]}),
                 'type_kho': fields.selection([('kho_congty', 'Kho công ty'), ('kho_taptrung', 'Kho tập trung'), ('kho_daily', 'Kho đại lý')], 'Loại hình kho', states={'done': [('readonly', True)]} ),
                  'dai_dien': fields.many2one('res.partner', 'Người đại diện VC',domain="['|',('parent_id','=',don_vi_vc),('parent_uyquyen_id','=',don_vi_vc),('check','=',True)]", track_visibility='onchange'
                              , states={'done': [('readonly', True)]}    ),
                 'haiduong_id': fields.related('sale_id', 'haiduong_id', type='many2one', relation='sale.shop', store=True, string='Đơn vị thực hiện'),
                 'dv_thuchien': fields.many2one('sale.shop', 'Đơn vị thực hiện', track_visibility='onchange', states={'done': [('readonly', True)]}),
                 'pvc_ids':fields.one2many('icsc.phieu.vanchuyen','phieu_xuat','PVC', readonly=True,),
                 'is_npp': fields.boolean('Chọn nhà phân phối', states={'done': [('readonly', True)]}),
 #                'dt_laixe': fields.boolean('Số điện thoại lái xe', states={'done': [('readonly', True)]}),
                 'npp_id': fields.many2one('res.partner', 'Chọn nhà phân phối', states={'done': [('readonly', True)]}),
            'npp_delivery_id': fields.many2one('res.partner', 'Địa chỉ giao hàng', states={'done': [('readonly', True)]}),
            'npp_mavung': fields.char( 'Mã vùng', states={'done': [('readonly', True)]}),
                     }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context={}   
        type=vals.get('type')        
        if type=='internal':           
            vals['name']=self.pool.get('ir.sequence').get(cr, uid, 'stock.picking')
        partner_id= super(stock_picking,self).create(cr, uid, vals, context=context)      
        return partner_id
    
    def write(self, cr, uid, ids, vals, context=None):
        # if alias_model has been changed, update alias_model_id accordingly
        if vals.get('state'):
            state=vals.get('state')
            string=matinh=''
            if state=='done':
                for task in self.browse(cr, uid, ids, context):
                    partner_id=task.partner_id.ma_quanly
                    if partner_id:
                        left_code_kh=partner_id+'-'
                    else:
                        left_code_kh=''
                    string +=left_code_kh
                    for move in task.move_lines:                
                        doitac_giaohang=move.doitac_giaohang
                        if doitac_giaohang:
                            matinh=doitac_giaohang.state_id.code
                    if matinh!=None:
                        string +=matinh
                        vals['ma_vung']=string
        vals['nguoi_lap_phieu']=uid
        return super(stock_picking, self).write(cr, uid, ids, vals, context=context)
   
stock_picking()  
class stock_picking_in(osv.osv):
    _description="Delivery Orders"
    _inherit = 'stock.picking.in'
    _order = 'id desc'
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}   
        kh_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')     
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'ngay_giao': False,
                'loai_lenh_vc':False,              
                'donvi_vanchuyen':False,
                'ma_vung':False,              
            } 
            loai_lenh_vc=False       
            if order.sale_id:
                loai_lenh_vc=order.sale_id.loai_lenh_vc
            val=0     
            string=matinh=''   
            if order.state=='done':
                partner_id=order.partner_id.ma_quanly
                left_code_kh=''
                if partner_id:
                    left_code_kh=partner_id+'-'
                string +=left_code_kh
            for line in order.move_lines:
                if line.doitac_giaohang:
                    matinh=line.doitac_giaohang.state_id.code                
                if line.state!='cancel':
                    val+= line.product_qty   
            if matinh:
                string +=matinh        
            nha_vc=order.partner_id.id
            if order.kehoach_vanchuyen_id:                
                if order.kehoach_vanchuyen_id.parent_id: 
                    kehoach=order.kehoach_vanchuyen_id.id            
                    kh_ids = kh_pool.search(cr, uid, [('kehoach_cha','=',kehoach)], limit=1, context=context)    
                    if kh_ids:
                        kh_obj = kh_pool.browse(cr, uid, kh_ids[0], context=context)                   
                        nha_vc=kh_obj.congty_vc and kh_obj.congty_vc.id or False
                else:
                    nha_vc=order.kehoach_vanchuyen_id.congty_vc.id
            res[order.id]['loai_lenh_vc']= loai_lenh_vc 
            res[order.id]['ngay_giao']= order.date_done
            res[order.id]['donvi_vanchuyen']= nha_vc       
            res[order.id]['ma_vung']= string                 
        return res
    def _kehoach_cha(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        kh_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = False
            nha_vc=False
            kh=task.kehoach_vanchuyen_id
            if kh:                
                if task.kehoach_vanchuyen_id.parent_id: 
                    kehoach=task.kehoach_vanchuyen_id.id    
                    kh_ids = kh_pool.search(cr, uid, [('kehoach_cha','=',kehoach)], limit=1, context=context)    
                    if kh_ids:
                        kh_obj = kh_pool.browse(cr, uid, kh_ids[0], context=context)                   
                        nha_vc=kh_obj.congty_vc and kh_obj.congty_vc.id or False
                else:
                    nha_vc=task.kehoach_vanchuyen_id.congty_vc.id
            else:
                nha_vc=task.partner_id.id
            res[task.id] =nha_vc           
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[line.picking_id.id] = True
        return result.keys()
    
    def _get_khvc(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, ids, context=context):
            for pk in line.xuatkho_lines:
                result[pk.id] = True
        return result.keys()
    _columns = {      
                 
                'ngay_giao': fields.function(_amount_all,type='date', string='Ngày giao',
                    store={
                        'stock.picking.in': (lambda self, cr, uid, ids, c={}: ids, ['date_done','state'], 10),
                       
                    }, multi="all",help="KL còn lại"),
                'so_theo_doi_vc': fields.char( 'Sổ theo dõi vận chuyển', size=564, states={'done': [('readonly', True)]}),
                'doitac_giaohang':fields.many2one('res.partner', 'Đối tác nhận hàng',domain=[('check','=',True),('supplier','=',True)], states={'done': [('readonly', True)]}),
                #'ma_vung': fields.char( 'Mã vùng', size=500,),
                 'don_vi_vc': fields.function(_kehoach_cha, string='Tên đơn vị vận chuyển',type="many2one",relation="res.partner", track_visibility='onchange', states={'done': [('readonly', True)]}),
                'kehoach_vanchuyen_id':fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển số', states={'done': [('readonly', True)]}),
                 'bang_kiem_soat': fields.char( 'Bảng kiểm soát/số toa', size=1000,states={'done': [('readonly', True)]}),
                'khoxuat_id':fields.many2one('res.partner', 'Kho xuất',domain=[('kho','=',True)], states={'done': [('readonly', True)]}),
                  'loai_vanchuyen': fields.selection([  
                  ('diennuoc', ''),
                  ('oto', 'Ô tô (Đường sắt – ô tô; đường thủy – ô tô, kho – ô tô)'),
                
                ('nhan_tai_ga', 'Nhận tại ga (cảng, kho ngoài)'),
                   
                
                ], 'Hình thức vận chuyển',track_visibility='onchange',), 
                 'hoa_don_id':fields.many2one('account.invoice', 'Hóa đơn thanh toán', states={'done': [('readonly', True)]}),
               # 'donvi_vanchuyen':fields.many2one('res.partner', 'Tên đơn vị vận chuyển', states={'done': [('readonly', True)]}),
                 'daidien_muahang':fields.many2one('res.partner', 'Người đại diện mua hàng',domain="['|',('parent_id','=',partner_id),('parent_uyquyen_id','=',partner_id),('check','=',True)]", states={'done': [('readonly', True)]}),
                'type_kho': fields.selection([('kho_congty', 'Kho công ty'), ('kho_taptrung', 'Kho tập trung'), ('kho_daily', 'Kho đại lý')], 'Loại hình kho', states={'done': [('readonly', True)]} ),
                'dai_dien': fields.many2one('res.partner', 'Người đại diện VC',domain="['|',('parent_id','=',don_vi_vc),('parent_uyquyen_id','=',don_vi_vc),('check','=',True)]", track_visibility='onchange'
                              , states={'done': [('readonly', True)]}    ),
                 'haiduong_id': fields.related('sale_id', 'haiduong_id', type='many2one', relation='sale.shop', store=True, string='Đơn vị thực hiện'),
                 'dv_thuchien': fields.many2one('sale.shop', 'Đơn vị thực hiện', track_visibility='onchange', states={'done': [('readonly', True)]}),
                 'loai_lenh_vc': fields.function(_amount_all,type='selection', selection=_TASK_STATE,string='Loại đơn hàng',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state','bang_kiem_soat'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state','bang_kiem_soat'], 10),
                       
                    }, multi="all",help="Loại đơn hàng"),
                 'donvi_vanchuyen': fields.function(_amount_all,type='many2one', relation='res.partner',string='Đơn vị vận chuyển',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines','don_vi_vc','kehoach_vanchuyen_id','partner_id'], 10),
                        #'stock.move': (_get_order, ['product_qty','state','product_uos_qty','picking_id','doitac_giaohang'], 10),
                        'icsc.hopdong.vanchuyen.giacuoc.kehoach': (_get_khvc, ['parent_id','state','kehoach_cha','xuatkho_lines','congty_vc'], 10),
                    }, multi="all"),
                
                 'ma_vung': fields.function(_amount_all,type='char', string='Mã Vùng',
                    store={
                        'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                        'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines','don_vi_vc','kehoach_vanchuyen_id','partner_id'], 10),
                        'stock.move': (_get_order, ['picking_id','doitac_giaohang'], 10),
                        'icsc.hopdong.vanchuyen.giacuoc.kehoach': (_get_khvc, ['parent_id','state','kehoach_cha','xuatkho_lines','congty_vc'], 10),
                    }, multi="all"),
                 'is_npp': fields.boolean('Chọn nhà phân phối', states={'done': [('readonly', True)]}),
                 'npp_id': fields.many2one('res.partner', 'Chọn nhà phân phối', states={'done': [('readonly', True)]}),
            'npp_delivery_id': fields.many2one('res.partner', 'Địa chỉ giao hàng', states={'done': [('readonly', True)]}),
            'npp_mavung': fields.char( 'Mã vùng', states={'done': [('readonly', True)]}),
                }
      
stock_picking_in()
class stock_picking_out(osv.osv):
    _description = "Delivery Orders"
    _inherit = 'stock.picking.out'
    _order = 'id desc'
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}   
        kh_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')     
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                        'ngay_giao': False,
                        'loai_lenh_vc':False,
                        'tong_khoiluong':0,
                        'donvi_vanchuyen':False,
                        'ma_vung':False,
                        } 
            loai_lenh_vc=False   
            string=matinh=''    
            if order.sale_id:
                loai_lenh_vc=order.sale_id.loai_lenh_vc            
            if order.state=='done':
                partner_id=order.partner_id.ma_quanly
                left_code_kh=''
                if partner_id:
                    left_code_kh=partner_id+'-'
                string +=left_code_kh
            val=0        
            for line in order.move_lines:
                if line.doitac_giaohang:
                    matinh=line.doitac_giaohang.state_id.code
                if line.state!='cancel':
                    val+= line.product_qty
            if matinh:
                string +=matinh
            nha_vc=order.partner_id.id
            if order.kehoach_vanchuyen_id:                
                if order.kehoach_vanchuyen_id.parent_id: 
                    kehoach=order.kehoach_vanchuyen_id.id            
                    kh_ids = kh_pool.search(cr, uid, [('kehoach_cha','=',kehoach)], limit=1, context=context)    
                    if kh_ids:
                        kh_obj = kh_pool.browse(cr, uid, kh_ids[0], context=context)                   
                        nha_vc=kh_obj.congty_vc and kh_obj.congty_vc.id or False
                else:
                    nha_vc=order.kehoach_vanchuyen_id.congty_vc.id
            res[order.id]['tong_khoiluong']= val
            res[order.id]['loai_lenh_vc']= loai_lenh_vc 
            res[order.id]['ngay_giao']= order.date_done
            res[order.id]['donvi_vanchuyen']= nha_vc       
            res[order.id]['ma_vung']= string                 
        return res
    
    def _kehoach_cha(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        kh_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = False
            nha_vc=False
            kh=task.kehoach_vanchuyen_id
            if kh:                
                if task.kehoach_vanchuyen_id.parent_id: 
                    kehoach=task.kehoach_vanchuyen_id.id    
                    kh_ids = kh_pool.search(cr, uid, [('kehoach_cha','=',kehoach)], limit=1, context=context)    
                    if kh_ids:
                        kh_obj = kh_pool.browse(cr, uid, kh_ids[0], context=context)                   
                        nha_vc=kh_obj.congty_vc and kh_obj.congty_vc.id or False
                else:
                    nha_vc=task.kehoach_vanchuyen_id.congty_vc.id
            else:
                nha_vc=task.partner_id.id
            res[task.id] =nha_vc           
        return res
    
    def _update_name(self, cr, uid, ids, name, args, context=None):
        res = {}        
        kq=False   
        table_name = 'stock_picking'     
        for stock in self.browse(cr, uid, ids, context=context): 
            type=stock.loai_xuatkho
            code =  'stock.picking.' + type
            if stock.state in ('done') and stock.type=='out':
                dem = 1
                if type=='thongthuong':                
                    query = """ select left(name,3) as name,id,ROW_NUMBER() over (order by id) as STT
                                from stock_picking where name = '"""+ str(stock.name) +"""'
                                order by id
                            """ 
                else:                                 
                    query = """ select left(name,4) as name,id,ROW_NUMBER() over (order by id) as STT
                                from stock_picking where name = '"""+ str(stock.name) +"""'
                                order by id
                            """ 
                cr.execute(query)
                for item in cr.dictfetchall():
                    name = item['name']
                    sale_id = item['id']
                    stt = item['stt']
                    if stt > 1:
                        tenmoi = self.pool.get('sequence.custormize.pickingout').get_names(cr, uid,code,table_name,type,dem)
                        check_trung = self.pool.get('stock.picking').search(cr, uid, [('name', '=', tenmoi),('id', '!=', stock.id)])
                        if check_trung:
                            return res
                        kq = self.write(cr,uid,[sale_id],{'name':tenmoi})
                        dem += 1
            res[stock.id] = kq
        return res
    def _get_tongkhoiluong(self, cr, uid, ids, name=None, args=None, context=None):
        res={}        
        if context is None:
            context = {}        
        for order in self.browse(cr, uid, ids, context):  
            val=0        
            for line in order.move_lines:
                if line.state!='cancel':
                    val+=line.product_qty
            res[order.id]=val            
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[line.picking_id.id] = True
        return result.keys()
    
    def _get_khvc(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, ids, context=context):
            for pk in line.xuatkho_lines:
                result[pk.id] = True
        return result.keys()
    
    _columns = {    
            'tong_khoiluong_tmp': fields.function(_get_tongkhoiluong,type='float',string='Tổng KL', digits=(15,3)),
            #'tong_khoiluong': fields.function(_get_tongkhoiluong,type='float',string='Tổng KL'),
            'auto_update_name':  fields.function(_update_name, type='boolean', string='Tự động cập nhập tên trùng'),
            'tong_khoiluong': fields.function(_amount_all,type='float',string='Tổng KL',digits=(15,3),
               store={
                   'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['name','date_done','sale_id','state','bang_kiem_soat','origin','invoice_state','move_lines','mistake_delivery'], 10),
                   'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['name','date_done','sale_id','state','bang_kiem_soat','origin','invoice_state','move_lines','mistake_delivery'], 10),
                   'stock.move': (_get_order, ['product_qty','state','product_uos_qty','sale_line_id'], 10),
               }, multi="sums",help="Tổng KL"),
            'loai_lenh_vc': fields.function(_amount_all,type='selection', selection=_TASK_STATE,string='Loại đơn hàng',
               store={
                   'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state','bang_kiem_soat'], 10),
                   'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state','bang_kiem_soat'], 10),
                  
               }, multi="all",help="Loại đơn hàng"),
            'ngay_giao': fields.function(_amount_all,type='date', string='Ngày giao',
               store={
                   'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state'], 10),
                   'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['date_done','sale_id','state'], 10),
                  
               }, multi="all",help="KL còn lại"),
            'so_theo_doi_vc': fields.char( 'Sổ theo dõi vận chuyển', size=564, states={'done': [('readonly', True)]}),
            'doitac_giaohang':fields.many2one('res.partner', 'Đối tác nhận hàng',domain=[('check','=',True),('supplier','=',True)], states={'done': [('readonly', True)]}),
            'don_vi_vc': fields.function(_kehoach_cha, string='Tên đơn vị vận chuyển',type="many2one",relation="res.partner", track_visibility='onchange', states={'done': [('readonly', True)]}),
            'kehoach_vanchuyen_id':fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển số', states={'done': [('readonly', True)]}),
            'bang_kiem_soat': fields.char( 'Bảng kiểm soát/số toa', size=1000, states={'done': [('readonly', True)]}),
            'khoxuat_id':fields.many2one('res.partner', 'Kho xuất',domain=[('kho','=',True)], states={'done': [('readonly', True)]}),
            'loai_vanchuyen': fields.selection([  
                        ('diennuoc', ''),
                        ('oto', 'Ô tô (Đường sắt – ô tô; đường thủy – ô tô, kho – ô tô)'),
                        ('nhan_tai_ga', 'Nhận tại ga (cảng, kho ngoài)'),
                        ], 'Hình thức vận chuyển',track_visibility='onchange',), 
            'hoa_don_id':fields.many2one('account.invoice', 'Hóa đơn thanh toán', states={'done': [('readonly', True)]}),
            #'donvi_vanchuyen':fields.many2one('res.partner', 'Tên đơn vị vận chuyển', states={'done': [('readonly', True)]}),
            'daidien_muahang':fields.many2one('res.partner', 'Người đại diện mua hàng',domain="['|',('parent_id','=',partner_id),('parent_uyquyen_id','=',partner_id),('check','=',True)]", states={'done': [('readonly', True)]}),
            'type_kho': fields.selection([('kho_congty', 'Kho công ty'), ('kho_taptrung', 'Kho tập trung'), ('kho_daily', 'Kho đại lý')], 'Loại hình kho', states={'done': [('readonly', True)]} ),
            'dai_dien': fields.many2one('res.partner', 'Người đại diện VC',domain="['|',('parent_id','=',don_vi_vc),('parent_uyquyen_id','=',don_vi_vc),('check','=',True)]", track_visibility='onchange'
                         , states={'done': [('readonly', True)]}    ),
            'haiduong_id': fields.related('sale_id', 'haiduong_id', type='many2one', relation='sale.shop', store=True, string='Đơn vị thực hiện'),
            'pvc_ids':fields.one2many('icsc.phieu.vanchuyen','phieu_xuat','PVC', readonly=True,),
            'donvi_vanchuyen': fields.function(_amount_all,type='many2one', relation='res.partner',string='Đơn vị vận chuyển',
               store={
                   'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                   'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines','don_vi_vc','kehoach_vanchuyen_id','partner_id'], 10),
                   #'stock.move': (_get_order, ['product_qty','state','product_uos_qty','picking_id','doitac_giaohang'], 10),
                   'icsc.hopdong.vanchuyen.giacuoc.kehoach': (_get_khvc, ['parent_id','state','kehoach_cha','xuatkho_lines','congty_vc'], 10),
               }, multi="all"),
            
            'ma_vung': fields.function(_amount_all,type='char', string='Mã Vùng',
               store={
                   'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines'], 10),
                   'stock.picking.out': (lambda self, cr, uid, ids, c={}: ids, ['sale_id','date_done','state','bang_kiem_soat','move_lines','don_vi_vc','kehoach_vanchuyen_id','partner_id'], 10),
                   'stock.move': (_get_order, ['picking_id','doitac_giaohang'], 10),
                   'icsc.hopdong.vanchuyen.giacuoc.kehoach': (_get_khvc, ['parent_id','state','kehoach_cha','xuatkho_lines','congty_vc'], 10),
               }, multi="all"),
            'is_npp': fields.boolean('Chọn nhà phân phối', states={'done': [('readonly', True)]}),
            'npp_id': fields.many2one('res.partner', 'Nhà phân phối', states={'done': [('readonly', True)]}),
            'npp_delivery_id': fields.many2one('res.partner', 'Địa chỉ giao hàng', states={'done': [('readonly', True)]}),
            'npp_mavung': fields.char( 'Mã vùng', states={'done': [('readonly', True)]}),
    }
    _defaults = {
             'loai_vanchuyen': 'oto',
             'is_npp': False,
           
         }
    
    def onchange_npp_id(self, cr, uid, ids, npp_id, npp_delivery_id, context=None):
        if not npp_delivery_id or not npp_id:
            return {}
        partner = self.pool.get('res.partner').browse(cr, uid, npp_delivery_id, context=context)
        npp = self.pool.get('res.partner').browse(cr, uid, npp_id, context=context)
        return {'value': {'npp_mavung': npp.ma_quanly + '-' + partner.ma_vung}}

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context={}   
        sale_id=vals.get('sale_id')
        
        if sale_id==False or sale_id is None:
            raise osv.except_osv(_("Thông báo!"), _("Phải chọn ít nhất một Lệnh xuất hàng") )
        vals['loai_lenh_vc']=self.pool.get('sale.order').browse(cr, uid, sale_id, context=context).loai_lenh_vc   
        partner_id= super(stock_picking_out,self).create(cr, uid, vals, context=context)
      
        return partner_id
    
    def write(self, cr, uid, ids, vals, context=None):        
        # cap nhat nguoi lap phieu
        vals['nguoi_lap_phieu']=uid
        return super(stock_picking_out, self).write(cr, uid, ids, vals, context=context)
    
    def load_ma_vung(self, cr, uid, ids, partner_id,doitac_giaohang, context=None):
        if not doitac_giaohang:
            return {}
        string=''
        district_object=self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        khachhang_code=district_object.ma_quanly
        if khachhang_code:
            left_code_kh=khachhang_code+'-'
        else:
            left_code_kh=''
            
        string +=left_code_kh
        diachinhan_object=self.pool.get('res.partner').browse(cr, uid, doitac_giaohang, context=context)
        tinh_id=diachinhan_object.state_id.id
        if tinh_id:
            tinh_code=diachinhan_object.state_id.code
            string+=tinh_code
        return {'value': {'ma_vung':string}}
    
stock_picking_out()  
class stock_move(osv.osv):
    _description= "Stock Move"
    _inherit = 'stock.move'
    _order = 'id'
    def get_count_id(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=1
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):           
            #count+=1  
            if data.picking_id:
                query="""select count(*) as count from stock_move where picking_id= """+str(data.picking_id.id)+""" and id <= """+str(data.id)    
                cr.execute(query)
                for item in cr.dictfetchall():
                    count =item['count']
            res[data.id]=count
           
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context):                      
            kh=data.picking_id.id               
            result[kh] = True           
        return result.keys()
    _columns = {     
               'doitac_giaohang':fields.many2one('res.partner', 'Địa chỉ nhận hàng',domain=[('check','=',True),('customer','=',True)]),             
               'chitiet_kh': fields.many2one('icsc.hopdong.vanchuyen.chitiet', 'Chi tiết vận chuyển', ),
               'kho_xuat_id':fields.many2one('res.partner', 'Kho xuất',domain=[('kho','=',True)]),
               'no': fields.function(get_count_id, type='integer', string='STT'),
               'check':fields.boolean('Chọn'),
                }
    _defaults={'check':False,}
stock_move()  
class account_invoice(osv.osv):
    _inherit = "account.invoice"   
    _description = 'Invoice'
    _order = 'id desc'
    
    def _get_soluong(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        if context is None:
            context = {}        
        for order in self.browse(cr, uid, ids, context):  
            val=0 
            if order.loai_hoadon!='thongthuong':       
                for line in order.invoice_line:
                    val+=line.quantity
            else:
                for line in order.invoice_line:
                    if line.uos_id.id!=18:
                        val+=line.quantity
            res[order.id]=val
            
        return res
    _columns = {      
                'tong_khoiluong': fields.function(_get_soluong,type='float',string='Tổng khối lượng'),
                'lenh_xuat_hang_id':fields.many2one('sale.order', 'Lệnh xuất hàng',readonly=True),             
                'hinh_thuc_khuyenmai':fields.char( 'Hình thức khuyến mãi',size=256,readonly=True),
                'co_phi_baove':fields.boolean( 'Phí bảo vệ môi trường',readonly=True, states={'draft':[('readonly',False)]}), 
                'lenh_xuat_kho_id':fields.many2one('stock.picking.out', 'Phiếu xuất kho',readonly=True),
                'so_quyen':fields.char( 'Số quyển',size=500, readonly=True,states={'draft':[('readonly',False)]}),
                'daidien_muahang':fields.many2one('res.partner', 'Người đại diện mua hàng',domain="[('check','=',True),('parent_id','=',partner_id)]", readonly=True, states={'draft':[('readonly',False)]}),
                'daidien_muahangs':fields.related('lenh_xuat_kho_id','daidien_muahang',type='many2one', relation='res.partner',string='Người đại diện mua hàng',store=True,states={'draft':[('readonly',False)]}),
                'haiduong_id': fields.related('lenh_xuat_hang_id', 'haiduong_id', type='many2one', relation='sale.shop', store=True, string='Đơn vị thực hiện'), 
                'loai_lenh_xuat': fields.related('lenh_xuat_hang_id', 'lenh_xuat', type='many2one', relation='icsc.lt.loai.xuat.hang', store=True, string='Loại lệnh xuất hàng'), 
                }
    def onchange_partner_in(self,cr, uid, ids,partner_id):
        return {}  
    def load_hinh_thuc_khuyenmai(self, cr, uid, ids, hinh_thuc_khuyenmai, context=None):
        if not hinh_thuc_khuyenmai:
            return {}  
        hinhthuc_khuyenmai=loai_hoadon=False
        phieuxuat= self.pool.get('sale.order').browse(cr, uid, hinh_thuc_khuyenmai)
        hinhthuc_khuyenmai=phieuxuat.hinhthuc_khuyenmai
        loai_lenh_xuat=phieuxuat.loai_lenh_xuat
        if loai_lenh_xuat=='vat':
            loai_hoadon='thongthuong'
        else:
            loai_hoadon='noibo'
            
        return {'value': {'hinh_thuc_khuyenmai':hinhthuc_khuyenmai,'loai_hoadon':loai_hoadon,}} 

account_invoice()
class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line"   
    def onchange_tax(self, cr, uid, ids,tax_id,product_id,vat=False, context=None):
        fpos =False
        if not product_id:
            # lay thue san pham ton tai tren form
            if ids:
                product=self.browse(cr, uid, ids, context).product_id
                if product:
                    return {'value': {'invoice_line_tax_id':self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product.taxes_id)  }}
        if product_id:
            product_object=self.pool.get('product.product').browse(cr, uid, product_id)
            return {'value': {'invoice_line_tax_id':self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_object.taxes_id)  }}
        return  {}
account_invoice_line()