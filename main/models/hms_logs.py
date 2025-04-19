from odoo import models, fields,api

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'

    patient_id = fields.Many2one('hms.patient', string="Patient", required=True)
    name = fields.Char(string="Patient Name", compute='_compute_patient_name')
    created_by = fields.Many2one('res.users', string="Created by", default=lambda self: self.env.user)
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Description")

    @api.depends('patient_id')
    def _compute_patient_name(self):
        for record in self:
            record.name = record.patient_id.name if record.patient_id else False