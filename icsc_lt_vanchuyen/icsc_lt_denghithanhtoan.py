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
from datetime import datetime

def rounding(f, r):
    if not r:
        return f
    return round(f / r) * r


class sequence_custormize_thanhtoan(osv.osv):
    _name = 'sequence.custormize.thanhtoan'

    def get_name(self, cr, uid, code, table_name, type):
        import datetime
        today = datetime.datetime.now()
        year = today.year
        cr.execute("select id,number_next,number_increment,prefix,suffix,padding from ir_sequence where code='" + code + "' and active=True")
        res = cr.dictfetchone()
        if res:
            prefix = 1
            name_type = type.upper()
            cr.execute('select max(name::int)::text as max  from ' + table_name)
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
                            return '%%0%sd' % res['padding'] % p_order_number
                            break
                        i += 1

            return '%%0%sd' % res['padding'] % 1
        else:
            return '%%0%sd' % res['padding'] % 1


sequence_custormize_thanhtoan()

class icsc_denghithanhtoan_vanchuyen(osv.osv):
    _description = 'icsc_denghithanhtoan_vanchuyen'
    _name = 'icsc.denghithanhtoan.vanchuyen'
    _inherit = ['mail.thread']
    _order = 'id desc'
    def _amount_all(self, cr, uid, ids, field_name, arg, context = None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {'amount_vc_total': 0.0,
             'amount_vp_total': 0.0,
             'amount_total': 0.0}
            val = val1 = 0.0
            for line in order.chitiet_denghi:
                val1 += line.tong_tien

            res[order.id]['amount_vc_total'] = val1
            for line in order.chitiet_denghi_vipham:
                val += line.tong_tien

            res[order.id]['amount_vp_total'] = val
            res[order.id]['amount_total'] = res[order.id]['amount_vc_total'] + res[order.id]['amount_vp_total']

        return res

    def _get_order_vc(self, cr, uid, ids, context = None):
        result = {}
        for line in self.pool.get('icsc.denghithanhtoan.vanchuyen.chitiet').browse(cr, uid, ids, context=context):
            result[line.phieu_id.id] = True

        return result.keys()

    def _get_order_vp(self, cr, uid, ids, context = None):
        result = {}
        for line in self.pool.get('icsc.denghithanhtoan.vipham.vanchuyen.chitiet').browse(cr, uid, ids, context=context):
            result[line.phieu_id.id] = True

        return result.keys()

    def _sl_phieu_vc(self, cr, uid, ids, name = None, args = None, context = None):
        res = {}
        if context is None:
            context = {}
        for data in self.browse(cr, uid, ids, context):
            count = 0
            for line in data.chitiet_denghi:
                count += 1

            res[data.id] = count

        return res

    _columns = {
     'name': fields.char('Số phiếu đề nghị TT', size=500, required=True, track_visibility='onchange', states={'done': [('readonly', True)],
              'confirm': [('readonly', True)]}),
     'hp_vanchuyen': fields.many2one('icsc.hopdong.vanchuyen', 'Hợp đồng vận chuyển', domain="[('congty_vc','=',tennha_vanchuyen),('ngay_ki','>=','2013-9-01')]", required=True, track_visibility='onchange', states={'done': [('readonly', True)],
                      'confirm': [('readonly', True)]}),
     'tennha_vanchuyen': fields.many2one('res.partner', 'Tên nhà vận chuyển', required=True, domain=[('check', '=', True), ('supplier', '=', True)], track_visibility='onchange', states={'done': [('readonly', True)],
                          'confirm': [('readonly', True)]}),
     'state': fields.selection([('draft', 'Chưa xác nhận'),
               ('confirm', 'Xác nhận'),
               ('done', 'Đã đề nghị'),
               ('cancel', 'Đã hủy')], 'Trạng thái', readonly=True, track_visibility='onchange'),
     'ngay_thanhtoan': fields.date('Ngày thanh to\xc3\xa1n', track_visibility='onchange', states={'done': [('readonly', True)],
                        'confirm': [('readonly', True)]}),
     'ly_do': fields.text('Diễn giải', track_visibility='onchange', states={'done': [('readonly', True)],
               'confirm': [('readonly', True)]}),
     'thanhtoan_tungay': fields.date('TT cho phiếu từ ngày', required=True, track_visibility='onchange', states={'done': [('readonly', True)],
                          'confirm': [('readonly', True)]}),
     'thanhtoan_denngay': fields.date('TT cho phiếu đền ngày', required=True, track_visibility='onchange', states={'done': [('readonly', True)],
                           'confirm': [('readonly', True)]}),
     'daidien_lamthao1': fields.many2one('hr.employee', '1. Ông/Bà', track_visibility='onchange', states={'done': [('readonly', True)],
                          'confirm': [('readonly', True)]}),
     'daidien_lamthao2': fields.many2one('hr.employee', '2. Ông/Bà', track_visibility='onchange', states={'done': [('readonly', True)],
                          'confirm': [('readonly', True)]}),
     'chucvu_lamthao1': fields.many2one('hr.job', 'Chức vụ', track_visibility='onchange', states={'done': [('readonly', True)],
                         'confirm': [('readonly', True)]}),
     'chucvu_lamthao2': fields.many2one('hr.job', 'Chức vụ', track_visibility='onchange', states={'done': [('readonly', True)],
                         'confirm': [('readonly', True)]}),
     'daidien_khachhang1': fields.many2one('res.partner', '1. Ông/Bà', domain="[('parent_id','=',tennha_vanchuyen)]", track_visibility='onchange', states={'done': [('readonly', True)],
                            'confirm': [('readonly', True)]}),
     'daidien_khachhang2': fields.many2one('res.partner', '2. Ông/Bà', domain="[('parent_id','=',tennha_vanchuyen)]", track_visibility='onchange', states={'done': [('readonly', True)],
                            'confirm': [('readonly', True)]}),
     'chucvu_khachhang1': fields.char('Chức vụ', track_visibility='onchange', states={'done': [('readonly', True)],
                           'confirm': [('readonly', True)]}),
     'chucvu_khachhang2': fields.char('Chức vụ', track_visibility='onchange', states={'done': [('readonly', True)],
                           'confirm': [('readonly', True)]}),
     'chitiet_denghi': fields.one2many('icsc.denghithanhtoan.vanchuyen.chitiet', 'phieu_id', 'Chi tiết', states={'done': [('readonly', True)],
                        'confirm': [('readonly', True)]}),
     'chitiet_denghi_vipham': fields.one2many('icsc.denghithanhtoan.vipham.vanchuyen.chitiet', 'phieu_id', 'Chi tiết', states={'done': [('readonly', True)],
                               'confirm': [('readonly', True)]}),
     'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng tiền', store={'icsc.denghithanhtoan.vanchuyen': (lambda self, cr, uid, ids, c = {}: ids, ['chitiet_denghi', 'chitiet_denghi_vipham'], 10),
                      'icsc.denghithanhtoan.vanchuyen.chitiet': (_get_order_vc, ['tong_tien',
                                                                  'so_phieu_vc',
                                                                  'phieu_id',
                                                                  'ngay_vc',
                                                                  'danhsach_capnhat'], 10),
                      'icsc.denghithanhtoan.vipham.vanchuyen.chitiet': (_get_order_vp, ['tong_tien',
                                                                         'so_phieu_vc',
                                                                         'phieu_id',
                                                                         'ngay_vc'], 10)}, multi='sums', help='The total amount.'),
     'amount_vp_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng tiền vi phạm', store={'icsc.denghithanhtoan.vanchuyen': (lambda self, cr, uid, ids, c = {}: ids, ['chitiet_denghi', 'chitiet_denghi_vipham'], 10),
                         'icsc.denghithanhtoan.vanchuyen.chitiet': (_get_order_vc, ['tong_tien',
                                                                     'so_phieu_vc',
                                                                     'phieu_id',
                                                                     'ngay_vc',
                                                                     'danhsach_capnhat'], 10),
                         'icsc.denghithanhtoan.vipham.vanchuyen.chitiet': (_get_order_vp, ['tong_tien',
                                                                            'so_phieu_vc',
                                                                            'phieu_id',
                                                                            'ngay_vc'], 10)}, multi='sums', help='The total amount.'),
     'amount_vc_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tổng tiền vận chuyển', store={'icsc.denghithanhtoan.vanchuyen': (lambda self, cr, uid, ids, c = {}: ids, ['chitiet_denghi', 'chitiet_denghi_vipham'], 10),
                         'icsc.denghithanhtoan.vanchuyen.chitiet': (_get_order_vc, ['tong_tien',
                                                                     'so_phieu_vc',
                                                                     'phieu_id',
                                                                     'ngay_vc',
                                                                     'danhsach_capnhat'], 10),
                         'icsc.denghithanhtoan.vipham.vanchuyen.chitiet': (_get_order_vp, ['tong_tien',
                                                                            'so_phieu_vc',
                                                                            'phieu_id',
                                                                            'ngay_vc'], 10)}, multi='sums', help='The total amount.'),
     'sl_phieu_vc': fields.function(_sl_phieu_vc, type='integer', string='Tổng số PVC', track_visibility='onchange')}
    _defaults = {'state': 'draft',
     'name': lambda self, cr, uid, c: self.pool.get('sequence.custormize.thanhtoan').get_name(cr, uid, 'icsc.denghithanhtoan.vanchuyen', 'icsc_denghithanhtoan_vanchuyen', '')}

    def unlink(self, cr, uid, ids, context = None):
        sale_orders = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        phieu_vp_ids = []
        for s in sale_orders:
            if s['state'] in ('draft',):
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Lỗi!'), _('Bạn chỉ có thể xóa phiếu ĐNTT ở Trạng thái Chưa xác nhận!'))

        for data in self.browse(cr, uid, ids, context):
            for item in data.chitiet_denghi:
                so_phieu_vc = item.so_phieu_vc.id
                tung_phan = item.so_phieu_vc.tung_phan
                if tung_phan == False:
                    self.pool.get('icsc.phieu.vanchuyen').write(cr, uid, so_phieu_vc, {'duavao_thanhtoan': False}, context)
                else:
                    for line in item.danhsach_capnhat:
                        self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, line.id, {'duavao_thanhtoan': False}, context)

            for line in data.chitiet_denghi_vipham:
                phieu_vp = line.so_phieu_vc.id
                phieu_vp_ids.append(phieu_vp)

        self.pool.get('icsc.phieuvipham.vanchuyen').write(cr, uid, phieu_vp_ids, {'state': 'confirm'}, context)
        return osv.osv.unlink(self, cr, uid, ids, context=context)

    def action_taithongtin(self, cr, uid, ids, context = None):
        chitiet_denghi = self.pool.get('icsc.denghithanhtoan.vanchuyen.chitiet')
        chitiet_denghi_vipham = self.pool.get('icsc.denghithanhtoan.vipham.vanchuyen.chitiet')
        for data in self.browse(cr, uid, ids, context):
            tungay = data.thanhtoan_tungay
            denngay = data.thanhtoan_denngay
            hdvc = data.hp_vanchuyen.id
            nvc = data.tennha_vanchuyen.id
            phieu_vc_pool = self.pool.get('icsc.phieu.vanchuyen')
            phieu_vc_pool_capnhat = self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat')
            query = "select * from icsc_phieu_vanchuyen where coalesce(duavao_thanhtoan,False)=False and hopdong_vanchuyen=%s and congty_vc=%s and state in ('du_dk','du_dk_tung_phan') and ngay_vc between '%s' and '%s'"%(hdvc,nvc,tungay,denngay)
            cr.execute(query)
            for item in cr.dictfetchall():
                so_phieu_vc = item['id']
                ngay_vc = item['ngay_vc']
                duavao_thanhtoan = item['duavao_thanhtoan']
                phieu_vc_obj = phieu_vc_pool.browse(cr, uid, so_phieu_vc, context)
                chitiet_capnhat = False
                tong_tien = item['amount_total']
                cr.execute('update icsc_phieu_vanchuyen set duavao_thanhtoan=True where id= ' + str(so_phieu_vc))
                if tong_tien > 0:
                    chitiet_denghi.create(cr, uid, {'ngay_vc': ngay_vc,
                     'so_phieu_vc': so_phieu_vc,
                     'tong_tien': tong_tien,
                     'phieu_id': data.id}, context=context)

            query_ctcn = "select * from icsc_phieu_vanchuyen where hopdong_vanchuyen=%s and congty_vc=%s and state='du_dk'"%(hdvc,nvc)
            cr.execute(query_ctcn)
            for item_ctcn in cr.dictfetchall():
                phieucn_id = item_ctcn['id']
                value = []
                phieu_vc_obj_cn = phieu_vc_pool.browse(cr, uid, phieucn_id, context)
                tong_tien = 0
                for line in phieu_vc_obj_cn.chitiet_vc_capnhat:
                    state = line.state
                    thanh_toan = line.duavao_thanhtoan
                    ngay_vc = line.ngay_capnhat
                    tn = datetime.strptime(tungay, '%Y-%m-%d')
                    dn = datetime.strptime(denngay, '%Y-%m-%d')
                    vc = datetime.strptime(ngay_vc, '%Y-%m-%d')
                    if vc >= tn and vc <= dn:
                        if state == 'draft' and thanh_toan == False:
                            tong_tien += line.kl_vc * line.thanh_tien
                            value.append(line.id)
                        phieu_vc_pool_capnhat.write(cr, uid, line.id, {'duavao_thanhtoan': True}, context)

                if tong_tien > 0:
                    denghi = chitiet_denghi.create(cr, uid, {'ngay_vc': ngay_vc,
                     'so_phieu_vc': phieucn_id,
                     'tong_tien': tong_tien,
                     'phieu_id': data.id}, context=context)
                    for cn in value:
                        query_real = 'INSERT INTO icsc_denghitt_ctcapnhat_rel(denghi_id, capnhat_id) VALUES (%s, %s)'
                        values = (denghi, cn)
                        cr.execute(query_real, values)

            query2 = "select vp.id,vp.ngay_vc as ngay_phat ,vp.amount_total from icsc_phieuvipham_vanchuyen vp left join icsc_phieu_vanchuyen pvc on pvc.id=vp.phieu_vanchuyen left join icsc_hopdong_vanchuyen hd on hd.id=pvc.hopdong_vanchuyen where hd.id=%s and vp.state='confirm' and pvc.congty_vc=%s and vp.ngay_vc between '%s' and '%s'"%(hdvc,nvc,tungay,denngay)
            cr.execute(query2)
            for item2 in cr.dictfetchall():
                so_phieu_vcs = item2['id']
                ngay_viphams = item2['ngay_phat']
                tong_tiens = item2['amount_total']
                chitiet_denghi_vipham.create(cr, uid, {'ngay_vipham': ngay_viphams,
                                                        'so_phieu_vc': so_phieu_vcs,
                                                        'tong_tien': tong_tiens,
                                                        'phieu_id': data.id}, context=context)
                cr.execute("update icsc_phieuvipham_vanchuyen set state='done' where id= " + str(so_phieu_vcs))
        return True

    def onchange_nhavc(self, cr, uid, ids, tennha_vanchuyen, context = None):
        if not tennha_vanchuyen:
            return {}
        vals = {}
        hd = False
        sale_object = self.pool.get('res.partner').browse(cr, uid, tennha_vanchuyen)
        count = 0
        # for item in sale_object.child_ids:
        #     count += 1
        #     if count == 1:
        #         daidien_khachhang1 = item.id
        #         vals = {'daidien_khachhang1': daidien_khachhang1}
        #     else:
        #         if count > 1:
        #             daidien_khachhang2 = item.id
        #         vals.update({'daidien_khachhang2': daidien_khachhang2})

        query_hd = 'select id from icsc_hopdong_vanchuyen where congty_vc= ' + str(tennha_vanchuyen) + ' and "check"=True'
        cr.execute(query_hd)
        for item_hd in cr.dictfetchall():
            hd = item_hd['id']
            vals = {'hp_vanchuyen': hd}

        return {'value': vals}

    def onchange_chucvu_daidien1(self, cr, uid, ids, lai_xe, context = None):
        if not lai_xe:
            return {}
        sale_object = self.pool.get('hr.employee').browse(cr, uid, lai_xe)
        function = sale_object.job_id.id
        return {'value': {'chucvu_lamthao1': function}}

    def onchange_chucvu_daidien2(self, cr, uid, ids, lai_xe, context = None):
        if not lai_xe:
            return {}
        sale_object = self.pool.get('hr.employee').browse(cr, uid, lai_xe)
        function = sale_object.job_id.id
        return {'value': {'chucvu_lamthao2': function}}

    def onchange_chucvu1(self, cr, uid, ids, lai_xe, context = None):
        if not lai_xe:
            return {}
        sale_object = self.pool.get('res.partner').browse(cr, uid, lai_xe)
        function = sale_object.function
        return {'value': {'chucvu_khachhang1': function}}

    def onchange_chucvu2(self, cr, uid, ids, lai_xe, context = None):
        if not lai_xe:
            return {}
        sale_object = self.pool.get('res.partner').browse(cr, uid, lai_xe)
        function = sale_object.function
        return {'value': {'chucvu_khachhang2': function}}

    def action_confirm(self, cr, uid, ids, context = None):
        phieu_pool = self.pool.get('icsc.phieu.vanchuyen')
        pvc_chitiet = self.pool.get('icsc.phieu.vanchuyen.chitiet')
        phieu_vc = []
        pvc_lines = []
        for item in self.browse(cr, uid, ids, context):
            id1 = item.id
            self.write(cr, uid, id1, {'state': 'confirm'}, context)
            for line in item.chitiet_denghi:
                tung_phan = line.so_phieu_vc.tung_phan
                if tung_phan == False or tung_phan is None:
                    phieu_vc.append(line.so_phieu_vc.id)
                    for pvc_line in line.so_phieu_vc.chitiet_vc:
                        pvc_lines.append(pvc_line.id)

            phieu_pool.write(cr, uid, phieu_vc, {'state': 'done'}, context)
            pvc_chitiet.write(cr, uid, pvc_lines, {'state': 'done'}, context)

        return True

    def action_done(self, cr, uid, ids, context = None):
        phieu_pool = self.pool.get('icsc.phieu.vanchuyen')
        pvc_chitiet = self.pool.get('icsc.phieu.vanchuyen.chitiet')
        phieu_vc = []
        pvc_lines = []
        for item in self.browse(cr, uid, ids, context):
            id1 = item.id
            self.write(cr, uid, id1, {'state': 'done'}, context)
            for line in item.chitiet_denghi:
                tung_phan = line.so_phieu_vc.tung_phan
                if tung_phan == False or tung_phan is None:
                    phieu_vc.append(line.so_phieu_vc.id)
                    for pvc_line in line.so_phieu_vc.chitiet_vc:
                        pvc_lines.append(pvc_line.id)

            pvc_chitiet.write(cr, uid, pvc_lines, {'state': 'done'}, context)
            phieu_pool.write(cr, uid, phieu_vc, {'state': 'done'}, context)

        return True

    def action_cancel(self, cr, uid, ids, context = None):
        phieu_vc = []
        phieu_vc_tunphan = []
        pvc_lines = []
        phieu_vp_ids = []
        pvc_chitiet = self.pool.get('icsc.phieu.vanchuyen.chitiet')
        for data in self.browse(cr, uid, ids, context):
            id1 = data.id
            for item in data.chitiet_denghi:
                so_phieu_vc = item.so_phieu_vc
                tung_phan = so_phieu_vc.tung_phan
                if tung_phan == False or tung_phan is None:
                    phieu_vc.append(so_phieu_vc.id)
                    for pvc_line in item.so_phieu_vc.chitiet_vc:
                        pvc_lines.append(pvc_line.id)

                else:
                    for line in item.danhsach_capnhat:
                        phieu_vc_tunphan.append(line.id)

                for line in data.chitiet_denghi_vipham:
                    phieu_vp = line.so_phieu_vc.id
                    phieu_vp_ids.append(phieu_vp)

            self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, phieu_vc_tunphan, {'duavao_thanhtoan': False}, context)
            pvc_chitiet.write(cr, uid, pvc_lines, {'state': 'du_dk'}, context)
            self.pool.get('icsc.phieu.vanchuyen').write(cr, uid, phieu_vc, {'duavao_thanhtoan': False,
             'state': 'du_dk'}, context)
            self.write(cr, uid, id1, {'state': 'cancel'}, context)
            self.pool.get('icsc.phieuvipham.vanchuyen').write(cr, uid, phieu_vp_ids, {'state': 'confirm'}, context)

        return True

    def action_return(self, cr, uid, ids, context = None):
        for data in self.browse(cr, uid, ids, context):
            id1 = data.id
            for item in data.chitiet_denghi:
                so_phieu_vc = item.so_phieu_vc.id
                tung_phan = item.so_phieu_vc.tung_phan
                if tung_phan == False:
                    self.pool.get('icsc.phieu.vanchuyen').write(cr, uid, so_phieu_vc, {'duavao_thanhtoan': True}, context)
                else:
                    for line in item.danhsach_capnhat:
                        self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, line.id, {'duavao_thanhtoan': True}, context)

            self.write(cr, uid, id1, {'state': 'draft'}, context)

        return True


