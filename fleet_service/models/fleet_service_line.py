
from odoo import models, fields, api


class fleetserviceline(models.Model):
    _name = 'fleet.service.line'
    _description = 'fleet_service'
  

    fleet_service_id = fields.Many2one('fleet.service.record',string='Service',required=True,ondelete='cascade'
    )
    description = fields.Char(string='Part/Labour Discription',required=True)
    quantity = fields.Integer(default=1)
    unit_price = fields.Float(string='Unit Price (INR)',default=0)
