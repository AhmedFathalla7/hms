from odoo import models, fields,api

class HmsDepartment(models.Model):
    _name = 'hms.department'

    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened", default=True)
    patient_ids = fields.One2many('hms.patient', 'department_ids', string="Patients")
    # doctor_ids = fields.One2many('hms.doctor', 'department_ids', string="Doctors")

