

from odoo import models, fields, api


class fleetservicerecord(models.Model):
    _name = 'fleet.service.record'
    _description = 'fleet_service.record'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    name = fields.Char(string="Service reference",required=True,copy=False,default='New')
    vehicle_id = fields.Many2one('fleet.vehicle')
    technician_id = fields.Many2one('res.users',string="Assigned Technician")
    service_date = fields.Date(required=True,default=fields.Date.context_today)
    service_type = fields.Selection([('oil_change','Oil Change'),('tyre','Tyre'),('brake','Brake'),('engine','Engine'),('general','General')])
    cost = fields.Float(string='Cost',default=0.0,digit=(10,2))
    state = fields.Selection([('draft','Draft'),('in_progress','IN progress'),('done','Done'),('cancelled','Cancelled')])
    notes = fields.Text(string='Internal notes')
    tag_ids = fields.Many2many(
        'fleet.service.tag',
        'fleet_service_tag_rel',
        'service_id',
        'tag_id',
        string='Tags'
    )
    service_line_ids = fields.One2many('fleet.service.line', 'fleet_service_id', string='Service Line')


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.service.record') or 'New'
        return super().create(vals)

    # 🔁 State Actions
    def action_start(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("Can only start from Draft"))
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError(_("Can only mark Done from In Progress"))
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state not in ['draft', 'in_progress']:
                raise UserError(_("Can only cancel from Draft or In Progress"))
            rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_("Can only reset to Draft from Cancelled"))
            rec.state = 'draft'