#-*- coding: utf-8 -*-
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
from datetime import datetime 
import openerp.addons.decimal_precision as dp
from lxml import etree
from openerp import SUPERUSER_ID
from openerp.addons.mail.mail_message import decode

class sequence_custormize_hopdong(osv.osv):
    _name = "sequence.custormize.hopdong"
    def get_name(self, cr, uid, code, table_name,type):
        import datetime
        today =datetime.datetime.now()
        year =today.year
        cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='" + code + "' and active=True")
        res = cr.dictfetchone()
        if res:
            prefix = 1
            name_type = type.upper()   
            cr.execute("select max(substr(name,1,2)) as max  from " + table_name +" where EXTRACT(year FROM create_date)= "+str(year))          
        #              cr.execute("select max(substr(name, "+str(prefix)+", "+str(res['padding'])+")) as max  from " + table_name )
            p_order_number = cr.dictfetchone()
            if p_order_number:#                 
                if p_order_number['max']:
                    purchace_order_name_replace = p_order_number['max']
                    i=1
                    while (i <= len(purchace_order_name_replace)):
                        number = int(purchace_order_name_replace[:i])
                        if number > 0:
                            p_oder_number = int(purchace_order_name_replace[i-1:])
                            p_order_number = p_oder_number + 1
                            return  '%%0%sd'  % res['padding'] % p_order_number + '/'  + str(year) + '/' + 'HĐVC'
                        #                             return '%%0%sd'  % res['padding'] % p_order_number
                            break
                        i+=1
            return   '%%0%sd'  % res['padding'] % 1 + '/' + str(year) + '/' + 'HĐVC'
        else:
            return  '%%0%sd'  % res['padding'] % 1 + '/' + str(year) + '/' + 'HĐVC'
sequence_custormize_hopdong()
class sequence_custormize_hopdong_vipham(osv.osv):
    _name = "sequence.custormize.hopdong.vipham"
    def get_name(self, cr, uid, code, table_name,type):
         #pool_seq=self.pool.get('ir.sequence')
         import datetime
         today =datetime.datetime.now()
         year =today.year

#          cr.execute("select max(left(name,4)) as max  from " + table_name +" where EXTRACT(year FROM create_date)= "+str(year))
         cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='" + code + "' and active=True")
         res = cr.dictfetchone()
         if res:
             prefix = 1
             name_type = type.upper()   
             cr.execute("select max(name::int)::text as max  from " + table_name )          
#              cr.execute("select max(substr(name, "+str(prefix)+", "+str(res['padding'])+")) as max  from " + table_name )
             p_order_number = cr.dictfetchone()
             if p_order_number:#                 
                 if p_order_number['max']:
                     purchace_order_name_replace = p_order_number['max']
                     i=1
                     while (i <= len(purchace_order_name_replace)):
                        number = int(purchace_order_name_replace[:i])
                        if number > 0:
                            p_oder_number = int(purchace_order_name_replace[i-1:])
                            p_order_number = p_oder_number + 1
                            return  '%%0%sd'  % res['padding'] % p_order_number  
#                             return '%%0%sd'  % res['padding'] % p_order_number
                            break
                        i+=1
             return '%%0%sd'  % res['padding'] % 1
         else:
             return  '%%0%sd'  % res['padding'] % 1
sequence_custormize_hopdong_vipham()

class sequence_custormize_vanchuyen(osv.osv):
    _name = "sequence.custormize.vanchuyen"
    def get_name(self, cr, uid, code, table_name,type):
         #pool_seq=self.pool.get('ir.sequence')
         import datetime
         today =datetime.datetime.now()
         year =today.year
         
#          cr.execute("select max(left(name,4)) as max  from " + table_name +" where EXTRACT(year FROM create_date)= "+str(year))
         cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='" + code + "' and active=True")
         res = cr.dictfetchone()
         if res:
             prefix = 1
             name_type = type.upper()   
             cr.execute("select max(substr(name,6,6)) as max  from " + table_name +" where phuongtien_vc in ('duongbo','duongthuy','duongsat_chuyentuyen') and EXTRACT(year FROM create_date)= "+str(year))          
#              cr.execute("select max(substr(name, "+str(prefix)+", "+str(res['padding'])+")) as max  from " + table_name )
             p_order_number = cr.dictfetchone()
             if p_order_number:#                 
                 if p_order_number['max']:
                     purchace_order_name_replace = p_order_number['max']
                     i=1
                     while (i <= len(purchace_order_name_replace)):
                        number = int(purchace_order_name_replace[:i])
                        if number > 0:
                            p_oder_number = int(purchace_order_name_replace[i-1:])
                            p_order_number = p_oder_number + 1
                            return str(year) + '-' + '%%0%sd'  % res['padding'] % p_order_number
#                             return '%%0%sd'  % res['padding'] % p_order_number
                            break
                        i+=1
             return str(year) + '-' +'%%0%sd'  % res['padding'] % 1
         else:
             return  str(year) + '-' +'%%0%sd'  % res['padding'] % 1
sequence_custormize_vanchuyen()
class sequence_custormize_vanchuyen_kehoach(osv.osv):
    _name = "sequence.custormize.vanchuyen.kehoach"
    def get_name(self, cr, uid, code, table_name,type):
         #pool_seq=self.pool.get('ir.sequence')
         import datetime
         today =datetime.datetime.now()
         year =today.year
         month =today.month
         
         thang=str(month)
         if month<10:
             thang='0'+str(month)        
         day =today.day
         ngay=str(day)
         if day<10:
             ngay='0'+str(day)
        
         string_year=str(year)+thang+ngay
#          cr.execute("select max(left(name,4)) as max  from " + table_name +" where EXTRACT(year FROM create_date)= "+str(year))
         cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='" + code + "' and active=True")
         res = cr.dictfetchone()
         if res:
             res['padding']=2
             prefix = 1
             name_type = type.upper()   
             cr.execute("select max(substr(name,10,2)) as max  from " + table_name +" where  coalesce(kehoach_cha,0) = 0 and EXTRACT(year FROM create_date)= "+str(year)+" and EXTRACT(month FROM create_date)= "+str(month)+" and EXTRACT(day FROM create_date)= "+str(day))          
#              cr.execute("select max(substr(name, "+str(prefix)+", "+str(res['padding'])+")) as max  from " + table_name )
             p_order_number = cr.dictfetchone()
             if p_order_number:#                 
                 if p_order_number['max']:
                     purchace_order_name_replace = p_order_number['max']
                     i=1
                     while (i <= len(purchace_order_name_replace)):
                        number = int(purchace_order_name_replace[:i])
                        if number > 0:
                            p_oder_number = int(purchace_order_name_replace[i-1:])
                            p_order_number = p_oder_number + 1
                            return string_year + '-' + '%%0%sd'  % res['padding'] % p_order_number
#                             return '%%0%sd'  % res['padding'] % p_order_number
                            break
                        i+=1
             return string_year + '-' + '%%0%sd'  % res['padding'] % 1
         else:
             return  string_year + '-' + '%%0%sd'  % res['padding'] % 1
sequence_custormize_vanchuyen_kehoach()

def rounding(f, r):
    if not r:
        return f
    return round(f / r) * r

class icsc_hopdong_vanchuyen_dieukien(osv.osv):
    _description="icsc_hopdong_vanchuyen_dieukien"
    _name = 'icsc.hopdong.vanchuyen.dieukien'
    _inherit = ['mail.thread']
    _order= 'id desc'
    _columns = {
      
        'name': fields.char('Điều kiện', size=500,
            required=True)  ,
        'description': fields.char( 'Mô tả' ,size=500,),
      
        
    }
icsc_hopdong_vanchuyen_dieukien()  
class icsc_hopdong_vanchuyen(osv.osv):
    _description="Hop dong van chuyen"
    _name = 'icsc.hopdong.vanchuyen'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order= 'id desc'
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}        
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] =0
        return res   
     
    def _check(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        check=False
        if context is None:
            context = {}
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for line in self.browse(cr, uid, ids, context):          
            ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
            if line.ngay_hieuluc and line.ngay_kethuc:                    
                ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                    check=True
            if line.ngay_hieuluc and not line.ngay_kethuc:
                if todays_date >=ngay_hieuluc:   
                    check=True    
            res[line.id]=check
            #bg_pool=self.pool.get('icsc.hopdong.vanchuyen.chitietbanggia')
            #now=datetime.now().strftime('%Y-%m-%d')  
            # xet hieu luc bang gia
            for con in line.chitiet_banggia:  
                hieu_luc=con.hieu_luc                              
                ngay_hieu_luc=datetime.strptime(con.ngay_hieu_luc,'%Y-%m-%d')
                todays_date = datetime.strptime(str(now), '%Y-%m-%d')           
                if con.ngay_het_hieu_luc:                                                           
                    ngay_kethuc=datetime.strptime(con.ngay_het_hieu_luc,'%Y-%m-%d')                
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieu_luc:   
                        hieu_luc=True 
                    else:
                        hieu_luc=False                
                else:
                    if todays_date >=ngay_hieu_luc:   
                        hieu_luc=True 
                    else:
                        hieu_luc=False 
                try:               
                    pass
                    #cr.execute("""update icsc_hopdong_vanchuyen_chitietbanggia set hieu_luc= %s where id = %s"""%(hieu_luc,con.id))
                except:
                    return res
            for het in line.chitiet_banggia_hethan:
                hieu_luc1=het.hieu_luc    
                ngay_hieu_luc=datetime.strptime(het.ngay_hieu_luc,'%Y-%m-%d')
                #todays_date = datetime.strptime(str(now), '%Y-%m-%d')           
                if het.ngay_het_hieu_luc:                                                           
                    ngay_kethuc=datetime.strptime(het.ngay_het_hieu_luc,'%Y-%m-%d')                
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieu_luc:   
                        hieu_luc1=True 
                    else:
                        hieu_luc1=False                
                else:
                    if todays_date >=ngay_hieu_luc:   
                        hieu_luc1=True 
                    else:
                        hieu_luc1=False              
                try:
                    pass
                    #cr.execute("""update icsc_hopdong_vanchuyen_chitietbanggia set hieu_luc=%s  where id = %s"""%(hieu_luc1,het.id))
                except:
                    return res
        return res
    
    def _check_detail(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        if context is None:
            context = {}
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for line in self.browse(cr, uid, ids, context):    
            res[line.id]=True    
            # xet hieu luc bang gia
            for con in line.chitiet_banggia:  
                hieu_luc=con.hieu_luc                              
                ngay_hieu_luc=datetime.strptime(con.ngay_hieu_luc,'%Y-%m-%d')
                todays_date = datetime.strptime(str(now), '%Y-%m-%d')           
                if con.ngay_het_hieu_luc:                                                           
                    ngay_kethuc=datetime.strptime(con.ngay_het_hieu_luc,'%Y-%m-%d')                
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieu_luc:   
                        hieu_luc=True 
                    else:
                        hieu_luc=False                
                else:
                    if todays_date >=ngay_hieu_luc:   
                        hieu_luc=True 
                    else:
                        hieu_luc=False 
                try:
                    pass     
                    #cr.execute("""update icsc_hopdong_vanchuyen_chitietbanggia set hieu_luc= %s where id = %s"""%(hieu_luc, con.id))
                except:
                    return res
            for het in line.chitiet_banggia_hethan:
                hieu_luc1=het.hieu_luc    
                ngay_hieu_luc=datetime.strptime(het.ngay_hieu_luc,'%Y-%m-%d')
                #todays_date = datetime.strptime(str(now), '%Y-%m-%d')           
                if het.ngay_het_hieu_luc:                                                           
                    ngay_kethuc=datetime.strptime(het.ngay_het_hieu_luc,'%Y-%m-%d')                
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieu_luc:   
                        hieu_luc1=True 
                    else:
                        hieu_luc1=False                
                else:
                    if todays_date >=ngay_hieu_luc:   
                        hieu_luc1=True 
                    else:
                        hieu_luc1=False              
                try:
                    pass
                    #cr.execute("""update icsc_hopdong_vanchuyen_chitietbanggia set hieu_luc=%s where id = %s """(hieu_luc1,het.id))
                except:
                    return res
        return res
    _columns = {
        'tu_dong':fields.function(_check, type='boolean', string='Đang hoạt động'),
        'name': fields.char('Số hợp đồng vận chuyển', size=500, required=True, track_visibility='onchange')  ,
        'congty_vc': fields.many2one('res.partner', 'Tên công ty vận chuyển',domain=[('check','=',True),('supplier','=',True)], required=True, track_visibility='onchange',select=True),
        'ngay_ki': fields.date('Ngày kí hợp đồng', required=True , track_visibility='onchange')  ,
        'ngay_hieuluc': fields.date('Ngày có hiệu lực',
                            help='Ngày mà hợp đồng có hiệu lực', required=True , track_visibility='onchange')  ,
        'ngay_kethuc': fields.date('Ngày hết hiệu lực',
                            help='Ngày mà hợp đồng hết hiệu lực', required=True , track_visibility='onchange')  ,
        'state': fields.selection([
            ('draft', 'Bản dự thảo'),
            ('confirm', 'Xác nhận'),
            ('done', 'Hoàn tất'),
            ('cancel', 'Đã hủy'),
            
            
            ], 'Trạng thái hợp đồng', readonly=True, track_visibility='onchange'), 
        'kvvc_toithieu_ngay': fields.float('KL vận chuyển tối thiểu/Ngày' , track_visibility='onchange')  ,  
        'kvvc_toithieu_chuyen': fields.float('KL vận chuyển tối thiểu/Chuyến' , track_visibility='onchange')  ,  
        'kvvc_toida_ngay': fields.float('KL vận chuyển tối đa/Ngày' , track_visibility='onchange')  ,  
        'kvvc_toida_chuyen': fields.float('KL vận chuyển tối đa/Chuyến' , track_visibility='onchange')  ,  
        'so_thanhly': fields.char('Số thanh lý HĐ', size=500, track_visibility='onchange')  ,
        'ngay_thanhly': fields.date('Ngày thanh lý HĐ',
                            help='Ngày mà hợp đồng được thanh ly', track_visibility='onchange')  ,
        'lydo_thanhly': fields.char('Lý do thanh lý', size=500, track_visibility='onchange')  ,
        'dien_giai': fields.char('Diễn giải', size=500, track_visibility='onchange')  ,
        'tong_khoiluong': fields.float('Tổng khối lượng', track_visibility='onchange'),
        'dieukien_dambao': fields.many2one('icsc.hopdong.vanchuyen.dieukien', 'Điều kiện đảm bảo hợp đồng', track_visibility='onchange'),
        'chitiet_banggia': fields.one2many('icsc.hopdong.vanchuyen.chitietbanggia', 'hopdong_id','Chi tiết bảng giá',domain=[('hieu_luc','=',True)]),
        'chitiet_banggia_hethan': fields.one2many('icsc.hopdong.vanchuyen.chitietbanggia', 'hopdong_id','Chi tiết bảng giá hết hạn',domain=[('hieu_luc','!=',True)]),
        'chitiet_vattu': fields.one2many('icsc.hopdong.vanchuyen.chitietvattu', 'hopdong_id','Chi tiết vật tư'),
        'ds_kehoach_vc' : fields.one2many('icsc.hopdong.vanchuyen.giacuoc.kehoach','so_khvc','Danh sách kế hoạch vận chuyển',readonly=True),
        'chitiet_uyquyen': fields.one2many('icsc.hopdong.vanchuyen.uyquyen', 'hopdong_id','Thông tin ủy quyền' ),
        'ghi_chu': fields.text('Điều kiện đảm bảo hợp đồng', track_visibility='onchange' )  ,
        'check': fields.function(_check, type='boolean', string='Đang hoạt động',
           store={
               'icsc.hopdong.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['ngay_hieuluc','ngay_kethuc','tu_dong','chitiet_banggia','chitiet_banggia_hethan'], 10),
             
           },),
        'check_detail': fields.function(_check_detail, type='boolean', string='check chi tiet',
         ),
    }
    _defaults= {'state':'draft',
                'check':False,
                'name': lambda self, cr, uid, c: self.pool.get('sequence.custormize.hopdong').get_name(cr, uid, 'icsc.hopdong.vanchuyen'  , 'icsc_hopdong_vanchuyen','')}
    
    def _icsc_hopdong_vanchuyen(self, cr, uid, callback, context=None):
        if context is None:
            context = {}
        proxy = self.pool.get('icsc.hopdong.vanchuyen')
        domain = [ ('state', '!=', False) ]
        ids = proxy.search(cr, uid, domain, context=context)
        if ids:
            callback(cr, uid, ids, context=context)
        return True
    
    def run_set_check_scheduler(self, cr, uid, context=None):
        self._icsc_hopdong_vanchuyen(cr, uid, self.set_hoatdong, context=context)        
    def set_hoatdong(self, cr, uid, ids,  context=None):
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for line in self.browse(cr, uid, ids, context=context):
            check = False
            ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
            if line.ngay_hieuluc and line.ngay_kethuc:                    
                ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                    check=True
            if line.ngay_hieuluc and not line.ngay_kethuc:
                if todays_date >=ngay_hieuluc:   
                    check=True   
            query_update =""" UPDATE icsc_hopdong_vanchuyen
                               SET 
                                   "check"=%s
                             WHERE id=%s"""%(check,line.id)
            cr.execute(query_update)
        return True 
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context={}   
        type=''        
        seq_obj_name =  'icsc.hopdong.vanchuyen'               
        vals['client_code'] =  self.pool.get('sequence.custormize.hopdong').get_name(cr, uid, seq_obj_name, 'icsc_hopdong_vanchuyen',type)
        partner_id= super(icsc_hopdong_vanchuyen,self).create(cr, uid, vals, context=context)
      
        return partner_id
    
    def action_confirm(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'confirm',}, context)
        return True
    
    def action_done(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'done',}, context)
        return True
    
    def action_cancel(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'cancel',}, context)
        return True
    
    def action_return(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'draft',}, context)
        return True
    
icsc_hopdong_vanchuyen()

class icsc_hopdong_vanchuyen_uyquyen(osv.osv):
    _description="icsc_hopdong_vanchuyen_uyquyen"
    _name = 'icsc.hopdong.vanchuyen.uyquyen'
    _inherit = ['mail.thread']
    _order= 'id desc'
    _columns = {      
        'hopdong_id': fields.many2one('icsc.hopdong.vanchuyen', 'Hợp đồng')  ,
        'nguoi_duoc_uyquyen': fields.many2one('res.partner',
                                                domain="[('parent_id','=', parent.congty_vc)]",
                                               string= 'Người được ủy quyền/giới thiệu'),
        'loai_uyquyen': fields.selection([
            ('gioi_thieu', 'Giấy giới thiệu'),
            ('uy_quyen', 'Giấy uỷ quyền'),
          ], 'Loại'), 
        'chucvu': fields.char('Chức vụ'),
         'ngay': fields.date('Ngày'),   
            
       
    }
    _defaults= {'loai_uyquyen':'gioi_thieu',}
    
    def onchange_nguoi_duoc_uyquyen(self, cr, uid, ids, product_id, context=None):
        if not product_id:
            return {}
        district_object=self.pool.get('res.partner').browse(cr, uid, product_id, context=context)
        chucvu=district_object.function
        return {'value': {'chucvu':chucvu }}
icsc_hopdong_vanchuyen_uyquyen()

