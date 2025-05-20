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

def rounding(f, r):
    if not r:
        return f
    return round(f / r) * r


class sequence_custormize_thongbao(osv.osv):
    _name = 'sequence.custormize.thongbao'

    def get_name(self, cr, uid, code, table_name):
        import datetime
        today = datetime.datetime.now()
        year = today.year
        cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='" + code + "' and active=True")
        res = cr.dictfetchone()
        if res:
            cr.execute('select max(right(name,4)) as max  from ' + table_name)
            p_order_number = cr.dictfetchone()
            if p_order_number:
                if p_order_number['max']:
                    purchace_order_name_replace = p_order_number['max']
                    i = 1
                    while i <= len(purchace_order_name_replace):
                        number = int(purchace_order_name_replace[:i])
                        if number > 0:
                            p_oder_number = int(purchace_order_name_replace[i - 1:])
                            p_order_number = p_oder_number + 1
                            return 'TB' + '%%0%sd' % res['padding'] % p_order_number
                            break
                        i += 1

            return 'TB' + '%%0%sd' % res['padding'] % 1
        else:
            return 'TB' + '%%0%sd' % res['padding'] % 1


sequence_custormize_thongbao()

class icsc_khvc_thongbao_kho(osv.osv):
    _description = 'icsc_khvc_thongbao_kho'
    _name = 'icsc.khvc.thongbao.kho'
    _inherit = ['mail.thread']
    _order = 'id desc'
    _columns = {
         'name': fields.char('Số thông báo', size=500, required=True, track_visibility='onchange', states={'confirm': [('readonly', True)]}),
         'ngay_capnhat': fields.date('Ngày cập nhật KHVC', track_visibility='onchange', states={'confirm': [('readonly', True)]}),
         'line_ids': fields.one2many('icsc.khvc.thongbao.kho.line', 'parent_id', 'Chi tiết vận chuyển', readonly=True, states={'confirm': [('readonly', True)]}),
         'state': fields.selection([('draft', 'Mới'),
                   ('confirm', 'Đã xác nhận'),
                   ('done', 'Đã cập nhật'),
                   ('cancel', 'Đã hủy')], 'Trạng thái', readonly=True, track_visibility='onchange'),
         'so_khvc': fields.many2one('icsc.hopdong.vanchuyen.giacuoc.kehoach', 'Số KHVC', states={'done': [('readonly', True)],
                     'confirm': [('readonly', True)]}, track_visibility='onchange', ondelete='cascade'),
         'sale_id': fields.many2one('sale.order', 'Lệnh xuất hàng', states={'done': [('readonly', True)],
                     'confirm': [('readonly', True)]}, track_visibility='onchange', ondelete='cascade'),
         'congty_vc': fields.many2one('res.partner', 'Đơn vị vận chuyển', domain=[('check', '=', True), ('supplier', '=', True)], states={'done': [('readonly', True)],
                       'confirm': [('readonly', True)]}, track_visibility='onchange', ondelete='cascade'),
         'picking_ids': fields.many2many('stock.picking', 'icsc_khvc_thongbao_kho_rel', 'thongbao_id', 'picking_id', 'Danh sách phiếu xuất kho', readonly=True),
         'dien_giai': fields.text('Diễn giải')
     }
    _defaults = {
         'state': 'draft',
         'name': lambda self, cr, uid, c: self.pool.get('sequence.custormize.thongbao').get_name(cr, uid, 'icsc.khvc.thongbao.kho', 'icsc_khvc_thongbao_kho') or '/'
     }

    def action_confirm(self, cr, uid, ids, context = None):
        for data in self.browse(cr, uid, ids, context):
            self.write(cr, uid, data.id, {'state': 'confirm'}, context)

        return True

    def action_done(self, cr, uid, ids, context = None):
        for data in self.browse(cr, uid, ids, context):
            self.write(cr, uid, data.id, {'state': 'done'}, context)

        return True

    def action_cancel(self, cr, uid, ids, context = None):
        for data in self.browse(cr, uid, ids, context):
            self.write(cr, uid, data.id, {'state': 'cancel'}, context)

        return True


icsc_khvc_thongbao_kho()

class icsc_khvc_thongbao_kho_line(osv.osv):
    _name = 'icsc.khvc.thongbao.kho.line'
    _description = 'Sua doi KHVC'
    _columns = {
         'parent_id': fields.many2one('icsc.khvc.thongbao.kho', 'Cập nhật', ondelete='cascade'),
         'chitiet_kh': fields.many2one('icsc.hopdong.vanchuyen.chitiet', 'Cập nhật'),
         'dia_chi_giao': fields.many2one('res.partner', 'Địa chỉ giao hàng', domain="[('parent_other_id','=',parent.khach_hang)]"),
         'sale_order_line': fields.many2one('sale.order.line', 'Chi tiết LXH', ondelete='cascade'),
         'product_id': fields.many2one('product.product', 'Sản phẩm'),
         'kl_vc_kehoach_cu': fields.float('KL KL vận chuyển KH ban đầu'),
         'kl_vc_kehoach_moi': fields.float('KL vận chuyển KH mới')
     }


icsc_khvc_thongbao_kho_line()