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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from openerp.osv import fields, osv
from openerp.osv.orm import browse_record, browse_null
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class icsc_hoadon_update(osv.osv):
    _name = 'icsc.hoadon.update'
    _description = 'Sua doi hoa don'
    _order="id desc"
    _columns = {
        'hoadon_id' : fields.many2one('account.invoice', 'Hóa đơn', ondelete="cascade"),
        'so_hoa_don_cu': fields.char('Số hóa đơn ban đầu', size=500)  , 
        'so_hoa_don': fields.char('Số hóa đơn thay đổi', size=500)  , 
        'ngay_capnhat': fields.date('Ngày cập nhật'),     
        'user_id' : fields.many2one('res.users', 'Người cập nhật'),
        'so_quyen':fields.char( 'Số quyển',size=500, ),  
        'date_invoice': fields.date('Ngày lập hóa đơn', help="Keep empty to use the current date"),   
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
        picking_pool = self.pool.get('account.invoice')     
        vals= []
        picking_obj = picking_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(icsc_hoadon_update, self).default_get(cr, uid, fields, context=context) 
        if picking_obj.id:
            hoadon_id=picking_obj.id            
            so_hd=picking_obj.so_hoa_don
            if 'hoadon_id' in fields:
                res.update({'hoadon_id': hoadon_id})           
            if 'so_hoa_don_cu' in fields:
                res.update({'so_hoa_don_cu': so_hd})   
            if 'so_hoa_don' in fields:              
                res.update({'so_hoa_don': so_hd})       
            if 'ngay_capnhat' in fields:
				datehd = datetime.now(timezone('UTC'))
				ngay_capnhat = datehd.astimezone(timezone('Asia/Ho_Chi_Minh'))
				res.update({'ngay_capnhat': ngay_capnhat.strftime("%Y-%m-%d")})
            if 'user_id' in fields:
                res.update({'user_id': uid}) 
            if 'so_quyen' in fields:
                res.update({'so_quyen': picking_obj.so_quyen}) 
            if 'date_invoice' in fields:
                res.update({'date_invoice': picking_obj.date_invoice}) 
        return res
    
    def action_correct_delivery(self, cr, uid, ids,  context=None):
        invoice_pool = self.pool.get('account.invoice')        
        for data in self.browse(cr, uid, ids, context): 
            context={'uid':uid}
            if  data.so_hoa_don is False:
                so_hoa_don=str(data.so_hoa_don)
            else:
                so_hoa_don=str(data.so_hoa_don.encode("utf-8"))            
            date = datetime.strptime(data.date_invoice, "%Y-%m-%d")
            date_invoice = date + timedelta(days=0, hours=7)
            invoice_pool.write(cr, uid, [data.hoadon_id.id], {'write_uid':uid,'so_quyen':data.so_quyen,'date_invoice':date_invoice,'so_hoa_don':so_hoa_don},context)
        return {'type': 'ir.actions.act_window_close'}
    
icsc_hoadon_update()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
