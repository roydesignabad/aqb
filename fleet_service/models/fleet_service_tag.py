

from odoo import models, fields, api


class FleetServiceTag(models.Model):
    _name = 'fleet.service.tag'
    _description = 'Service Tag'

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index")


