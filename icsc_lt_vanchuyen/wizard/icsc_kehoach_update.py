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

class icsc_kehoach_update(osv.osv):
    _name = 'icsc.kehoach.update'
    _description = 'Sua doi KHVC'
    _columns = {
         'name': fields.char('Tên',size=256)  , 
        'user_id' : fields.many2one('res.users', 'Người cập nhật'),  
        'kehoach_id' : fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Kế hoạch vận chuyển', ondelete="cascade"),
        'dien_giai': fields.text('Diễn giải')  , 
        'ngay_capnhat': fields.date('Ngày cập nhật'),     
        'line_ids' : fields.one2many('icsc.kehoach.update.line','parent_id','Chi tiết kế hoạch' ),      
        'tu_diem': fields.many2one('res.partner', 'Đơn hàng từ điểm' ),
        'den_diem': fields.many2one('res.partner', 'Đơn hàng đến điểm' ),
        'cuoc_tu_diem': fields.many2one('res.country.diadiem', 'Tính cước từ điểm', ondelete="cascade"),
        'cuoc_den_diem': fields.many2one('res.country.diadiem', 'Tính cước đến điểm', 
                                         domain=[('van_chuyen','=',True)],
                                         ondelete="cascade"),
        'trung_chuyen': fields.boolean('Có trung chuyển'),
        'congty_vc': fields.many2one('res.partner', 'Tên nhà vận chuyển',domain=[('check','=',True),('supplier','=',True)], ondelete="cascade"),
         'state': fields.selection([
            ('draft', 'Chưa thực hiện'),
            ('confirm', 'Xác nhận'),
             ('process', 'Đang vận chuyển'),
            ('done', 'Hoàn tất'),
            ('cancel', 'Đã hủy'),
            
            
            ], 'Trạng thái', readonly=True ), 
        'so_khvc': fields.many2one('icsc.hopdong.vanchuyen','Số HĐVC',domain="[('check','=',True),('congty_vc','=',congty_vc)]")  ,
        'loai_khvc': fields.selection([
            ('vat', 'VAT'),  
            ('gui_ban', 'Gửi hàng có đảm bảo'),
            ('kho_tap_trung', 'Gửi kho tập trung'),      
            ('kho_dai_ly', 'Hàng nguyên liệu gia công'),            
           ], 'Loại kế hoạch vận chuyển',required=True), 
        'kiem_soat': fields.many2one('res.country.tramkiemsoat', 'Trạm kiểm soát' ),
          'chang_khvc': fields.selection([
            ('chang_1', 'Chặng 1'),  
            ('chang_2', 'Chặng 2'),                    
           ], 'Chặng vận chuyển',), 
          'phuongthuc_vc': fields.selection([                
            ('duongsat_chuyentuyen', 'Đường sắt + Đường bộ'), 
             ('duongsat_thongthuong', 'Đường sắt'), 
            ('duongbo', 'Đường bộ'),          
            ('duongthuy', 'Đường thủy + Đường bộ'),             
            
            ], 'Phương thức vận chuyển',required=True), 
         'ngay_lap': fields.date('Ngày lập KHVC',required=True),
         'giam_sat_kho': fields.many2one('icsc.giamsatkho', 'Giám sát kho'),
       
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
        res = super(icsc_kehoach_update, self).default_get(cr, uid, fields, context=context) 
        if picking_obj.id:
            kehoach_id=picking_obj.id
            loai_khvc=picking_obj.loai_khvc
            kiem_soat=picking_obj.kiem_soat.id
            chang_khvc=picking_obj.chang_khvc
            phuongthuc_vc=picking_obj.phuongthuc_vc
            ngay_lap=picking_obj.ngay_lap
            # lay dien giai
            dien_giai=""
            query="""select coalesce(dien_giai,' ') as dien_giai from icsc_khvc_thongbao_kho  where so_khvc=%s """%(kehoach_id)
            cr.execute(query)
            for item in cr.dictfetchall():
                dien_giai+=","+item['dien_giai']
            # end
            for line in picking_obj.chitiet_kh:
                #vals.append(line.id)
                vals.append({'product_id':line.product_id.id,
                             'dia_chi_giao': line.dia_chi_giao.id, 
                             'name': line.name,
                             'chitiet_kh':line.id,
                             'kl_vc_dukien':line.kl_vc_kehoach,
                             'kl_vc_kehoach':line.kl_vc_kehoach,
                             'kl_can_vanchuyen':line.kl_can_vanchuyen,
                             'kl_vc_conlai':line.kl_vc_conlai,
                             'kl_dangvc_dukien':line.kl_dangvc_dukien,
                             })
            if 'dien_giai' in fields:
                res.update({'dien_giai': dien_giai})
            if 'chang_khvc' in fields:
                res.update({'chang_khvc': chang_khvc})
            if 'ngay_lap' in fields:
                res.update({'ngay_lap': ngay_lap})
            if 'phuongthuc_vc' in fields:
                res.update({'phuongthuc_vc': phuongthuc_vc})
            if 'kehoach_id' in fields:
                res.update({'kehoach_id': kehoach_id})    
            if 'kiem_soat' in fields:
                res.update({'kiem_soat': kiem_soat})  
            if 'name' in fields:
                res.update({'name': 'Lịch sử sửa KHVC'})   
            if 'loai_khvc' in fields:
                res.update({'loai_khvc': loai_khvc})            
            if 'line_ids' in fields:
                res.update({'line_ids': vals})  
            if 'ngay_capnhat' in fields:
                res.update({'ngay_capnhat': time.strftime('%Y-%m-%d')})
            if 'tu_diem' in fields:
                res.update({'tu_diem': picking_obj.tu_diem.id})            
            if 'den_diem' in fields:
                res.update({'den_diem': picking_obj.den_diem.id}) 
            if 'cuoc_tu_diem' in fields:
                res.update({'cuoc_tu_diem': picking_obj.cuoc_tu_diem.id})            
            if 'cuoc_den_diem' in fields:
                res.update({'cuoc_den_diem': picking_obj.cuoc_den_diem.id}) 
            if 'trung_chuyen' in fields:
                res.update({'trung_chuyen': picking_obj.trung_chuyen}) 
            if 'congty_vc' in fields:
                res.update({'congty_vc': picking_obj.congty_vc.id})
            if 'giam_sat_kho' in fields:
                if picking_obj.giam_sat_kho:
                    res.update({'giam_sat_kho': picking_obj.giam_sat_kho.id})
            state=picking_obj.state
            if 'state' in fields:
                res.update({'state': state})
            if 'so_khvc' in fields:
                res.update({'so_khvc': picking_obj.so_khvc.id})
            if 'user_id' in fields:
                res.update({'user_id': uid}) 
        return res
    def load_hop_dong(self, cr, uid, ids, congty_vc, context=None):
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
    def check_move(self, cr, uid, chitiet_kh,picking_id,chenh_lech1):
        qty_move=0
        # kiem tra xem có PXK nao con co the sua duoc k?
        query_checkmove="""select m.id,picking_id, coalesce(m.product_qty,0) as product_qty
              from stock_move m
              inner join stock_picking p on p.id=m.picking_id
              where m.chitiet_kh=%s  and p.state not in ('done','cancel')
              and coalesce(mistake_delivery,False)=False and picking_id!=%s
              and m.product_qty - coalesce(%s,0) >=0
              order by product_qty asc limit 1
               """%(chitiet_kh,picking_id,chenh_lech1)
        cr.execute(query_checkmove)
        for itemmove in cr.dictfetchall():
            qty_move +=itemmove['product_qty']
        return qty_move
    def get_balance(self, cr, uid, qty1, qty2):
        return qty1 + qty2
    def action_correct_delivery(self, cr, uid, ids,  context=None):
        a=[]
        p=[]
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach') 
        chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        thongbao_pool=self.pool.get('icsc.khvc.thongbao.kho')
        chitiet_thongbao_pool=self.pool.get('icsc.khvc.thongbao.kho.line')
        phieuvc_pool=self.pool.get('icsc.phieu.vanchuyen')
        move_pool=self.pool.get('stock.move')
        for data in self.browse(cr, uid, ids, context): 
            # cap nhat vao PVC
            phuongthuc_vc=data.phuongthuc_vc
            ngay_lap=data.ngay_lap           
            query_update_pt=""" update icsc_phieu_vanchuyen set phuongtien_vc= '%s' 
                            where kehoach_vanchuyen=%s """%(phuongthuc_vc,data.kehoach_id.id)
            cr.execute(query_update_pt)
            # lay id ke hoach, xac dinh cac con cua no
            kehoach_id=data.kehoach_id.id
            # xet trung chuyen
            trung_chuyen=data.trung_chuyen
            cuoc_den_diem=data.cuoc_den_diem.id
            cuoc_tu_diem=data.cuoc_tu_diem.id
            congty_vc=data.congty_vc.id
            so_khvc=data.so_khvc.id
            kiem_soat=data.kiem_soat.id
            giam_sat_kho=False
            if data.giam_sat_kho:
                giam_sat_kho=data.giam_sat_kho.id
            #if trung_chuyen==False: 
            # lay tat ca phieu van chuyen cua KHVC
            for phieu in data.kehoach_id.phieuvc_lines:
                pvc_id=phieu.id
                phieuvc_pool.write(cr, uid, [pvc_id], {'giam_sat_kho':giam_sat_kho,'kiem_soat':kiem_soat,'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem}, context=context)
            kehoach_pool.write(cr, uid, [kehoach_id], {'giam_sat_kho':giam_sat_kho,'ngay_lap':ngay_lap,'nhan_hang_tn':ngay_lap,'phuongthuc_vc':phuongthuc_vc,'kiem_soat':kiem_soat,'loai_khvc':data.loai_khvc,'so_khvc':so_khvc,'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem,'congty_vc':congty_vc,'dien_giai':data.dien_giai}, context=context)
            
            # gui thong bao ve kho
            dien_giai=data.dien_giai
            conty_vc=False
            if data.kehoach_id.congty_vc:
                conty_vc=data.kehoach_id.congty_vc.id
            sale_id=False
            if data.kehoach_id.sale_id:
                sale_id=data.kehoach_id.sale_id.id
            name= self.pool.get('sequence.custormize.thongbao').get_name(cr, uid, 'icsc.khvc.thongbao.kho','icsc_khvc_thongbao_kho')  or '/'
            thongbao_id=thongbao_pool.create(cr, uid, {
                                            'ngay_capnhat':time.strftime('%Y-%m-%d'),
                                             'name':name,
                                             'so_khvc':data.kehoach_id.id,
                                             'sale_id':sale_id, 
                                             'congty_vc' :conty_vc,  
                                             'dien_giai':dien_giai,                                                                                
                                            
                                             }, context=context) 
            for ct_xuatkho in data.kehoach_id.xuatkho_lines:
                cr.execute("""INSERT INTO icsc_khvc_thongbao_kho_rel(
                                        thongbao_id, picking_id)
                                VALUES (%s, %s)""",(thongbao_id,ct_xuatkho.id,)) 
            c=[]
            for line in data.line_ids: 
                chenh_lech=0   
                kl_vc_kehoach=line.kl_vc_kehoach 
                # chi tiet duoc thay doi
                chitiet_kh=line.chitiet_kh
                sale_order_line=chitiet_kh.sale_order_line.id
                product_id=line.product_id.id
                # kiem tra so luong
                so_luong_cu=chitiet_kh.kl_vc_kehoach
                so_luong_moi=kl_vc_kehoach
                kl_dangvc_dukien=chitiet_kh.kl_dangvc_dukien
                if round(so_luong_moi,2)<round(kl_dangvc_dukien,2):
                    raise osv.except_osv(_("Thông báo!"), _("Khối lượng kế hoạch phải >= khối lượng đang vận chuyển trên KHVC"))
                kl_dangvc=line.chitiet_kh.kl_dangvc
                kl_vc_kehoach=line.chitiet_kh.kl_vc_kehoach
                tong=kl_vc_kehoach - kl_dangvc
                if round(so_luong_moi,2)< round(tong,2):
                    raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết chi tiết KHVC khi số lượng KH sửa đổi < số lượng đang vận chuyển. Khối lượng sửa đổi tối thiểu = %s") %(tong))               
                    
                # kiem tra kl dang vc = kl vc kh
                dk=chitiet_kh.kl_dangvc_dukien
                kh=chitiet_kh.kl_vc_kehoach
                if dk==kh:
                    if round(so_luong_moi,2)<round(kh,2):
                        raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết chi tiết KHVC khi số lượng KH = số lượng đang vận chuyển."))               
                    
                # lay so luong thay doi
                chenh_lech=so_luong_moi-so_luong_cu
                # lay nhung ke hoach dang sau no
                kehoach_vanchuyen=line.parent_id.kehoach_id.id
                sale_id=line.parent_id.kehoach_id.sale_id.id 
                kehoach_sau=False
                query_kiemtra2="""select ct.* from icsc_hopdong_vanchuyen_chitiet ct 
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                where ct.sale_order_line= """+str(sale_order_line)+""" and kh.sale_id= """+str(sale_id)+""" and coalesce(kh.kehoach_cha,0)=0 and kh.id > """+str(kehoach_vanchuyen)+""" order by kh.id asc """
                cr.execute(query_kiemtra2)
                for item_kiemtra2 in cr.dictfetchall():
                    # lay ke hoach ke tiep 
                    kehoach_sau= item_kiemtra2['id']
                    # lay chi tiet cua ke hoach do
                    next_chitiet=chitiet_pool.browse(cr, uid, kehoach_sau, context)
                    #for next_chitiet in kh_next.chitiet_kh:
                    kl_suadoi=soluong_next=0
                    sale_order_line_next=next_chitiet.sale_order_line.id
                    product_id_next=next_chitiet.product_id.id
                    soluong_next=next_chitiet.kl_can_vanchuyen
                    kl_suadoi=soluong_next-chenh_lech
                    sale_order_line_next=next_chitiet.sale_order_line.id
                    product_id_next=next_chitiet.product_id.id
                    soluong_next=next_chitiet.kl_can_vanchuyen
                    kl_suadoi=soluong_next-chenh_lech
                    if sale_order_line_next==sale_order_line and product_id_next==product_id and chenh_lech!=0:                           
                        chitiet_pool.write(cr, uid, [next_chitiet.id], {'kl_can_vanchuyen':kl_suadoi}, context=context)
                        kl_suadoi=0
                # XET KHVC CHA
                if data.kehoach_id.parent_id:
                    # lay tat ca KHVC con -->cap nhat loai KHVC
                    # END
                    query_con= """ select ct.*,kh.chang_khvc from icsc_hopdong_vanchuyen_chitiet ct 
                       left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                        where ct.sale_order_line= """+str(sale_order_line)+""" 
                        and coalesce(kh.kehoach_cha,0)= """+ str(kehoach_id)+ """ order by kh.id asc """
                    cr.execute(query_con)
                    for item_con in cr.dictfetchall():
                        
                        # lay ke hoach ke tiep 
                        kehoach_sau= item_con['id']
                        chang_khvc=item_con['chang_khvc']
                        # lay chi tiet cua ke hoach do
                        next_chitiet_con=chitiet_pool.browse(cr, uid, kehoach_sau, context)
                        #for next_chitiet in kh_next.chitiet_kh:
                        kl_suadoicon=soluong_nextcon=0.0
                        sale_order_line_next_con=next_chitiet_con.sale_order_line.id
                        product_id_next=next_chitiet_con.product_id.id
                        soluong_con_next=next_chitiet_con.kl_can_vanchuyen
                        kl_suadoicon=soluong_nextcon-chenh_lech   
                        kl_vc_conlai=chitiet_kh.kl_vc_conlai+chenh_lech                
                        if chang_khvc=='chang_1':
                            if product_id_next==product_id and chenh_lech!=0:                           
                                chitiet_pool.write(cr, uid, [next_chitiet_con.id], {'kl_vc_dukien':so_luong_moi}, context=context)
                                kl_suadoicon=0.0
                        else:
                            if product_id_next==product_id and chenh_lech!=0:                           
                                #chitiet_pool.write(cr, uid, [next_chitiet_con.id], {'kl_vc_kehoach':so_luong_moi}, context=context)
                                query_update=""" update icsc_hopdong_vanchuyen_chitiet
                                                set kl_vc_kehoach = %s ,
                                                kl_vc_conlai= %s
                                                where id= %s """%(so_luong_moi,kl_vc_conlai,next_chitiet_con.id,)
                                cr.execute(query_update)
                                kl_suadoicon=0.0
                if chenh_lech!=0:
                    chitiet_pool.write(cr, uid, [chitiet_kh.id], {'kl_vc_kehoach':so_luong_moi}, context=context)
                    chitiet_thongbao_pool.create(cr, uid, {
                                            'parent_id':thongbao_id,
                                             'chitiet_kh':chitiet_kh.id,
                                             'dia_chi_giao':chitiet_kh.dia_chi_giao.id,
                                             'sale_order_line':sale_order_line, 
                                             'product_id' :product_id,                                                                                  
                                            'kl_vc_kehoach_cu':so_luong_cu,
                                            'kl_vc_kehoach_moi':so_luong_moi,
                                             }, context=context)
                # neu ta ca phieu vc done-->khong cho sua
                # chinh sua: Cho sua va tao moi PXK
                kt_tontai=False
                kh_id=data.kehoach_id.id
                cr.execute(""" select * from stock_picking where kehoach_vanchuyen_id= """+str(kh_id)+""" and state not in ('cancel','done') and
                            coalesce(mistake_delivery,False)=False
                            order by id desc """)
                for item_tontai in cr.dictfetchall():
                    kt_tontai=True
                #if kt_tontai==False and chenh_lech!=0:
                    #raise osv.except_osv(_("Thông báo!"), _("Không thể sửa đổi số lượng trên dòng chi tiết chi tiết KHVC khi tất cả các PXK hoàn tất"))               
                if kt_tontai==False and chenh_lech!=0 and data.kehoach_id.parent_id!=True:
                    # TAO pxk
                    move_type='direct'
                    loai=False
                    loai_khvc=data.kehoach_id.sale_id.loai_lenh_xuat
                    if loai_khvc=='vat':
                        loai='thongthuong'
                    else:
                        loai='noibo'                    
                    seq_obj_name =  'stock.picking.' +loai
                    picking_name =  self.pool.get('sequence.custormize.pickingout').get_name(cr, uid, seq_obj_name, 'stock_picking',loai)
                    company_id=self.pool.get('res.users').browse(cr, uid, uid).company_id.id
                    picking_pool = self.pool.get('stock.picking.out') 
                    partner_obj=data.kehoach_id.khach_hang
                    if partner_obj:
                        partner_id =partner_obj.id
                    #la ke hoach con
                    doitac_giaohang=False
                    if data.kehoach_id.kehoach_cha:                        
                        partner_id=data.kehoach_id.kehoach_cha.khach_hang.id
                    doitac_giaohang_obj=data.kehoach_id.congty_vc
                    if doitac_giaohang_obj:
                        doitac_giaohang=doitac_giaohang_obj.id
                    if doitac_giaohang==False:
                        doitac_giaohang=partner_id
                    khoxuat_id=data.kehoach_id.sale_id.kho_xuat_id.id
                    type_kho=data.kehoach_id.sale_id.type_kho
                    # tao stock_picking
                    cl=0
                    for line_donetest in data.line_ids:                       
                           
                        # kiem tra so luong
                        so_luong_cu=line_donetest.chitiet_kh.kl_vc_kehoach
                        so_luong_moi=line_donetest.kl_vc_kehoach    
                        # lay so luong thay doi
                        cl +=so_luong_moi-so_luong_cu
                    if cl!=0:
                        picking_id_done=picking_pool.create(cr, uid, {
                                                 'partner_id':partner_id,
                                                 'sale_id':sale_id,
                                                 'doitac_giaohang':doitac_giaohang,
                                                 'date':datetime.now(),                                           
                                                 'loai_xuatkho':loai,
                                                 'kehoach_vanchuyen_id':data.kehoach_id.id,
                                                 'khoxuat_id':khoxuat_id,
                                                 'move_type':move_type,
                                                 'company_id':company_id, 
                                                 'type':'out' ,  
                                                 'type_kho':type_kho,
                                                 'nguoi_lap_phieu':uid,                                                                             
                                                 }, context=context)
                    # end
                    # query
                    for line_done in data.line_ids: 
                        
                        query_truoc=""" select location_id, location_dest_id from stock_move
                        where chitiet_kh=%s order by id desc limit 1"""%(line_done.chitiet_kh.id)
                        cr.execute(query_truoc)
                        for move_truoc in cr.dictfetchall():
                            location_id=move_truoc['location_id']
                            location_dest_id=move_truoc['location_dest_id']
                            # end      
                            chenh_lech=0   
                            # kiem tra so luong
                            so_luong_cu=line_done.chitiet_kh.kl_vc_kehoach
                            so_luong_moi=line_done.kl_vc_kehoach    
                            # lay so luong thay doi
                            chenh_lech=so_luong_moi-so_luong_cu
                            
                            if chenh_lech>0:
                                move_pool.create(cr, uid, {
                                           'origin':line_done.product_id.name,
                                           'product_uos_qty':chenh_lech,                                                                  
                                           'product_uom': line_done.product_id.uom_id.id,
                                           'price_unit': line_done.chitiet_kh.sale_order_line.price_unit,
                                           'date_expected':  datetime.now(),
                                           'product_qty': chenh_lech,
                                           'product_uos':line_done.product_id.uom_id.id,
                                           'location_id': location_id,
                                           'name': line_done.product_id.name,
                                           'product_id': line_done.product_id.id,                                                        
                                           'partner_id':partner_id,
                                           'company_id':company_id,                                                          
                                           'picking_id':picking_id_done,                                                                                                                      
                                           'state': 'draft',
                                           'location_dest_id':location_dest_id,
                                           'sale_line_id':line_done.chitiet_kh.sale_order_line.id,                                                         
                                           'chitiet_kh': line_done.chitiet_kh.id,
                                           'doitac_giaohang':line_done.chitiet_kh.dia_chi_giao.id
                                           }, context=context) 
                                a.append(line_done.chitiet_kh.id)
                                
                           
                # end
                #cap nhat lai so luong tren PXK tuong ung
                # TH2: Ton tai dong chi tiet
                if kt_tontai==True and chenh_lech!=0 and data.kehoach_id.parent_id!=True:
                    picking_pool=self.pool.get('stock.picking')            
                    query_kho="""select id, state from stock_picking
                                where kehoach_vanchuyen_id = """+str(kehoach_id)+""" and 
                                state not in ('cancel','done') and
                                coalesce(mistake_delivery,False)=False
                                order by id desc --limit 1 """
                    cr.execute(query_kho)                
                    for item_kho in cr.dictfetchall():
                        # xet bien dem
                        state=item_kho['state']
                        picking_id=item_kho['id']
                        picking_obj=picking_pool.browse(cr, uid, picking_id, context)
                        for line_move in data.line_ids:  
                            count=0               
                            kl_vc_kehoach=line_move.kl_vc_kehoach
                            so_luong_cu1=line_move.chitiet_kh.kl_vc_kehoach
                            so_luong_moi1=kl_vc_kehoach 
                            chenh_lech1=so_luong_moi1 - so_luong_cu1
                            product_id_line=line_move.product_id.id
                            # kiem tra co stock move k?
                            check_stockmove=False
                            query_kho_move="""select id
                                from stock_move                                
                                where chitiet_kh = %s and 
                                  picking_id=%s and state !='cancel'
                                order by id desc limit 1 """ %(line_move.chitiet_kh.id,picking_obj.id)
                            cr.execute(query_kho_move) 
                            for check_move in cr.dictfetchall():
                                check_stockmove=True
                            for move in picking_obj.move_lines:
                                #checkm=False
                                soluong_nextcon1=move.product_qty
                                chitiet_kh=move.chitiet_kh.id
                                product_id_move=move.product_id.id
                                if chenh_lech1 >= 0 :
                                    kl_suadoicon = soluong_nextcon1 + chenh_lech1
                                else:
                                    kl_suadoicon = soluong_nextcon1 - abs(chenh_lech1)
                                check=False
                                if move.state !='cancel' and chitiet_kh not in a :                          
                                    if chitiet_kh==line_move.chitiet_kh.id and product_id_move==product_id_line and chitiet_kh not in a:                                 
                                        #if kl_suadoicon<0: 22/10
                                        #    raise osv.except_osv(_("Thông báo!"), _("Số lượng ở  PXK tương ứng sau khi thay đổi sẽ bị < 0. Vui lòng điều chỉnh lại số lượng."))
                                        if round(soluong_nextcon1,2) + round(chenh_lech1,2)>=0:
                                            move_pool.write(cr,uid, [move.id], {'product_qty':kl_suadoicon,'product_uos_qty':kl_suadoicon}, context=context)
                                        else: #22/10
                                            # kiem tra xem có PXK nao con co the sua duoc k?
                                            xet_move=abs(chenh_lech1)-soluong_nextcon1
                                            qty_move=self.check_move(cr, uid, chitiet_kh, picking_obj.id,xet_move)
                                            slmoimove=kl_suadoicon + qty_move                                                                                    
                                            if  round(soluong_nextcon1,2) + round(chenh_lech1,2)>=0 and chitiet_kh not in a  and picking_obj.id not in p: #and line.product_qty==dagiao:
                                                
                                                query_checkmove="""select m.id,picking_id, coalesce(m.product_qty,0) as product_qty
                                                  from stock_move m
                                                  inner join stock_picking p on p.id=m.picking_id
                                                  where m.chitiet_kh=%s  and p.state not in ('done','cancel')
                                                  and coalesce(mistake_delivery,False)=False 
                                                  and picking_id!= %s and m.product_qty - coalesce(%s,0)>=0
                                                  order by m.product_qty asc """%(chitiet_kh,picking_obj.id,xet_move)
                                                cr.execute(query_checkmove)
                                                for itemmove in cr.dictfetchall():
                                                    if check==False and itemmove['product_qty']>=slmoimove:    
                                                        move_pool.write(cr, uid, [itemmove['id']], {'product_qty':slmoimove,'product_uos_qty':slmoimove}, context=context)                                       
                                                        c.append(chitiet_kh)
                                                        check=True
                                                    #picking_pool.write(cr, uid, [picking_obj.id], {'state':'cancel'}, context=context) 
                                                p.append(picking_obj.id)   
                                                move_pool.write(cr, uid, [move.id], {'state':'cancel'}, context=context)   
                                                #move_pool.write(cr, uid, [move.id], {'product_qty':lech_cuoi,'product_uos_qty':lech_cuoi}, context=context)   
                                                c.append(chitiet_kh)
                                            else:
                                                if round(soluong_nextcon1,2) + round(chenh_lech1,2) < 0:
                                                    raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết bán hàng số lượng mà PXK tương ứng sau khi thay đổi sẽ bị < 0. Vui lòng điều chỉnh lại số lượng. " ))
                                        #cr.execute("""update stock_move set product_qty = """+str(kl_suadoicon)+""" where id= """+str(move.id))
                                        c.append(chitiet_kh)
                                        a.append(chitiet_kh)
                                        count +=1
                                    state_move='draft'
                                    if state!='draft':
                                        state_move='assigned'   
                                    if check_stockmove==False and count==0 and chenh_lech1!=0 and move.chitiet_kh.id not in a:
                                        # insert them dong    
                                        # lay location va location desc duoc danh truoc do
                                        # query
                                        query_truoc=""" select location_id, location_dest_id from stock_move
                                        where chitiet_kh=%s order by id desc limit 1"""%(line_move.chitiet_kh.id)
                                        cr.execute(query_truoc)
                                        for move_truoc in cr.dictfetchall():
                                            location_id=move_truoc['location_id']
                                            location_dest_id=move_truoc['location_dest_id']
                                            # end 
                                            if   chenh_lech1>0:   
                                                move_pool.create(cr, uid, {
                                                       'origin':picking_obj.name,
                                                       'product_uos_qty':chenh_lech1,                                                                  
                                                       'product_uom': line_move.product_id.uom_id.id,
                                                       'price_unit': line_move.chitiet_kh.sale_order_line.price_unit,
                                                       'date_expected':  datetime.now(),
                                                       'product_qty': chenh_lech1,
                                                       'product_uos':line_move.product_id.uom_id.id,
                                                       'location_id': location_id,
                                                       'name': line_move.product_id.name,
                                                       'product_id': line_move.product_id.id,                                                        
                                                       'partner_id':picking_obj.partner_id.id,
                                                       'company_id':picking_obj.company_id.id ,                                                          
                                                       'picking_id':picking_id,                                                                                                                      
                                                       'state':state_move,
                                                       'location_dest_id':location_dest_id,
                                                       'sale_line_id':line_move.chitiet_kh.sale_order_line.id,                                                         
                                                       'chitiet_kh': line_move.chitiet_kh.id,
                                                       'doitac_giaohang':line_move.chitiet_kh.dia_chi_giao.id
                                                       }, context=context)
                                                a.append(line_move.chitiet_kh.id)
                                            else:
                                                raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết khi số lượng sau khi sửa đổi: %s <= 0")%(chenh_lech1))               
                              
                # neu khong co move line - PXK trong
                if kt_tontai and a.__len__()==0:
                    # kiem tra PXK rong
                    state_null='draft'                
                    picking_pool_null=self.pool.get('stock.picking')            
                    query_kho_null="""select id, state from stock_picking
                                where kehoach_vanchuyen_id = """+str(kehoach_id)+""" and 
                                state not in ('cancel','done') and
                                coalesce(mistake_delivery,False)=False
                                order by id desc --limit 1 """
                    cr.execute(query_kho_null)
                    for item_kho_null in cr.dictfetchall():
                        state_null=item_kho_null['state']
                        picking_obj_null=picking_pool_null.browse(cr, uid, item_kho_null['id'], context)
                        for line_move_null in data.line_ids:
                            kl_vc_kehoach=line_move_null.kl_vc_kehoach
                            so_luong_cu1=line_move_null.chitiet_kh.kl_vc_kehoach
                            so_luong_moi1=kl_vc_kehoach 
                            chenh_lech1=so_luong_moi1-so_luong_cu1                           
                            kl_suadoicon=chenh_lech1
                            product_id_line=line_move_null.product_id.id
                            # kiem tra co stock move k?
                            check_stockmove=False
                            query_kho_move_null="""select id
                                from stock_move                                
                                where chitiet_kh = %s and 
                                  picking_id=%s and state !='cancel'
                                order by id desc limit 1 """ %(line_move_null.chitiet_kh.id,item_kho_null['id'])
                            cr.execute(query_kho_move_null) 
                            for check_move_null in cr.dictfetchall():
                                check_stockmove=True
                            if check_stockmove==False and chenh_lech1!=0:
                                    # insert them dong    
                                    # lay location va location desc duoc danh truoc do
                                    # query
                                    query_truoc=""" select location_id, location_dest_id from stock_move
                                    where chitiet_kh=%s order by id desc limit 1"""%(line_move_null.chitiet_kh.id)
                                    cr.execute(query_truoc)
                                    for move_truoc in cr.dictfetchall():
                                        location_id=move_truoc['location_id']
                                        location_dest_id=move_truoc['location_dest_id']
                                        # end    
                                        if state_null=='draft':
                                            state_move='draft'
                                        else:
                                            state_move='assigned'
                                        if chenh_lech1>0 and line_move_null.chitiet_kh.id not in a:  
                                            move_pool.create(cr, uid, {
                                                   'origin':picking_obj_null.name,
                                                   'product_uos_qty':chenh_lech1,                                                                  
                                                   'product_uom': line_move_null.product_id.uom_id.id,
                                                   'price_unit': line_move_null.chitiet_kh.sale_order_line.price_unit,
                                                   'date_expected':  datetime.now(),
                                                   'product_qty': chenh_lech1,
                                                   'product_uos':line_move_null.product_id.uom_id.id,
                                                   'location_id': location_id,
                                                   'name': line_move_null.product_id.name,
                                                   'product_id': line_move_null.product_id.id,                                                        
                                                   'partner_id':picking_obj_null.partner_id.id,
                                                   'company_id':picking_obj_null.company_id.id ,                                                          
                                                   'picking_id':item_kho_null['id'],                                                                                                                      
                                                   'state': state_move,
                                                   'location_dest_id':location_dest_id,
                                                   'sale_line_id':line_move_null.chitiet_kh.sale_order_line.id,                                                         
                                                   'chitiet_kh': line_move_null.chitiet_kh.id,
                                                   'doitac_giaohang':line_move_null.chitiet_kh.dia_chi_giao.id
                                                   }, context=context) 
                                            a.append(line_move_null.chitiet_kh.id)  
                                        else:
                                            raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết khi số lượng sau khi sửa đổi: %s <= 0")%(chenh_lech1))               
                    # insert them dong
                # end    
                        
                       
        return {'type': 'ir.actions.act_window_close'}
    def action_correct_delivery_chang1(self, cr, uid, ids,  context=None):
        a=[]
        c=[]
        p=[]
        i=0
        kehoach_pool = self.pool.get('icsc.hopdong.vanchuyen.giacuoc.kehoach') 
        chitiet_pool=self.pool.get('icsc.hopdong.vanchuyen.chitiet')
        thongbao_pool=self.pool.get('icsc.khvc.thongbao.kho')
        chitiet_thongbao_pool=self.pool.get('icsc.khvc.thongbao.kho.line')
        phieuvc_pool=self.pool.get('icsc.phieu.vanchuyen')
        if i>0:
            return {'type': 'ir.actions.act_window_close'}
        for data in self.browse(cr, uid, ids, context): 
            i +=1
            # lay id ke hoach, xac dinh cac con cua no
            kehoach_id=data.kehoach_id.id
            ngay_lap=data.ngay_lap
            # cap nhat vao PVC
            phuongthuc_vc=data.phuongthuc_vc
            query_update_pt=""" update icsc_phieu_vanchuyen set phuongtien_vc= '%s' 
                            where kehoach_vanchuyen=%s """%(phuongthuc_vc,kehoach_id)
            cr.execute(query_update_pt)
            # xet trung chuyen
            trung_chuyen=data.trung_chuyen
            cuoc_den_diem=data.cuoc_den_diem.id
            cuoc_tu_diem=data.cuoc_tu_diem.id
            congty_vc=data.congty_vc.id
            so_khvc=data.so_khvc.id
            giam_sat_kho=False
            if data.giam_sat_kho:
                giam_sat_kho=data.giam_sat_kho.id
            kiem_soat=data.kiem_soat.id
            # lay tat ca phieu van chuyen cua KHVC
            for phieu in data.kehoach_id.phieuvc_lines:
                pvc_id=phieu.id
                phieuvc_pool.write(cr, uid, [pvc_id], {'giam_sat_kho':giam_sat_kho,'kiem_soat':kiem_soat,'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem}, context=context)
            #if trung_chuyen==False:
            if so_khvc:
                kehoach_pool.write(cr, uid, [kehoach_id], {'giam_sat_kho':giam_sat_kho,'dien_giai':data.dien_giai,'ngay_lap':ngay_lap,'nhan_hang_tn':ngay_lap,'phuongthuc_vc':phuongthuc_vc,'kiem_soat':kiem_soat,'loai_khvc':data.loai_khvc,'so_khvc':so_khvc,'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem,'congty_vc':congty_vc}, context=context)
            else:
                kehoach_pool.write(cr, uid, [kehoach_id], {'giam_sat_kho':giam_sat_kho,'dien_giai':data.dien_giai,'ngay_lap':ngay_lap,'nhan_hang_tn':ngay_lap,'phuongthuc_vc':phuongthuc_vc,'kiem_soat':kiem_soat,'loai_khvc':data.loai_khvc,'cuoc_tu_diem':cuoc_tu_diem,'cuoc_den_diem':cuoc_den_diem,'congty_vc':congty_vc}, context=context)
            # gui thong bao ve kho
            dien_giai=data.dien_giai
            conty_vc=False
            if data.kehoach_id.congty_vc:
                conty_vc=data.kehoach_id.congty_vc.id
            sale_id=False
            if data.kehoach_id.sale_id:
                sale_id=data.kehoach_id.sale_id.id
            name= self.pool.get('sequence.custormize.thongbao').get_name(cr, uid, 'icsc.khvc.thongbao.kho','icsc_khvc_thongbao_kho')  or '/'
            thongbao_id=thongbao_pool.create(cr, uid, {
                                            'ngay_capnhat':time.strftime('%Y-%m-%d'),
                                             'name':name,
                                             'so_khvc':data.kehoach_id.id,
                                             'sale_id':sale_id, 
                                             'congty_vc' :conty_vc,  
                                             'dien_giai':dien_giai,                                                                                
                                            
                                             }, context=context) 
            for ct_xuatkho in data.kehoach_id.xuatkho_lines:
                cr.execute("""INSERT INTO icsc_khvc_thongbao_kho_rel(
                                        thongbao_id, picking_id)
                            VALUES (%s, %s)""",(thongbao_id,ct_xuatkho.id,)) 
            for line in data.line_ids: 
                    chenh_lech=0   
                    kl_vc_kehoach=line.kl_vc_kehoach 
                    # chi tiet duoc thay doi
                    chitiet_kh=line.chitiet_kh
                    sale_order_line=chitiet_kh.sale_order_line.id
                    product_id=line.product_id.id
                    # kiem tra so luong
                    so_luong_cu=chitiet_kh.kl_vc_kehoach
                    so_luong_moi=kl_vc_kehoach
                    kl_dangvc_dukien=chitiet_kh.kl_dangvc_dukien
                    if so_luong_moi<kl_dangvc_dukien:
                        raise osv.except_osv(_("Thông báo!"), _("Khối lượng kế hoạch phải >= khối lượng đang vận chuyển trên KHVC"))
                    # kiem tra kl dang vc = kl vc kh
                    kl_dangvc=chitiet_kh.kl_dangvc
                    kl_vc_kehoach=chitiet_kh.kl_vc_kehoach
                    tong=kl_vc_kehoach - kl_dangvc
                    if so_luong_moi<tong:
                        raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết chi tiết KHVC khi số lượng KH sửa đổi < số lượng đang vận chuyển. Khối lượng sửa đổi tối thiểu = %s") %(kl_dangvc))               
                     
                    dk=chitiet_kh.kl_dangvc_dukien
                    kh=chitiet_kh.kl_vc_kehoach
                    if dk==kh:
                        if so_luong_moi<kh:
                            raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết chi tiết KHVC khi số lượng KH = số lượng đang vận chuyển."))               
                    if  data.kehoach_id.chang_khvc!= 'chang_2':
                        chitiet_pool.write(cr, uid, [chitiet_kh.id], {'kl_vc_kehoach':so_luong_moi}, context=context)
                    # lay so luong thay doi
                    chenh_lech=so_luong_moi-so_luong_cu
                    if chenh_lech!=0:
                        chitiet_thongbao_pool.create(cr, uid, {
                                                'parent_id':thongbao_id,
                                                 'chitiet_kh':chitiet_kh.id,
                                                 'dia_chi_giao':chitiet_kh.dia_chi_giao.id,
                                                 'sale_order_line':sale_order_line, 
                                                 'product_id' :product_id,                                                                                  
                                                'kl_vc_kehoach_cu':so_luong_cu,
                                                'kl_vc_kehoach_moi':so_luong_moi,
                                                 }, context=context)                  
                    
            # neu ta ca phieu vc done-->khong cho sua
            # chinh sua: Cho sua va tao moi PXK
            move_pool=self.pool.get('stock.move')
            picking_pool = self.pool.get('stock.picking.out') 
            kt_tontai=False
            kh_id=data.kehoach_id.id
            cr.execute(""" select * from stock_picking where kehoach_vanchuyen_id= """+str(kh_id)+""" and state not in ('cancel','done') and
                        coalesce(mistake_delivery,False)=False
                        order by id desc """)
            for item_tontai in cr.dictfetchall():
                kt_tontai=True            
            if kt_tontai==False:
                    # TAO pxk
                    move_type='direct'
                    loai=False
                    loai_khvc=data.kehoach_id.sale_id.loai_lenh_xuat
                    if loai_khvc=='vat':
                        loai='thongthuong'
                    else:
                        loai='noibo'                    
                    company_id=self.pool.get('res.users').browse(cr, uid, uid).company_id.id                    
                    partner_obj=data.kehoach_id.khach_hang
                    if partner_obj:
                        partner_id =partner_obj.id
                    #la ke hoach con
                    if data.kehoach_id.kehoach_cha:                        
                        partner_id=data.kehoach_id.kehoach_cha.khach_hang.id
                    doitac_giaohang_obj=data.kehoach_id.congty_vc
                    if doitac_giaohang_obj:
                        doitac_giaohang=doitac_giaohang_obj.id
                    if doitac_giaohang==False:
                        doitac_giaohang=partner_id
                    khoxuat_id=data.kehoach_id.sale_id.kho_xuat_id.id
                    type_kho=data.kehoach_id.sale_id.type_kho
                    # tao stock_picking
                    for line_donetest in data.line_ids:                        
                        cl=0   
                        # kiem tra so luong
                        so_luong_cu=line_donetest.chitiet_kh.kl_vc_kehoach
                        so_luong_moi=line_donetest.kl_vc_kehoach    
                        # lay so luong thay doi
                        cl +=so_luong_moi-so_luong_cu
                    if cl!=0:
                        picking_id_done=picking_pool.create(cr, uid, {
                                                 'partner_id':partner_id,
                                                 'sale_id':sale_id,
                                                 'doitac_giaohang':doitac_giaohang,
                                                 'date':datetime.now(),                                           
                                                 'loai_xuatkho':loai,
                                                 'kehoach_vanchuyen_id':data.kehoach_id.id,
                                                 'khoxuat_id':khoxuat_id,
                                                 'move_type':move_type,
                                                 'company_id':company_id, 
                                                 'type':'out' ,  
                                                 'type_kho':type_kho,
                                                 'nguoi_lap_phieu':uid,                                                                             
                                                 }, context=context)
                    # end
                    # query
                    for line_done in data.line_ids: 
                        query_truoc=""" select location_id, location_dest_id from stock_move
                        where chitiet_kh=%s order by id desc limit 1"""%(line_done.chitiet_kh.id)
                        cr.execute(query_truoc)
                        for move_truoc in cr.dictfetchall():
                            location_id=move_truoc['location_id']
                            location_dest_id=move_truoc['location_dest_id']
                            # end      
                            chenh_lech=0   
                            # kiem tra so luong
                            so_luong_cu=line_done.chitiet_kh.kl_vc_kehoach
                            so_luong_moi=line_done.kl_vc_kehoach    
                            # lay so luong thay doi
                            chenh_lech=so_luong_moi-so_luong_cu
                            
                            if chenh_lech>0 and line_done.chitiet_kh.id not in a:
                                move_pool.create(cr, uid, {
                                           'origin':line_done.product_id.name,
                                           'product_uos_qty':chenh_lech,                                                                  
                                           'product_uom': line_done.product_id.uom_id.id,
                                           'price_unit': line_done.chitiet_kh.sale_order_line.price_unit,
                                           'date_expected':  datetime.now(),
                                           'product_qty': chenh_lech,
                                           'product_uos':line_done.product_id.uom_id.id,
                                           'location_id': location_id,
                                           'name': line_done.product_id.name,
                                           'product_id': line_done.product_id.id,                                                        
                                           'partner_id':partner_id,
                                           'company_id':company_id,                                                          
                                           'picking_id':picking_id_done,                                                                                                                      
                                           'state': 'draft',
                                           'location_dest_id':location_dest_id,
                                           'sale_line_id':line_done.chitiet_kh.sale_order_line.id,                                                         
                                           'chitiet_kh': line_done.chitiet_kh.id,
                                           'doitac_giaohang':line_done.chitiet_kh.dia_chi_giao.id
                                           }, context=context) 
                                a.append(line_done.chitiet_kh.id)
                            else:
                                kl_dangvc=line_done.chitiet_kh.kl_dangvc
                                kl_vc_kehoach=line_done.chitiet_kh.kl_vc_kehoach
                                tong=kl_vc_kehoach - kl_dangvc
                                if so_luong_moi<tong:
                                    raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết chi tiết KHVC khi số lượng sửa đổi < số lượng đang vận chuyển. Khối lượng sửa đổi tối thiểu = %s") %(tong))               
                                else:
                                    raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết khi số lượng sau khi sửa đổi: %s <= 0")%(chenh_lech))               
                                
            # end
            #cap nhat lai so luong tren PXK tuong ung
            # TH2: Ton tai dong chi tiet  
                   
            if kt_tontai==True:
                check=False 
                state='draft'                
                picking_pool=self.pool.get('stock.picking')            
                query_kho="""select id, state from stock_picking
                            where kehoach_vanchuyen_id = """+str(kehoach_id)+""" and 
                            state not in ('cancel','done') and
                            coalesce(mistake_delivery,False)=False
                            order by id desc --limit 1 """
                cr.execute(query_kho)
                for item_kho in cr.dictfetchall():
                    picking_id=item_kho['id']
                    state=item_kho['state']
                    picking_obj=picking_pool.browse(cr, uid, picking_id, context)
                    for move in picking_obj.move_lines:                        
                        count=0
                        chitiet_kh=move.chitiet_kh.id
                        product_id_move=move.product_id.id                        
                        for line_move in data.line_ids:
                             
                            kl_vc_kehoach=line_move.kl_vc_kehoach
                            so_luong_cu1=line_move.chitiet_kh.kl_vc_kehoach
                            so_luong_moi1=kl_vc_kehoach 
                            chenh_lech1=so_luong_moi1-so_luong_cu1                            
                            soluong_nextcon1=move.product_qty
                            kl_suadoicon=soluong_nextcon1+chenh_lech1
                            product_id_line=line_move.product_id.id
                            if kl_suadoicon>=0:
                                if move.state !='cancel' and chitiet_kh not in a: 
                                    if chitiet_kh==line_move.chitiet_kh.id and product_id_move==product_id_line :  
                                        cr.execute("""update stock_move set product_qty = """+str(kl_suadoicon)+""" where id= """+str(move.id))
                                        count +=1  
                                        a.append(chitiet_kh)
                                #move_pool.write(cr, 1, [move.id], {'product_qty':kl_suadoicon,'product_uos_qty':kl_suadoicon}, context=context)
                            else: #22/10
                                # kiem tra xem có PXK nao con co the sua duoc k?
                                xet_move=abs(chenh_lech1)-soluong_nextcon1
                                qty_move=self.check_move(cr, uid, chitiet_kh, picking_obj.id,xet_move)                            
                                # end
                                slmoimove=kl_suadoicon + qty_move
                                #check_dk=abs(chenh_lech) +  qty_move
                                if slmoimove>=0 and chitiet_kh not in a  and picking_obj.id not in p: #and line.product_qty==dagiao:
                                    query_checkmove="""select m.id,picking_id, coalesce(m.product_qty,0) as product_qty
                                                  from stock_move m
                                                  inner join stock_picking p on p.id=m.picking_id
                                                  where m.chitiet_kh=%s  and p.state not in ('done','cancel')
                                                  and coalesce(mistake_delivery,False)=False 
                                                  and picking_id!= %s and m.product_qty - coalesce(%s,0)>=0
                                                  order by m.product_qty asc """%(chitiet_kh,picking_obj.id,xet_move)
                                    cr.execute(query_checkmove)
                                    for itemmove in cr.dictfetchall():
                                        if check==False and itemmove['product_qty']>=slmoimove:    
                                            move_pool.write(cr, uid, [itemmove['id']], {'product_qty':slmoimove,'product_uos_qty':slmoimove}, context=context)                                       
                                            c.append(chitiet_kh)
                                            check=True
                                        #picking_pool.write(cr, uid, [picking_obj.id], {'state':'cancel'}, context=context) 
                                    p.append(picking_obj.id)   
                                    move_pool.write(cr, uid, [move.id], {'state':'cancel'}, context=context)   
                                    #move_pool.write(cr, uid, [move.id], {'product_qty':lech_cuoi,'product_uos_qty':lech_cuoi}, context=context)   
                                    c.append(chitiet_kh)
                                    a.append(chitiet_kh)
                                else:
                                    if slmoimove<0:
                                        raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết bán hàng số lượng mà PXK tương ứng sau khi thay đổi sẽ bị < 0. Vui lòng điều chỉnh lại số lượng."))
                            # kiem tra co stock move k?
                            check_stockmove=False
                            query_kho_move="""select id
                                from stock_move                                
                                where chitiet_kh = %s and 
                                  picking_id=%s and state !='cancel'
                                order by id desc limit 1  """ %(line_move.chitiet_kh.id,picking_id)
                            cr.execute(query_kho_move) 
                            for check_move in cr.dictfetchall():
                                check_stockmove=True
                            if check_stockmove==False and count==0 and chenh_lech1!=0:
                                    # insert them dong    
                                    # lay location va location desc duoc danh truoc do
                                    # query
                                    query_truoc=""" select location_id, location_dest_id from stock_move
                                    where chitiet_kh=%s order by id desc limit 1"""%(line_move.chitiet_kh.id)
                                    cr.execute(query_truoc)
                                    for move_truoc in cr.dictfetchall():
                                        location_id=move_truoc['location_id']
                                        location_dest_id=move_truoc['location_dest_id']
                                        # end    
                                        if state=='draft':
                                            state_move='draft'
                                        else:
                                            state_move='assigned'
                                        if chenh_lech1>0 and line_move.chitiet_kh.id not in a:  
                                            move_pool.create(cr, uid, {
                                                   'origin':picking_obj.name,
                                                   'product_uos_qty':chenh_lech1,                                                                  
                                                   'product_uom': line_move.product_id.uom_id.id,
                                                   'price_unit': line_move.chitiet_kh.sale_order_line.price_unit,
                                                   'date_expected':  datetime.now(),
                                                   'product_qty': chenh_lech1,
                                                   'product_uos':line_move.product_id.uom_id.id,
                                                   'location_id': location_id,
                                                   'name': line_move.product_id.name,
                                                   'product_id': line_move.product_id.id,                                                        
                                                   'partner_id':picking_obj.partner_id.id,
                                                   'company_id':picking_obj.company_id.id ,                                                          
                                                   'picking_id':picking_id,                                                                                                                      
                                                   'state': state_move,
                                                   'location_dest_id':location_dest_id,
                                                   'sale_line_id':line_move.chitiet_kh.sale_order_line.id,                                                         
                                                   'chitiet_kh': line_move.chitiet_kh.id,
                                                   'doitac_giaohang':line_move.chitiet_kh.dia_chi_giao.id
                                                   }, context=context) 
                                            a.append(line_move.chitiet_kh.id)  
                                        #else:
                                            #raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết khi số lượng sau khi sửa đổi: %s <= 0")%(chenh_lech1))               
                # neu khong co move line - PXK trong
                if kt_tontai and a.__len__()==0:
                    # kiem tra PXK rong
                    state_null='draft'                
                    picking_pool_null=self.pool.get('stock.picking')            
                    query_kho_null="""select id, state from stock_picking
                                where kehoach_vanchuyen_id = """+str(kehoach_id)+""" and 
                                state not in ('cancel','done') and
                                coalesce(mistake_delivery,False)=False
                                order by id desc --limit 1 """
                    cr.execute(query_kho_null)
                    for item_kho_null in cr.dictfetchall():
                        state_null=item_kho_null['state']
                        picking_obj_null=picking_pool_null.browse(cr, uid, item_kho_null['id'], context)
                        for line_move_null in data.line_ids:
                            kl_vc_kehoach=line_move_null.kl_vc_kehoach
                            so_luong_cu1=line_move_null.chitiet_kh.kl_vc_kehoach
                            so_luong_moi1=kl_vc_kehoach 
                            chenh_lech1=so_luong_moi1-so_luong_cu1                           
                            kl_suadoicon=chenh_lech1
                            product_id_line=line_move_null.product_id.id
                            # kiem tra co stock move k?
                            check_stockmove=False
                            query_kho_move_null="""select id
                                from stock_move                                
                                where chitiet_kh = %s and 
                                  picking_id=%s and state !='cancel'
                                order by id desc limit 1 """ %(line_move_null.chitiet_kh.id,item_kho_null['id'])
                            cr.execute(query_kho_move_null) 
                            for check_move_null in cr.dictfetchall():
                                check_stockmove=True
                            if check_stockmove==False and chenh_lech1!=0:
                                    # insert them dong    
                                    # lay location va location desc duoc danh truoc do
                                    # query
                                    query_truoc=""" select location_id, location_dest_id from stock_move
                                    where chitiet_kh=%s order by id desc limit 1"""%(line_move_null.chitiet_kh.id)
                                    cr.execute(query_truoc)
                                    for move_truoc in cr.dictfetchall():
                                        location_id=move_truoc['location_id']
                                        location_dest_id=move_truoc['location_dest_id']
                                        # end    
                                        if state_null=='draft':
                                            state_move='draft'
                                        else:
                                            state_move='assigned'
                                        if chenh_lech1>0 and line_move_null.chitiet_kh.id not in a:  
                                            move_pool.create(cr, uid, {
                                                   'origin':picking_obj_null.name,
                                                   'product_uos_qty':chenh_lech1,                                                                  
                                                   'product_uom': line_move_null.product_id.uom_id.id,
                                                   'price_unit': line_move_null.chitiet_kh.sale_order_line.price_unit,
                                                   'date_expected':  datetime.now(),
                                                   'product_qty': chenh_lech1,
                                                   'product_uos':line_move_null.product_id.uom_id.id,
                                                   'location_id': location_id,
                                                   'name': line_move_null.product_id.name,
                                                   'product_id': line_move_null.product_id.id,                                                        
                                                   'partner_id':picking_obj_null.partner_id.id,
                                                   'company_id':picking_obj_null.company_id.id ,                                                          
                                                   'picking_id':item_kho_null['id'],                                                                                                                      
                                                   'state': state_move,
                                                   'location_dest_id':location_dest_id,
                                                   'sale_line_id':line_move_null.chitiet_kh.sale_order_line.id,                                                         
                                                   'chitiet_kh': line_move_null.chitiet_kh.id,
                                                   'doitac_giaohang':line_move_null.chitiet_kh.dia_chi_giao.id
                                                   }, context=context) 
                                            a.append(line_move_null.chitiet_kh.id)  
                                        else:
                                            raise osv.except_osv(_("Thông báo!"), _("Không thể giảm số lượng trên dòng chi tiết khi số lượng sau khi sửa đổi: %s <= 0")%(chenh_lech1))               
                    # insert them dong
                # end         
                
                # lay nhung ke hoach dang sau no
                kehoach_vanchuyen=line.parent_id.kehoach_id.id
                sale_id=line.parent_id.kehoach_id.sale_id.id 
                kehoach_sau=False
                query_kiemtra2="""select ct.* from icsc_hopdong_vanchuyen_chitiet ct 
                left join icsc_hopdong_vanchuyen_giacuoc_kehoach kh on kh.id=ct.kehoach_id
                where kh.chang_khvc='chang_1' and ct.sale_order_line= """+str(sale_order_line)+""" and kh.sale_id= """+str(sale_id)+""" and coalesce(kh.kehoach_cha,0)>0 and kh.id > """+str(kehoach_vanchuyen)+""" order by kh.id asc """
                cr.execute(query_kiemtra2)
                for item_kiemtra2 in cr.dictfetchall():
                    # lay ke hoach ke tiep 
                    kehoach_sau= item_kiemtra2['id']
                    # lay chi tiet cua ke hoach do
                    next_chitiet=chitiet_pool.browse(cr, uid, kehoach_sau, context)
                    #for next_chitiet in kh_next.chitiet_kh:
                    kl_suadoi=soluong_next=0
                    sale_order_line_next=next_chitiet.sale_order_line.id
                    product_id_next=next_chitiet.product_id.id
                    soluong_next=next_chitiet.kl_can_vanchuyen
                    kl_suadoi=soluong_next-chenh_lech
                    sale_order_line_next=next_chitiet.sale_order_line.id
                    product_id_next=next_chitiet.product_id.id
                    soluong_next=next_chitiet.kl_can_vanchuyen
                    kl_suadoi=soluong_next-chenh_lech
                    if sale_order_line_next==sale_order_line and product_id_next==product_id:                           
                        chitiet_pool.write(cr, uid, [next_chitiet.id], {'kl_can_vanchuyen':kl_suadoi}, context=context)
                        kl_suadoi=0
                
                       
        return {'type': 'ir.actions.act_window_close'}
    
icsc_kehoach_update()
class icsc_kehoach_update_line(osv.osv):
    _name = 'icsc.kehoach.update.line'
    _description = 'Sua doi KHVC'
    _columns = {
        'parent_id' : fields.many2one('icsc.kehoach.update', 'Cập nhật'),
        'chitiet_kh' : fields.many2one('icsc.hopdong.vanchuyen.chitiet', 'Cập nhật', ondelete="cascade"), 
        'name': fields.char('STT', size=256),     
        'dia_chi_giao':fields.many2one('res.partner', 'Địa chỉ giao hàng',domain="[('parent_other_id','=',parent.khach_hang)]", ondelete="cascade"),
      
        'product_id': fields.many2one('product.product', 'Sản phẩm', ondelete="cascade"),        
        'kl_vc_dukien': fields.float('KLVC dự kiến ban đầu'),
        'kl_vc_kehoach': fields.float('KL KH'),
        'kl_can_vanchuyen': fields.float('KL cần VC'),
        'kl_vc_conlai': fields.float("KL còn lại"),
         'kl_dangvc_dukien': fields.float("KL đang VC"),
        }
icsc_kehoach_update_line()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
