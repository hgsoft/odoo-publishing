from openerp import models, fields, api

class stock_location(models.Model):
    _inherit = 'stock.location'

    consignee_id = fields.Many2one('res.partner','Consignee', readonly=True)
    is_consignment = fields.Boolean('Consignment Location', readonly=True)


    @api.one
    @api.constrains('consignee_id')
    def _check_internal_location(self):
        if self.consignee_id and self.usage != 'internal':
            raise Warning(_('A consignee Location must be always internal'))