class icsc_hopdong_vanchuyen_chitietbanggia(osv.osv):
    _description="icsc_hopdong_vanchuyen_chitietbanggia"
    _name = 'icsc.hopdong.vanchuyen.chitietbanggia'
    _inherit = ['mail.thread']
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'gia_chua_thue': 0.0,
                'gia_co_thue': 0.0,
                'hieu_luc':True,
                
            }
            check=True
            val = val1 = 0.0
            quyetdinh=order.so_quyet_dinh
            if quyetdinh:
                bang_gia=order.banggia_id
                if bang_gia:
                    # tim so quyet dinh
                    for line in bang_gia.chitiet_banggia:
                        name=line.name.id
                        if quyetdinh.id==name:
                            val=line.gia_chua_thue
                            val1=line.gia_co_thue
            else:        
                val=order.banggia_id.gia_chua_thue
                val1=order.banggia_id.gia_co_thue
            now=datetime.now().strftime('%Y-%m-%d')   
            ngay_hieu_luc=datetime.strptime(order.ngay_hieu_luc,'%Y-%m-%d')
            todays_date = datetime.strptime(str(now), '%Y-%m-%d') 
            query="""select now()::date as todays_date"""
            cr.execute(query)
            for item in cr.dictfetchall():
                todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')          
            if order.ngay_het_hieu_luc:                                                           
                ngay_kethuc=datetime.strptime(order.ngay_het_hieu_luc,'%Y-%m-%d')       
                if todays_date <=ngay_kethuc and todays_date >=ngay_hieu_luc:   
                    check=True
                else:
                    check=False
            else:                
                if todays_date >=ngay_hieu_luc:   
                    check=True                        
                else:
                    check=False                
                         
            res[order.id]['gia_chua_thue'] = val
            res[order.id]['gia_co_thue'] = val1
            res[order.id]['hieu_luc'] = check           
        return res
    def _gia_chua_thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}       
        if context is None:
            context = {}        
        for line in self.browse(cr, uid, ids, context):          
            gia_chua_thue=line.banggia_id.gia_chua_thue
            name=line.banggia_id.name
            res[line.id]=gia_chua_thue
            self.write(cr, uid, [line.id], {'gia_chua_thue':gia_chua_thue}, context)
        return res
    def _gia_co_thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
       
        if context is None:
            context = {}        
        for line in self.browse(cr, uid, ids, context):          
            gia_co_thue=line.banggia_id.gia_co_thue
            res[line.id]=gia_co_thue
            self.write(cr, uid, [line.id], {'gia_co_thue':gia_co_thue}, context)
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.hopdong.vanchuyen.giacuoc').browse(cr, uid, ids, context=context):
            query="""select id from icsc_hopdong_vanchuyen_chitietbanggia
                    where banggia_id= """+str(line.id)
            cr.execute(query)
            for item in cr.dictfetchall():                
                result[item['id']] = True
        return result.keys()
    def _get_orders(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.hopdong.vanchuyen.giacuoc.chitiet').browse(cr, uid, ids, context=context):
            query="""select id from icsc_hopdong_vanchuyen_chitietbanggia
                    where banggia_id= """+str(line.giacuoc_id.id)
            cr.execute(query)
            for item in cr.dictfetchall():                
                result[item['id']] = True
        return result.keys()
    _columns = {      
        'hopdong_id': fields.many2one('icsc.hopdong.vanchuyen', 'Hợp đồng',track_visibility='onchange', ondelete="cascade"),
        'tu_diem': fields.many2one('res.country.diadiem', 'Vận chuyển từ điểm',domain="[('van_chuyen','=',True)]" ,track_visibility='onchange' ),
        'den_diem': fields.many2one('res.country.diadiem', 'Vận chuyển đến điểm',domain="[('van_chuyen','=',True)]" ,track_visibility='onchange'),
        'banggia_id': fields.many2one('icsc.hopdong.vanchuyen.giacuoc', 'Tên bảng giá',track_visibility='onchange', ondelete="cascade"),
        'gia_chua_thue': fields.function(_amount_all,    digits=(16,0), string='Giá chưa thuế',
            store={
                'icsc.hopdong.vanchuyen.chitietbanggia': (lambda self, cr, uid, ids, c={}: ids, ['banggia_id','tax_id','ngay_hieu_luc','ngay_het_hieu_luc'], 10),
                'icsc.hopdong.vanchuyen.giacuoc': (_get_order, ['gia_chua_thue', 'gia_co_thue','tax_id','tu_diem','den_diem','check','quyet_dinh'], 10),
                 'icsc.hopdong.vanchuyen.giacuoc.chitiet': (_get_orders, ['tax_id','ngay_hieu_luc','ngay_het_hieu_luc','gia_co_thue','check','name','ngay_banhanh'], 10),
            },
            multi='sums', track_visibility='always'),
        'tax_id': fields.many2one('account.tax', 'Thuế', ondelete='cascade',track_visibility='onchange'),
        'gia_co_thue':fields.function(_amount_all,   digits=(16,0), string='Giá có thuế',
            store={
                'icsc.hopdong.vanchuyen.chitietbanggia': (lambda self, cr, uid, ids, c={}: ids, ['banggia_id','tax_id','ngay_hieu_luc','ngay_het_hieu_luc','gia_co_thue','tax_id','check','name','ngay_banhanh'], 10),
                'icsc.hopdong.vanchuyen.giacuoc': (_get_order, ['gia_chua_thue', 'gia_co_thue','tax_id','tu_diem','den_diem','check','quyet_dinh'], 10),
                 'icsc.hopdong.vanchuyen.giacuoc.chitiet': (_get_orders, ['tax_id','ngay_hieu_luc','ngay_het_hieu_luc','gia_co_thue','check','name','ngay_banhanh'], 10),
            },
            multi='sums', track_visibility='always'),
        'hieu_luc':fields.function(_amount_all,   string='Hiệu lực', type='boolean',
            store={
                'icsc.hopdong.vanchuyen.chitietbanggia': (lambda self, cr, uid, ids, c={}: ids, ['banggia_id','tax_id','ngay_hieu_luc','ngay_het_hieu_luc','gia_co_thue','tax_id','check','name','ngay_banhanh'], 10),
                'icsc.hopdong.vanchuyen.giacuoc': (_get_order, ['gia_chua_thue', 'gia_co_thue','tax_id','tu_diem','den_diem','check','quyet_dinh'], 10),
                'icsc.hopdong.vanchuyen.giacuoc.chitiet': (_get_orders, ['tax_id','ngay_hieu_luc','ngay_het_hieu_luc','gia_co_thue','check','name','ngay_banhanh'], 10),
            },
            multi='all'),
        #'gia_co_thues': fields.function(_gia_co_thue,type='float',string='Giá có thuế'),
        'ma_vung': fields.char('Mã vùng', size=500,track_visibility='onchange')  ,
        'so_quyet_dinh': fields.many2one('icsc.quyetdinh.giacuoc.vanchuyen','Sô quyết định',track_visibility='onchange'),
        'ngay_hieu_luc': fields.date('Ngày hiệu lực',track_visibility='onchange'),
        'ngay_het_hieu_luc': fields.date('Ngày hết hiệu lực',track_visibility='onchange'),
       
    }
    
    def onchange_banggia_id(self, cr, uid, ids, banggia_id, context=None):
        if not banggia_id:
            return {}
        banggia_id_object=self.pool.get('icsc.hopdong.vanchuyen.giacuoc').browse(cr, uid, banggia_id, context=context)
        gia_chua_thue=banggia_id_object.gia_chua_thue
        tax_id=banggia_id_object.tax_id.id
        gia_co_thue=banggia_id_object.gia_co_thue
        tu_diem=banggia_id_object.tu_diem.id
        den_diem=banggia_id_object.den_diem.id
        ngay_hieulucs = False
        ngay_kethucs = False
        so_quyet_dinhs = False
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d') 
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')                               
        for line in banggia_id_object.chitiet_banggia:   
            if  line.ngay_hieuluc:    
                ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
            if line.ngay_kethuc:
                ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
            if line.ngay_hieuluc and line.ngay_kethuc:                    
                ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                    ngay_hieulucs=line.ngay_hieuluc
                    ngay_kethucs=line.ngay_kethuc
                    so_quyet_dinhs=line.name.id 
            if line.ngay_hieuluc and not line.ngay_kethuc:
                if todays_date >=ngay_hieuluc:   
                    ngay_hieulucs=line.ngay_hieuluc
                    ngay_kethucs=False
                    so_quyet_dinhs=line.name.id   
        
        return {'value': {'gia_chua_thue':gia_chua_thue ,'tax_id':tax_id,'gia_co_thue':gia_co_thue,'tu_diem':tu_diem,'den_diem':den_diem,
                          'ngay_hieu_luc':ngay_hieulucs,'ngay_het_hieu_luc':ngay_kethucs, 'so_quyet_dinh':so_quyet_dinhs}}
        
icsc_hopdong_vanchuyen_chitietbanggia()

class icsc_hopdong_vanchuyen_chitietvattu(osv.osv):
    _description="icsc_hopdong_vanchuyen_chitietvattu"
    _name = 'icsc.hopdong.vanchuyen.chitietvattu'
    _inherit = ['mail.thread'] 
    
    _columns = {      
        'hopdong_id': fields.many2one('icsc.hopdong.vanchuyen', 'Hợp đồng', track_visibility='onchange'),       
        'product_id': fields.many2one('product.product', 'Sản phẩm', track_visibility='onchange' ),
        'loai_san_pham': fields.many2one('product.category', 'Loại sản phẩm', track_visibility='onchange'),
        'so_luong': fields.float('Số lượng', track_visibility='onchange'),
        'don_vi': fields.many2one('product.uom', 'Đơn vị', ondelete='cascade', track_visibility='onchange'),       
            
       
    }
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        if not product_id:
            return {}
        district_object=self.pool.get('product.product').browse(cr, uid, product_id, context=context)
        uom_id=district_object.uom_id.id
        loai_id=district_object.categ_id.id
        return {'value': {'don_vi':uom_id ,'loai_san_pham':loai_id}}
icsc_hopdong_vanchuyen_chitietvattu()

class icsc_quyetdinh_giacuoc_vanchuyen(osv.osv):
    _description="icsc_quyetdinh_giacuoc_vanchuyen"
    _name = 'icsc.quyetdinh.giacuoc.vanchuyen'
    _inherit = ['mail.thread'] 
    _order= 'id desc'
    _columns = {      
        'name':fields.char('Số quyết định', track_visibility='onchange'),
        'ngay_banhanh': fields.date('Ngày ban hành', required=True, track_visibility='onchange')  ,
        'ngay_hieuluc': fields.date('Ngày hiệu lực', required=True, track_visibility='onchange')  ,
        'ngay_kethuc': fields.date('Ngày hết hiệu lực',help='Ngày mà bảng giá cước hết hiệu lực',  track_visibility='onchange')  ,
        'check': fields.boolean('Đang hoạt động', track_visibility='onchange'),
    }
    def write(self, cr, uid, ids, vals, context=None):
        ngay_kethuc=vals.get('ngay_kethuc') or False
        ct_pool=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.chitiet')
        if ngay_kethuc:
            for data in self.browse(cr, uid, ids, context):
                # lay bang gia co quyet dinh
                domain = [ ('name', '=', data.id)]
                #gia_ids = ct_pool.search(cr, uid, domain, context=context)
                
                #ct_pool.write(cr, uid, gia_ids, {'ngay_kethuc':ngay_kethuc,}, context=context)
        return super(icsc_quyetdinh_giacuoc_vanchuyen, self).write(cr, uid, ids, vals, context=context)
    def _icsc_quyetdinh_giacuoc_vanchuyen(self, cr, uid, callback, context=None):
        if context is None:
            context = {}
        proxy = self.pool.get('icsc.quyetdinh.giacuoc.vanchuyen')
        domain = ['|', ('ngay_hieuluc', '!=', False),('ngay_kethuc', '!=', False) ]

        ids = proxy.search(cr, uid, domain, context=context)
        if ids:
            callback(cr, uid, ids, context=context)

        # tools.debug(callback)
        # tools.debug(ids)
        return True
    
    def run_set_quyetdinhhoatdong_scheduler(self, cr, uid, context=None):
        self._icsc_quyetdinh_giacuoc_vanchuyen(cr, uid, self.set_hoatdong, context=context)
        
    def set_hoatdong(self, cr, uid, ids,  context=None):
        try:
            cr.execute(""" update stock_move m
            set name=(select name_template from product_product p where p.id=m.product_id) 
            where coalesce(name,'')='' """)  
        except:
            pass         
        for tre in self.browse(cr, uid, ids, context=context):
            ngay_hieuluc=tre.ngay_hieuluc
            if ngay_hieuluc:
                ngay_hieuluc=datetime.strptime(ngay_hieuluc,'%Y-%m-%d')
            ngay_kethuc=tre.ngay_kethuc
            if ngay_kethuc:
                ngay_kethuc=datetime.strptime(ngay_kethuc,'%Y-%m-%d')
            now=datetime.now().strftime('%Y-%m-%d')
            todays_date = datetime.strptime(str(now), '%Y-%m-%d')
            query="""select now()::date as todays_date"""
            cr.execute(query)
            for item in cr.dictfetchall():
                todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')      
            check=tre.check
            if check==False:
                if ngay_kethuc:
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:         
                        self.write(cr, uid, tre.id, {'check': True})
                else:
                    if todays_date >=ngay_hieuluc:
                        self.write(cr, uid, tre.id, {'check': True})             
            else:
                if ngay_kethuc:
                    if todays_date >ngay_kethuc or todays_date <ngay_hieuluc:            
                        self.write(cr, uid, tre.id, {'check': False})
                else:
                    if todays_date <ngay_hieuluc:
                        self.write(cr, uid, tre.id, {'check': False})
                    
        return True 
icsc_quyetdinh_giacuoc_vanchuyen()

class icsc_loai_giacuoc_vanchuyen(osv.osv):
    _description="icsc_loai_giacuoc_vanchuyen"
    _name = 'icsc.loai.giacuoc.vanchuyen'
    _inherit = ['mail.thread'] 
    _order= 'id desc'
    _columns = {      
        'name':fields.char('Tên nhóm bảng giá cước', size=500,track_visibility='onchange'),
        'ghi_chu':fields.text('Ghi chú', track_visibility='onchange'),
    }
icsc_loai_giacuoc_vanchuyen()
class icsc_hopdong_vanchuyen_giacuoc(osv.osv):
    _description="icsc_hopdong_vanchuyen_giacuoc"
    _name = 'icsc.hopdong.vanchuyen.giacuoc'
    _inherit = ['mail.thread']
    # tu dong them quyet dinh khi co 1 bang gia moi duoc tao
    def _tien_chua_thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}    
        c=[]    
        if context is None:
            context = {}
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for data in self.browse(cr, uid, ids, context):  
            gia_chua_thue=0.0                     
            for line in data.chitiet_banggia: 
                if line.ngay_hieuluc and line.ngay_kethuc:       
                    ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
                    ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                        gia_chua_thue=line.gia_chua_thue 
                if line.ngay_hieuluc and  not line.ngay_kethuc:  
                        ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
                        try:
                            ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                        except:
                            ngay_kethuc=False
                        if todays_date >=ngay_hieuluc:   
                            gia_chua_thue=line.gia_chua_thue 
            res[data.id]=gia_chua_thue
        return res
    
    def _tien_co_thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        if context is None:
            context = {}
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for data in self.browse(cr, uid, ids, context):  
            gia_co_thue=0.0          
            for line in data.chitiet_banggia:               
                # quyet_dinh = line.name.name
                # self.write(cr, uid, [data.id], {'ngay_hieuluc': ngay_hieuluc, 'ngay_kethuc': ngay_kethuc,'so_quyet_dinh': quyet_dinh})
                ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')               
                if line.ngay_hieuluc and line.ngay_kethuc:                    
                    ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')  
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                        gia_co_thue=line.gia_co_thue  
                if line.ngay_hieuluc and not line.ngay_kethuc:                    
                    #ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')  
                    if todays_date >=ngay_hieuluc:   
                        gia_co_thue=line.gia_co_thue         
            res[data.id]=gia_co_thue
        return res
    
    def _thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        if context is None:
            context = {}
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for data in self.browse(cr, uid, ids, context):    
            thue=False        
            for line in data.chitiet_banggia:               
                ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
               
                if line.ngay_hieuluc and line.ngay_kethuc:                    
                    ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')                    
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                        thue=line.tax_id.id  
                if line.ngay_hieuluc and not line.ngay_kethuc:                  
                                        
                    if todays_date >=ngay_hieuluc:   
                        thue=line.tax_id.id         
            res[data.id]=thue
        return res
    def _so_quyet_dinh(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        if context is None:
            context = {}
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')
        for data in self.browse(cr, uid, ids, context):   
            qd=False         
            for line in data.chitiet_banggia:               
                ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
                if line.ngay_hieuluc and line.ngay_kethuc:                    
                    ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:   
                        qd=line.name.id  
                if line.ngay_hieuluc and not line.ngay_kethuc:
                    if todays_date >=ngay_hieuluc:   
                        qd=line.name.id       
            res[data.id]=qd
        return res
    def tudiem(self, cr, uid, context=None):
        res={}
        
        string=False
        if context is None:
            context = {}       
       
        cr.execute("""select * from icsc_hopdong_vanchuyen_giacuoc order by id desc limit 1""")
        for item in cr.dictfetchall():
            string=item['tu_diem']
        return string
    def thue(self, cr, uid, context=None):
        res={}
        
        string=False
        if context is None:
            context = {}       
       
        cr.execute("""select * from icsc_hopdong_vanchuyen_giacuoc order by id desc limit 1""")
        for item in cr.dictfetchall():
            string=item['tax_id']
        return string
    _columns = {
      
        'name': fields.char('Tên bảng giá', size=1000,
            required=True, track_visibility='onchange')  ,
       'ngay_banhanh': fields.date('Ngày ban hành', track_visibility='onchange')  ,
       # 'ngay_hieuluc': fields.function(_ngay_hieuluc, type='datetime', string='Ngày hiệu lực')  ,
       #'ngay_kethuc': fields.function(_ngay_het_hieuluc, type='datetime', string='Ngày hết hiệu lực',)  ,
        'loai_vanchuyen': fields.selection([
            ('thongthuong', 'Đường sắt'),
            ('chuyentuyen', 'Đường sắt + Đường bộ'),
            ('duongthuy', 'Đường thuỷ + Đường bộ'),
            ('duongbo', 'Đường bộ'),           
            
            ], 'Phương thức vận chuyển', track_visibility='onchange'), 
        'tu_diem': fields.many2one('res.country.diadiem',   'Vận chuyển từ điểm',domain="[('van_chuyen','=',True)]" , track_visibility='onchange',required=True,select=True),
        'den_diem': fields.many2one('res.country.diadiem', 'Vận chuyển đến điểm',domain="[('van_chuyen','=',True)]" ,track_visibility='onchange',required=True,select=True),
        'gia_chua_thue':fields.function(_tien_chua_thue, type='float',   digits=(16,0),string='Giá trước thuế/Tấn'), 
        #'tax_id':fields.function(_thue, type='many2one', relation='account.tax',string='Thuế'), 
        'tax_id':fields.many2one('account.tax', 'Thuế'),   
        'gia_co_thue': fields.function(_tien_co_thue, type='float', string='Giá có thuế/Tấn'),
        'ma_vung': fields.char('Mã vùng', size=500, track_visibility='onchange')  ,
        'gia_thanhtoan': fields.float('Giá thanh toán', track_visibility='onchange'),
        'check': fields.boolean('Đang hoạt động', track_visibility='onchange'),
        'chitiet_banggia':fields.one2many('icsc.hopdong.vanchuyen.giacuoc.chitiet','giacuoc_id','Chi tiết bảng giá'),
        #'so_quyet_dinh': fields.char('Số quyết định', size=64, track_visibility='onchange'),
        'nhom_banggia': fields.many2one('icsc.loai.giacuoc.vanchuyen', 'Nhóm tên bảng giá'),
        'quyet_dinh': fields.function(_so_quyet_dinh, type='many2one',relation='icsc.quyetdinh.giacuoc.vanchuyen',  string='Số quyết định'),
        'price_round': fields.float('Chỉ số làm tròn',
            digits_compute= dp.get_precision('Product Price'),
            help="Sets the price so that it is a multiple of this value.\n" \
              "Rounding is applied after the discount and before the surcharge.\n" \
              "To have prices that end in 9.99, set rounding 10, surcharge -0.01" \
            ),
         'so_quyet_dinh': fields.many2one('icsc.quyetdinh.giacuoc.vanchuyen',  string='Số quyết định'),
    }
    _defaults={ 'tu_diem':tudiem,
                'tax_id':thue,
               # 'price_round':0,
               }
    def onchange_tudiem(self, cr, uid, ids, tu_diem, den_diem, context=None):
        if not tu_diem:
            return {}
        district_object=self.pool.get('res.country.diadiem').browse(cr, uid, tu_diem, context=context)
        district_code=district_object.district_code
        string_tenbg=''
        tudiem_name=district_object.name
        string_tenbg +=tudiem_name
        if den_diem:
            den_diem_object=self.pool.get('res.country.diadiem').browse(cr, uid, den_diem, context=context)
            den_diem_name=den_diem_object.name
            string_tenbg +=' - '+den_diem_name
        return {'value': {'ma_vung':district_code,'name': string_tenbg}}
    def onchange_dendiem(self, cr, uid, ids, tu_diem, den_diem, context=None):
        if not den_diem:
            return {}
        string_tenbg=''
        if tu_diem:
            district_object=self.pool.get('res.country.diadiem').browse(cr, uid, tu_diem, context=context)
            district_code=district_object.district_code
            
            tudiem_name=district_object.name
            string_tenbg +=tudiem_name
        if den_diem:
            den_diem_object=self.pool.get('res.country.diadiem').browse(cr, uid, den_diem, context=context)
            den_diem_name=den_diem_object.name
            string_tenbg +=' - '+den_diem_name
        return {'value': {'name': string_tenbg}}
    
    def _icsc_hopdong_vanchuyen_giacuoc(self, cr, uid, callback, context=None):
        if context is None:
            context = {}
        proxy = self.pool.get('icsc.hopdong.vanchuyen.giacuoc')
        domain = [ ('name', '!=', False) ]

        ids = proxy.search(cr, uid, domain, context=context)
        if ids:
            callback(cr, uid, ids, context=context)
        return True
    def run_set_hoatdong_scheduler(self, cr, uid, context=None):
        self._icsc_hopdong_vanchuyen_giacuoc(cr, uid, self.set_hoatdong, context=context)
    def set_hoatdong(self, cr, uid, ids,  context=None):
        now = datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        for data in self.browse(cr, uid, ids, context=context):
            for line in data.chitiet_banggia:
                gia_chua_thue = line.gia_chua_thue 
                quyet_dinh = line.name.id
                if line.ngay_hieuluc and line.ngay_kethuc:
                    ngay_hieuluc=datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
                    ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:  
                        query="""select distinct hd.id from icsc_hopdong_vanchuyen hd
                                left join icsc_hopdong_vanchuyen_chitietbanggia ct on ct.hopdong_id=hd.id
                                where ct.tu_diem = %s and  ct.den_diem =%s """%(data.tu_diem.id, data.den_diem.id)
                        cr.execute(query)
                        for item_gia in cr.dictfetchall():
                            hopdong_id = item_gia['id']
                            domain = [('hopdong_id','=',hopdong_id),('so_quyet_dinh','=',quyet_dinh),('banggia_id','=',data.id)]
                            item_ids = self.pool.get('icsc.hopdong.vanchuyen.chitietbanggia').search(cr, uid, domain)
                            if len(item_ids) == 0:
                                self.pool.get('icsc.hopdong.vanchuyen.chitietbanggia').create(cr, uid, {
                                                'banggia_id': data.id,
                                                'tu_diem': data.tu_diem.id,
                                                'den_diem': data.den_diem.id,
                                                'gia_chua_thue': gia_chua_thue, 
                                                'tax_id': line.tax_id.id,
                                                'gia_co_thue': line.gia_co_thue,
                                                'so_quyet_dinh': line.name.id,
                                                'ngay_hieu_luc': line.ngay_hieuluc,
                                                'ngay_het_hieu_luc': line.ngay_kethuc, 
                                                'hopdong_id': hopdong_id,
                                                 }, context=context)
                elif line.ngay_hieuluc and not line.ngay_kethuc:
                    ngay_hieuluc = datetime.strptime(line.ngay_hieuluc,'%Y-%m-%d')
                    try:
                        ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')
                    except:
                        ngay_kethuc=False
                    if todays_date >= ngay_hieuluc:
                        query="""select distinct hd.id from icsc_hopdong_vanchuyen hd
                                left join icsc_hopdong_vanchuyen_chitietbanggia ct on ct.hopdong_id=hd.id
                                where ct.tu_diem = %s and  ct.den_diem =%s"""%(data.tu_diem.id, data.den_diem.id)
                        cr.execute(query)
                        for item_gia in cr.dictfetchall():
                            hopdong_id = item_gia['id']
                            domain = [('hopdong_id','=',hopdong_id),('so_quyet_dinh','=',quyet_dinh),('banggia_id','=',data.id)]
                            item_ids = self.pool.get('icsc.hopdong.vanchuyen.chitietbanggia').search(cr, uid, domain)
                            if len(item_ids) == 0:
                                self.pool.get('icsc.hopdong.vanchuyen.chitietbanggia').create(cr, uid, {
                                                'banggia_id': data.id,
                                                'tu_diem': data.tu_diem.id,
                                                'den_diem': data.den_diem.id,
                                                'gia_chua_thue': gia_chua_thue, 
                                                'tax_id': line.tax_id.id,
                                                'gia_co_thue': line.gia_co_thue,
                                                'so_quyet_dinh': line.name.id,
                                                'ngay_hieu_luc': line.ngay_hieuluc,
                                                'ngay_het_hieu_luc': line.ngay_kethuc, 
                                                'hopdong_id': hopdong_id,        
                                                 }, context=context)
            self.write(cr, uid, [data.id], {'so_quyet_dinh': data.quyet_dinh.id or False})
        return True
    
icsc_hopdong_vanchuyen_giacuoc()

class icsc_hopdong_vanchuyen_giacuoc_chitiet(osv.osv):
    _description="icsc_hopdong_vanchuyen_giacuoc_chitiet"
    _name = 'icsc.hopdong.vanchuyen.giacuoc.chitiet'
    _order='id desc'
    _inherit = ['mail.thread']
    
    def _tien_chua_thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=0
        tienthue=chuathue=0
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            
            tax_id=data.tax_id.id
            thanhtoan=data.gia_co_thue
            if tax_id==False:
                tienthue=0
            else:
                tienthue=data.tax_id.amount
                chuathue =thanhtoan/(1+tienthue)
            
            res[data.id]=chuathue
        return res
    def _get_nhom_banggia(self, cr, uid, ids, name=None, args=None, context=None):
        res={}       
        if context is None:
            context = {}
        nhom=False
        for data in self.browse(cr, uid, ids, context):   
            if data.giacuoc_id:
                if data.giacuoc_id.nhom_banggia:
                    nhom=data.giacuoc_id.nhom_banggia.id         
            res[data.id]=nhom
        return res
    def _get_tu_diem(self, cr, uid, ids, name=None, args=None, context=None):
        res={}       
        if context is None:
            context = {}
        tu_diem=False
        for data in self.browse(cr, uid, ids, context):   
            if data.giacuoc_id:
                if data.giacuoc_id.tu_diem:
                    tu_diem=data.giacuoc_id.tu_diem.id         
            res[data.id]=tu_diem
        return res
    def _get_den_diem(self, cr, uid, ids, name=None, args=None, context=None):
        res={}       
        if context is None:
            context = {}
        den_diem=False
        for data in self.browse(cr, uid, ids, context):   
            if data.giacuoc_id:
                if data.giacuoc_id.den_diem:
                    den_diem=data.giacuoc_id.den_diem.id         
            res[data.id]=den_diem
        return res
    
    def _function_all(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for data in self.browse(cursor, user, ids, context=context):
            res[data.id] = {
                'gia_chua_thue': 0.0,  
                'nhom_banggia':False,
                'tu_diem':False,
                'den_diem':False,                             
            }
            tienthue = chuathue =  0
            if data.tax_id:
                tienthue=data.tax_id.amount
                chuathue =data.gia_co_thue/(1+tienthue)
            res[data.id]['gia_chua_thue'] =chuathue
            nhom = tu_diem = den_diem = False
            if data.giacuoc_id:
                if data.giacuoc_id.nhom_banggia:
                    nhom=data.giacuoc_id.nhom_banggia.id
                if data.giacuoc_id.tu_diem:
                    tu_diem=data.giacuoc_id.tu_diem.id
                if data.giacuoc_id.den_diem:
                    den_diem=data.giacuoc_id.den_diem.id
            res[data.id]['nhom_banggia'] =nhom
            res[data.id]['tu_diem'] =tu_diem
            res[data.id]['den_diem'] =den_diem
        return res
    
    _columns = {
       'giacuoc_id': fields.many2one('icsc.hopdong.vanchuyen.giacuoc',  'Bảng giá', domain=[('check','=',True)],ondelete='cascade',required=True, ),
       'name': fields.many2one('icsc.quyetdinh.giacuoc.vanchuyen',  'Số quyết định', domain=[('check','=',True)],ondelete='cascade',required=True, select=True),
       'ngay_banhanh': fields.date('Ngày ban hành', track_visibility='onchange')  ,
       'ngay_hieuluc': fields.date('Ngày hiệu lực',required=True, track_visibility='onchange')  ,
       'ngay_kethuc': fields.date('Ngày hết hiệu lực',
                            help='Ngày mà bảng giá cước hết hiệu lực', track_visibility='onchange')  ,
        'loai_vanchuyen': fields.selection([
            ('thongthuong', 'Đường sắt'),
            ('chuyentuyen', 'Đường sắt + Đường bộ'),
            ('duongthuy', 'Đường thuỷ + Đường bộ'),
            ('duongbo', 'Đường bộ'),           
            
            ], 'Phương thức vận chuyển'),      
       # 'gia_chua_thue':fields.function(_tien_chua_thue, type='float',  digits=(16,0),string='Giá trước thuế/Tấn', track_visibility='onchange'), 
        'gia_chua_thue': fields.function(_function_all, digits_compute=dp.get_precision('Account'), string='Giá trước thuế/Tấn',
            multi='all'),
        'tax_id': fields.many2one('account.tax', 'Thuế', ondelete='cascade', track_visibility='onchange'),
        'gia_co_thue': fields.float('Giá có thuế/Tấn', track_visibility='onchange'),        
        'check': fields.boolean('Đang hoạt động'),           
#         'nhom_banggia':fields.function(_get_nhom_banggia, type='many2one', 
#                                        relation='icsc.loai.giacuoc.vanchuyen',
#                                        string='Nhóm'),
        'nhom_banggia': fields.function(_function_all, type='many2one', 
                                        relation='icsc.loai.giacuoc.vanchuyen',
                                        string='Nhóm', multi='all'),
#         'tu_diem':fields.function(_get_tu_diem, type='many2one', 
#                                        relation='res.country.diadiem',
#                                        string='Vận chuyển từ điểm'),
                
        'tu_diem':fields.function(_function_all, type='many2one', 
                                       relation='res.country.diadiem',
                                       string='Vận chuyển từ điểm', multi='all'),
                
#         'den_diem':fields.function(_get_den_diem, type='many2one', 
#                                        relation='res.country.diadiem',
#                                        string='Vận chuyển đến điểm'),
        'den_diem':fields.function(_function_all, type='many2one', 
                                       relation='res.country.diadiem',
                                       string='Vận chuyển đến điểm', multi='all'),
    }
    def _check_date(self, cursor, user, ids, context=None):
        for pricelist_version in self.browse(cursor, user, ids, context=context):
            #if not pricelist_version.check:
            #    continue
            where = []
            if pricelist_version.ngay_hieuluc:
                where.append("((ngay_kethuc>='%s') or (ngay_kethuc is null))" % (pricelist_version.ngay_hieuluc,))
            if pricelist_version.ngay_kethuc:
                where.append("((ngay_hieuluc<='%s') or (ngay_hieuluc is null))" % (pricelist_version.ngay_kethuc,))

            cursor.execute('SELECT id ' \
                    'FROM icsc_hopdong_vanchuyen_giacuoc_chitiet ' \
                    'WHERE '+' and '.join(where) + (where and ' and ' or '')+
                        'giacuoc_id = %s ' \
                        
                        'AND id <> %s', (
                            pricelist_version.giacuoc_id.id,
                            pricelist_version.id))
            if cursor.fetchall():
                return False
        return True

#     _constraints = [
#         (_check_date, 'Không thể tồn tại 2 mức giá trong cùng 1 thời điểm',
#             ['ngay_hieuluc', 'ngay_kethuc'])
#     ]
    def onchange_quyetdinh(self, cr, uid, ids, quyetdinh, context=None):
        if not quyetdinh:
            return {}
        quyetdinh_object=self.pool.get('icsc.quyetdinh.giacuoc.vanchuyen').browse(cr, uid, quyetdinh, context=context)
        ngay_banhanh=quyetdinh_object.ngay_banhanh
        ngay_hieuluc=quyetdinh_object.ngay_hieuluc
        ngay_kethuc=quyetdinh_object.ngay_kethuc                
        return {'value': {'ngay_banhanh':ngay_banhanh,'ngay_hieuluc':ngay_hieuluc,
                          'ngay_kethuc':ngay_kethuc, 'check':quyetdinh_object.check }}
    def onchange_ngayhieuluc(self, cr, uid, ids, ngay_hieuluc, ngay_kethuc, context=None):
        if not ngay_hieuluc:
            return {}
        check=True        
        if ngay_hieuluc:
            ngay_hieuluc=datetime.strptime(ngay_hieuluc,'%Y-%m-%d')
        if ngay_kethuc:
            ngay_kethuc=datetime.strptime(ngay_kethuc,'%Y-%m-%d')
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')      
        if check==False:
            if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:         
                check = True
        else:
            if ngay_kethuc:
                if todays_date > ngay_kethuc or todays_date < ngay_hieuluc:            
                    check = False  
            else:
                if  todays_date < ngay_hieuluc:
                    check = False    
        return {'value': {'check':check }}
    
    def _icsc_hopdong_vanchuyen_giacuoc_chitiet(self, cr, uid, callback, context=None):
        if context is None:
            context = {}
        proxy = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.chitiet')
        domain = [('ngay_hieuluc', '!=', False) ]
        ids = proxy.search(cr, uid, domain, context=context)
        if ids:
            callback(cr, uid, ids, context=context)
        return True
    
    def run_set_hoatdong_scheduler(self, cr, uid, context=None):
        self._icsc_hopdong_vanchuyen_giacuoc_chitiet(cr, uid, self.set_hoatdong, context=context)
    def set_hoatdong(self, cr, uid, ids,  context=None):
        now=datetime.now().strftime('%Y-%m-%d')
        todays_date = datetime.strptime(str(now), '%Y-%m-%d')
        query="""select now()::date as todays_date"""
        cr.execute(query)
        for item in cr.dictfetchall():
            todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d') 
        on_ids = off_ids = []  
        for tre in self.browse(cr, uid, ids, context=context):
            ngay_hieuluc=tre.ngay_hieuluc
            if ngay_hieuluc:
                ngay_hieuluc=datetime.strptime(ngay_hieuluc,'%Y-%m-%d')
            ngay_kethuc=tre.ngay_kethuc
            if ngay_kethuc:
                ngay_kethuc=datetime.strptime(ngay_kethuc,'%Y-%m-%d')               
            check=tre.check
            if check==False:
                if ngay_kethuc and ngay_hieuluc:
                    if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:         
                        #self.write(cr, uid, [tre.id], {'check': True})
                        on_ids.append(tre.id)
                else:
                    if todays_date >=ngay_hieuluc:         
                        #self.write(cr, uid, [tre.id], {'check': True})
                        on_ids.append(tre.id)
            else:
                if ngay_kethuc and ngay_hieuluc:
                    if todays_date >ngay_kethuc or todays_date >ngay_hieuluc:            
                        #self.write(cr, uid, [tre.id], {'check': False})
                        off_ids.append(tre.id)
        if off_ids:
            self.write(cr, uid, off_ids, {'check': False})
        if on_ids:
            self.write(cr, uid, on_ids, {'check': True})
        return True 
    def run_update_obj_scheduler(self, cr, uid, context=None):
        self._icsc_hopdong_vanchuyen_giacuoc_chitiet(cr, uid, self.update_object, context=context)
    def update_object(self, cr, uid, ids,  context=None):
        try:
            query="""UPDATE icsc_phieu_vanchuyen pvc
                    SET haiduong_id=(select haiduong_id from sale_order od where od.id=pvc.sale_id)"""   
            cr.execute(query)
        except:
            pass
        try:
            query_stock="""UPDATE stock_picking pk
                    SET haiduong_id=(select haiduong_id from sale_order od where od.id=pk.sale_id)"""   
            cr.execute(query_stock)
        except:
            pass
        try:
            query_vc="""UPDATE icsc_hopdong_vanchuyen_giacuoc_kehoach pk
                    SET haiduong_id=(select haiduong_id from sale_order od where od.id=pk.sale_id)"""   
            cr.execute(query_vc)
        except:
            pass
        try:
            query_kho=""" UPDATE stock_move mv
               SET date=coalesce((select pk.date_done from stock_picking pk where pk.id=mv.picking_id and pk.state='done' and coalesce(date_done,now()+ interval '100 years')!=now()+ interval '100 years'),mv.date)
               where picking_id>0"""
            cr.execute(query_kho)
        except:
            pass  
#         try:
#             query_loai="""UPDATE stock_picking pk 
#                SET  loai_lenh_vc=(select loai_lenh_vc from sale_order o where pk.sale_id=o.id)
#              WHERE coalesce(loai_lenh_vc,'')=''"""   
#             cr.execute(query_loai)
#         except:
#             pass      
        return True 
icsc_hopdong_vanchuyen_giacuoc_chitiet()    
class icsc_hopdong_vanchuyen_giacuoc_xa(osv.osv):
    _description="icsc_hopdong_vanchuyen_giacuoc_xa"
    _name = 'icsc.hopdong.vanchuyen.giacuoc.xa'
    _inherit = ['mail.thread'] 
    
    def _tien_chua_thue(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=0
        tienthue=chuathue=0
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            tax_id=data.tax_id.id
            thanhtoan=data.gia_co_thue
            if tax_id==False:
                tienthue=0
            else:
                tienthue=data.tax_id.amount
                chuathue =thanhtoan/(1+tienthue)
            res[data.id]=chuathue
        return res
    _columns = {
      
        'name': fields.char('Số quyết định', size=500,
            required=True, track_visibility='onchange')  ,
       'ngay_banhanh': fields.date('Ngày ban hành', required=True, track_visibility='onchange')  ,
        'ngay_hieuluc': fields.date('Ngày hiệu lực', required=True, track_visibility='onchange')  ,
       'ngay_kethuc': fields.date('Ngày hết hiệu lực',
                            help='Ngày mà bảng giá cước hết hiệu lực', required=True, track_visibility='onchange')  ,     
       'gia_chua_thue':fields.function(_tien_chua_thue, type='float', string='Giá trước thuế/Tấn', track_visibility='onchange'), 
        'tax_id': fields.many2one('account.tax', 'Thuế', ondelete='cascade', track_visibility='onchange'),
        'gia_co_thue': fields.float('Đơn giá có thuế/Tấn', track_visibility='onchange'),       
        'dien_giai': fields.text('Diễn giải', track_visibility='onchange')  ,
        'gia_thanhtoan': fields.float('Giá thanh toán', track_visibility='onchange'),
          'check': fields.boolean('Đang hoạt động', track_visibility='onchange'),
    }
    def _icsc_hopdong_vanchuyen_giacuoc_xa(self, cr, uid, callback, context=None):
        if context is None:
            context = {}
        proxy = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.xa')
        domain = [ ('ngay_hieuluc', '!=', False),('ngay_kethuc', '!=', False) ]

        ids = proxy.search(cr, uid, domain, context=context)
        if ids:
            callback(cr, uid, ids, context=context)

        # tools.debug(callback)
        # tools.debug(ids)
        return True
    def run_set_hoatdong_xa_scheduler(self, cr, uid, context=None):
        self._icsc_hopdong_vanchuyen_giacuoc_xa(cr, uid, self.set_hoatdong, context=context)
    def set_hoatdong(self, cr, uid, ids,  context=None):
        res = {}        
        for tre in self.browse(cr, uid, ids, context=context):
            ngay_hieuluc=tre.ngay_hieuluc
            if ngay_hieuluc:
                ngay_hieuluc=datetime.strptime(ngay_hieuluc,'%Y-%m-%d')
            ngay_kethuc=tre.ngay_kethuc
            if ngay_kethuc:
                ngay_kethuc=datetime.strptime(ngay_kethuc,'%Y-%m-%d')
            now=datetime.now().strftime('%Y-%m-%d')
            todays_date = datetime.strptime(str(now), '%Y-%m-%d')
            query="""select now()::date as todays_date"""
            cr.execute(query)
            for item in cr.dictfetchall():
                todays_date = datetime.strptime(str(item['todays_date']), '%Y-%m-%d')      
            check=tre.check
            if check==False:
                if todays_date <=ngay_kethuc and todays_date >=ngay_hieuluc:         
                    self.write(cr, uid, tre.id, {'check': True})
            else:
                if todays_date >ngay_kethuc or todays_date <ngay_hieuluc:            
                    self.write(cr, uid, tre.id, {'check': False})
        return True 
icsc_hopdong_vanchuyen_giacuoc_xa()
class icsc_hopdong_vanchuyen_kehoach(osv.osv):
    _description="Ke hoach van chuyen"
    _name = 'icsc.hopdong.vanchuyen.giacuoc.kehoach'
    _inherit = ['mail.thread']
    _order='id desc'
    def _kl_dang_vc(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        #confirm=False       
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            count=0 
            #state=data.state
            #if state=='confirm':
                #confirm=True
            for line in data.chitiet_kh:
                count +=line.kl_dangvc_dukien
            res[data.id]=count
        return res
    def _get_street(self, cr, uid, ids, field_name, arg, context=None):
       
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] =False
            khachhang_obj=order.order_partner_id
            if khachhang_obj: 
                street=khachhang_obj.street
                #street=khachhang_obj.street
                if street==False:
                    street=''
                state_id=khachhang_obj.state_id.name
                if state_id==None:
                    state_id=''
                district_id=khachhang_obj.district_id.name
                if district_id==None:
                    district_id=''
                ward_id=khachhang_obj.ward_id.name
                if ward_id==None:
                    ward_id=''
                diachi=street+' - '+ward_id+' - '+district_id+' - '+state_id
        
                res[order.id] = diachi
        return res
    def _get_khoiluongkh(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        if context is None:
            context = {}        
        for order in self.browse(cr, uid, ids, context):  
            val=0        
            for line in order.chitiet_kh:
                
                val+=line.kl_vc_kehoach
            res[order.id]=val
            
        return res
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            res[data.id] = {              
                'check_state':False,
            }
            state=data.state
            confirm=False
            count=0
            if state=='confirm':
                confirm=True
            for line in data.chitiet_kh:
                count +=line.kl_dangvc_dukien
            if count>0 and confirm: 
                #self.write(cr, uid, [data.id], {'state': 'process'})              
                #break
                if data.state!='process':
                    cr.execute("""update icsc_hopdong_vanchuyen_giacuoc_kehoach set state='process' 
                                    where id= """+str(data.id))
            kl_conlai=0
            dem_huy=0
            kl_dangvcdk=0
            #lay tat ca khoi luong van chuyen con lai
            for line in data.chitiet_kh:                
                kl_conlai +=line.kl_vc_conlai
                kl_dangvcdk +=line.kl_dangvc_dukien
            
            # neu con lai = 0
            check_pvc=True
            count_huy=0
            # xem cacs phieu van chuyen lien quan
            # NEU XUAT HIEN PVC TON TAI TRANG THAI KHAC DONE, CANCEL
            query="""select * from icsc_phieu_vanchuyen
                    where kehoach_vanchuyen= """+str(data.id)
            cr.execute(query)
            for item in cr.dictfetchall():
                state=item['state']
                if state not in ('cancel','done'):
                    check_pvc=False
            # NEU TAT CA PHIEU DEU O TRANG THAI HUY -->KHONG DONE
            query_huy="""select count(*) as sl from icsc_phieu_vanchuyen
                    where kehoach_vanchuyen= """+str(data.id)+""" and state='cancel'"""
            cr.execute(query_huy)
            for item_huy in cr.dictfetchall():
                count_huy =item_huy['sl']
            # kiem tra tong so PVC cua KHVC
            query_count="""select count(*) as sl from icsc_phieu_vanchuyen
                    where kehoach_vanchuyen= """+str(data.id)
            cr.execute(query_count)
            for item_count in cr.dictfetchall():
                dem_huy =item_count['sl']
            # Neu TAT CA CAC PVC O TRANG THAI HUY
            if count_huy==dem_huy and count_huy!=0 and dem_huy!=0 :
                return True
            if kl_conlai==0 and check_pvc:
                if data.state!='done':
                    cr.execute("""update icsc_hopdong_vanchuyen_giacuoc_kehoach set state='done' 
                                    where id= """+str(data.id))
            if kl_dangvcdk==0:                
                if data.state!='confirm':
                    cr.execute("""update icsc_hopdong_vanchuyen_giacuoc_kehoach set state='confirm' 
                                    where id= """+str(data.id))
        return res
    def _chang_khvc(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        #confirm=False       
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            if data.trung_chuyen:
                res[data.id]="KH cha"
                if data.chang_khvc:
                    if data.chang_khvc=='chang_1':
                        res[data.id]="Chặng 1"
                    else:
                        res[data.id]="Chặng 2"
            else:
                res[data.id]=False            
                
        return res
    def _khach_hang(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        
        #confirm=False       
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            res[data.id]=False
            if data.chang_khvc:
                if data.chang_khvc=='chang_1':
                    if data.donvi_nhanhang:
                        res[data.id]=data.donvi_nhanhang.id
                else:
                    if data.khach_hang:
                        res[data.id]=data.khach_hang.id
            else:
                if data.khach_hang:
                    res[data.id]=data.khach_hang.id
        return res
    _columns = {
      'kh_tmp': fields.function(_khach_hang,type='many2one',string='Đơn vị nhận hàng', relation='res.partner'),
      'chang_tmp': fields.function(_chang_khvc,type='char',string='Chặng VC', size=256),
      'tong_khoiluong': fields.function(_get_khoiluongkh,type='float',string='Tổng KLKH'),
       'name': fields.char('Lệnh Xuất Hàng - Mã KHVC', size=500,select=True,
            required=True, track_visibility='onchange' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]})  ,
       'tao_khvc_ngoaile': fields.boolean('Tạo kế hoạch ngoại lệ' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},track_visibility='onchange'),
       'so_khvc': fields.many2one('icsc.hopdong.vanchuyen','Số HĐVC',domain="[('check','=',True),('congty_vc','=',congty_vc)]",states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange')  ,
       'loai_khvc': fields.selection([
            ('vat', 'VAT'),  
            ('gui_ban', 'Hàng gửi'),
            ('kho_tap_trung', 'Hàng kho TT'),      
            ('kho_dai_ly', 'Hàng N.Liệu'),            
           ], 'Loại KHVC',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'), 
         'phuongthuc_vc': fields.selection([                
            ('duongsat_chuyentuyen', 'Đường sắt + Đường bộ'), 
             ('duongsat_thongthuong', 'Đường sắt'), 
            ('duongbo', 'Đường bộ'),          
            ('duongthuy', 'Đường thủy + Đường bộ'),             
            
            ], 'Phương thức vận chuyển',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'), 
       'congty_vc': fields.many2one('res.partner', 'Tên nhà vận chuyển',domain=[('check','=',True),('supplier','=',True),('is_company','=',True)], states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
       'sale_id': fields.many2one('sale.order', 'Số lệnh xuất hàng', required=True ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
       'khach_hang': fields.many2one('res.partner', 'Tên khách hàng',domain=[('check','=',True),('customer','=',True)] ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
       'kl_dang_vc':fields.function(_kl_dang_vc, type='float', string='Tổng KL đang VC', track_visibility='onchange'),
       'ngay_tao': fields.date('Ngày tạo đơn hàng', track_visibility='onchange',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},)  ,
       'ngay_lap': fields.date('Ngày lập KHVC', track_visibility='onchange',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True)  ,  
       #'dia_chi_khach_hang': fields.many2one('res.country.diadiem', 'Địa chỉ khách hàng', ), 
       'dia_chi_khach_hang': fields.char('Địa chỉ khách hàng', size=500,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True), 
        'dien_giai': fields.text('Diễn giải', track_visibility='onchange')  ,      
         'state': fields.selection([
            ('draft', 'Chưa thực hiện'),
            ('confirm', 'Xác nhận'),
            ('process', 'Đang VC'),
            ('done', 'Hoàn tất'),
            ('cancel', 'Đã hủy'),
            ], 'Trạng thái', readonly=True ,states={'process': [('readonly', True)],'process': [('readonly', True)],'done':[('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'), 
        'state_pheduyet': fields.selection([
            ('draft', 'Chưa duyệt'),
            ('confirm', 'Xác nhận'),
            ('done', 'Đã duyệt'),
            ('cancel', 'Đã hủy'),
            ], 'Trạng thái phê duyệt' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'), 
        'ngay_duyet': fields.date('Ngày duyệt',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange')  ,
        'nguoi_duyet': fields.many2one('hr.employee', 'Người duyệt',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
        'kiem_soat': fields.many2one('res.country.tramkiemsoat', 'Trạm kiểm soát' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',required=True),
        'giam_sat_kho': fields.many2one('icsc.giamsatkho', 'Giám sát kho' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
        'tu_diem': fields.many2one('res.partner', 'Đơn hàng từ điểm' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
        'den_diem': fields.many2one('res.partner', 'Đơn hàng đến điểm' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
        'diem_trung_chuyen': fields.many2one('res.partner', 'Đến điểm trung chuyển' ,domain="[('is_trungchuyen','=',True)]",states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
        'cuoc_tu_diem': fields.many2one('res.country.diadiem', 'Tính cước từ điểm'  ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True,domain=[('van_chuyen','=',True)]),
        'cuoc_den_diem': fields.many2one('res.country.diadiem', 'Tính cước đến điểm',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True,domain=[('van_chuyen','=',True)]),
        'nhan_hang_tn': fields.date('Nhận hàng từ ngày' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},track_visibility='onchange')  ,
        'nhan_hang_dn': fields.date('Nhận hàng đến ngày' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange')  ,  
        'tinh_denxa': fields.boolean('Tính giá đến xã' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
        'chitiet_kh': fields.one2many('icsc.hopdong.vanchuyen.chitiet','kehoach_id', 'Chi tiết vận chuyển' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},),
        'parent_id': fields.boolean('Là kế hoạch cha',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
        'kehoach_cha': fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch cha',domain=[('parent_id','=',True)],states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},),
        'donvi_thuchien': fields.many2one('res.partner','Nơi xuất hàng' ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},track_visibility='onchange'), 
        'la_khach_hang': fields.boolean('Đơn vị nhận hàng là khách hàng',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
        'donvi_nhanhang': fields.many2one('res.partner', 'Đơn vị nhận hàng',domain=[('check','=',True),('supplier','=',True)],states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True),
        'dia_chi_donvi_nhanhang': fields.many2one('res.country.diadiem', 'Địa chỉ đơn vị nhận hàng',domain="[('van_chuyen','=',True)]" ,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True ), 
        'trung_chuyen': fields.boolean('Có trung chuyển',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
        'xuatkho_lines': fields.one2many('stock.picking','kehoach_vanchuyen_id', 'Chi tiết xuất kho' ),
        'phieuvc_lines': fields.one2many('icsc.phieu.vanchuyen','kehoach_vanchuyen', 'Chi tiết phiếu vận chuyển',),
        'dia_chi_khach_hang_con': fields.char('Địa chỉ khách hàng', size=500,states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'), 
        'chang_khvc': fields.selection([
            ('chang_1', 'Chặng 1'),  
            ('chang_2', 'Chặng 2'),                    
           ], 'Chặng VC',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'), 
       
          'order_partner_id': fields.related('sale_id', 'partner_id', type='many2one', relation='res.partner', store=True, string='Tên khách hàng',select=True),
          'street': fields.function(_get_street,type='char',            
           size=500, string='Địa chỉ'),
          'haiduong_id': fields.related('sale_id', 'haiduong_id', type='many2one', relation='sale.shop', store=True, string='Đơn vị thực hiện',select=True),
          'ngoai_le': fields.boolean('KHVC Ngoại lệ',states={'process': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange'),
    }
    _defaults= {'state':'draft',
                 #'donvi_thuchien':'lamthao',
                 #'chang_khvc':'chang_1',
                 'phuongthuc_vc':'duongbo',
                 'state_pheduyet':'draft',
                 'ngoai_le':False,
                  'ngay_lap':fields.date.context_today,#time.strftime('%Y-%m-%d'),
                  # 'name': lambda self, cr, uid, c: self.pool.get('sequence.custormize.vanchuyen.kehoach').get_name(cr, uid, 'icsc.phieu.vanchuyen', 'icsc_hopdong_vanchuyen_giacuoc_kehoach','')
                  }
    #oanhle
    def _icsc_hopdong_vanchuyen_giacuoc_kehoach(self, cr, uid, callback, context=None):
        if context is None:
            context = {}
        proxy = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        domain = [ ('state', 'in', ('confirm','process')) ]

        ids = proxy.search(cr, uid, domain, context=context)
        if ids:
            callback(cr, uid, ids, context=context)

        # tools.debug(callback)
        # tools.debug(ids)
        return True
    def run_set_hoantat_scheduler(self, cr, uid, context=None):
        self._icsc_hopdong_vanchuyen_giacuoc_kehoach(cr, uid, self.set_hoantat, context=context)
    def set_hoantat(self, cr, uid, ids,  context=None):
        res = {}        
        for data in self.browse(cr, uid, ids, context=context):
            state=data.state
            confirm=False
            count=0
            if state=='confirm':
                confirm=True
            for line in data.chitiet_kh:
                count +=line.kl_dangvc_dukien
            if count>0 and confirm: 
                #self.write(cr, uid, [data.id], {'state': 'process'})              
                #break
                if data.state!='process':
                    cr.execute("""update icsc_hopdong_vanchuyen_giacuoc_kehoach set state='process' 
                                    where id= """+str(data.id))
            kl_conlai=0
            dem_huy=0
            kl_dangvcdk=0
            #lay tat ca khoi luong van chuyen con lai
            for line in data.chitiet_kh:                
                kl_conlai +=line.kl_vc_conlai
                kl_dangvcdk +=line.kl_dangvc_dukien
            
            # neu con lai = 0
            check_pvc=True
            check_huy=False
            count_huy=0
            # xem cacs phieu van chuyen lien quan
            # NEU XUAT HIEN PVC TON TAI TRANG THAI KHAC DONE, CANCEL
            query="""select * from icsc_phieu_vanchuyen
                    where kehoach_vanchuyen= """+str(data.id)
            cr.execute(query)
            for item in cr.dictfetchall():
                state=item['state']
                if state not in ('cancel','done'):
                    check_pvc=False
            # NEU TAT CA PHIEU DEU O TRANG THAI HUY -->KHONG DONE
            query_huy="""select count(*) as sl from icsc_phieu_vanchuyen
                    where kehoach_vanchuyen= """+str(data.id)+""" and state='cancel'"""
            cr.execute(query_huy)
            for item_huy in cr.dictfetchall():
                count_huy =item_huy['sl']
            # kiem tra tong so PVC cua KHVC
            query_count="""select count(*) as sl from icsc_phieu_vanchuyen
                    where kehoach_vanchuyen= """+str(data.id)
            cr.execute(query_count)
            for item_count in cr.dictfetchall():
                dem_huy =item_count['sl']
            # Neu TAT CA CAC PVC O TRANG THAI HUY
            if count_huy==dem_huy and count_huy!=0 and dem_huy!=0 :
                return True
            if kl_conlai==0 and check_pvc:
                #self.write(cr, uid, [data.id], {'state': 'done'})
                if data.state!='done':
                    cr.execute("""update icsc_hopdong_vanchuyen_giacuoc_kehoach set state='done' 
                                    where id= """+str(data.id))
                #break
            if kl_dangvcdk==0:                
                #self.write(cr, uid, [data.id], {'state': 'confirm'})
                if data.state!='confirm':
                    cr.execute("""update icsc_hopdong_vanchuyen_giacuoc_kehoach set state='confirm' 
                                    where id= """+str(data.id))
        return True
    def unlink(self, cr, uid, ids, context=None):
        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in sale_orders:
            if s['state'] in ['draft', 'cancel']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Lỗi!'), _('Bạn chỉ có thể xóa KHVC ở trạng thái Dự thảo và Đã hủy!'))

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        
        if context is None:
            context = {}
       
        if context.get('active_model', '') in ['icsc.hopdong.vanchuyen.giacuoc.kehoach'] and context.get('active_ids', False) and context['active_ids']:
            partner = self.pool.get(context['active_model']).read(cr, uid, context['active_ids'], ['parent_id','trung_chuyen'])[0]
            if not view_type:
                view_id = self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'icsc.hopdong.vanchuyen.giacuoc.kehoach.form')])
                view_type = 'tree'            
        if view_id and isinstance(view_id, (list, tuple)):
            view_id = view_id[0]
        res = super(icsc_hopdong_vanchuyen_kehoach,self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        for field in res['fields']:
            if field == 'parent_id' and type:                
                parent_id=res['fields'][field]['selectable']
        doc = etree.XML(res['arch'])
        if view_type == 'form':
            partner_string = _('Cha')
            if parent_id ==True:
                partner_string = _('LXH')
                for node in doc.xpath("//tree[@name='chitiet_tree']"):
                    node.set('string', partner_string)
            
            res['arch'] = etree.tostring(doc)
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        # if alias_model has been changed, update alias_model_id accordingly
        nhan_hang_tn=vals.get('nhan_hang_tn')
        ngay_lap= vals.get('ngay_lap') 
        kehoach_cha=vals.get('kehoach_cha')
        
        if not ngay_lap:
            for data in self.browse(cr, uid, ids, context):    
                ngay_lap=data.ngay_lap 
                kehoach_cha=data.kehoach_cha                
        if ngay_lap and nhan_hang_tn and kehoach_cha:   
            tn=datetime.strptime(nhan_hang_tn,'%Y-%m-%d')     
            ngay_lap1=datetime.strptime(ngay_lap,'%Y-%m-%d') 
            if tn != ngay_lap1:     
                raise osv.except_osv(_("Thông báo!"), _("Ngày tạo KHVC phải giống Nhận hàng từ ngày ."))   
                        
            
        return super(icsc_hopdong_vanchuyen_kehoach, self).write(cr, uid, ids, vals, context=context)
    
    def load_hopdong(self, cr, uid, ids, congty_vc, context=None):
        if not congty_vc:
            return {}  
        so_khvc=False
        now=datetime.now()
        query="""select * from icsc_hopdong_vanchuyen 
        where congty_vc= """+str(congty_vc)+""" and ngay_hieuluc<= '"""+str(now)+"""'::date and ngay_kethuc>= '""" +str(now)+"""'::date"""
        cr.execute(query)        
        for item in cr.dictfetchall():
            so_khvc=item['id']
        return {'value': {'so_khvc':so_khvc}}
    
    def onchange_phuongthuc_vc(self, cr, uid, ids, phuongthuc_vc, context=None):
        if not phuongthuc_vc:
            return {}
        if phuongthuc_vc=='duongsat_thongthuong':            
            return {'value': {'cuoc_tu_diem':113}}
        else:
            return {}
    def onchange_diem_trung_chuyen(self, cr, uid, ids, diem_trung_chuyen, context=None):
        if not diem_trung_chuyen:
            return {}          
        return {'value': {'den_diem':diem_trung_chuyen}}   
    def create(self, cr, uid, vals, context=None):
        kehoach_cha=vals.get('kehoach_cha')
        trung_chuyen=vals.get('trung_chuyen')
        if kehoach_cha or (trung_chuyen==False or trung_chuyen==None):
            nhan_hang_tn=vals.get('nhan_hang_tn')
            ngay_lap= vals.get('ngay_lap') 
            if ngay_lap and nhan_hang_tn:
                tn=datetime.strptime(nhan_hang_tn,'%Y-%m-%d')       
               
                ngay_lap1=datetime.strptime(ngay_lap,'%Y-%m-%d') 
                if tn != ngay_lap1:     
                    raise osv.except_osv(_("Thông báo!"), _("Ngày tạo KHVC phải giống Nhận hàng từ ngày ."))   
                            
        sale_order=vals.get('sale_id')
        sale_pool = self.pool.get('sale.order') 
        dem=0
        if sale_order:
            sale_object=sale_pool.browse(cr, uid, sale_order, context)
            sale_id=sale_object.id
            query="""select coalesce(count(*),0) as soluong 
                    from  icsc_hopdong_vanchuyen_giacuoc_kehoach
                    where sale_id= """+str(sale_id)
            cr.execute(query)
            for item in cr.dictfetchall():
                dem+=item['soluong']
            if dem==0:
                sale_pool.write(cr, 1, [sale_id], {'state': 'sent'}, context=context)
        return super(icsc_hopdong_vanchuyen_kehoach, self).create(cr, uid, vals, context=context)
    def action_load_tu_cha(self, cr, uid, ids,  context=None):
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.chitiet') 
        kehoach_cha=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        for data in self.browse(cr, uid, ids, context):
            kehoach_cha_id=data.kehoach_cha.id
            data_cha = kehoach_cha.browse(cr, uid, kehoach_cha_id, context)
            for line in data_cha.chitiet_kh:                
                kehoach_pool.create(cr, uid, {'product_id':line.product_id.id,
                                             'kl_vc_dukien':line.kl_vc_dukien,
                                             'kehoach_id':data.id,
                                             'dia_chi_giao':line.dia_chi_giao.id,                                            
                                             'kl_can_vanchuyen':line.kl_can_vanchuyen,
                                             'kl_vc_kehoach':line.kl_vc_kehoach,
                                             'sale_order_line':line.sale_order_line.id,
                                             'cha_id':line.id,
                                             }, context=context)
        return True
    def onchange_khach_hang(self, cr, uid, ids, khach_hang, context=None):
        if not khach_hang:
            return {}   
        khachhang_pool=self.pool.get('res.partner')
        khachhang_obj=khachhang_pool.browse(cr, uid, khach_hang)
        street=khachhang_obj.street
        if street==False:
            street=''
        state_id=khachhang_obj.state_id.name
        if state_id==None:
            state_id=''
        district_id=khachhang_obj.district_id.name
        if district_id==None:
            district_id=''
        ward_id=khachhang_obj.ward_id.name
        if ward_id==None:
            ward_id=''
        diachi=street+' - '+ward_id+' - '+district_id+' - '+state_id
        
        return {'value': {'dia_chi_khach_hang':diachi}}
    def onchange_khach_hang_con(self, cr, uid, ids, donvi_nhanhang, context=None):
        if not donvi_nhanhang:
            return {}   
        khachhang_pool=self.pool.get('res.partner')
        khachhang_obj=khachhang_pool.browse(cr, uid, donvi_nhanhang)
        street=khachhang_obj.street
        if street==False:
            street=''
        state_id=khachhang_obj.state_id.name
        if state_id==None:
            state_id=''
        district_id=khachhang_obj.district_id.name
        if district_id==None:
            district_id=''
        ward_id=khachhang_obj.ward_id.name
        if ward_id==None:
            ward_id=''
        diachi=street+' - '+ward_id+' - '+district_id+' - '+state_id
        
        return {'value': {'dia_chi_khach_hang_con':diachi}}
    def onchange_la_khach_hang(self, cr, uid, ids, la_khach_hang, sale_id, cuoc_den_diem, khach_hang,context=None):
        if la_khach_hang:
            if sale_id:
                dia_chi_giao=False
                sale_object=self.pool.get('sale.order').browse(cr, uid, sale_id)
                for item2 in sale_object.order_line:
                    dia_chi_giao=item2.dia_chi_giao.id
                return {'value': {'den_diem':dia_chi_giao}}#         
        else:
            return {}
    def onchange_sale_id(self, cr, uid, ids, sale_id, parent_id,trung_chuyen,la_khach_hang,chang_khvc,name,context=None):
        if not sale_id:
            return {}   
        sale_object=self.pool.get('sale.order').browse(cr, uid, sale_id)
        loai_lenh_xuat=sale_object.loai_lenh_xuat
        tu_diem=sale_object.kho_xuat_id.id
        khach_hang=sale_object.partner_id.id
        kho_xuat=sale_object.kho_xuat_id.id
        ngay_batdau=sale_object.ngay_batdau
        ngay_kethuc=sale_object.ngay_kethuc
        for item in sale_object.order_line:
            dia_chi_giao=item.dia_chi_giao.id
        # NEU LXH la kho cong ty va kho xuat blank 
        #-->DON HANG TU DIEM: KHO LAM THAO
        type_kho=sale_object.type_kho
        kho_xuatss=sale_object.kho_xuat_id.id
        
        if type_kho=='kho_congty' and (kho_xuatss is None or kho_xuatss==False):
            tu_diem=62
        #end        
        date_order=sale_object.date_order
        if chang_khvc=='chang_1':
            dia_chi_giao=False
        dc_nhan=False
        if chang_khvc=='chang_2':
            dc_nhan=sale_object.partner_id.id
        #danh ten theo LXH
        
        name_lxh=sale_object.name
        name_string =name_lxh+'_'
        max=0 
        if parent_id:     
            query="""  SELECT name
                      FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                      where sale_id=%s and parent_id=True
                      order by name desc limit 1"""
        else:
            query="""  SELECT name
                      FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                      where sale_id=%s and parent_id=False and coalesce(ngoai_le,False) = False
                      order by name desc limit 1"""
        cr.execute(query,(sale_id,))
        for item in  cr.dictfetchall():               
                project_name = item['name']
                if project_name:
                    length=len(project_name)
                    sub=length-1
                    strs = project_name[sub:]
                    str2=strs
                    #project_name_replace = project_name[sub:]
                    project_name_replace = str2
                    if len(project_name_replace)==0:
                        name_string= name_lxh
                        #raise osv.except_osv(_('Error!'), _("Please check format EL Code in Engagement Letter list latest! "))
                    p_order_number = project_name_replace
                    try:
                        if int(p_order_number)>max:
                            max=int(p_order_number)  
                            tmp= p_order_number
                    except:
                        tmp='00'
        if max:
                i=1
                while (i <= len(tmp)):
                    number = int(tmp[:i])
                    if number > 0:
                        p_oder_number = int(tmp[i-1:])
                        p_order_number = p_oder_number + 1                       
                        name_string= name_string  + '%%0%sd'  % 2 % p_order_number
                        break
                    i+=1               
        else:              
                name_string= name_string  + '%%0%sd'  % 2 % 1  
        if parent_id or trung_chuyen==False:
            return {'value': {'name':name_string,'nhan_hang_tn':ngay_batdau,'nhan_hang_dn':ngay_kethuc,'khach_hang':khach_hang,'ngay_tao':date_order,'tu_diem':tu_diem,'den_diem':dia_chi_giao,'donvi_thuchien':tu_diem}}
        else:            
            return {'value': {'donvi_nhanhang':dc_nhan,'nhan_hang_tn':ngay_batdau,'nhan_hang_dn':ngay_kethuc,'ngay_tao':date_order,'donvi_thuchien':kho_xuat,'den_diem':dia_chi_giao}}
    def onchange_sale_id_ngoaile(self, cr, uid, ids, sale_id, ngoai_le,context=None):
        if not sale_id:
            return {}   
        sale_object=self.pool.get('sale.order').browse(cr, uid, sale_id)
        tu_diem=sale_object.kho_xuat_id.id
        khach_hang=sale_object.partner_id.id
        ngay_batdau=sale_object.ngay_batdau
        ngay_kethuc=sale_object.ngay_kethuc
        dia_chi_giao=False
        for item in sale_object.order_line:
            dia_chi_giao=item.dia_chi_giao.id
        # NEU LXH la kho cong ty va kho xuat blank 
        #-->DON HANG TU DIEM: KHO LAM THAO
        type_kho=sale_object.type_kho
        kho_xuatss=sale_object.kho_xuat_id.id
        if type_kho=='kho_congty' and (kho_xuatss is None or kho_xuatss==False):
            tu_diem=62
        name_lxh=sale_object.name
        name_string ='NL_'+name_lxh+'_'
        max=0
        date_order=sale_object.date_order
        query="""  SELECT name
                      FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                      where sale_id=%s and parent_id=False and coalesce(ngoai_le,False) = True
                      order by name desc limit 1"""
        cr.execute(query,(sale_id,))
        for item in  cr.dictfetchall():               
                project_name = item['name']
                if project_name:
                    length=len(project_name)
                    sub=length-1
                    strs = project_name[sub:]
                    str2=strs
                    #project_name_replace = project_name[sub:]
                    project_name_replace = str2
                    if len(project_name_replace)==0:
                        name_string= name_lxh
                        #raise osv.except_osv(_('Error!'), _("Please check format EL Code in Engagement Letter list latest! "))
                    p_order_number = project_name_replace
                    try:
                        if int(p_order_number)>max:
                            max=int(p_order_number)  
                            tmp= p_order_number
                    except:
                        tmp='00'
        if max:
                i=1
                while (i <= len(tmp)):
                    number = int(tmp[:i])
                    if number > 0:
                        p_oder_number = int(tmp[i-1:])
                        p_order_number = p_oder_number + 1                       
                        name_string= name_string  + '%%0%sd'  % 2 % p_order_number
                        break
                    i+=1               
        else:              
                name_string= name_string  + '%%0%sd'  % 2 % 1 
        return {'value': {'name':name_string,'nhan_hang_tn':ngay_batdau,'nhan_hang_dn':ngay_kethuc,'khach_hang':khach_hang,'ngay_tao':date_order,'tu_diem':tu_diem,'den_diem':dia_chi_giao,'donvi_thuchien':tu_diem}}
        
    def onchange_parent_id(self, cr, uid, ids, parent_id,chang_khvc, context=None):
        if not parent_id:
            return {}  
        count=0  
        for id in ids:
            count +=1
        project_name=''
        if count==0:
            sale_object=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, parent_id)
            name_parent=sale_object.name
            name_string=name_parent+'_'
            sale_id=sale_object.sale_id.id
            ngay_tao=sale_object.ngay_tao
            donvi_thuchien=sale_object.donvi_thuchien
            loai_khvc=sale_object.loai_khvc   
            max=0     
            query="""  SELECT name
                      FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                      where kehoach_cha=%s
                      order by id desc limit 1"""
            cr.execute(query,(parent_id,))
            for item in  cr.dictfetchall():               
                    project_name = item['name']
                    if project_name:
                        length=len(project_name)
                        sub=length-1
                        strs = project_name[sub:]
                        str2=strs
                        #project_name_replace = project_name[sub:]
                        project_name_replace = str2
                        if len(project_name_replace)==0:
                            name_string= name_parent+'_'
                            #raise osv.except_osv(_('Error!'), _("Please check format EL Code in Engagement Letter list latest! "))
                        p_order_number = project_name_replace
                        try:
                            if int(p_order_number)>max:
                                max=int(p_order_number)  
                                tmp= p_order_number
                        except:
                            tmp='0000'
            if max:
                    i=1
                    while (i <= len(tmp)):
                        number = int(tmp[:i])
                        if number > 0:
                            p_oder_number = int(tmp[i-1:])
                            p_order_number = p_oder_number + 1                       
                            name_string= name_string  + '%%0%sd'  % 1 % p_order_number
                            break
                        i+=1               
            else:              
                    name_string= name_string  + '%%0%sd'  % 1 % 1 
            # xu ly viec load dia diem dua vao cau truc cha - con
            tudiem=dendiem=la_khach_hang=False
            # kiem tra xem van chuyen la ke hoach I
            dem=0
            if project_name==False:
                project_name=''
            query_chang1="""select *  FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                              where kehoach_cha=%s 
                              order by name desc limit 1"""        
            cr.execute(query_chang1,(parent_id,))
            for item_chang1 in cr.dictfetchall():
                dem +=1
                tu_diem=item_chang1['tu_diem']
                den_diem=item_chang1['den_diem']
                la_khach_hang=item_chang1['la_khach_hang']
                donvi_nhanhang=item_chang1['donvi_nhanhang']
            if dem==0:
                #la chang I
                tudiem=sale_object.tu_diem.id
                dendiem=sale_object.den_diem.id
                # tu diem va den diem duoc lay tu ke hoach cha
            else:
                # LA CAC CHANG TIEP THEO    
                if chang_khvc=='chang_1':
                    tudiem=sale_object.tu_diem.id
                    dendiem=False
                else:         
                    tudiem=den_diem
                    if la_khach_hang:
                        dendiem=den_diem
                    else:
                        dendiem=donvi_nhanhang
            # return {'value': {'loai_khvc':loai_khvc,'ngay_tao':ngay_tao,'donvi_thuchien':donvi_thuchien, 'sale_id':sale_id,'name':name_string,'tu_diem':tudiem,'den_diem':dendiem}}
        else:
            sale_object=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, parent_id)
            name_parent=sale_object.name
            name_string=name_parent+'_'
            sale_id=sale_object.sale_id.id
            ngay_tao=sale_object.ngay_tao
            donvi_thuchien=sale_object.donvi_thuchien
            loai_khvc=sale_object.loai_khvc   
            max=0     
            project_name=False
            query="""  SELECT name
                      FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                      where kehoach_cha=%s and id=%s
                      order by name desc limit 1"""
            cr.execute(query,(parent_id,ids[0],))
            for item in  cr.dictfetchall():               
                    project_name = item['name']
            if project_name!=False:
                length=len(project_name)
                sub=length-1
                strs = project_name[sub:]
                str2=strs
                #project_name_replace = project_name[sub:]
                project_name_replace = str2
                if len(project_name_replace)==0:
                    name_string= name_parent+'_'
                    #raise osv.except_osv(_('Error!'), _("Please check format EL Code in Engagement Letter list latest! "))
                p_order_number = project_name_replace
                try:
                    if int(p_order_number)>max:
                        max=int(p_order_number)  
                        tmp= p_order_number
                except:
                    tmp='0000'
                if max>0:
                        i=1
                        while (i <= len(tmp)):
                            number = int(tmp[:i])
                            if number > 0:
                                p_oder_number = int(tmp[i-1:])
                                p_order_number = p_oder_number + 1                       
                                name_string= name_string  + '%%0%sd'  % 1 % p_order_number
                                break
                            i+=1               
                else:              
                        name_string= name_string  + '%%0%sd'  % 1 % 1 
            else:
                name_string=project_name
            # xu ly viec load dia diem dua vao cau truc cha - con
            tudiem=dendiem=la_khach_hang=False
            # kiem tra xem van chuyen la ke hoach I
            dem=0
            if project_name==False:
                project_name=''
            query_chang1="""select *  FROM icsc_hopdong_vanchuyen_giacuoc_kehoach
                              where kehoach_cha=%s and id!=%s and name<%s
                              order by name desc limit 1"""        
            cr.execute(query_chang1,(parent_id,ids[0],project_name,))
            for item_chang1 in cr.dictfetchall():
                dem +=1
                tu_diem=item_chang1['tu_diem']
                den_diem=item_chang1['den_diem']
                la_khach_hang=item_chang1['la_khach_hang']
                donvi_nhanhang=item_chang1['donvi_nhanhang']
            if dem==0:
                #la chang I
                tudiem=sale_object.tu_diem.id
                dendiem=sale_object.den_diem.id
                # tu diem va den diem duoc lay tu ke hoach cha
            else:
                # LA CAC CHANG TIEP THEO  
                if chang_khvc=='chang_1':
                    tudiem=sale_object.tu_diem.id
                    dendiem=False  
                else:         
                    tudiem=den_diem
                    if la_khach_hang:
                        dendiem=den_diem
                    else:
                        dendiem=donvi_nhanhang
        return {'value': {'loai_khvc':loai_khvc,'ngay_tao':ngay_tao, 'sale_id':sale_id,'name':name_string,'tu_diem':tudiem,'den_diem':dendiem}}
    
    def action_confirm(self, cr, uid, ids, context=None):
        kho_dai_ly=False
        kho_khach_hang=False
#         query="""select * from stock_location where name='Kho Đại Lý' and loai_hinh='kho_daily'"""
#         cr.execute(query)
#         for item in cr.dictfetchall():
#             kho_dai_ly=item['id']
#         if kho_dai_ly==False:
#                 raise osv.except_osv(_('Thông báo!'), _("Bạn phải tạo một Kho Đại Lý. Ghi chú: Kho hàng/Các địa điểm và tạo mới 1 Kho Đại Lý."))
        query_kh="""select * from stock_location where name='Customers' or name='Các khách hàng' """
        cr.execute(query_kh)
        for item_kh in cr.dictfetchall():
            kho_khach_hang=item_kh['id']
        if kho_khach_hang==False:
                raise osv.except_osv(_('Thông báo!'), _("Bạn phải tạo một vị trí giao hàng cho khách hàng. Ghi chú: Kho hàng/Các địa điểm và tạo mới 1 vị trí xuất hàng."))
             
        picking_pool = self.pool.get('stock.picking.out') 
        picking_id=False
        location_id=False
        move_pool = self.pool.get('stock.move')
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, [id1], {'state':'confirm',}, context)
            # kiem tra xem co trung chuyen hay khong
            is_parent=item.parent_id
            ke_hoach_cha=item.kehoach_cha.id
            trung_chuyen=item.trung_chuyen
            chang_khvc=item.chang_khvc            
            if item.tong_khoiluong<=0:
                raise osv.except_osv(_('Thông báo!'), _('Không thể xác nhận KHVC khi tổng KLVC=0. Vui lòng xem lại KHVC') )
            if (trung_chuyen==True and ke_hoach_cha and chang_khvc=='chang_1') or (trung_chuyen==False and is_parent==False and ke_hoach_cha==False ):
                # TAO PICKING
                string=''
                partner_id=item.khach_hang.id
                #la ke hoach con
                if ke_hoach_cha:
                    
                    partner_id=item.kehoach_cha.khach_hang.id
                    
                    
                partner_code=item.khach_hang.ma_quanly
                if partner_code: 
                    left_partner_code=partner_code[:2]+'-'
                else:
                    left_partner_code=''
                string +=left_partner_code
                sale_id=item.sale_id.id
                doitac_giaohang=item.congty_vc.id
                phuongthuc_vc=item.phuongthuc_vc
                tinh_code=item.congty_vc.ma_vung
                type_kho=item.sale_id.type_kho
                if tinh_code:
                    string +=tinh_code
                if doitac_giaohang==False:
                    doitac_giaohang=partner_id
                date=datetime.now()               
                kehoach_vanchuyen_id=item.id               
                khoxuat_id=item.sale_id.kho_xuat_id.id
                move_type='direct'
                loai=False
                loai_khvc=item.sale_id.loai_lenh_xuat
                if loai_khvc=='vat':
                    loai='thongthuong'
                else:
                    loai='noibo'
                
                seq_obj_name =  'stock.picking.' +loai
                picking_name =  self.pool.get('sequence.custormize.pickingout').get_name(cr, uid, seq_obj_name, 'stock_picking',loai)
                company_id=self.pool.get('res.users').browse(cr, uid, uid).company_id.id
                picking_id=picking_pool.create(cr, uid, {'partner_id':partner_id,
                                             'sale_id':sale_id,
                                             'doitac_giaohang':doitac_giaohang,
                                             'date':date,                                           
                                              'loai_xuatkho':loai,
                                             'kehoach_vanchuyen_id':kehoach_vanchuyen_id,
                                             'khoxuat_id':khoxuat_id,
                                             'move_type':move_type,
                                             'company_id':company_id, 
                                             'type':'out' ,  
                                            #'ma_vung':string,
                                             'type_kho':type_kho,
                                            # 'loai_vanchuyen':phuongthuc_vc, 
                                             'nguoi_lap_phieu':uid,
                                                                         
                                             }, context=context)
                # insert workflow wkf_instance
                cr.execute('select id from wkf where osv=%s',('stock.picking',))
                id_wkf=cr.fetchone()[0]
                cr.execute('INSERT INTO wkf_instance( '\
                            'wkf_id, uid, res_id, res_type, state) VALUES (%s,%s,%s,%s,%s)',
                            (id_wkf,uid,picking_id,'stock.picking','active',))  
                cr.execute('select id from wkf_instance order by id desc limit 1')
                inst_id_wkf=cr.fetchone()[0]
                cr.execute('select id from wkf_activity where wkf_id=%s and name=%s',(id_wkf,'draft',))   
                act_id_wkf=cr.fetchone()[0]
                cr.execute('INSERT INTO wkf_workitem( '\
                            'act_id, inst_id,  state) VALUES (%s,%s,%s)',
                            (act_id_wkf,inst_id_wkf,'complete',))
                # ket thuc workflow   
                #  TAO STOCK MOVE
                for line in item.chitiet_kh:
                    origin=item.name
                    product_id=line.product_id.id
                    product_name=line.product_id.name
                    product_qty=line.kl_vc_kehoach
                    product_uos=line.sale_order_line.product_uom_qty
                    sale_line_id=line.sale_order_line.id
                    
                    #vi_tri_xuat_den=item.sale_id.shop_id.warehouse_id.lot_stock_id.id
                    #den_diem_vt=item.den_diem.vi_tri
                   
                    sale_line_id_obj=line.sale_order_line
                    price_unit=line.sale_order_line.price_unit
                    product_uom=line.product_id.uom_id.id                    
                    
                    lot_stock_id=kho_khach_hang
                    gui_kho=item.sale_id.gui_kho
                    if loai=='thongthuong':
                        lot_stock_id=kho_khach_hang
                    else:
                        if gui_kho=='kho_ngoai' or gui_kho=='kho_ngoai_tt':
                            den_diem_vt=line.sale_order_line.dia_chi_giao
                            #neu khong tick chon kho -->loi
                            lakho=den_diem_vt.kho
#                             if lakho==False:
#                                 raise osv.except_osv(_("Thông báo!"), _("Không thể xuất kho với địa chỉ giao hàng '%s' không phải là kho")%(den_diem_vt.name))
                            if den_diem_vt:
                                den_diem_id=den_diem_vt.id
                                queryvt="""select * from stock_location where partner_id_diadiem= """+str(den_diem_id)
                                cr.execute(queryvt)
                                for vt in cr.dictfetchall():
                                    lot_stock_id=vt['id']
                        else:
                            den_diem_vt=line.dia_chi_giao
                            if den_diem_vt:
                                den_diem_id=den_diem_vt.vi_tri_lienket
                                if den_diem_id:
                                    lot_stock_id=den_diem_id.id 
                    if lot_stock_id==False:
                        lot_stock_id=kho_khach_hang
                    #-----------  XET TRUONG HOP KHO NGUON ---- #
                    # NEU LOAI HINH LA KHO CONG TY
                    order=item.sale_id
                    if type_kho=="kho_congty":
                        kho_xuat_congty=order.kho_xuat_id
                        if kho_xuat_congty:
                            #kho_xuat_congty_id=kho_xuat_congty.id
                            kho_xuat_congty_name=kho_xuat_congty.ref
                            if kho_xuat_congty_name=='kho_lam_thao': # neu kho xuat la kho lam thao
                                # nguon = dia chia trong san pham
                                location_id=line.product_id.vi_tri.id
                            else:   
                                # neu khac kho cong ty lam thao                 
                                la_kho1=kho_xuat_congty.kho
                                la_dd1=kho_xuat_congty.is_diadiem                    
                                tmp_kho1=False
                                if la_dd1:
                                    query_diadiem1="""select id from stock_location where partner_id_diadiem= """+str(kho_xuat_congty.id)
                                    cr.execute(query_diadiem1)
                                    for kho_diadiem1 in cr.dictfetchall():
                                        location_id=kho_diadiem1['id']
                                        tmp_kho1=location_id
                                if la_kho1:
                                    query_kho1="""select lot_input_id from stock_warehouse where partner_id= """+str(kho_xuat_congty.id)
                                    cr.execute(query_kho1)
                                    for kho_vt1 in cr.dictfetchall():
                                        location_id=kho_vt1['lot_input_id']
                                        tmp_kho1=kho_vt1['lot_input_id']
                                location_id=tmp_kho1 # lay theo kho xuat
                        else:
                            # neu kho xuat khong chon --> nguon la lam thao
                            location_id=25
                    else:
                        kho_xuat_congty=order.kho_xuat_id
                        if kho_xuat_congty: # neu kho xuat khac rong-->kho xuat
                            la_kho1=kho_xuat_congty.kho
                            la_dd1=kho_xuat_congty.is_diadiem                    
                            tmp_kho1=False
                            if la_dd1:
                                query_diadiem1="""select id from stock_location where partner_id_diadiem= """+str(kho_xuat_congty.id)
                                cr.execute(query_diadiem1)
                                for kho_diadiem1 in cr.dictfetchall():
                                    location_id=kho_diadiem1['id']
                                    tmp_kho1=location_id
                            if la_kho1:
                                query_kho1="""select lot_input_id from stock_warehouse where partner_id= """+str(kho_xuat_congty.id)
                                cr.execute(query_kho1)
                                for kho_vt1 in cr.dictfetchall():
                                    location_id=kho_vt1['lot_input_id']
                                    tmp_kho1=kho_vt1['lot_input_id']
                            location_id=tmp_kho1 # lay theo kho xuat
                             
                        else:
                            #neu kho xuat rong
                            nhan_hang_khac=line.sale_order_line.dia_chi_giao
                            if nhan_hang_khac: # neu dia chi nhan hang la kho --> lay dia chi
                                nhan_hang_khac_id=nhan_hang_khac.id
                                nhan_hang_kho=nhan_hang_khac.kho
                                #nhan_hang_is_diadiem=nhan_hang_khac.is_diadiem
                                if nhan_hang_kho:
                                    queryvt_khac="""select * from stock_location where partner_id_diadiem= """+str(nhan_hang_khac_id)
                                    cr.execute(queryvt_khac)
                                    for vt in cr.dictfetchall():
                                        location_id=vt['id']
                                else:
                                    location_id= kho_khach_hang
                    if location_id==False:
                        location_id=kho_khach_hang
                    if product_qty<=0:
                        raise osv.except_osv(_('Thông báo!'), _('Không thể tạo PXK khi khổi lượng =0. Vui lòng xem lại KHVC') )
                    move_pool.create(cr, uid, {
                                                                   'origin': origin,
                                                                   'product_uos_qty':product_uos,                                                                  
                                                                   'product_uom': product_uom,
                                                                   'price_unit': price_unit,
                                                                   'date_expected': date,
                                                                   'product_qty': product_qty,
                                                                   'product_uos': product_uom,
                                                                   'location_id': location_id,
                                                                   'name': product_name,
                                                                   'product_id': product_id,                                                        
                                                                   'partner_id':partner_id,
                                                                   'company_id':company_id ,                                                          
                                                                   'picking_id':picking_id,                                                                                                                      
                                                                   'state': 'draft',
                                                                   'location_dest_id':lot_stock_id,
                                                                   'sale_line_id':sale_line_id ,                                                         
                                                                   'chitiet_kh': line.id,
                                                                   'doitac_giaohang':line.dia_chi_giao.id
                                                                   }, context=context)    


        return True
    def action_confirm_ngoaile(self, cr, uid, ids, context=None):
        for item in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [item.id], {'state':'confirm',}, context)
        return True
    def action_process(self, cr, uid, ids, context=None):
        for item in self.browse(cr, uid, ids, context):
            self.write(cr, uid, [item.id], {'state':'process',}, context)
        return True
    def action_done(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, [id1], {'state':'done',}, context)
        return True
    def action_cancel(self, cr, uid, ids, context=None):
        picking_pool=self.pool.get('stock.picking')
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            # kiem tra KHVC Con da huy chua
            # chua huy ->loi
            dem_con=0
            cr.execute("""select count(*) as sl from icsc_hopdong_vanchuyen_giacuoc_kehoach
                        where state !='cancel' 
                        and kehoach_cha= """+str(id1))
            for count_con in cr.dictfetchall():                
                dem_con+=count_con['sl'] 
            if dem_con>0:
                raise osv.except_osv(
                        _('Thông báo'),
                        _('Kế hoạch vận chuyển con chưa hủy. Vui lòng hủy các KHVC con trước!'))
            # Neu chang 2 -->phai huy 1 truoc
            chang=item.chang_khvc
            cha_kh=item.kehoach_cha
            if chang=='chang_1' and cha_kh:
                dem_1=0
                cr.execute("""select count(*) as sl from icsc_hopdong_vanchuyen_giacuoc_kehoach
                            where state !='cancel' and  chang_khvc='chang_2'
                            and kehoach_cha= """+str(cha_kh.id))
                for count_con in cr.dictfetchall():                
                    dem_1+=count_con['sl'] 
                if dem_1>0:
                    raise osv.except_osv(
                        _('Thông báo'),
                        _('Kế hoạch vận chuyển con chặng 2 chưa hủy. Vui lòng hủy các KHVC con chặng 2 trước!'))
            count1=0
            cr.execute("""select * from stock_picking
            where state ='done' and type='out' and  coalesce(mistake_delivery,False)=False  and kehoach_vanchuyen_id= """+str(id1))
            for item2 in cr.dictfetchall():
                count1 +=1
                pxk=item2['name']
            if count1>0:
                raise osv.except_osv(
                        _('Thông báo'),
                        _('PXK %s liên quan đến KHVC đã giao hàng hoàn tất. Bạn không được phép hủy KHVC này.') % (pxk))
            cr.execute("""select * from stock_picking
            where state not in ('done','cancel') and kehoach_vanchuyen_id= """+str(id1))
            for item3 in cr.dictfetchall():                
                pxk=item3['id']
                picking_pool.unlink(cr, uid, [pxk], context)
            self.write(cr, uid, [id1], {'state':'cancel',}, context)
        return True
    def action_return(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, [id1], {'state':'draft',}, context)
        return True
icsc_hopdong_vanchuyen_kehoach()

class icsc_hopdong_vanchuyen_chitiet(osv.osv):
    _description="icsc_hopdong_vanchuyen_chitiet"
    _name = 'icsc.hopdong.vanchuyen.chitiet'
    _inherit = ['mail.thread']
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        val1=val=vatra=dukien=0.0
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'kl_vc_conlai': 0.0,
                'kl_dangvc_dukien': 0.0, 
                            
            } 
            
            kehoach_name=order.kehoach_id.name
            is_parent=order.kehoach_id.parent_id
            ke_hoach_cha=order.kehoach_id.kehoach_cha.id
            sale_order_line=order.sale_order_line.id
            product_id=order.product_id.id
            trung_chuyen=order.kehoach_id.trung_chuyen
            chang_khvc=order.kehoach_id.chang_khvc
            if  trung_chuyen==False or (ke_hoach_cha and chang_khvc=='chang_1'): 
                
                valtra=0            
                query="""SELECT  coalesce( sum(kl_vc),0) as khoiluong
                FROM icsc_phieu_vanchuyen_chitiet ct
                left join icsc_hopdong_vanchuyen_chitiet hd on ct.name=hd.id
                left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=pvc.kehoach_vanchuyen
                where ((coalesce(kh.kehoach_cha,0) !=0 and kh.chang_khvc!='chang_2') or coalesce(kh.trung_chuyen,False)=False ) and  
                ct.state not in ('draft','cancel') and ct.name= """+str(order.id)
                cr.execute(query)
                for tong in cr.dictfetchall(): 
                    val = tong['khoiluong']                    
                dukien=val 
                  
            if  (ke_hoach_cha and chang_khvc=='chang_2'): 
                val=0   
                #lay danh sach id cua chang 1
                cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                where kh.chang_khvc='chang_1' and kh.kehoach_cha=  """+str(ke_hoach_cha))
                for item_con in cr.dictfetchall():
                    con_id=item_con['id']       
                    query="""SELECT  coalesce( sum(kl_vc),0) as khoiluong
                    FROM icsc_phieu_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_chitiet hd on ct.name=hd.id
                    left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=pvc.kehoach_vanchuyen
                    where kh.chang_khvc='chang_2' and  
                    ct.state not in ('draft','cancel') and ct.name = """+str(con_id)
                    cr.execute(query)
                    for tong in cr.dictfetchall(): 
                        val += tong['khoiluong']                    
                dukien=val         
            if is_parent:
                val=valtra=0
                for lines in order.kehoach_id.chitiet_kh:                        
                        line_id=lines.id                        
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                      where kh.chang_khvc='chang_1' and ct.cha_id=  """+str(line_id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            query="""SELECT  coalesce( sum(kl_vc),0) as khoiluong
                                FROM icsc_phieu_vanchuyen_chitiet ct
                                left join icsc_hopdong_vanchuyen_chitiet hd on ct.name=hd.id
                                left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id
                                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=pvc.kehoach_vanchuyen
                                where kh.chang_khvc!='chang_2' and 
                                 ct.state not in ('draft','cancel') and ct.name= """+str(con_id)
                            cr.execute(query)
                            for tong in cr.dictfetchall(): 
                                val += tong['khoiluong'] 
                dukien=val
            
            res[order.id]['kl_dangvc_dukien']=dukien
            
            val1=order.kl_vc_kehoach - dukien       
            res[order.id]['kl_vc_conlai']=val1
        return res
    def _amount_alls(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        val1=val=vatra=dukien=0.0
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'kl_vc_conlai': 0.0,
                'kl_dangvc_dukien': 0.0,               
            } 
            
            kehoach_name=order.kehoach_id.name
            is_parent=order.kehoach_id.parent_id
            ke_hoach_cha=order.kehoach_id.kehoach_cha.id
            sale_order_line=order.sale_order_line.id
            product_id=order.product_id.id
            trung_chuyen=order.kehoach_id.trung_chuyen
            chang_khvc=order.kehoach_id.chang_khvc
            if  trung_chuyen==False or (ke_hoach_cha and chang_khvc=='chang_1'): 
                if sale_order_line and  product_id: 
                    valtra=0            
                    query="""select coalesce(sum(mv.product_qty),0) as soluong 
                    from stock_move mv
                    left join stock_picking pk on pk.id=mv.picking_id
                    where mv.state='done'  and coalesce(pk.mistake_delivery,False)=False
                    and mv.chitiet_kh= """+str(order.id)+""" and  pk.type='out' and
                    mv.sale_line_id= """+str(sale_order_line)+""" and  mv.product_id= """+str(product_id)
                   
                    cr.execute(query)
                    for tong in cr.dictfetchall(): 
                        val = tong['soluong']
                    query_tra="""select coalesce(sum(mv.product_qty),0) as soluong 
                    from stock_move mv
                    left join stock_picking pk on pk.id=mv.picking_id
                    where mv.state='done'  and coalesce(pk.mistake_delivery,False)=False   
                    and mv.chitiet_kh= """+str(order.id)+""" and  pk.type='in' and
                    mv.sale_line_id= """+str(sale_order_line)+""" and  mv.product_id= """+str(product_id)
                   
                    cr.execute(query_tra)
                    for tong in cr.dictfetchall(): 
                        valtra = tong['soluong']
                    dukien=val-valtra
            #res[order.id]['kl_dangvc_dukien']=dukien
            if ke_hoach_cha and chang_khvc=='chang_2': 
                    val=valtra=0              
                    for lines in order.kehoach_id.kehoach_cha.chitiet_kh:
                        sale_line_id=lines.sale_order_line.id                        
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                      where kh.chang_khvc='chang_1' and ct.cha_id=  """+str(lines.id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            if sale_order_line==sale_line_id:
                                query_in="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv 
                               
                                left join stock_picking pk on pk.id=mv.picking_id
                                 where mv.state='done' and coalesce(pk.mistake_delivery,False)=False
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='out' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_in)
                                for tong in cr.dictfetchall(): 
                                    val += tong['soluong']
                                query_tra="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv                     
                                left join stock_picking pk on pk.id=mv.picking_id
                                where mv.state='done' and pk.type='out'  and coalesce(pk.mistake_delivery,False)=False   
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='in' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_tra)
                                for tong in cr.dictfetchall(): 
                                    valtra += tong['soluong']
                        dukien=val-valtra
            #res[order.id]['kl_dangvc_dukien']=dukien
            if is_parent:
                val=valtra=0
                for lines in order.kehoach_id.chitiet_kh:
                        sale_line_id=lines.sale_order_line.id
                        line_id=lines.id
                        
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                      where kh.chang_khvc='chang_1' and ct.cha_id=  """+str(line_id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            if sale_order_line==sale_line_id:
                                query_in="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv 
                               
                                left join stock_picking pk on pk.id=mv.picking_id
                                 where mv.state='done' and coalesce(pk.mistake_delivery,False)=False
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='out' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_in)
                                for tong in cr.dictfetchall(): 
                                    val += tong['soluong']
                                query_tra="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv                     
                                left join stock_picking pk on pk.id=mv.picking_id
                                where mv.state='done' and pk.type='out'  and coalesce(pk.mistake_delivery,False)=False   
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='in' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_tra)
                                for tong in cr.dictfetchall(): 
                                    valtra += tong['soluong']
                        dukien=val-valtra
            
            res[order.id]['kl_dangvc_dukien']=dukien
            val1=order.kl_vc_kehoach - dukien       
            res[order.id]['kl_vc_conlai']=val1
        return res
    def get_count_id(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=1
        tmp=''
        if context is None:
            context = {}        
        for data in self.browse(cr, uid, ids, context):
#             chang_khvc=data.kehoach_id.chang_khvc
#             if data.kehoach_id.parent_id:
#                 kh=data.kehoach_id.id
#                 
#                 for data_line in self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, kh, context).chitiet_kh:
#                     cha_id=data_line.id
#                     return_history=0
#                     if cha_id:
#                         cr.execute("""select coalesce(sum(ct.kl_dangvc_dukien),0) as kl_dangvc_dukien
#                                                 from  icsc_hopdong_vanchuyen_chitiet ct
#                                                 left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
#                                                 where kh.chang_khvc='chang_1' and ct.cha_id= """+str(cha_id)) 
#                         for item_dk in cr.dictfetchall():                             
#                             return_history +=  item_dk['kl_dangvc_dukien']
#                 cr.execute("""update icsc_hopdong_vanchuyen_chitiet set kl_dangvc_dukien= """+str(return_history)+""" where id = """+str(cha_id))
#             kehoach_cha=data.kehoach_id.kehoach_cha
#             if kehoach_cha and chang_khvc=='chang_2':
#                 kl_dangvc_dukien=data.cha_id.kl_dangvc_dukien
#                 cr.execute("""update icsc_hopdong_vanchuyen_chitiet set kl_dangvc_dukien= """+str(kl_dangvc_dukien)+""" where id = """+str(data.id))   
#                      
            if data.cha_id:
                tmp=''
                cha_id=data.cha_id.chi_tiet_lxh
                if cha_id:
                    tmp +=cha_id
            else: 
                tmp=''
                tmp +=  data.kehoach_id.name   
                if data.kehoach_id: 
                    query="""select count(*) as count from icsc_hopdong_vanchuyen_chitiet where kehoach_id= """+str(data.kehoach_id.id)+""" and id <= """+str(data.id)        
                    cr.execute(query)
                    for item in cr.dictfetchall():
                        count =item['count']
                tmp +=' - '+str(count)+''
            res[data.id]=tmp
            cr.execute("""update icsc_hopdong_vanchuyen_chitiet set chi_tiet_lxh= '"""+str(tmp)+"""' where id= """+str(data.id))
        return res
    
    def _get_conlai(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=0
        
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            count=data.kl_can_vanchuyen-data.kl_vc_kehoach
            
            res[data.id]=count
        return res
    def _get_phieuvc_all(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=0
        
        if context is None:
            context = {}
        for order in self.browse(cr, uid, ids, context):
            kehoach_name=order.kehoach_id.name
            is_parent=order.kehoach_id.parent_id
            ke_hoach_cha=order.kehoach_id.kehoach_cha.id
            sale_order_line=order.sale_order_line.id
            product_id=order.product_id.id
            trung_chuyen=order.kehoach_id.trung_chuyen
            chang_khvc=order.kehoach_id.chang_khvc
            if  trung_chuyen==False or (ke_hoach_cha and chang_khvc=='chang_1'): 
                
                valtra=0            
                query="""SELECT  coalesce( sum(kl_vc),0) as khoiluong
                FROM icsc_phieu_vanchuyen_chitiet ct
                left join icsc_hopdong_vanchuyen_chitiet hd on ct.name=hd.id
                left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=pvc.kehoach_vanchuyen
                where ((coalesce(kh.kehoach_cha,0) !=0 and kh.chang_khvc!='chang_2') or coalesce(kh.trung_chuyen,False)=False ) and  
                ct.state not in ('cancel') and ct.name= """+str(order.id)
                cr.execute(query)
                for tong in cr.dictfetchall(): 
                    val = tong['khoiluong']                    
                dukien=val 
                  
            if  (ke_hoach_cha and chang_khvc=='chang_2'): 
                val=0   
                #lay danh sach id cua chang 1
                cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                where kh.chang_khvc='chang_1' and kh.kehoach_cha=  """+str(ke_hoach_cha))
                for item_con in cr.dictfetchall():
                    con_id=item_con['id']       
                    query="""SELECT  coalesce( sum(kl_vc),0) as khoiluong
                    FROM icsc_phieu_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_chitiet hd on ct.name=hd.id
                    left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=pvc.kehoach_vanchuyen
                    where kh.chang_khvc='chang_2' and  
                    ct.state not in ('cancel') and ct.name = """+str(con_id)
                    cr.execute(query)
                    for tong in cr.dictfetchall(): 
                        val += tong['khoiluong']                    
                dukien=val         
            if is_parent:
                val=valtra=0
                for lines in order.kehoach_id.chitiet_kh:                        
                        line_id=lines.id                        
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                      where kh.chang_khvc='chang_1' and ct.cha_id=  """+str(line_id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            query="""SELECT  coalesce( sum(kl_vc),0) as khoiluong
                                FROM icsc_phieu_vanchuyen_chitiet ct
                                left join icsc_hopdong_vanchuyen_chitiet hd on ct.name=hd.id
                                left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id
                                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=pvc.kehoach_vanchuyen
                                where kh.chang_khvc!='chang_2' and 
                                 ct.state not in ('cancel') and ct.name= """+str(con_id)
                            cr.execute(query)
                            for tong in cr.dictfetchall(): 
                                val += tong['khoiluong'] 
                dukien=val           
            res[order.id]=dukien
        return res
    def _get_dangvc(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=0
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            kehoach_name=data.kehoach_id.name
            is_parent=data.kehoach_id.parent_id
            ke_hoach_cha=data.kehoach_id.kehoach_cha.id
            sale_order_line=data.sale_order_line.id
            product_id=data.product_id.id
            trung_chuyen=data.kehoach_id.trung_chuyen
            if  trung_chuyen==False or is_parent==True: 
                if sale_order_line and  product_id:             
                    query="""select coalesce(sum(product_qty),0) as soluong 
                    from stock_move where state='done' 
                    and chitiet_kh= """+str(data.id)+""" and 
                    sale_line_id= """+str(sale_order_line)+""" and  product_id= """+str(product_id)
                   
                    cr.execute(query)
                    for tong in cr.dictfetchall(): 
                        count = tong['soluong']
            if ke_hoach_cha:
                for lines in data.kehoach_id.kehoach_cha.chitiet_kh:
                    sale_line_id=lines.sale_order_line.id
                    if sale_order_line==sale_line_id:
                        query="""select coalesce(sum(product_qty),0) as soluong 
                        from stock_move where state='done' 
                        and chitiet_kh= """+str(lines.id)+""" and 
                        sale_line_id= """+str(sale_line_id)+""" and  product_id= """+str(product_id)
                       
                        cr.execute(query)
                        for tong in cr.dictfetchall(): 
                            count = tong['soluong']
                        
            res[data.id]=count
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context): 
                     
            kh=data.picking_id.kehoach_vanchuyen_id    
              
            if kh:
                for item in kh.chitiet_kh:                    
                    cha=item.cha_id         
                    if cha:         
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                          where kh.chang_khvc='chang_2' and ct.cha_id= """+str(cha.id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            result[con_id] = True
                        result[cha.id] = True
                    result[item.id] = True
                    
        return result.keys()
    def _get_picking(self, cr, uid, ids, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context): 
                     
            kh=data.kehoach_vanchuyen_id    
            
            if kh:
                for item in kh.chitiet_kh:
                    
                    
                    cha=item.cha_id                  
                    if cha:                    
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                          where kh.chang_khvc='chang_2' and ct.cha_id= """+str(cha.id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            result[con_id] = True
                        result[cha.id] = True
                    result[item.id] = True
        return result.keys()
    def name_get(self, cr, uid, ids, context=None):
        ct_ds=self.pool.get('icsc.phieu.vanchuyen.chitiet.duongsat')
        pvc_ds=self.pool.get('icsc.phieu.vanchuyen.duongsat')
        kehoach_obj=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','product_id','kl_vc_kehoach','kl_vc_conlai','phieu_id','kl_dangvc_all'], context=context)
        res = []
        for record in reads:        
            # lay ke hoach van chuyen
           
            # end
            dvt=''
            product_id = record['product_id'][0]
            if product_id:
                dvt_obj=self.pool.get('product.product').browse(cr, uid, product_id, context)
                dvt=dvt_obj.uom_id.name
#             sum=0
#             pvc_ds_id=ct_ds.search(cr, uid, [('name', '=', record['id'])])
#             ct_ds_obj=ct_ds.browse(cr, uid, pvc_ds_id, context)
#             for ct in ct_ds_obj:
#                 sum+=ct.kl_vc
            # record['kl_vc_conlai'] 
            kl_vc_kehoach=str(record['kl_vc_kehoach'] - record['kl_dangvc_all'])
            name = record['name']
            if record['product_id'] and kl_vc_kehoach:
                name = name+'/'+record['product_id'][1]+' / ['+kl_vc_kehoach+' '+dvt+']'
            if record['product_id'] and kl_vc_kehoach==False:
                name = name+'/'+record['product_id'][1]
            if not record['product_id'] and kl_vc_kehoach:
                name= name + '['+kl_vc_kehoach+kl_vc_kehoach+' '+dvt+']'
            if not record['product_id'] and not kl_vc_kehoach:
                name=name
            
            res.append((record['id'], name))
        return res
    
    #def name_get(self, cr, uid, ids, context=None):
    #    if not ids:
    #        return []       
    #    return [(r['id'], '[%s]-%s-%s' % (r['name'],r['product_id'],r['kl_vc_kehoach'])) for r in self.read(cr, uid, ids, [ 'name','product_id','kl_vc_kehoach'], context, load='_classic_write')]
    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if name:
            ids = self.search(cr, user, [('product_id','=',name)]+ args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, user, [('chi_tiet_lxh','=',name)]+ args, limit=limit, context=context)
            if not ids:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching products, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                ids = set()
                ids.update(self.search(cr, user, args + [('product_id',operator,name)], limit=limit, context=context))
                if not limit or len(ids) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    ids.update(self.search(cr, user, args + [('chi_tiet_lxh',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
                    # vivek
                    # Purpose  : To filter the product by using part_number
                    #ids.update(self.search(cr, user, args + [('part_number',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
                    #End
                ids = list(ids)
            #if not ids:
                #ptrn = re.compile('(\[(.*?)\])')
                #res = ptrn.search(name)
                #if res:
                    #ids = self.search(cr, user, [('chi_tiet_lxh','=', res.group(2))] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)
        return result
    def _get_order_ct(self, cr, uid, ids, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context):                      
            kh=data.name.id   
            kh_pvc=data.phieu_id.kehoach_vanchuyen
            #lay chang khvc
            chang_khvc=kh_pvc.chang_khvc
            if chang_khvc!='chang_2':
                if kh:               
                    result[kh] = True
                    cha_id=data.name.cha_id                        
                    if cha_id:        
                        result[cha_id.id] = True
            # kiem tra KHVC/PVC la chang 2
            kh_pvc=data.phieu_id.kehoach_vanchuyen
            if kh_pvc:
                #lay chang khvc
                chang_khvc=kh_pvc.chang_khvc
                # neu chang 2
                if chang_khvc=='chang_2':                    
                    # neu la chang 2 -->lay tat ca pvc chang 2 la con cua cha
                    # lay ct cua moi dong                   
                    # xac dinh cha cua dong
                    cha=data.name.cha_id  
                    cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                          where kh.chang_khvc='chang_2' and ct.cha_id= """+str(cha.id))
                    for item_con in cr.dictfetchall():
                        con_id=item_con['id']
                        result[con_id] = True
                    
        return result.keys()
    def _get_dangvanchuyen(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        val1=val=vatra=dukien=0.0
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):            
            kehoach_name=order.kehoach_id.name
            is_parent=order.kehoach_id.parent_id
            ke_hoach_cha=order.kehoach_id.kehoach_cha.id
            sale_order_line=order.sale_order_line.id
            product_id=order.product_id.id
            trung_chuyen=order.kehoach_id.trung_chuyen
            chang_khvc=order.kehoach_id.chang_khvc
            if  trung_chuyen==False or (ke_hoach_cha and chang_khvc=='chang_1'): 
                if sale_order_line and  product_id: 
                    valtra=0            
                    query="""select coalesce(sum(mv.product_qty),0) as soluong 
                    from stock_move mv
                    left join stock_picking pk on pk.id=mv.picking_id
                    where mv.state='done'  and coalesce(pk.mistake_delivery,False)=False
                    and mv.chitiet_kh= """+str(order.id)+""" and  pk.type='out' and
                    mv.sale_line_id= """+str(sale_order_line)+""" and  mv.product_id= """+str(product_id)
                   
                    cr.execute(query)
                    for tong in cr.dictfetchall(): 
                        val = tong['soluong']
                    query_tra="""select coalesce(sum(mv.product_qty),0) as soluong 
                    from stock_move mv
                    left join stock_picking pk on pk.id=mv.picking_id
                    where mv.state='done'  and coalesce(pk.mistake_delivery,False)=False   
                    and mv.chitiet_kh= """+str(order.id)+""" and  pk.type='in' and
                    mv.sale_line_id= """+str(sale_order_line)+""" and  mv.product_id= """+str(product_id)
                   
                    cr.execute(query_tra)
                    for tong in cr.dictfetchall(): 
                        valtra = tong['soluong']
                    dukien=val-valtra
            #res[order.id]['kl_dangvc_dukien']=dukien
            if ke_hoach_cha and chang_khvc=='chang_2': 
                    val=valtra=0              
                    for lines in order.kehoach_id.kehoach_cha.chitiet_kh:
                        sale_line_id=lines.sale_order_line.id                        
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                      where kh.chang_khvc='chang_1' and ct.cha_id=  """+str(lines.id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            if sale_order_line==sale_line_id:
                                query_in="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv 
                               
                                left join stock_picking pk on pk.id=mv.picking_id
                                 where mv.state='done' and coalesce(pk.mistake_delivery,False)=False
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='out' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_in)
                                for tong in cr.dictfetchall(): 
                                    val += tong['soluong']
                                query_tra="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv                     
                                left join stock_picking pk on pk.id=mv.picking_id
                                where mv.state='done' and pk.type='out'  and coalesce(pk.mistake_delivery,False)=False   
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='in' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_tra)
                                for tong in cr.dictfetchall(): 
                                    valtra += tong['soluong']
                        dukien=val-valtra
            #res[order.id]['kl_dangvc_dukien']=dukien
            if is_parent:
                val=valtra=0
                for lines in order.kehoach_id.chitiet_kh:
                        sale_line_id=lines.sale_order_line.id
                        line_id=lines.id
                        
                        cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                    left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                      where kh.chang_khvc='chang_1' and ct.cha_id=  """+str(line_id))
                        for item_con in cr.dictfetchall():
                            con_id=item_con['id']
                            if sale_order_line==sale_line_id:
                                query_in="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv 
                               
                                left join stock_picking pk on pk.id=mv.picking_id
                                 where mv.state='done' and coalesce(pk.mistake_delivery,False)=False
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='out' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_in)
                                for tong in cr.dictfetchall(): 
                                    val += tong['soluong']
                                query_tra="""select coalesce(sum(mv.product_qty),0) as soluong 
                                from stock_move  mv                     
                                left join stock_picking pk on pk.id=mv.picking_id
                                where mv.state='done' and pk.type='out'  and coalesce(pk.mistake_delivery,False)=False   
                                and mv.chitiet_kh= """+str(con_id)+""" and  pk.type='in' and
                                mv.sale_line_id= """+str(sale_line_id)+""" and  mv.product_id= """+str(product_id)
                               
                                cr.execute(query_tra)
                                for tong in cr.dictfetchall(): 
                                    valtra += tong['soluong']
                        dukien=val-valtra
            
            res[order.id]=order.kl_vc_kehoach - dukien
            
        return res
    _columns = {
           'kl_dangvc_all': fields.function(_get_phieuvc_all,type='float', string='KL đã đưa vào PVC'),
         'name': fields.function(get_count_id, type='char', string='STT'),     
          'dia_chi_giao':fields.many2one('res.partner', 'Địa chỉ giao hàng',domain="[('parent_other_id','=',parent.khach_hang)]",select=True),
         'chi_tiet_lxh': fields.char('Chi tiết LXH'),
         'product_id': fields.many2one('product.product', 'Sản phẩm', ondelete='cascade',select=True),        
         'kl_vc_dukien': fields.float('KL vận chuyển dự kiến ban đầu'),
        'kl_vc_kehoach': fields.float('KL KH',),
         #'kl_vc_conlai': fields.function(_get_conlai,type='float', string='KL vận chuyển dự kiến còn lại'),
        'kl_dangvc': fields.function(_get_dangvanchuyen,type='float', string='KL đang vận chuyển'),
        'kl_can_vanchuyen': fields.float('KL cần vận chuyển'),
        'kehoach_id': fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch', ondelete='cascade',select=True),  
        'sale_order_line': fields.many2one('sale.order.line', 'Chi tiết LXH', ondelete='cascade'),           
#         'kl_vc_conlai': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='KL vận chuyển dự kiến còn lại',
#             store={
#                 'icsc.hopdong.vanchuyen.chitiet': (lambda self, cr, uid, ids, c={}: ids, ['kl_vc_kehoach','kl_vc_dukien','kl_can_vanchuyen','kehoach_id','sale_order_line','product_id','cha_id'], 10),
#                 'stock.move': (_get_order, ['product_qty','product_id','state'], 10),
#                 'stock.picking': (_get_picking, ['mistake_delivery','kehoach_vanchuyen_id','state'], 10),
#             }, multi="sums",help="KL còn lại"),
#          'kl_dangvc_dukien': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='KL đang vận chuyển',
#             store={
#                 'icsc.hopdong.vanchuyen.chitiet': (lambda self, cr, uid, ids, c={}: ids, ['kl_vc_kehoach','kl_vc_dukien','kl_can_vanchuyen','kehoach_id','sale_order_line','product_id','cha_id'], 10),
#                 'stock.move': (_get_order, ['product_qty','product_id','state'], 10),
#                  'stock.picking': (_get_picking, ['mistake_delivery','kehoach_vanchuyen_id','state'], 10),
#             }, multi="sums",help="KL đang vận chuyển"),
         'kl_vc_conlai': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='KL vận chuyển dự kiến còn lại',
            store={
                'icsc.hopdong.vanchuyen.chitiet': (lambda self, cr, uid, ids, c={}: ids, ['kl_vc_kehoach','kl_vc_dukien','kl_can_vanchuyen','kehoach_id','sale_order_line','product_id','cha_id'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order_ct, ['kl_vc','product_id','state','gia_chua_thues','name','kl_vc_conlai','kl_dangvc_dukien'], 10),
                'icsc.phieu.vanchuyen.chitiet.duongsat': (_get_order_ct, ['kl_vc','product_id','state','gia_chua_thues','name','kl_vc_conlai','kl_dangvc_dukien'], 10),
                
            }, multi="sums",help="KL còn lại"),
         'kl_dangvc_dukien': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='KL đang vận chuyển',
            store={
                'icsc.hopdong.vanchuyen.chitiet': (lambda self, cr, uid, ids, c={}: ids, ['kl_vc_kehoach','kl_vc_dukien','kl_can_vanchuyen','kehoach_id','sale_order_line','product_id','cha_id'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order_ct, ['kl_vc','product_id','state','gia_chua_thues','name','kl_vc_conlai','kl_dangvc_dukien'], 10),
                'icsc.phieu.vanchuyen.chitiet.duongsat': (_get_order_ct, ['kl_vc','product_id','state','gia_chua_thues','name','kl_vc_conlai','kl_dangvc_dukien'], 10),
                
            }, multi="sums",help="KL đang vận chuyển"),
         'cha_id': fields.many2one('icsc.hopdong.vanchuyen.chitiet', 'STT', ondelete='cascade'),
    }
    def create(self, cr, uid, vals, context=None):
        if context is None: context = {}  
        lxh_chitiet_pool=self.pool.get('sale.order.line')
        ctvc_chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        sale_order_line=vals.get('sale_order_line') 
        project_id=False
        if sale_order_line: 
            ct_data=lxh_chitiet_pool.browse(cr, uid, sale_order_line)
            kl=ct_data.product_uom_qty
            kl_vc= vals.get('kl_vc_kehoach')
            khvc_id= vals.get('kehoach_id')
            kehoach_diadiem=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
            kh_obj=kehoach_diadiem.browse(cr, uid, khvc_id)
            ngoai_le = kh_obj.ngoai_le
            trungchuyen=kh_obj.trung_chuyen
            parent_id=kh_obj.parent_id
            chang_khvc=kh_obj.chang_khvc
            kehoach_cha=kh_obj.kehoach_cha
            if (trungchuyen==True and parent_id==True) or (trungchuyen==False and parent_id==False):
                sum_total=0
                cr.execute("""select coalesce(sum(ct.kl_vc_kehoach),0) as kl_vc 
                    from icsc_hopdong_vanchuyen_chitiet ct
                    inner join icsc_hopdong_vanchuyen_giacuoc_kehoach vc on vc.id=ct.kehoach_id
                    where coalesce(vc.ngoai_le,False)=False and ((vc.trung_chuyen=True and vc.parent_id=True) 
                    or (coalesce(vc.trung_chuyen,False)=False))
                    and ct.sale_order_line=  """+str(sale_order_line))
                for line in cr.dictfetchall():
                    sum_total=line['kl_vc']
                if kl_vc:
                    sum_total +=kl_vc
                if kl<sum_total and not ngoai_le:
                    raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu KHVC lớn hơn Khối lượng trên chi tiết LXH. Vui lòng chọn LXH khác hoặc điều chỉnh lại khối lượng VC Kế hoạch."))
                else:
                    project_id = super(icsc_hopdong_vanchuyen_chitiet, self).create(cr, uid, vals, context)
            else:
                if (trungchuyen==True and kehoach_cha and chang_khvc=='chang_1'):
                    if chang_khvc=='chang_1':
                        return_history=0                        
                        cha_id=vals.get('cha_id')
                        if cha_id:
                            ctvc_data=ctvc_chitiet_pool.browse(cr, uid, cha_id)
                            klvc=ctvc_data.kl_vc_kehoach
                            cr.execute("""select coalesce(sum(ct.kl_vc_kehoach),0) as kl_vc_kehoach
                                        from  icsc_hopdong_vanchuyen_chitiet ct
                                        inner join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                                        where kh.chang_khvc='chang_1' and ct.cha_id= """+str(cha_id)) 
                            for item in cr.dictfetchall():                             
                                return_history +=  item['kl_vc_kehoach']
                            if kl_vc:
                                return_history +=kl_vc
                            if klvc<return_history:
                                raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu KHVC con chặng 1 phải <= tổng khối lượng kế hoạch/LXH trên chi tiết KHVC cha tương ứng."))
                project_id = super(icsc_hopdong_vanchuyen_chitiet, self).create(cr, uid, vals, context)
        return project_id
    def write(self, cr, uid, ids, vals, context=None):
        # if alias_model has been changed, update alias_model_id accordingly
        ctvc_chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        if vals.get('kl_vc_kehoach'):
            kl_vc=vals.get('kl_vc_kehoach')
            for data in self.browse(cr, uid, ids, context):
                kl_old=data.kl_vc_kehoach
                if kl_old==kl_vc:
                    return True
                trungchuyen=data.kehoach_id.trung_chuyen
                parent_id=data.kehoach_id.parent_id
                chang_khvc=data.kehoach_id.chang_khvc
                kehoach_cha=data.kehoach_id.kehoach_cha
                ngoai_le = data.kehoach_id.ngoai_le
                if (trungchuyen==True and kehoach_cha and chang_khvc=='chang_1'):
                    if chang_khvc=='chang_1':
                        return_history=0                        
                        cha_id=data.cha_id
                        if cha_id:
                            cha=cha_id.id
                            ctvc_data=ctvc_chitiet_pool.browse(cr, uid, cha)
                            klvc=ctvc_data.kl_vc_kehoach
                            cr.execute("""select coalesce(sum(ct.kl_vc_kehoach),0) as kl_vc_kehoach
                                        from  icsc_hopdong_vanchuyen_chitiet ct
                                        inner join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                                        where kh.chang_khvc='chang_1' and ct.cha_id= """+str(cha)+""" and ct.id != """+str(data.id)) 
                            for item in cr.dictfetchall():                             
                                return_history +=  item['kl_vc_kehoach']
                            if kl_vc:
                                return_history +=kl_vc
                            chenhlech=klvc-kl_vc
                            
                            if klvc<return_history and chenhlech!=0:
                                raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu KHVC con chặng 1 phải <= tổng khối lượng kế hoạch/LXH trên chi tiết KHVC cha tương ứng."))
                if (trungchuyen==True and kehoach_cha and chang_khvc=='chang_2'):
                    if chang_khvc=='chang_2' and parent_id==False :
                        sale_order_line=data.sale_order_line.id
                        if sale_order_line:
                            kl=data.sale_order_line.product_uom_qty
                        sum_total=0
                        if data.cha_id:
                            cha=data.cha_id
                            sum_total=cha.kl_vc_kehoach
                        if kl_vc:
                            sum_total +=kl_vc
                        chenhlech=kl-kl_vc
                        if kl!=sum_total and chenhlech!=0:
                            raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu KHVC chặng 2 luôn phải bằng Khối lượng trên chi tiết KHVC cha. Vui lòng điều chỉnh lại khối lượng VC Kế hoạch."))   
                            
                if (trungchuyen==True and parent_id==True) or trungchuyen==False:
                    sale_order_line=data.sale_order_line.id
                    if sale_order_line:
                        kl=data.sale_order_line.product_uom_qty
                    sum_total=0
                    cr.execute("""select coalesce(sum(ct.kl_vc_kehoach),0) as kl_vc 
                    from icsc_hopdong_vanchuyen_chitiet ct
                    inner join icsc_hopdong_vanchuyen_giacuoc_kehoach vc on vc.id=ct.kehoach_id
                    where coalesce(vc.ngoai_le,False) = False and ((vc.trung_chuyen=True and vc.parent_id=True) 
                    or (coalesce(vc.trung_chuyen,False)=False))   
                    and vc.state!='cancel'  and ct.sale_order_line=  """+str(sale_order_line)+""" and ct.id!= """+str(data.id))
                    for line in cr.dictfetchall():
                        sum_total=line['kl_vc']
                    if kl_vc:
                        sum_total +=kl_vc
                    chenhlech=kl-kl_vc
                    if kl<sum_total and chenhlech!=0 and not ngoai_le:
                        raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu KHVC lớn hơn Khối lượng trên chi tiết LXH. Vui lòng chọn LXH khác hoặc điều chỉnh lại khối lượng VC Kế hoạch."))   
                    #xet khvc con chang 1
                    for data in self.browse(cr, uid, ids, context):
                        return_history=0
                        kl_old=data.kl_vc_kehoach
                        ctvc_data=ctvc_chitiet_pool.browse(cr, uid, data.id)
                        klvc=ctvc_data.kl_vc_kehoach
                        cr.execute("""select coalesce(sum(ct.kl_vc_kehoach),0) as kl_vc_kehoach
                                    from  icsc_hopdong_vanchuyen_chitiet ct
                                    inner join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                                    where kh.chang_khvc='chang_1' and ct.cha_id= """+str(data.id)+""" and ct.id != """+str(data.id)) 
                        for item in cr.dictfetchall():                             
                            return_history +=  item['kl_vc_kehoach']                        
                        if kl_vc<return_history:
                            raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu KHVC con chặng 1 phải <= tổng khối lượng kế hoạch/LXH trên chi tiết KHVC cha tương ứng."))   
                    
        return super(icsc_hopdong_vanchuyen_chitiet, self).write(cr, uid, ids, vals, context=context)
    def button_update(self, cr, uid, ids, context=None):
        result={}
        if context is None:
            context = {}

        for vc in self.browse(cr, uid, ids) :           
            product_id1=vc.product_id1.id      
            name=vc.product_id1.name
            product_uom_qty=vc.product_uom_qty
            price_unit=vc.price_unit
            date_order=vc.date_order
            product_uom1=vc.product_uom1.id   
            tax_id=vc.tax_id.id       
            move_ids = self.pool.get('purchase.order.line').create(cr, uid, {
                        'date_planned': date_order,
                        'product_id': product_id1,
                        'product_qty': product_uom_qty,
                        'product_uom': product_uom1,
                        'price_unit': price_unit,     
                        'name': name,       
                        'order_id': vc.id,                        
                    }, context=context)   
        self.merge_order_line(cr, uid, ids[0], context=context)
        self.write(cr, uid, [ids[0]], {'product_id1' : None, 'product_uom_qty' :1, 'product_uom1': None, 'price_unit': 0,'product_color':''})
        return True  
    
icsc_hopdong_vanchuyen_chitiet()
#_TASK_STATE = [ ('thongthuong', 'Thông thường'),  
# ('noibo', 'Nội bộ'),    ]
class icsc_phieu_vanchuyen(osv.osv):
    _description="Phieu van chuyen"
    _name = 'icsc.phieu.vanchuyen'
    _inherit = ['mail.thread']
    _order= 'id desc'    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {               
                'amount_total': 0.0,
                'amount_thanhtien': 0.0,
                'amount_denxa': 0.0,
                'amount_da_vc':0.0,
                'amount_con_lai':0.0,
                'banggia_id':False,   
                'nhom_bangia':False ,
                'dem_phieu':0    
            }
            val=val1 =val2= val3=0.0        
            for line in order.chitiet_vc:
                val1 += line.thanh_tien * line.kl_vc
                val +=order.chiphi_denxa * line.kl_vc
                if order.tung_phan:
                    for item in line.history_ids:
                        val2 +=item.kl_vc * item.thanh_tien
                else:
                    val2=val1
            val3=val1-val2
            res[order.id]['amount_thanhtien'] = val1            
            res[order.id]['amount_da_vc'] = val2    
            res[order.id]['amount_denxa'] = val 
            res[order.id]['amount_total'] = val1
            res[order.id]['amount_con_lai'] = val3
            res[order.id]['dem_phieu'] = 1
            # Tim bang giá
            banggia_id=False 
            nhom_ids=False                                  
            cuoc_tu_diem=order.cuoc_tu_diem.id
            cuoc_den_diem=order.cuoc_den_diem.id                       
            for gia in order.hopdong_vanchuyen.chitiet_banggia:
                tu_diem=gia.tu_diem.id
                den_diem=gia.den_diem.id                    
                if tu_diem==cuoc_tu_diem and den_diem==cuoc_den_diem:                        
                    banggia_id=gia.banggia_id.id  
                    nhom_id=gia.banggia_id.nhom_banggia
                    if nhom_id:
                        nhom_ids=nhom_id.id
            if banggia_id==False or nhom_ids==False:
                for gia in order.hopdong_vanchuyen.chitiet_banggia_hethan:
                    tu_diem=gia.tu_diem.id
                    den_diem=gia.den_diem.id                    
                    if tu_diem==cuoc_tu_diem and den_diem==cuoc_den_diem:  
                        if banggia_id==False:                    
                            banggia_id=gia.banggia_id.id  
                        nhom_id=gia.banggia_id.nhom_banggia
                        if nhom_ids==False and nhom_id:
                            nhom_ids=nhom_id.id
            res[order.id]['nhom_bangia'] = nhom_ids
            res[order.id]['banggia_id'] = banggia_id 
        return res
    def _kehoach_cha(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = False
            if task.kehoach_vanchuyen.kehoach_cha:               
                res[task.id] = task.kehoach_vanchuyen.kehoach_cha.id
        return res
    def _tongkhoiluong(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):          
            kq=0
            for line in task.chitiet_vc:
                kq+= line.kl_vc
            res[task.id] = kq
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.phieu.vanchuyen.chitiet').browse(cr, uid, ids, context=context):
            result[line.phieu_id.id] = True
        return result.keys()
    def _get_orders(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').browse(cr, uid, ids, context=context):
            result[line.phieu_id.id] = True
        return result.keys()
    def _check_pxk_pvc(self, cursor, user, ids, context=None):
        for pricelist_version in self.browse(cursor, user, ids, context=context):
            phieu_xuat=False
            congty_vc=False
            if pricelist_version.phieu_xuat:
                phieu_xuat=pricelist_version.phieu_xuat.id
            if pricelist_version.congty_vc:
                congty_vc=pricelist_version.congty_vc.id
            if phieu_xuat and congty_vc:
                state=pricelist_version.state
                if state!='cancel':
                    query =""" select id from icsc_phieu_vanchuyen
                                where phieu_xuat=%s and congty_vc=%s 
                                and id !=%s and state !='cancel'
                            """%(phieu_xuat,congty_vc,pricelist_version.id)
                    cursor.execute(query)
                    if cursor.fetchall():
                        return False           
        return True
    def _check_pvc_trung(self, cursor, user, ids, context=None):
        for data in self.browse(cursor, user, ids, context=context):            
            if data.phuongtien_vc !='duongsat_thongthuong':
                query = """ select left(name,5) as name,id,ROW_NUMBER() over (order by id) as STT
                            from icsc_phieu_vanchuyen where name = '"""+ str(data.name) +"""'
                            and phuongtien_vc !='duongsat_thongthuong' 
                            and id !=""" +str(data.id)+ """
                            order by id
                        """ 
                cursor.execute(query)            
                if cursor.fetchall():
                    return False           
        return True
    def _update_name(self, cr, uid, ids, name, args, context=None):
        res = {}        
        # kq=False   
        # for sale in self.browse(cr, uid, ids, context=context): 
        #     dem = 1
        #     query = """ select left(name,5) as name,id,ROW_NUMBER() over (order by id) as STT
        #                 from icsc_phieu_vanchuyen where name = '"""+ str(sale.name) +"""'
        #                 and phuongtien_vc !='duongsat_thongthuong'
        #                 order by id
        #             """ 
        #     cr.execute(query)
        #     for item in cr.dictfetchall():
        #         sale_id = item['id']
        #         stt = item['stt']
        #         if stt > 1:
        #             tenmoi =self.pool.get('sequence.custormize.vanchuyen').get_name(cr, uid, 'icsc.phieu.vanchuyen', 'icsc_phieu_vanchuyen','')
        #             kq = self.write(cr,uid,sale_id,{
        #                                        'name':tenmoi,
        #                                        })
        #             dem += 1
        #     res[sale.id] = kq
        return res
    
    _columns = {
       'auto_update_name':  fields.function(_update_name, type='boolean', string='Tự động cập nhập tên trùng'),
       'name': fields.char('Số phiếu', size=500,
             track_visibility='onchange',states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]} )  ,
     
       'hopdong_vanchuyen': fields.many2one('icsc.hopdong.vanchuyen','Hợp đồng vận chuyển', track_visibility='onchange',states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, required=True,select=True)  , 
       'kehoach_vanchuyen': fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'KHVC',
                                            domain="[('so_khvc','=',hopdong_vanchuyen),('sale_id','=',sale_id)]" , 
                                            track_visibility='onchange'
                                            ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, select=True),
       'giam_sat_kho': fields.related('kehoach_vanchuyen','giam_sat_kho',relation='icsc.giamsatkho',
                                       string= 'Giám sát kho', stored=True, type="many2one"
                                       ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}), 
       'loai_phieu': fields.selection([
            ('thongthuong', 'VAT'),  
            ('noibo', 'Nội bộ'),           
           ], 'Loại phiếu', 
            track_visibility='onchange'
            ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},), 
        'loai_trungchuyen': fields.selection([                
            ('thongthuong', 'Thông thường'),  
            ('noibo', 'Nội bộ'),      
           ], 'Loại trung chuyển', track_visibility='onchange'
           ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},), 
       'kehoach_cha': fields.function(_kehoach_cha, string='Kế hoạch vận chuyển cha',type="many2one",relation="icsc.hopdong.vanchuyen.giacuoc.kehoach", track_visibility='onchange'),  
       'cha_id': fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển',select=True),
       'phieu_xuat': fields.many2one('stock.picking','PXK',domain="[('don_vi_vc','=',congty_vc),('type','=','out'),('state','=','done'),('mistake_delivery','=',False),('loai_lenh_vc','=','vanchuyen')]" , 
                                    track_visibility='onchange',states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True)  ,  
       'so_hoa_don': fields.many2one('account.invoice','Số hoá đơn', 
                                    track_visibility='onchange',select=True
                                    )  ,          
       'phuongtien_vc': fields.selection([               
            
            ('duongbo', 'Đường bộ'),          
            ('duongthuy', 'Đường thủy + Đường bộ'),   
             ('duongsat_chuyentuyen', 'Đường sắt + Đường bộ'),            
            
            ], 'Phương thức vận chuyển', 
            track_visibility='onchange', required=True,
            states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},),  
      'khach_hang': fields.many2one('res.partner', 'Vận chuyển cho khách hàng',
                                    domain=[('check','=',True),('customer','=',True)], track_visibility='onchange'
                                    ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True ),       
      'cuoc_tu_diem': fields.many2one('res.country.diadiem', 
                                      'Tính cước từ điểm',domain="[('van_chuyen','=',True)]" , 
                                      track_visibility='onchange'
                                      ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True),
      'cuoc_den_diem': fields.many2one('res.country.diadiem', 
                                       'Tính cước đến điểm', domain="[('van_chuyen','=',True)]" ,
                                       track_visibility='onchange'
                                       ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True ),
      'kiem_soat': fields.many2one('res.country.tramkiemsoat',
                                    'Trạm kiểm soát', track_visibility='onchange'
                                    ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True), 
      'state': fields.selection([
                ('draft', 'Chưa vận chuyển'),
                ('confirm', 'Đang VC'),
                ('du_dk', 'Đủ ĐK thanh toán'),
                ('done', 'Hoàn tất'),
                ('cancel', 'Đã hủy'),           
                ], 'Trạng thái', readonly=True, track_visibility='onchange'),             
       'congty_vc': fields.many2one('res.partner', 'Tên ĐVVC',
                                    domain=[('check','=',True),('supplier','=',True)], track_visibility='onchange'
                                    ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True),
       'dai_dien': fields.many2one('res.partner', 'Người đại diện',domain="['|',('parent_id','=',congty_vc),('parent_uyquyen_id','=',congty_vc),('check','=',True)]", track_visibility='onchange'
                                   ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True),
       'lai_xe': fields.many2one('res.partner', 'Lái xe',domain="['|',('parent_id','=',congty_vc),('parent_uyquyen_id','=',congty_vc),('check','=',True)]", track_visibility='onchange',select=True),
        'giayphep_laixe': fields.char('Giấy phép lái xe',size=500, track_visibility='onchange')  , 
       'bang_kiem_soat': fields.char('Bảng kiểm soát/Số toa',size=500
                                     ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, track_visibility='onchange',select=True)  , 
       'ga_den': fields.char('Ga đến',size=500, track_visibility='onchange'
                             ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True)  ,    
       'ngay_vc': fields.date('Ngày VC', track_visibility='onchange'
                              ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}, required=True,select=True)  ,    
       'chitiet_vc': fields.one2many('icsc.phieu.vanchuyen.chitiet', 'phieu_id','Chi tiết vận chuyển'
                                     ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True  ),
       'chitiet_vc_capnhat': fields.one2many('icsc.phieu.vanchuyen.chitiet.capnhat', 'phieu_id','Chi tiết vận chuyển',select=True  ),
       'donvi_nhanhang': fields.many2one('res.partner', 'Đơn vị nhận hàng',domain=[('check','=',True),('supplier','=',True)],
                                          track_visibility='onchange',states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True),
       'tinh_denxa': fields.boolean('Tính giá đến xã', track_visibility='onchange'
                                    ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True),
       'chiphi_denxa': fields.float('Chi phí vận chuyển đến xã', track_visibility='onchange'), 
#        'trung_chuyen': fields.boolean('Có trung chuyển', track_visibility='onchange'
#                                       ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True), 
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Thành tiền',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien','kl_dangvc_dukien','kl_vc_conlai','tung_phan','history_ids'], 10),
                 'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_orders, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),   
        'amount_thanhtien': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Chi phí cần vận chuyển',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien','kl_dangvc_dukien','kl_vc_conlai','tung_phan','history_ids'], 10),
              'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_orders, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),   
         'amount_denxa': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Chi phí vận chuyển đến xã',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien','kl_dangvc_dukien','kl_vc_conlai','tung_phan','history_ids'], 10),
                'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_orders, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),  
           'ghi_chu': fields.text('Ghi chú',track_visibility='onchange')  , 
           'sale_id': fields.many2one('sale.order', 'LXH', 
                                      ondelete='cascade', 
                                      track_visibility='onchange'
                                      ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},),
           'tung_phan': fields.boolean('Hoàn tất một phần', track_visibility='onchange'),
         'amount_da_vc': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng chi phí đã VC',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien','kl_dangvc_dukien','kl_vc_conlai','tung_phan','history_ids'], 10),
                 'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_orders, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
                 
           
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),   
        'amount_con_lai': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng chi phí VC còn lại',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien','kl_dangvc_dukien','kl_vc_conlai','tung_phan','history_ids'], 10),
                  'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_orders, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),  
         'dem_phieu': fields.function(_amount_all, type="integer", string='Số phiếu',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien','kl_dangvc_dukien','kl_vc_conlai','tung_phan','history_ids'], 10),
                  'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_orders, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),   
       'duavao_thanhtoan': fields.boolean('Đưa vào ĐNTT'
                                          ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},), 
        'duavao_vipham': fields.boolean('Đã tạo phiếu vi phạm VC'
                                        ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},), 
       'haiduong_id': fields.related('sale_id', 'haiduong_id', type='many2one', relation='sale.shop', store=True, string='Đơn vị thực hiện'),
       
       'dia_chi_giao': fields.related('kehoach_vanchuyen', 'den_diem', type='many2one', relation='res.partner', store=True, string='Địa chỉ giao hàng'),  
       'banggia_id': fields.function(_amount_all,  string='Bảng giá cước vận chuyển',type='many2one',
                                       relation='icsc.hopdong.vanchuyen.giacuoc',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['hopdong_vanchuyen','cuoc_tu_diem','cuoc_den_diem','kehoach_vanchuyen','tung_phan'], 10),
              
              
            },
            multi='all'),   
       'nhom_bangia': fields.function(_amount_all,  string='Nhóm bảng giá cước vận chuyển',type='many2one',
                                       relation='icsc.loai.giacuoc.vanchuyen',
            store={
                'icsc.phieu.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['hopdong_vanchuyen','cuoc_tu_diem','cuoc_den_diem','kehoach_vanchuyen','tung_phan'], 10),
              
              
            },
            multi='all'), 
     'chang_khvc': fields.related('kehoach_vanchuyen', 'chang_khvc', type='char',  store=True, string='Chặng VC'),
     'trung_chuyen': fields.related('kehoach_vanchuyen', 'trung_chuyen', type='boolean',  store=True, string='Trung chuyển'),
     
     'tong_kl': fields.function(_tongkhoiluong, string='Tổng khối lượng',type="float"),  
     'is_chang2':fields.boolean('Là KHVC chặng 2'),
     'is_not_pay': fields.boolean('Không được phép thanh toán'),
    }
    
    _constraints = [
        (_check_pxk_pvc, 'Phiếu xuất kho này đã lập Phiếu vận chuyển cho Nhà vận chuyển này rồi!',
            ['phieu_xuat', 'congty_vc']),
        (_check_pvc_trung, 'Số phiếu này đã tồn tại. Vui lòng nhập số phiếu khác!',
            ['name'])
    ]
    _defaults= {'state':'draft',
                 'duavao_vipham':False,
                 'duavao_thanhtoan':False,
                 'phuongtien_vc':'duongbo',
                 'loai_phieu':'thongthuong',
                 'loai_trungchuyen':'thongthuong'  ,
                 'ngay_vc':fields.date.context_today,
                 'is_chang2':False,
                 'is_not_pay': False,
                # 'name': lambda self, cr, uid, c: 
                  } 
    def create(self, cr, uid, vals, context=None):   
        phuongtien_vc=vals.get('phuongtien_vc') 
        vanchuyen_id=False  
        # bat so hoa don
        hoa_don=vals.get('so_hoa_don')  
        if hoa_don:
            hoadon_pool=self.pool.get('account.invoice')
            hoadon_obj=hoadon_pool.browse(cr, uid, hoa_don, context)
            #check trang thai
            hoadon_state=hoadon_obj.state
            if hoadon_state in ('draft','cancel'):
                raise osv.except_osv(_('Thông báo!'), _('Vui lòng xác nhận hoặc thanh toán hóa đơn %s trước!')%(hoadon_obj.so_hoa_don))
            #end
        if phuongtien_vc!='duongsat_thongthuong':
            vals['name']=self.pool.get('sequence.custormize.vanchuyen').get_name(cr, uid, 'icsc.phieu.vanchuyen', 'icsc_phieu_vanchuyen','')
            vanchuyen_id=super(icsc_phieu_vanchuyen, self).create(cr, uid, vals, context=context)
            self.write(cr, uid, [vanchuyen_id],{'duavao_vipham':False,}, context=context)
        else:
            vanchuyen_id=super(icsc_phieu_vanchuyen, self).create(cr, uid, vals, context=context)
            self.write(cr, uid, [vanchuyen_id],{'duavao_vipham':False,}, context=context)
        return vanchuyen_id
    def write(self, cr, uid, ids,vals, context=None):   
        phuongtien_vc=vals.get('phuongtien_vc') or False        
        if  phuongtien_vc==False:
            try:
                for data in self.browse(cr, uid, ids, context):
                    phuongtien_vc=data.phuongtien_vc
            except:
                for data in self.browse(cr, uid, [ids], context):
                    phuongtien_vc=data.phuongtien_vc                   
        # bat so hoa don
        hoa_don=vals.get('so_hoa_don')  
        if hoa_don:
            hoadon_pool=self.pool.get('account.invoice')
            hoadon_obj=hoadon_pool.browse(cr, uid, hoa_don, context)
            #check trang thai
            hoadon_state=hoadon_obj.state
            if hoadon_state in ('draft','cancel'):
                raise osv.except_osv(_('Thông báo!'), _('Vui lòng xác nhận hoặc thanh toán hóa đơn %s trước!')%(hoadon_obj.so_hoa_don))
            #end
        return super(icsc_phieu_vanchuyen, self).write(cr, uid, ids,vals, context=context)
    
    def unlink(self, cr, uid, ids, context=None):
        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in sale_orders:
            if s['state'] in ['draft', 'cancel']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Lỗi!'), _('Bạn chỉ có thể xóa PVC ở trạng thái Dự thảo và Đã hủy!'))

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
    def onchange_hoadon(self, cr, uid, ids, hoa_don, context=None):
        if not hoa_don:
            return {}  
        # bat so hoa don         
        if hoa_don:
            hoadon_pool=self.pool.get('account.invoice')
            hoadon_obj=hoadon_pool.browse(cr, uid, hoa_don, context)
            #check trang thai
            hoadon_state=hoadon_obj.state
            if hoadon_state in ('draft','cancel'):
                raise osv.except_osv(_('Thông báo!'), _('Vui lòng xác nhận hoặc thanh toán hóa đơn %s trước!')%(hoadon_obj.so_hoa_don))
            #end
        return {} 
    
    def onchange_is_chang2(self, cr, uid, ids, is_chang2, congty_vc, sale_id, hopdong_vanchuyen, kehoach_vanchuyen, context=None):
        khvc_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        if not is_chang2:
            return {} 
        if is_chang2:
            if not congty_vc:
                raise osv.except_osv(_('Thông báo!'), _('Vui lòng chọn tên nhà vận chuyển trước!'))
            if not hopdong_vanchuyen:
                raise osv.except_osv(_('Thông báo!'), _('Vui lòng chọn hợp đồng vận chuyển trước!'))
            if not sale_id:
                raise osv.except_osv(_('Thông báo!'), _('Vui lòng chọn lệnh xuất hàng trước!'))           
            khvc_data = khvc_pool.search(cr, uid, [('congty_vc','=',congty_vc),('sale_id','=',sale_id),('so_khvc','=',hopdong_vanchuyen)])
            if khvc_data:
                return {'value': {'kehoach_vanchuyen':khvc_data[0]}} 
        return {} 
    
    def load_sotoa(self, cr, uid, ids, phieu_xuat, context=None):
        if not phieu_xuat:
            return {}  
        sotoa=False
        don_vi_vc=False
        kehoach_vanchuyen=False
        phieuxuat= self.pool.get('stock.picking').browse(cr, uid, phieu_xuat)
        sotoa=phieuxuat.bang_kiem_soat
        sohoadon=phieuxuat.hoa_don_id.id
        #daidien_muahang=phieuxuat.daidien_muahang.id
        don_vi_vc_obj=phieuxuat.don_vi_vc
        if don_vi_vc_obj:
            don_vi_vc=don_vi_vc_obj.id
        sale_id=phieuxuat.sale_id.id
        loai_lenh_xuat=phieuxuat.loai_xuatkho
        if phieuxuat.kehoach_vanchuyen_id:
            kehoach_vanchuyen= phieuxuat.kehoach_vanchuyen_id.id
        #,'dai_dien':daidien_muahang
        return {'value': {'kehoach_vanchuyen':kehoach_vanchuyen,'congty_vc':don_vi_vc,'loai_phieu':loai_lenh_xuat,'sale_id':sale_id,'bang_kiem_soat':sotoa,'so_hoa_don':sohoadon}} 
    def onchange_cuoc_den_diem(self, cr, uid, ids, cuoc_den_diem,kehoach_vanchuyen, context=None):
        if not cuoc_den_diem:
            return {} 
        res=[] 
        sotoa=False
        kehoach= self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, kehoach_vanchuyen)
        cuoc_den_diem_kh=kehoach.cuoc_den_diem.id
        if cuoc_den_diem_kh==False:
            raise osv.except_osv(_('Thông báo!'), _("Cước đến điểm trên KHVC chưa được chọn. Vui lòng xác định cước đến điểm cho KHVC trước khi lập PVC"))
        if cuoc_den_diem_kh!=cuoc_den_diem:
            raise osv.except_osv(_('Thông báo!'), _("Cước đến điểm trên KHVC là: %s")%(kehoach.cuoc_den_diem.name))       
        return res
    def onchange_cuoc_tu_diem(self, cr, uid, ids, cuoc_tu_diem,kehoach_vanchuyen, context=None):
        if not cuoc_tu_diem:
            return {} 
        res=[] 
        sotoa=False
        kehoach= self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, kehoach_vanchuyen)
        cuoc_tu_diem_kh=kehoach.cuoc_tu_diem.id
        if cuoc_tu_diem_kh==False:
            raise osv.except_osv(_('Thông báo!'), _("Cước từ điểm trên KHVC chưa được chọn. Vui lòng xác định cước từ điểm cho KHVC trước khi lập PVC"))
        if cuoc_tu_diem!=cuoc_tu_diem_kh:
            raise osv.except_osv(_('Thông báo!'), _("Cước từ điểm trên KHVC là: %s")%(kehoach.cuoc_tu_diem.name))       
        return res
    def onchange_sale_id(self, cr, uid, ids, sale_id, context=None):
        if not sale_id:
            return {}  
        loai_phieu=False
        phieuxuat= self.pool.get('sale.order').browse(cr, uid, sale_id)
        loai_lenh_xuat=phieuxuat.loai_lenh_xuat
        if loai_lenh_xuat=='vat':
            loai_phieu='thongthuong'
        else:
            loai_phieu='noibo'
        return {'value': {'loai_phieu':loai_phieu}} 
    def action_load_tu_phieu_xuat(self, cr, uid, ids, context=None):
        for data in self.browse(cr, uid, ids, context):
            phieu_xuat=data.phieu_xuat.id
            cuoc_tu_diem=data.cuoc_tu_diem.id
            cuoc_den_diem=data.cuoc_den_diem.id
            banggia_id=False
            if data.cuoc_tu_diem.id==False:
                raise osv.except_osv(_('Thông báo!'), _("Vui lòng chọn Tính cước từ điểm"))
            if data.cuoc_den_diem.id==False:
                raise osv.except_osv(_('Thông báo!'), _("Vui lòng chọn Tính cước đến điểm"))
            if phieu_xuat:
                for line in data.phieu_xuat.move_lines:
                    #diem_den=line.chitiet_kh.den_diem
                    product_id=line.product_id.id                       
                    product_qty=line.product_qty
                    product_uom=line.product_uom.id                                  
                    chitiet_kh=line.chitiet_kh.id              
                    tax_id=False
                    gia_chua_thue=gia_co_thue=0
                    sokh=data.hopdong_vanchuyen.id
                    ngay_vc=datetime.strptime(data.ngay_vc,'%Y-%m-%d')  
                    if sokh:
                        tax_id=False
                        gia_chua_thue=0
                        gia_co_thue=0
                        for gia in data.hopdong_vanchuyen.chitiet_banggia:
                            tu_diem=gia.tu_diem.id
                            den_diem=gia.den_diem.id
                            ngay_hieu_luc=gia.ngay_hieu_luc
                            ngay_batdau=datetime.strptime(ngay_hieu_luc,'%Y-%m-%d')                   
                            ngay_het_hieu_luc=gia.ngay_het_hieu_luc                            
                            if tu_diem==cuoc_tu_diem and den_diem==cuoc_den_diem:
                                if ngay_hieu_luc and ngay_het_hieu_luc: 
                                    
                                    ngay_kethuc=datetime.strptime(ngay_het_hieu_luc,'%Y-%m-%d')  
                                    if ngay_vc <=ngay_kethuc and ngay_vc >=ngay_batdau:   
                                        tax_id=gia.tax_id.id
                                        gia_chua_thue=gia.gia_chua_thue
                                        gia_co_thue=gia.gia_co_thue 
                                        banggia_id=gia.banggia_id.id
                                if ngay_hieu_luc and not ngay_het_hieu_luc:                    
                                    #ngay_kethuc=datetime.strptime(line.ngay_kethuc,'%Y-%m-%d')  
                                    if ngay_vc >=ngay_batdau:   
                                        tax_id=gia.tax_id.id
                                        gia_chua_thue=gia.gia_chua_thue
                                        gia_co_thue=gia.gia_co_thue 
                                        banggia_id=gia.banggia_id.id
                                
                    count4=0
                    query_check4="""select count(*) as count from icsc_phieu_vanchuyen_chitiet
                                 where name= """+str(chitiet_kh)+""" and phieu_id= """+str(data.id)+""" and move_id= """+str(line.id)
                    cr.execute(query_check4)
                    for check4 in cr.dictfetchall():
                        count4 =check4['count']
                    if count4==0:
                        self.pool.get('icsc.phieu.vanchuyen.chitiet').create(cr, uid, {
                                               'product_id': product_id,
                                               'kl_vc':product_qty,                                                                  
                                               'don_vi': product_uom,
                                               'phieu_id':data.id,
                                               'diem_den':cuoc_den_diem,
                                               'thue_id':tax_id,
                                               'gia_chua_thue':gia_chua_thue,
                                               'thanh_tien':gia_co_thue,
                                               'name':chitiet_kh,
                                               'move_id':line.id,
                                               }, context=context)
                    
                
            self.write(cr, uid, data.id, {'banggia_id':banggia_id,}, context)     
        return True
    def kehoach_vanchuyen(self, cr, uid, ids, kehoach_vanchuyen,hopdong_vanchuyen,congty_vc,context=None):
        if not kehoach_vanchuyen:
            return {}           
        kehoach_vanchuyen_object=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, kehoach_vanchuyen)
        #phuongthuc_vc=kehoach_vanchuyen_object.phuongthuc_vc
                         
        loai_phieu=kehoach_vanchuyen_object.loai_khvc
        cuoc_tu_diem=kehoach_vanchuyen_object.cuoc_tu_diem.id
        cuoc_den_diem=kehoach_vanchuyen_object.cuoc_den_diem.id
        if hopdong_vanchuyen==False or hopdong_vanchuyen is None:            
            hopdong_vanchuyen= kehoach_vanchuyen_object.so_khvc.id 
        if congty_vc==False or congty_vc is None: 
            congty_vc=kehoach_vanchuyen_object.congty_vc.id                   
        donvi_nhanhang=kehoach_vanchuyen_object.donvi_nhanhang.id
        if kehoach_vanchuyen_object.la_khach_hang:
            if kehoach_vanchuyen_object.kehoach_cha:
                dv=kehoach_vanchuyen_object.kehoach_cha
                if dv:
                    donvi_nhanhang=dv.khach_hang.id
        if kehoach_vanchuyen_object.trung_chuyen==False:
            donvi_nhanhang=kehoach_vanchuyen_object.order_partner_id.id
        phuongtien_vc=kehoach_vanchuyen_object.phuongthuc_vc  
        # lxh_id=kehoach_vanchuyen_object.sale_id.id
        kh_cha=False  
        if  kehoach_vanchuyen_object.kehoach_cha:
            khach_hang=kehoach_vanchuyen_object.kehoach_cha.khach_hang.id  
            kh_cha=kehoach_vanchuyen_object.kehoach_cha.id
        else:
            khach_hang=kehoach_vanchuyen_object.khach_hang.id                        
