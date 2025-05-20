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

class stock_update_internal(osv.osv):
    _name = 'stock.update.internal'
    _description = 'Update stock internal'
    _order = 'id desc'
    _columns = {
        'phieu_id' : fields.many2one('stock.picking', 'PXK'),      
        'ngay_capnhat': fields.date('Ngày cập nhật'),
        'user_id' : fields.many2one('res.users', 'Người cập nhật'),
        'date_done': fields.date('Ngày giao hàng'),  
        'name': fields.char('Name', size=256),      
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
        picking_pool = self.pool.get('stock.picking')     
        picking_obj = picking_pool.browse(cr, uid, context.get('active_id', False))      
        res = super(stock_update_internal, self).default_get(cr, uid, fields, context=context) 
        if picking_obj.id:
            picking_id=picking_obj.id           
            if 'phieu_id' in fields:
                res.update({'phieu_id': picking_id})          
            if 'ngay_capnhat' in fields:
                res.update({'ngay_capnhat': time.strftime('%Y-%m-%d')})
            if 'date_done' in fields:
                res.update({'date_done': picking_obj.date})
            if 'user_id' in fields:
                res.update({'user_id': uid}) 
            if 'name' in fields:
                res.update({'name': 'Cập nhật phiếu nội bộ'}) 
        return res
    def action_correct_delivery(self, cr, uid, ids,  context=None):
        picking_pool = self.pool.get('stock.picking') 
        move_pool=self.pool.get('stock.move')
        line_ids=[]
        for data in self.browse(cr, uid, ids, context):
            date_done = data.date_done
            phieu_id = data.phieu_id.id     
            picking_obj = picking_pool.browse(cr, uid, phieu_id, context)          
            picking_pool.write(cr, uid, phieu_id, {'date_done':date_done,'date':date_done}, context=context)
            for line in picking_obj.move_lines:
                line_ids.append(line.id)
            move_pool.write(cr, uid, line_ids, { 'date':date_done}, context=context)
        return {'type': 'ir.actions.act_window_close'}
    
stock_update_internal()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