icsc_denghithanhtoan_vanchuyen()

class icsc_denghithanhtoan_vanchuyen_chitiet(osv.osv):
    _description = 'icsc_denghithanhtoan_vanchuyen_chitiet'
    _name = 'icsc.denghithanhtoan.vanchuyen.chitiet'
    _columns = {
     'name': fields.char('Diễn giải', size=500),
     'so_phieu_vc': fields.many2one('icsc.phieu.vanchuyen', 'Số phiếu vận chuyển', ondelete='cascade'),
     'tong_tien': fields.float('Tổng tiền'),
     'phieu_id': fields.many2one('icsc.denghithanhtoan.vanchuyen', 'Phiếu đề nghị', ondelete='cascade'),
     'ngay_vc': fields.date('Ngày vận chuyển'),
     'danhsach_capnhat': fields.many2many('icsc.phieu.vanchuyen.chitiet.capnhat', 'icsc_denghitt_ctcapnhat_rel', 'denghi_id', 'capnhat_id', 'Phiếu đề nghị', ondelete='cascade')
     }

    def unlink(self, cr, uid, ids, context = None):
        for item in self.browse(cr, uid, ids, context):
            so_phieu_vc = item.so_phieu_vc.id
            tung_phan = item.so_phieu_vc.tung_phan
            if tung_phan == False:
                self.pool.get('icsc.phieu.vanchuyen').write(cr, uid, so_phieu_vc, {'duavao_thanhtoan': False}, context)
            else:
                for line in item.danhsach_capnhat:
                    self.pool.get('icsc.phieu.vanchuyen.chitiet.capnhat').write(cr, uid, line.id, {'duavao_thanhtoan': False}, context)

        return osv.osv.unlink(self, cr, uid, ids, context=context)


