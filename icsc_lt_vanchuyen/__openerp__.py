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

{
    "name" : "ICSC - LAM THAO vận chuyển",
    "version" : "1.1",
    "depends" : [
                 'base','icsc_lt_base','account','sale','hr','stock','sale_stock',
                 'mail','icsc_lt_banhang', 'web_kanban'
                ],
    'description': """ ICSC - LAM THAO vận chuyển""",
    "author" : "Oanhle@icsc.vn",
    "website" : "http://icsc.vn",
    'category': 'Generic Modules/Others',
    "init_xml" : [
                  'security/lct_customer_security.xml', 
                  'security/ir.model.access.csv', 
                  ],
    'data' : [     
                'security/lct_customer_security.xml', 
                'security/ir.model.access.csv',  
                'wizard/icsc_diem_tinhcuoc_view.xml'  , 
                'wizard/icsc_lt_sanpham_chang1_vanchuyen_view.xml'  , 
                'wizard/icsc_lt_sanpham_vanchuyen_view.xml'  ,  
                'wizard/icsc_lt_sanpham_phieu_vanchuyen_view.xml'  , 
                'wizard/icsc_kehoach_update_view.xml',   
                'wizard/icsc_phieuvc_update_view.xml',    
                'wizard/icsc_hoadon_update_view.xml'  ,  
                'wizard/icsc_pvc_duongsat_view.xml' ,   
                'wizard/stock_update_view.xml' ,     
                'icsc_lt_vanchuyen_view.xml' ,   
                'icsc_lt_xuatkho_view.xml',    
                'icsc_lt_denghithanhtoan_view.xml',
                'icsc_thongbao_capnhat_sequence.xml',
                'icsc_lt_thongbao_kho_view.xml',                
                'hopdong_vanchuyen_sequence.xml',
                'phieu_vanchuyen_sequence.xml',
            ],
   
    'css' : [ "static/src/css/base.css",],     
    "installable" : True,
    'application': True,
    "active" : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
