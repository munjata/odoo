from datetime import timedelta, datetime

from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            try:
                record.date_deadline = self.create_date + timedelta(record.validity)
            except Exception as e:  # occurs on first creation
                record.date_deadline = fields.Date.today() + timedelta(record.validity)

    def _inverse_deadline(self):
        for record in self:
            delta = record.date_deadline - fields.Date.today()
            record.validity = delta.days