icsc_denghithanhtoan_vanchuyen_chitiet()

class icsc_denghithanhtoan_vipham_vanchuyen_chitiet(osv.osv):
    _description = 'icsc_denghithanhtoan_vipham_vanchuyen_chitiet'
    _name = 'icsc.denghithanhtoan.vipham.vanchuyen.chitiet'
    _columns = {
     'name': fields.char('Diễn giải', size=500),
     'so_phieu_vc': fields.many2one('icsc.phieuvipham.vanchuyen', 'Số phiếu vi phạm', ondelete='cascade'),
     'tong_tien': fields.float('Tổng tiền'),
     'phieu_id': fields.many2one('icsc.denghithanhtoan.vanchuyen', 'Phiếu đề nghị', ondelete='cascade'),
     'ngay_vipham': fields.date('Ngày vận chuyển')}

    def unlink(self, cr, uid, ids, context = None):
        for item in self.browse(cr, uid, ids, context):
            so_phieu_vc = item.so_phieu_vc.id
            self.pool.get('icsc.phieuvipham.vanchuyen').write(cr, uid, so_phieu_vc, {'state': 'confirm'}, context)

        return osv.osv.unlink(self, cr, uid, ids, context=context)


icsc_denghithanhtoan_vipham_vanchuyen_chitiet()