# -*- coding: utf-8 -*-

from openerp import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    is_consignment_order = fields.Boolean("Consignment Order")

    @api.multi
    def action_view_sale_consignment_products(self):
        # invoice_ids = self.mapped('invoice_ids')
        imd = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']

        action_id = imd.xmlid_to_res_id('consignment_sales.consignee_open_quants')
        action = act_obj.browse(action_id)
        list_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_tree')
        form_view_id = imd.xmlid_to_res_id('stock.view_stock_quant_form')
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            # 'target': action.target,

            'context': {'search_default_locationgroup': 1, 'search_default_internal_loc': 1, 
                        'search_default_productgroup': 1},
            # 'domain': {''}
            'res_model': action.res_model,
            'domain': "[('location_id','=',%s)]" % self.partner_id.consignee_location_id.id
        }

        return result

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    @api.depends('product_id')
    def _compute_consignment_stock(self):
        if not self.product_id:
            return
        consignent_location = self.order_id.partner_id.consignee_location_id
        if not consignent_location:
            return False
        # Fetch the stock at this customer's consignee location
        consignment_quants = self.env['stock.quant'].search([('location_id','=',consignent_location.id),
                                                              ('product_id','=', self.product_id.id)
                                                            ])
        line_data = []
        product_qty = 0
        for each_quant in consignment_quants:
            product_qty += each_quant.qty

        self.consignment_stock = product_qty

    consignment_stock = fields.Float(string='Consignment Stock',
        compute='_compute_consignment_stock')
