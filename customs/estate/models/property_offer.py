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
    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _order = "price DESC"
    _sql_constraints = [
        ("offer_price_positive", "CHECK(price > 0)", "Offer Price must be strictly positive"),
    ]

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

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            # Set the property info
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