#         ngay_vc=kehoach_vanchuyen_object.ngay_tao
        kiem_soat=kehoach_vanchuyen_object.kiem_soat.id
        chiphi_denxa=0
        tinh_denxa=kehoach_vanchuyen_object.tinh_denxa
        trung_chuyen=kehoach_vanchuyen_object.trung_chuyen
        if tinh_denxa:
            #
            query_denxa="""SELECT *
                          FROM icsc_hopdong_vanchuyen_giacuoc_xa
                          where now()::date between ngay_hieuluc and ngay_kethuc
                          order by id desc limit 1
                        """
            cr.execute(query_denxa)
            for item_xa in cr.dictfetchall():
                xa_id=item_xa['id']
                xa_obj=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.xa').browse(cr, uid, xa_id)
                chiphi_denxa=xa_obj.gia_co_thue  
        return {'value': {'congty_vc':congty_vc,
                          'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem,
                          'hopdong_vanchuyen':hopdong_vanchuyen,'donvi_nhanhang':donvi_nhanhang,
                          'phuongtien_vc':phuongtien_vc,'khach_hang':khach_hang,
#                           'ngay_vc':ngay_vc,
                          'kiem_soat':kiem_soat,
                          'tinh_denxa':tinh_denxa,
                          'chiphi_denxa':chiphi_denxa,
                          'trung_chuyen':trung_chuyen,
                          'cha_id':kh_cha,
                          #'sale_id':lxh_id,
                          }}
        
    def onchange_hdvc(self, cr, uid, ids, congty_vc,context=None):
        if not congty_vc:
            return {}           
        sale_object=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, congty_vc)
        hd_vc=sale_object.so_khvc.id        
        return {'value': {'hopdong_vanchuyen':hd_vc}}
    def load_loai_vanchuyen(self, cr, uid, ids, sale_id,context=None):
        if not sale_id:
            return {}   
        loai=False        
        sale_object=self.pool.get('sale.order').browse(cr, uid, sale_id)
        loai_lenh_xuat=sale_object.loai_lenh_xuat
        if loai_lenh_xuat=='vat':
            loai='thongthuong'
        if loai_lenh_xuat=='guikho':
            loai='noibo'     
        return {'value': {'loai_phieu':loai}}
    
    def onchange_nhavanchuyen(self, cr, uid, ids, congty_vc, is_chang2, sale_id, kehoach_vanchuyen, context=None):
        if not congty_vc:
            return {}           
        hd_vc=False
        now=datetime.now()
        query="""select * from icsc_hopdong_vanchuyen 
        where congty_vc= """+str(congty_vc)+""" and ngay_hieuluc<= '"""+str(now)+"""'::date and ngay_kethuc>= '""" +str(now)+"""'::date"""
        cr.execute(query)   
        for item in cr.dictfetchall():
            hd_vc=item['id']
        if is_chang2:
            khvc_data = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').search(cr, uid, [('congty_vc','=',congty_vc),('sale_id','=',sale_id),('so_khvc','=',hd_vc)])
            if khvc_data:
                kehoach_vanchuyen = khvc_data[0]
        return {'value': {'hopdong_vanchuyen':hd_vc, 'kehoach_vanchuyen':kehoach_vanchuyen}}
         
    def onchange_laixe(self, cr, uid, ids, lai_xe,context=None):
        if not lai_xe:
            return {}           
        sale_object=self.pool.get('res.partner').browse(cr, uid, lai_xe)
        giayphep_laixe=sale_object.giayphep_laixe        
        return {'value': {'giayphep_laixe':giayphep_laixe}}
    
    def action_confirm(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            amount_thanhtien=0            
            for line in item.chitiet_vc:
                amount_thanhtien +=line.thanh_tien
            if amount_thanhtien==0:
                raise osv.except_osv(_('Lỗi!'), _('Tổng chi phí cần vận chuyển & tổng chi phí vận chuyển/KH phải khác 0!'))
            congty_vc=item.congty_vc.id
            phieu_xuat=item.kehoach_vanchuyen
            if phieu_xuat:
                cty=phieu_xuat.congty_vc.id
                ten_cty=phieu_xuat.congty_vc.name
                if cty!=congty_vc:
                    raise osv.except_osv(
                        _('Thông báo'),
                        _('Công ty vận chuyển trên Kế hoạch vận chuyển là %s .') % (ten_cty))
                     
            id1=item.id
            self.write(cr, uid, id1, {'state':'confirm',}, context)
            for line in item.chitiet_vc:
                self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'confirm',}, context)
        
        return True
    def action_du_dk(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'du_dk',}, context)
            for line in item.chitiet_vc:
                if item.tung_phan:
                    self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'du_dk_tung_phan',}, context)
                else:
                    self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'du_dk',}, context)
        return True
    def action_du_dk_tungphan(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'du_dk',}, context)
            for line in item.chitiet_vc:
                self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'du_dk_tung_phan',}, context)
        return True
    
    def action_vipham(self, cr, uid, ids, context=None):
        phieu_vipham=self.pool.get('icsc.phieuvipham.vanchuyen')
        phieu_chitiet=self.pool.get('icsc.phieuvipham.vanchuyen.chitiet')
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'confirm',}, context)
            # tao phieu vi pham van chuyen
            ngay_vc=item.ngay_vc
            congty_vc=item.congty_vc.id
            donvi_nhanhang=item.donvi_nhanhang.id
            khach_hang=item.khach_hang.id
            ngay_lap= time.strftime('%Y-%m-%d')
            state='draft'
            name= self.pool.get('sequence.custormize.hopdong').get_name(cr, uid, 'icsc.hopdong.vanchuyen'  , 'icsc_phieuvipham_vanchuyen','')
            vipham_id= phieu_vipham.create(cr, uid, {
                                                'name':name,
                                               'ngay_vc': ngay_vc,                                                                                                           
                                               'congty_vc': congty_vc,
                                               'donvi_nhanhang':donvi_nhanhang,                                               
                                               'khach_hang':khach_hang,
                                               'ngay_lap':ngay_lap,
                                               'state':state,
                                               'phieu_vanchuyen':id1,
                                               'duavao_vipham':True,
                                               }, context=context)
            for line in item.chitiet_vc:
                product_id=line.product_id.id
                don_vi=line.don_vi.id
                gia_cuoc=line.thanh_tien
                don_gia=line.product_id.list_price
                query_gia=""" select l.id,l.product_id,l.price_unit
                            from icsc_phieu_vanchuyen vc 
                            left join icsc_hopdong_vanchuyen_giacuoc_kehoach khvc on khvc.id=vc.kehoach_vanchuyen
                            left join sale_order o on o.id=khvc.sale_id
                            left join sale_order_line l on l.order_id=o.id
                            where vc.id= """+str(item.id)
                cr.execute(query_gia)
                for item_gia in cr.dictfetchall():
                    product_ids=item_gia['product_id']
                    price_unit=item_gia['price_unit']
                    line_id=item_gia['id']
                    tax_amount=0
                    line_object=self.pool.get('sale.order.line').browse(cr, uid, line_id, context)
                    for tax_id in line_object.tax_id:
                        tax=tax_id.id
                        thue_objet=self.pool.get('account.tax').browse(cr, uid, tax, context)
                        tax_amount=thue_objet.amount
                    if product_id==product_ids:
                        don_gia=round(price_unit+(price_unit*tax_amount))
                    
                phieu_chitiet.create(cr, uid, {
                                               'product_id': product_id,                                                                                                           
                                               'don_vi': don_vi,
                                               'phieu_id':vipham_id,                                               
                                               'gia_cuoc':gia_cuoc,
                                               'don_gia':don_gia,
                                               }, context=context)
            self.write(cr, uid, id1, {'duavao_vipham':True,}, context)
            return {    'domain': "[('id', 'in', ["+str(vipham_id)+"])]",    
                    'name':'Phiếu vi phạm vận chuyển',
                    'view_type':'form',
                    'view_mode':'tree,form',                                          
                    'res_model':'icsc.phieuvipham.vanchuyen',
                    'type':'ir.actions.act_window',                   
                    } 
    def action_done(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            amount_thanhtien=0     
            self.write(cr, uid, id1, {'state':'done',}, context)
            for line in item.chitiet_vc:
                amount_thanhtien +=line.thanh_tien
                self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'done',}, context)
            for line_capnhat in item.chitiet_vc_capnhat:
                self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, line_capnhat.id, {'state':'done',}, context)
            if amount_thanhtien==0:
                raise osv.except_osv(_('Lỗi!'), _('Tổng chi phí cần vận chuyển & tổng chi phí vận chuyển/KH phải khác 0!'))    
        return True
    def action_cancel(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            count=0
            # kiem tra xem PVP van chuyen da duowc dua vao DE nghi thanh toan chua
            query="""select count(ct.*) 
                    from icsc_denghithanhtoan_vanchuyen_chitiet ct
                    left join icsc_denghithanhtoan_vanchuyen dn on dn.id=ct.phieu_id
                    where so_phieu_vc= """+str(id1)+""" and dn.state !='cancel' """
            cr.execute(query)
            for data in cr.dictfetchall():
                count +=data['count']
            if count>0:
                raise osv.except_osv(_('Lỗi!'), _('Bạn không thể hủy Phiếu vận chuyển khi phiếu này đã được đưa vào giấy ĐNTT!'))
            self.write(cr, uid, id1, {'state':'cancel',}, context)
            for line in item.chitiet_vc:
                self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'cancel',}, context)
          
        return True
    def action_return(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'draft',}, context)
            for line in item.chitiet_vc:
                self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, line.id, {'state':'draft',}, context)
            for line_capnhat in item.chitiet_vc_capnhat:
                self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, line_capnhat.id, {'state':'draft',}, context)
                  
        return True
