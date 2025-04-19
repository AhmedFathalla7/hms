from odoo import models, fields,api
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")
    vat = fields.Char(string="Tax ID", required=True)

    @api.constrains('email')
    def _check_email_not_in_patient(self):
        for partner in self:
            if partner.email:
                patient = self.env['hms.patient'].search([('email', '=', partner.email)], limit=1)
                if patient:
                    raise ValidationError("This email is already used by a patient. Please use a different email.")

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise UserError("You cannot delete a customer linked to a patient.")
        return super(ResPartner, self).unlink()