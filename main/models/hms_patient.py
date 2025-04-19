from email.policy import default

from odoo import models, fields,api
from odoo.exceptions import ValidationError, UserError
import re
from datetime import datetime

class HmsPatient(models.Model):
    _name = 'hms.patient'

    email = fields.Char(string='Email')
    partner_id = fields.Many2one('res.partner', string="Partner")

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name' , required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age')

    department_ids = fields.Many2one('hms.department', string="Department")
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")

    department_caps = fields.Integer(related="department_ids.capacity" ,string="Capacity")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string="State", default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Log History")

    def action_good(self):
        self.state = 'good'
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': "State changed to Good"
        })

    def action_fair(self):
        self.state = 'fair'
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': "State changed to Fair"
        })

    def action_serious(self):
        self.state = 'serious'
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': "State changed to Serious"
        })

    # @api.model
    # def create(self, vals):
    #     patient = super().create(vals)
    #
    #     self.env['hms.patient.log'].create({
    #         'patient_id': patient.id,
    #         'created_by': self.env.user.id,
    #         'date': fields.Datetime.now(),
    #         'description': 'Patient created'
    #     })
    #
    #     if vals.get('state'):
    #         self.env['hms.patient.log'].create({
    #             'patient_id': patient.id,
    #             'description': f"State set to {vals['state']}"
    #         })
    #
    #     return patient
    #
    # def write(self, vals):
    #     for rec in self:
    #         if 'state' in vals and rec.state != vals['state']:
    #             self.env['hms.patient.log'].create({
    #                 'patient_id': rec.id,
    #                 'description': f"State changed from {rec.state} to {vals['state']}"
    #             })
    #     return super().write(vals)

    @api.onchange('department_ids')
    def onchange_department_opened(self):
        if self.department_ids and not self.department_ids.is_opened:
            return {
                'warning': {
                    'title': "Closed Department",
                    'message': "You can't assign a closed department to a patient."
                },
                'value': {
                    'department_ids': False
                }
            }

    @api.onchange('pcr')
    def onchange_pcr(self):
        if self.pcr and not self.cr_ratio:
            return {
                'warning': {
                    'title': "CR Ratio Required",
                    'message': "You must provide CR Ratio if PCR is checked."
                }
            }


    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked Automatically",
                    'message': "PCR has been checked automatically since age is below 30."
                }
            }


    @api.constrains('email')
    def check_email_format(self):
        for rec in self:
            if rec.email:
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, rec.email):
                    raise ValidationError("Invalid email format.")

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                birth_date = fields.Date.from_string(patient.birth_date)
                today = datetime.today()
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                patient.age = age
            else:
                patient.age = 0







#@api.onchange('state')
    # def onchange_state(self):
    #     if self.state:
    #         if self.id:
    #             self.env['hms.patient.log'].create({
    #                 'patient_id': self.id,
    #                 'created_by': self.env.user.id,
    #                 'date': fields.Datetime.now(),
    #                 'description': f"State changed to {self.state}",
    #             })
    #         else:
    #             raise UserError("Patient ID is missing.")

# @api.constrains('department_ids')
    # def check_department_opened(self):
    #     for rec in self:
    #         if rec.department_ids and not rec.department_ids.is_opened:
    #             raise ValidationError("You can't assign a closed department to a patient.")

 # @api.onchange('state')
    # def _onchange_state_log(self):
    #     if self.state:
    #         return {
    #             'warning': {
    #                 'title': 'State Changed',
    #                 'message': f'State changed to {self.state}'
    #             }
    #         }
# @api.model
    # def create(self, vals):
    #     patient = super(HmsPatient, self).create(vals)
    #
    #     self.env['hms.patient.log'].create({
    #         'patient_id': patient.id,
    #         'created_by': self.env.user.id,
    #         'date': fields.Datetime.now(),
    #         'description': 'Patient created'
    #     })
    #
    #     return patient
    #
    # @api.onchange('state')
    # def onchange_state(self):
    #     if self.state:
    #         self.env['hms.patient.log'].create({
    #             'patient_id': self.id,
    #             'description': f"State changed to {self.state}",
    #         })