icsc_phieu_vanchuyen()


class icsc_phieu_vanchuyen_chitiet_capnhat(osv.osv):
    _description="icsc_phieu_vanchuyen_chitiet_capnhat"
    _name = 'icsc.phieu.vanchuyen.chitiet.capnhat'
    _inherit = ['mail.thread']
    def get_count_id(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=1
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            if data.phieu_id: 
                query="""select count(*) as count from icsc_phieu_vanchuyen_chitiet_capnhat where phieu_id= """+str(data.phieu_id.id)+""" and id <= """+str(data.id)        
                cr.execute(query)
                for item in cr.dictfetchall():
                    count =item['count']         
            
            res[data.id]=count
        return res
    _columns = {
        'name': fields.many2one('icsc.phieu.vanchuyen.chitiet','Chi tiết KHVC', size=500),  
        'product_id': fields.many2one('product.product', 'Tên vật tư', ondelete='cascade'),  
        'kl_vc': fields.float('KL vận chuyển/tấn'),       
        'phieu_id': fields.many2one('icsc.phieu.vanchuyen', 'Phiếu vận chuyển', ondelete='cascade'),  
        'thanh_tien': fields.float('Giá có thuế'),      
        'no': fields.function(get_count_id, type='integer', string='STT'),
        'ngay_capnhat': fields.date('Ngày cập nhật'),  
        'duavao_thanhtoan': fields.boolean('Đề nghị thanh toán'), 
        'thanh_toan': fields.boolean('Thanh toán'), 
        'state': fields.selection([
            ('draft', 'Mới'),          
            ('done', 'Hoàn tất'),
            ('cancel', 'Đã hủy'),
            
            
            ], 'Trạng thái', readonly=True, track_visibility='onchange'), 
        
                   
    }
    _defaults= {'state':'draft',
                
                  } 
    def action_done(self, cr, uid, ids,  context=None):
        for data in self.browse(cr, uid, ids, context):
            chitiet=data.name.id
            soluong_total=data.name.kl_vc
            soluong_hoantat=data.kl_vc
            sums=soluong_hoantat
            for item in data.name.history_ids:
                trangthai=item.state
                if trangthai=='done':
                    sums +=item.kl_vc
            if sums==soluong_total:
                self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, chitiet, {'state':'done',}, context)
            self.write(cr, uid, data.id, {'state':'done',}, context)
        return True
    def action_reset(self, cr, uid, ids,  context=None):
        for data in self.browse(cr, uid, ids, context):
            chitiet=data.name.id           
            
            self.pool.get('icsc.phieu.vanchuyen.chitiet').write(cr, uid, chitiet, {'state':'draft',}, context)
            self.write(cr, uid, data.id, {'state':'draft',}, context)
        return True
