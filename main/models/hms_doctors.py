from odoo import models, fields,api

class HmsDoctor(models.Model):
    _name = 'hms.doctor'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    name = fields.Char(compute="_compute_name", store=True)
    image = fields.Image(string="Image")
    patients_id = fields.Many2many('hms.patient', string="Patients")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}"