icsc_phieu_vanchuyen_chitiet_capnhat()
class icsc_phieu_vanchuyen_duongsat(osv.osv):
    _name = "icsc.phieu.vanchuyen.duongsat"
    _inherit = "icsc.phieu.vanchuyen"
    _table = "icsc_phieu_vanchuyen"
    _description = "Phiếu vận chuyển đường sắt"
    _order= 'id desc'
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {               
                'amount_total': 0.0,
                'amount_thanhtien': 0.0,  
                    
            }
            val=val1 =val2= val3=0.0        
            for line in order.chitiet_vc:
                val1 += line.thanh_tien #* line.kl_vc               
            res[order.id]['amount_thanhtien'] = val1           
        
            res[order.id]['amount_total'] = val1
            
           
        return res   
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.phieu.vanchuyen.chitiet.duongsat').browse(cr, uid, ids, context=context):
            result[line.phieu_id.id] = True
        return result.keys()
    def _get_congty_vc(self, cr, uid, context=None):
       
        congty_vc=False
        query=""" select congty_vc from icsc_phieu_vanchuyen where phuongtien_vc='duongsat_thongthuong' order by id desc limit 1"""
        cr.execute(query)
        for data in cr.dictfetchall():
            congty_vc = 1#data['congty_vc']
        return congty_vc
    
    def _tongkhoiluong(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task in self.browse(cr, uid, ids, context=context):          
            kq=0
            for line in task.chitiet_vc:
                kq+= line.kl_vc
            res[task.id] = kq
        return res
    _columns = { 
    
     'tong_kl': fields.function(_tongkhoiluong, string='Tổng khối lượng',type="float"),        
       'phuongtien_vc': fields.selection([               
            
             ('duongsat_thongthuong', 'Đường sắt thông thường'), 
                    
            
            ], 'Phương thức vận chuyển',  required=True
            ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},),  
     'chitiet_vc': fields.one2many('icsc.phieu.vanchuyen.chitiet.duongsat', 'phieu_id','Chi tiết vận chuyển' 
                                   ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]}),
     'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng chi phí vận chuyển',
            store={
                'icsc.phieu.vanchuyen.duongsat': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet.duongsat': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien'], 10),
                 
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),   
        'amount_thanhtien': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Chi phí cần vận chuyển',
            store={
                'icsc.phieu.vanchuyen.duongsat': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_vc','chiphi_denxa','tung_phan'], 10),
                'icsc.phieu.vanchuyen.chitiet.duongsat': (_get_order, ['gia_chua_thue', 'thue_id', 'kl_vc', 'thanh_tien'], 10),
              
            },
            multi='sums', help="The total amount.", track_visibility='onchange'),   
       'kehoach_vanchuyen': fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển',
                                            domain="[('so_khvc','=',hopdong_vanchuyen),('so_khvc','!=',False)]" , 
                                            track_visibility='onchange'
                                            ,states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True),
      'phieu_xuat': fields.many2one('stock.picking','Phiếu xuất kho',domain="['|',('kehoach_vanchuyen_id','=',kehoach_vanchuyen),('kehoach_vanchuyen_id','=',kehoach_cha),('kehoach_vanchuyen_id','!=',False)]" , 
                                    track_visibility='onchange',states={'du_dk': [('readonly', True)],'done': [('readonly', True)],'confirm': [('readonly', True)]},select=True)  , 
      'is_chang2':fields.boolean('Là KHVC chặng 2'),
    
     
    }
    _defaults = {
         'phuongtien_vc': 'duongsat_thongthuong',
         'name':'',
         'congty_vc':_get_congty_vc,
         #'cuoc_den_diem':113,
    }
    
#     def onchange_nhavanchuyen_ds(self, cr, uid, ids, congty_vc, context=None):
#         if not congty_vc:
#             return {}           
#         hd_vc=False
#         now=datetime.now()
#         query="""select * from icsc_hopdong_vanchuyen 
#         where congty_vc= """+str(congty_vc)+""" and ngay_hieuluc<= '"""+str(now)+"""'::date and ngay_kethuc>= '""" +str(now)+"""'::date"""
#         cr.execute(query)   
#         for item in cr.dictfetchall():
#             hd_vc=item['id']
#         return {'value': {'hopdong_vanchuyen':hd_vc}}
    
    def create(self, cr, uid, vals, context=None): 
        name=vals.get('name') or False
        if name==False:
            raise osv.except_osv(_('Thông báo!'), _('Vui lòng nhập Số Vận đơn đường sắt !'))        
        return super(icsc_phieu_vanchuyen_duongsat, self).create(cr, uid, vals, context=context)
    def unlink(self, cr, uid, ids, context=None):
        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in sale_orders:
            if s['state'] in ['draft', 'cancel']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Lỗi!'), _('Bạn chỉ có thể xóa KHVC đường sắt ở trạng thái Dự thảo và Đã hủy!'))

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

    def kehoach_vanchuyen(self, cr, uid, ids, kehoach_vanchuyen,hopdong_vanchuyen,congty_vc,context=None):
        if not kehoach_vanchuyen:
            return {}           
        kehoach_vanchuyen_object=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach').browse(cr, uid, kehoach_vanchuyen)
        if hopdong_vanchuyen==False or hopdong_vanchuyen is None:            
            hopdong_vanchuyen= kehoach_vanchuyen_object.so_khvc.id 
        if congty_vc==False or congty_vc is None: 
            congty_vc=kehoach_vanchuyen_object.congty_vc.id  
        #congty_vc=kehoach_vanchuyen_object.congty_vc.id                   
        loai_phieu=kehoach_vanchuyen_object.loai_khvc
        cuoc_tu_diem=kehoach_vanchuyen_object.cuoc_tu_diem.id
        cuoc_den_diem=kehoach_vanchuyen_object.cuoc_den_diem.id
        #hopdong_vanchuyen= kehoach_vanchuyen_object.so_khvc.id 
                         
        donvi_nhanhang=kehoach_vanchuyen_object.donvi_nhanhang.id
        # neu la khong trung chuyen thi lay khách hang
        #kiem tra trung chuyen
        trung_chuyen=kehoach_vanchuyen_object.trung_chuyen
        if trung_chuyen==False:
            donvi_nhanhang=kehoach_vanchuyen_object.khach_hang.id
        else:
            la_khach_hang=kehoach_vanchuyen_object.la_khach_hang
            parent_id=kehoach_vanchuyen_object.parent_id
            if la_khach_hang:
                try:
                    donvi_nhanhang=kehoach_vanchuyen_object.kehoach_cha.khach_hang.id
                except:
                    pass
            if parent_id:
                donvi_nhanhang=kehoach_vanchuyen_object.khach_hang.id
        phuongtien_vc=kehoach_vanchuyen_object.phuongthuc_vc  
        lxh_id=kehoach_vanchuyen_object.sale_id.id
        kh_cha=False  
        if  kehoach_vanchuyen_object.kehoach_cha:
            khach_hang=kehoach_vanchuyen_object.kehoach_cha.khach_hang.id  
            kh_cha=kehoach_vanchuyen_object.kehoach_cha.id
              
        else:
            khach_hang=kehoach_vanchuyen_object.khach_hang.id                        
#         ngay_vc=kehoach_vanchuyen_object.ngay_tao
        kiem_soat=kehoach_vanchuyen_object.kiem_soat.id
        chiphi_denxa=0
        tinh_denxa=kehoach_vanchuyen_object.tinh_denxa
        
        if tinh_denxa:
            #
            query_denxa="""SELECT *
                          FROM icsc_hopdong_vanchuyen_giacuoc_xa
                          where now()::date between ngay_hieuluc and ngay_kethuc
                          order by id desc limit 1
                        """
            cr.execute(query_denxa)
            for item_xa in cr.dictfetchall():
                xa_id=item_xa['id']
                xa_obj=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.xa').browse(cr, uid, xa_id)
                chiphi_denxa=xa_obj.gia_co_thue  
        return {'value': {'congty_vc':congty_vc,'loai_phieu':loai_phieu,
                          'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem,
                          'hopdong_vanchuyen':hopdong_vanchuyen,
                          'donvi_nhanhang':donvi_nhanhang,
                          'phuongtien_vc':phuongtien_vc,
                          'khach_hang':khach_hang,
#                           'ngay_vc':ngay_vc,
                          'kiem_soat':kiem_soat,
                          'tinh_denxa':tinh_denxa,
                          'chiphi_denxa':chiphi_denxa,
                          'trung_chuyen':trung_chuyen,
                          'cha_id':kh_cha,
                          'sale_id':lxh_id,
                          }}
icsc_phieu_vanchuyen_duongsat()    
class icsc_phieu_vanchuyen_chitiet(osv.osv):
    _description="icsc_phieu_vanchuyen_chitiet"
    _name = 'icsc.phieu.vanchuyen.chitiet'
   
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
              
        for order in self.browse(cr, uid, ids, context=context):
            
            val1=val=kl_vc=0.0  
            res[order.id] = {
                'kl_vc_conlai': 0.0,
                'kl_dangvc_dukien': 0.0,               
            } 
            for line in order.history_ids:
                val1 +=line.kl_vc 
            kl_vc=order.kl_vc       
            res[order.id]['kl_vc_conlai']=kl_vc-val1
            res[order.id]['kl_dangvc_dukien']=val1
          
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context):           
            kh=data.name            
            if kh:
                result[kh.id] = True
           
        return result.keys()
    def get_count_id(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=1
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            if data.phieu_id: 
                query="""select count(*) as count from icsc_phieu_vanchuyen_chitiet where phieu_id= """+str(data.phieu_id.id)+""" and id <= """+str(data.id)        
                cr.execute(query)
                for item in cr.dictfetchall():
                    count =item['count']             
           
            res[data.id]=count
        return res
    
    _columns = {
        'no': fields.function(get_count_id, type='integer', string='STT'),
        'move_id': fields.many2one('stock.move', 'Chi tiết PXK', ondelete='cascade', domain="[('picking_id','=',parent.phieu_xuat)]"),  
        'name': fields.many2one('icsc.hopdong.vanchuyen.chitiet', 'Chi tiết KHVC', domain="[('kehoach_id','=',parent.kehoach_vanchuyen)]", ), 
        'product_id': fields.many2one('product.product', 'Tên vật tư', ondelete='cascade'),  
        'don_vi': fields.many2one('product.uom', 'Đơn vị', ondelete='cascade'),  
        'kl_vc': fields.float('KL vận chuyển/tấn'),       
        'phieu_id': fields.many2one('icsc.phieu.vanchuyen', 'Phiếu vận chuyển', ondelete='cascade'),  
        'diem_den': fields.many2one('res.country.diadiem', 'Chi tiết điểm đến',domain="[('van_chuyen','=',True)]" ),  
        'gia_chua_thue': fields.float('Giá chưa thuế'),  
        'thanh_tien': fields.float('Thành tiền'),        
        'thue_id': fields.many2one('account.tax','Thuế'),      
        'ghi_chu': fields.text('Ghi chú'),   
         'state': fields.selection([
            ('draft', 'Chưa vận chuyển'),
            ('confirm', 'Đang VC'),
            ('du_dk', 'Đủ ĐK thanh toán'),
           ( 'du_dk_tung_phan','Đủ ĐK thanh toán từng phần'),
            ('done', 'Hoàn tất'),
            ('cancel', 'Đã hủy'),
            
            ], 'Trạng thái', readonly=True), 
        'history_ids':fields.one2many('icsc.phieu.vanchuyen.chitiet.capnhat','name','chi tiết cập nhật'),
        'kl_dangvc_dukien': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='KL đã VC/tấn',
            store={
                'icsc.phieu.vanchuyen.chitiet': (lambda self, cr, uid, ids, c={}: ids, ['history_ids','kl_vc','thanh_tien'], 10),
                'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_order, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums'),
         'kl_vc_conlai': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='KL VC còn lại/tấn',
            store={
                'icsc.phieu.vanchuyen.chitiet': (lambda self, cr, uid, ids, c={}: ids, ['history_ids','kl_vc','thanh_tien','product_id','phieu_id'], 10),
                'icsc.phieu.vanchuyen.chitiet.capnhat': (_get_order, ['product_id', 'kl_vc', 'name', 'phieu_id','thanh_tien','ngay_capnhat','duavao_thanhtoan','thanh_toan'], 10),
            },
            multi='sums'),
        'tung_phan': fields.boolean('Hoàn tất một phần'),
                 
    }
    _defaults= {'state':'draft',
                
                  } 
    def create(self, cr, uid, vals, context=None):
        if context is None: context = {}  
        kh_chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        PVC_pool=self.pool.get('icsc.phieu.vanchuyen')
        khvc_pool=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        # xet chang KHVC
        # neu KHVC la chang 2
        chang_khvc=''
        phieu_id=vals.get('phieu_id') or False
        #lay PVC
        kehoach_vanchuyen=PVC_pool.browse(cr, uid, phieu_id).kehoach_vanchuyen.id
        if kehoach_vanchuyen:
            #xet chang KHVC
            khvc_obj=khvc_pool.browse(cr, uid, kehoach_vanchuyen)
            chang_khvc=khvc_obj.chang_khvc
        if chang_khvc!='chang_2':
            ct_kh=vals.get('name') 
            if ct_kh: 
                ct_data=kh_chitiet_pool.browse(cr, uid, ct_kh)
                kl=ct_data.kl_vc_kehoach
                kl_vc= vals.get('kl_vc')
                sum=0
                cr.execute("""select coalesce(sum(ct.kl_vc),0) as kl_vc 
                        from icsc_phieu_vanchuyen_chitiet ct
                        left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id 
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach vc on vc.id=pvc.kehoach_vanchuyen
                        where  ((coalesce(vc.kehoach_cha,0) !=0 and vc.chang_khvc!='chang_2') or coalesce(vc.trung_chuyen,False)=False ) and 
                         ct.state!='cancel' 
                          and ct.name= """+str(ct_kh))
                for line in cr.dictfetchall():
                    sum=line['kl_vc']
                if kl_vc:
                    sum +=kl_vc
                if kl<sum:
                    raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu vận chuyển lớn hơn Khối lượng trên chi tiết phiếu KHVC. Vui lòng chọn KHVC khác hoặc điều chỉnh lại khối lượng VC"))
                else:
                    project_id = super(icsc_phieu_vanchuyen_chitiet, self).create(cr, uid, vals, context)
                    return project_id
        else:
            ct_kh=vals.get('name') 
            if ct_kh: 
                ct_data=kh_chitiet_pool.browse(cr, uid, ct_kh)
                kl=ct_data.kl_vc_kehoach
                kl_vc= vals.get('kl_vc')
                cha_id=ct_data.cha_id.id
                sum=0
                cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                          where kh.chang_khvc!='chang_2' and ct.cha_id= """+str(cha_id))
                for item_con in cr.dictfetchall():
                    con_id=item_con['id']
                    cr.execute("""select coalesce(sum(ct.kl_vc),0) as kl_vc 
                            from icsc_phieu_vanchuyen_chitiet ct
                            left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id 
                            left join icsc_hopdong_vanchuyen_giacuoc_kehoach vc on vc.id=pvc.kehoach_vanchuyen
                            where   vc.chang_khvc ='chang_2' and ct.state!='cancel' 
                              and (ct.name= """+str(con_id)+""" or ct.name= """+str(ct_data.id)+""" )""")
                    for line in cr.dictfetchall():
                        sum +=line['kl_vc']
                if kl_vc:
                    sum +=kl_vc
                if kl<sum:
                    raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu vận chuyển lớn hơn Khối lượng trên chi tiết phiếu KHVC. Vui lòng chọn KHVC khác hoặc điều chỉnh lại khối lượng VC"))
                else:
                    project_id = super(icsc_phieu_vanchuyen_chitiet, self).create(cr, uid, vals, context)
                    return project_id
        return super(icsc_phieu_vanchuyen_chitiet, self).create(cr, uid, vals, context)
    def write(self, cr, uid, ids, vals, context=None):
        # if alias_model has been changed, update alias_model_id accordingly
        kh_chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        PVC_pool=self.pool.get('icsc.phieu.vanchuyen')
        PVC_ct=self.pool.get('icsc.phieu.vanchuyen.chitiet')
        khvc_pool=self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach')
        pvc_id=kehoach_vanchuyen=False
        # xet chang KHVC
        try:
            for ct_obj in PVC_ct.browse(cr, uid, ids, context):           
                pvc_id=ct_obj.phieu_id.id
        except:
            for ct_obj in PVC_ct.browse(cr, uid, [ids], context):           
                pvc_id=ct_obj.phieu_id.id
        # neu KHVC la chang 2
        chang_khvc=''
        phieu_id=vals.get('phieu_id') or pvc_id
        #lay PVC
        if phieu_id:
            kehoach_vanchuyen=PVC_pool.browse(cr, uid, phieu_id).kehoach_vanchuyen.id
        if kehoach_vanchuyen:
            #xet chang KHVC
            khvc_obj=khvc_pool.browse(cr, uid, kehoach_vanchuyen)
            chang_khvc=khvc_obj.chang_khvc
        if chang_khvc!='chang_2':
            if vals.get('kl_vc'):
                kl_vc=vals.get('kl_vc')
                for data in self.browse(cr, uid, ids, context):
                    name=data.name.id
                    if name:
                        kl=data.name.kl_vc_kehoach
                    sum=0
                    cr.execute("""select coalesce(sum(ct.kl_vc),0) as kl_vc 
                        from icsc_phieu_vanchuyen_chitiet ct
                        left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id 
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach vc on vc.id=pvc.kehoach_vanchuyen
                        where   ((coalesce(vc.kehoach_cha,0) !=0 and vc.chang_khvc!='chang_2') or coalesce(vc.trung_chuyen,False)=False ) and  ct.state!='cancel' 
                          and ct.name= """+str(name) +""" and ct.id!= """+str(data.id))
                    for line in cr.dictfetchall():
                        sum=line['kl_vc']
                    if kl_vc:
                        sum +=kl_vc
                    if kl<sum:
                        raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu vận chuyển lớn hơn Khối lượng trên chi tiết phiếu KHVC. Vui lòng chọn KHVC khác hoặc điều chỉnh lại khối lượng VC"))   
        else:
            if vals.get('kl_vc'):
                kl_vc=vals.get('kl_vc')
                for data in self.browse(cr, uid, ids, context):
                    name=data.name.id
                    cha_id=data.name.cha_id.id
                    if name:
                        kl=data.name.kl_vc_kehoach
                    sum=0
                    cr.execute("""select ct.id from icsc_hopdong_vanchuyen_chitiet ct
                        left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                          where kh.chang_khvc!='chang_2' and ct.cha_id= """+str(cha_id))
                    for item_con in cr.dictfetchall():
                        con_id=item_con['id']
                        cr.execute("""select coalesce(sum(ct.kl_vc),0) as kl_vc 
                                from icsc_phieu_vanchuyen_chitiet ct
                                left join icsc_phieu_vanchuyen pvc on pvc.id=ct.phieu_id 
                                left join icsc_hopdong_vanchuyen_giacuoc_kehoach vc on vc.id=pvc.kehoach_vanchuyen
                                where   vc.chang_khvc ='chang_2' and ct.state!='cancel' 
                                  and (ct.name= """+str(con_id)+""" or ct.name= """+str(name)+""") and ct.id != """+str(data.id))
                        for line in cr.dictfetchall():
                            sum +=line['kl_vc']
                    if kl_vc:
                        sum +=kl_vc
                    if kl<sum:
                        raise osv.except_osv(_("Thông báo!"), _("Tổng khối lượng trên chi tiết phiếu vận chuyển lớn hơn Khối lượng trên chi tiết phiếu KHVC. Vui lòng chọn KHVC khác hoặc điều chỉnh lại khối lượng VC"))   
                                   
            
        return super(icsc_phieu_vanchuyen_chitiet, self).write(cr, uid, ids, vals, context=context)
    def onchange_move_id(self, cr, uid, ids, lai_xe,context=None):
        if not lai_xe:
            return {}           
        sale_object=self.pool.get('stock.move').browse(cr, uid, lai_xe)
        chitiet_kh=sale_object.chitiet_kh.id  
        product_id=sale_object.product_id.id 
        diem_den=sale_object.doitac_giaohang.id
        cuoc_den_diem=False
        if chitiet_kh:
            cuoc_den_diem=sale_object.chitiet_kh.kehoach_id.cuoc_den_diem.id
        return {'value': {'name':chitiet_kh,'diem_den':cuoc_den_diem,'product_id':product_id}}
    def onchange_khvc(self, cr, uid, ids, name,context=None):
        if not name:
            return {}           
        sale_object=self.pool.get('icsc.hopdong.vanchuyen.chitiet').browse(cr, uid, name)
        #chitiet_kh=sale_object.chitiet_kh.id  
        product_id=sale_object.product_id.id 
        diem_den=sale_object.dia_chi_giao.id
        cuoc_den_diem=False
        if diem_den:
            cuoc_den_diem=sale_object.kehoach_id.cuoc_den_diem.id
        return {'value': {'diem_den':cuoc_den_diem,'product_id':product_id}}
  
    def action_done(self, cr, uid, ids,  context=None):
        for data in self.browse(cr, uid, ids, context):            
            for item in data.history_ids:              
                self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, item.id, {'state':'done',}, context)
            self.write(cr, uid, data.id, {'state':'done',}, context)
        return True
    def action_reset(self, cr, uid, ids,  context=None):
        for data in self.browse(cr, uid, ids, context):            
            for item in data.history_ids:              
                self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, item.id, {'state':'draft',}, context)
            self.write(cr, uid, data.id, {'state':'draft',}, context)
        return True
    def chitiet_vanchuyen(self, cr, uid, ids, phieu_vanchuyen,context=None):
        if not phieu_vanchuyen:
            return {}           
        phieu_vanchuyen_object=self.pool.get('icsc.phieu.vanchuyen').browse(cr, uid, phieu_vanchuyen)
        ngay_vc=phieu_vanchuyen_object.ngay_vc
        congty_vc=phieu_vanchuyen_object.congty_vc.id
        donvi_nhanhang=phieu_vanchuyen_object.donvi_nhanhang.id
        khach_hang=phieu_vanchuyen_object.khach_hang.id
        return {'value': {'congty_vc':congty_vc,                         
                          'donvi_nhanhang':donvi_nhanhang,'khach_hang':khach_hang,
                          'ngay_vc':ngay_vc,
                          
                          
                          }}
icsc_phieu_vanchuyen_chitiet()

class icsc_phieu_vanchuyen_chitiet_duongsat(osv.osv):
    _name = "icsc.phieu.vanchuyen.chitiet.duongsat"
    _inherit = "icsc.phieu.vanchuyen.chitiet"
    _table = "icsc_phieu_vanchuyen_chitiet"
    _description = "Phiếu vận chuyển đường sắt"
    def get_dvt(self, cr, uid, context=None):
       
        dvt=False     
           
        query="select id from product_uom where name='Toa'"
        cr.execute(query)
        for item in cr.dictfetchall():
            dvt=item['id']            
        return dvt
    def _get_thue(self, cr, uid, ids, field_name, arg, context=None):
        thue=False
        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            phieu=data.phieu_id.kehoach_vanchuyen
            
            if  phieu:                     
                cuoc_tu_diem=data.phieu_id.cuoc_tu_diem.id
                cuoc_den_diem=data.phieu_id.cuoc_den_diem.id
                sokh=data.phieu_id.kehoach_vanchuyen.so_khvc
                if sokh:
                    for gia in data.phieu_id.kehoach_vanchuyen.so_khvc.chitiet_banggia:
                        tu_diem=gia.tu_diem.id
                        den_diem=gia.den_diem.id
                        
                        if tu_diem==cuoc_tu_diem and den_diem==cuoc_den_diem:
                            thue=gia.tax_id.id   
                                             
            res[data.id] = thue
           
        return res
    def _giachua_thue(self, cr, uid, ids, field_name, arg, context=None):
        thue=False
        gt_thue=thanhtien=tien_thue=0
        res = {}
        for data in self.browse(cr, uid, ids, context=context):
            thue=data.thue_ids
            if thue:
                gt_thue=data.thue_ids.amount
                thanhtien= data.thanh_tien
                tien_thue=thanhtien / (1+gt_thue)
                
                                     
            res[data.id] = tien_thue
            self.write(cr, uid, data.id, {'gia_chua_thue':tien_thue,}, context)
        return res
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}  
        thue=False
        gt_thue=thanhtien=tien_thue=0      
        for data in self.browse(cr, uid, ids, context=context):
            res[data.id] = {               
                'gia_chua_thues': 0.0,                
            }
            thue=data.thue_id
            if thue:
                gt_thue=data.thue_id.amount
                thanhtien= data.thanh_tien
                tien_thue=thanhtien / (1+gt_thue)
                
            res[data.id]['gia_chua_thues']=tien_thue
            self.write(cr, uid, data.id, {'gia_chua_thue':tien_thue,}, context)
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for data in self.browse(cr, uid, ids, context):           
            kh=data.chitiet_vc        
            if kh:
                for item in data.chitiet_vc:
                    result[item.id] = True
           
        return result.keys()
    def get_count_id(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=1
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            if data.phieu_id: 
                query="""select count(*) as count from icsc_phieu_vanchuyen_chitiet where phieu_id= """+str(data.phieu_id.id)+""" and id <= """+str(data.id)        
                cr.execute(query)
                for item in cr.dictfetchall():
                    count =item['count']            
           
            res[data.id]=count
        return res
    _columns = {   
         'no': fields.function(get_count_id, type='integer', string='STT'),           
        'phieu_id': fields.many2one('icsc.phieu.vanchuyen.duongsat', 'Phiếu vận chuyển', ondelete='cascade'),  
        'thue_ids': fields.function(_get_thue, type='many2one', relation='account.tax' ,string='Thuế'), 
        #'gia_chua_thues': fields.function(_giachua_thue, type='float', string='Giá chưa thuế'), 
        'gia_chua_thues': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Giá chưa thuế',
            store={
                'icsc.phieu.vanchuyen.chitiet.duongsat': (lambda self, cr, uid, ids, c={}: ids, ['thue_ids','thanh_tien','kl_vc','don_vi','diem_den','product_id'], 10),
                'icsc.phieu.vanchuyen.duongsat': (_get_order, ['cuoc_tu_diem', 'cuoc_den_diem', 'kehoach_vanchuyen'], 10),
            },
            multi='sums', help="Giá chưa thuế."),
      
    }
    _defaults = {
        'don_vi': get_dvt,
         'thue_id':4,
        
    }
icsc_phieu_vanchuyen_chitiet_duongsat()
 
class icsc_loai_phat(osv.osv):
    _description="icsc_loai_phat"
    _name = 'icsc.loai.phat'
    _inherit = ['mail.thread']
    _order= 'id desc'
    _columns = {
      
        'name': fields.char('Lý do phạt', size=500,
            required=True, track_visibility='onchange')  ,        
        'mo_ta': fields.text( 'Mô tả', track_visibility='onchange' ),    
           
    }
   
icsc_loai_phat()

class icsc_phieuvipham_vanchuyen(osv.osv):
    _description="icsc_phieuvipham_vanchuyen"
    _name = 'icsc.phieuvipham.vanchuyen'
    _inherit = ['mail.thread']
    _order= 'id desc'
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {               
                'amount_total': 0.0,
            }
            val1 = 0.0        
            for line in order.chitiet_phat:
                val1 += line.thanh_tien                
            
            res[order.id]['amount_total'] = val1
        return res
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('icsc.phieuvipham.vanchuyen.chitiet').browse(cr, uid, ids, context=context):
            result[line.phieu_id.id] = True
        return result.keys()
    def get_count_id(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        kq=False
        if context is None:
            context = {}
        cr.execute("""select id from icsc_loai_phat order by id asc limit 1""")
        for item in cr.dictfetchall():
            kq=item['id']
        return kq
    def _get_check_DNTT(self, cr, uid, ids, name=None, args=None, context=None):
        res={}        
        if context is None:
            context = {}        
        for order in self.browse(cr, uid, ids, context): 
            if order.state == 'cancel':
                res[order.id]= True
            else:       
                val=0        
                query = """ select count(ct.*) as sl 
                from icsc_denghithanhtoan_vipham_vanchuyen_chitiet ct
                inner join icsc_denghithanhtoan_vanchuyen dn on dn.id=ct.phieu_id
                where so_phieu_vc=%s and dn.state!='cancel'"""%(order.id)
                cr.execute(query)
                for line in cr.dictfetchall():
                    val = line['sl'] or 0
                if val> 0:
                    res[order.id] = True
                else:
                    res[order.id]= False       
        return res
    _columns = {
      
       'name': fields.char('Số phiếu vi phạm', size=500,
            required=True, track_visibility='onchange'
            ,states={'cancel': [('readonly', True)]})  ,
     
       'phieu_vanchuyen': fields.many2one('icsc.phieu.vanchuyen','Phiếu vận chuyển', 
                                          track_visibility='onchange'
                                          ,states={'cancel': [('readonly', True)]},select=True),  
       'ly_do': fields.many2one('icsc.loai.phat', 'Lý do phạt', track_visibility='onchange'
                                ,states={'cancel': [('readonly', True)]}),  
        'ngay_lap': fields.date('Ngày', track_visibility='onchange'
                                ,states={'cancel': [('readonly', True)]}),  
        'ngay_phat': fields.date('Ngày lập biên bản', track_visibility='onchange'
                                 ,states={'cancel': [('readonly', True)]}),  
        'congty_vc': fields.many2one('res.partner', 'Công ty vận chuyển',
                                     domain=[('check','=',True),('supplier','=',True)], 
                                     track_visibility='onchange'
                                      ,states={'cancel': [('readonly', True)]}),  
        'donvi_nhanhang': fields.many2one('res.partner', 'Đơn vị nhận hàng',
                                          domain=[('customer','=',True)], 
                                          track_visibility='onchange'
                                          ,states={'cancel': [('readonly', True)]},select=True),  
        'khach_hang': fields.many2one('res.partner', 'Vận chuyển cho khách hàng',domain=[('customer','=',True)], 
                                      track_visibility='onchange'
                                      ,states={'cancel': [('readonly', True)]},select=True),  
        'state': fields.selection([
            ('draft', 'Chưa xử lý'),
            ('confirm', 'Xác nhận'),
            ('done', 'Đã xử lý'),
            ('cancel', 'Đã hủy'),
            
            
            ], 'Trạng thái', readonly=True, track_visibility='onchange'),         
    
        'ghi_chu': fields.text('Ghi chú', track_visibility='onchange')  ,    
           
         'chitiet_phat': fields.one2many('icsc.phieuvipham.vanchuyen.chitiet',
                                          'phieu_id','Chi tiết'
                                           ,states={'cancel': [('readonly', True)]}),  
           'ngay_vc': fields.date('Ngày vận chuyển', track_visibility='onchange'
                                  ,states={'cancel': [('readonly', True)]}),  
         'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng tiền',
            store={
                'icsc.phieuvipham.vanchuyen': (lambda self, cr, uid, ids, c={}: ids, ['chitiet_phat'], 10),
                'icsc.phieuvipham.vanchuyen.chitiet': (_get_order, ['don_gia', 'gia_cuoc', 'so_luong', 'thanh_tien'], 10),
            },
            multi='sums', help="The total amount."),
         'duavao_vipham': fields.boolean('Đã tải sản phẩm từ PVC'
                                         ,states={'done': [('readonly', True)],'confirm': [('readonly', True)]}),   
        'check_dntt': fields.function(_get_check_DNTT,type='boolean',string='Check readonly'), 
    }
  
    _defaults= {
                'ly_do': get_count_id,
                 'duavao_vipham': False,
                'state':'draft',
                'ngay_lap':time.strftime('%Y-%m-%d'),
                'name': lambda self, cr, uid, c: self.pool.get('sequence.custormize.hopdong.vipham').get_name(cr, uid, 'icsc.phieuvipham.vanchuyen'  , 'icsc_phieuvipham_vanchuyen',''),
                }
    def unlink(self, cr, uid, ids, context=None):
        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in sale_orders:
            if s['state'] in ['draft', 'cancel']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Lỗi!'), _('Bạn chỉ có thể xóa Phiếu VPVC ở trạng thái Dự thảo và Đã hủy!'))

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

    def action_load_tu_phieu_vc(self, cr, uid, ids, context=None):
        phieu_chitiet=self.pool.get('icsc.phieuvipham.vanchuyen.chitiet')
        for data in self.browse(cr, uid, ids, context):
            id1=data.id
            cr.execute("""delete from icsc_phieuvipham_vanchuyen_chitiet where phieu_id= """+str(id1))
            for line in data.phieu_vanchuyen.chitiet_vc:
                product_id=line.product_id.id
                don_vi=line.don_vi.id
                gia_cuoc=line.thanh_tien
                don_gia=line.product_id.list_price
                vc_id=data.phieu_vanchuyen.id
                query_gia=""" select l.id,l.product_id,l.price_unit
                            from icsc_phieu_vanchuyen vc 
                            left join icsc_hopdong_vanchuyen_giacuoc_kehoach khvc on khvc.id=vc.kehoach_vanchuyen
                            left join sale_order o on o.id=khvc.sale_id
                            left join sale_order_line l on l.order_id=o.id
                            where vc.id= """+str(vc_id)
                cr.execute(query_gia)
                for item_gia in cr.dictfetchall():
                    product_ids=item_gia['product_id']
                    price_unit=item_gia['price_unit']
                    line_id=item_gia['id']
                    tax_amount=0
                    line_object=self.pool.get('sale.order.line').browse(cr, uid, line_id, context)
                    for tax_id in line_object.tax_id:
                        tax=tax_id.id
                        thue_objet=self.pool.get('account.tax').browse(cr, uid, tax, context)
                        tax_amount=thue_objet.amount
                    if product_id==product_ids:
                        don_gia=round(price_unit+(price_unit*tax_amount))
                    
                phieu_chitiet.create(cr, uid, {
                                               'product_id': product_id,                                                                                                           
                                               'don_vi': don_vi,
                                               'phieu_id':data.id,                                               
                                               'gia_cuoc':gia_cuoc,
                                               'don_gia':don_gia,
                                               }, context=context)
            self.write(cr, uid, data.id, {'duavao_vipham':True,}, context)

        return True
    def phieu_vanchuyen(self, cr, uid, ids, phieu_vanchuyen,context=None):
        if not phieu_vanchuyen:
            return {}           
        phieu_vanchuyen_object=self.pool.get('icsc.phieu.vanchuyen').browse(cr, uid, phieu_vanchuyen)
        ngay_vc=phieu_vanchuyen_object.ngay_vc
        congty_vc=phieu_vanchuyen_object.congty_vc.id
        donvi_nhanhang=phieu_vanchuyen_object.donvi_nhanhang.id
        khach_hang=phieu_vanchuyen_object.khach_hang.id
        return {'value': {'congty_vc':congty_vc,                         
                          'donvi_nhanhang':donvi_nhanhang,'khach_hang':khach_hang,
                          'ngay_vc':ngay_vc,
                            'ngay_phat':ngay_vc,
                          }}
    def onchange_laixe(self, cr, uid, ids, lai_xe,context=None):
        if not lai_xe:
            return {}           
        sale_object=self.pool.get('res.partner').browse(cr, uid, lai_xe)
        giayphep_laixe=sale_object.giayphep_laixe        
        return {'value': {'giayphep_laixe':giayphep_laixe}}
    
    def action_confirm(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            
            id1=item.id
            self.write(cr, uid, id1, {'state':'confirm',}, context)
        return True
    def action_done(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            self.write(cr, uid, id1, {'state':'done',}, context)
        return True
    def action_cancel(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            count=0
            # kiem tra xem PVP van chuyen da duowc dua vao DE nghi thanh toan chua
            query="""select count(ct.*) 
                    from icsc_denghithanhtoan_vipham_vanchuyen_chitiet ct
                    left join icsc_denghithanhtoan_vanchuyen dn on dn.id=ct.phieu_id
                    where so_phieu_vc= """+str(id1)+""" and dn.state !='cancel' """
            cr.execute(query)
            for data in cr.dictfetchall():
                count +=data['count']
            if count>0:
                raise osv.except_osv(_('Lỗi!'), _('Bạn không thể hủy Phiếu vi phạm VC khi phiếu này đã được đưa vào giấy ĐNTT!'))
            self.write(cr, uid, id1, {'state':'cancel',}, context)
        return True
    def action_return(self, cr, uid, ids, context=None):
       
        for item in self.browse(cr, uid, ids, context):
            id1=item.id
            
            self.write(cr, uid, id1, {'state':'draft',}, context)
        return True
icsc_phieuvipham_vanchuyen()
class icsc_phieuvipham_vanchuyen_chitiet(osv.osv):
    _description="icsc_phieuvipham_vanchuyen_chitiet"
    _name = 'icsc.phieuvipham.vanchuyen.chitiet'
    _inherit = ['mail.thread']
    
    def _thanh_tien(self, cr, uid, ids, name=None, args=None, context=None):
        res={}
        count=0
        if context is None:
            context = {}
        #Thành tiền = đơn giá * số lượng hao hụt + giá cước * số lượng hao hụt.
        for data in self.browse(cr, uid, ids, context):
            count=data.don_gia*data.so_luong+data.gia_cuoc*data.so_luong
            res[data.id]=count
        return res
    _columns = {
      
        'name': fields.char('Chi tiết KHVC', size=500,
            )  ,        
        'product_id': fields.many2one('product.product', 'Sản phẩm', ondelete='cascade'),  
        'don_vi': fields.many2one('product.uom', 'Đơn vị', ondelete='cascade'),  
        'so_luong': fields.float('Số lượng hao hụt', digits=(15,3)),  
        'don_gia': fields.float('Giá có thuế'),  
        'phieu_id': fields.many2one('icsc.phieuvipham.vanchuyen', 'Phiếu vi phạm', ondelete='cascade'),  
        'gia_cuoc': fields.float('Giá cước'),   
        'thanh_tien': fields.function(_thanh_tien, type='float',string='Thành tiền'),     
    }
   
icsc_phieuvipham_vanchuyen_chitiet()
class sale_order_line(osv.osv):
    _description="Sales Order Line"
    _inherit = 'sale.order.line'
    def get_soluong_ton_khvc(self, cr, uid, ids, name=None, args=None, context=None):
        res={}        
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            query_check="""select coalesce(sum(kl_vc_kehoach),0) as tong
             from icsc_hopdong_vanchuyen_chitiet ct 
             left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
             where ((coalesce(trung_chuyen,False)=False  and coalesce(parent_id,False)=False) or (coalesce(trung_chuyen,False)=True  and coalesce(parent_id,False)=True))
                         and coalesce(kehoach_cha,0)=0 and 
            sale_order_line= """+str(data.id)+""" and kh.state !='cancel'"""
            cr.execute(query_check)
            for check in cr.dictfetchall():
                tong =check['tong']
            res[data.id]=data.product_uom_qty - tong
        return res
    _columns = {   
               
                'ton_khvc': fields.function(get_soluong_ton_khvc, type='float',digits_compute= dp.get_precision('Product UoS'), string='KL Còn lại/LXH'),
               
                }
sale_order_line()   