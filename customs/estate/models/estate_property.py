from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of an Estate"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Availability",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
        help="Date of Availability",
    )
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
        help="The expected sell price of the property",
    )
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2, help="Number of bedrooms")
    facades = fields.Integer()
    garage = fields.Boolean(string="Garage", help="Has Garage")
    living_area = fields.Integer(string="Living Area(sqm)", help="The surface of the Living Area")
    gardern_area = fields.Integer(string="Gardern Area", help="The surface of the garden")
    gardern_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Garden Orientation",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        default="new",
        selection=[
            ("new", "New"),
            ("offer", "Offer"),
            ("received", " Received"),
            ("accepted", "Offer Accepted"),
            ("canceled", "Sold Canceled"),
            ("sold", "Sold"),
        ],
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="SalesPerson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(string="Total Area", compute="_compute_total", help="The Total surface Area")
    best_price = fields.Float(string="Price Price", compute="_best_price", help="Highest Price Offered")

    _order = "id DESC"
    _sql_constraints = [
        ("expected_price_positive", "CHECK(expected_price > 0)", "Expected price must be strictly positive"),
        ("selling_price_positive", "CHECK(selling_price >= 0)", "Selling price must be positive"),
    ]

    @api.depends("living_area", "gardern_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.gardern_area

    @api.depends("offer_ids.price")
    def _best_price(self):
        for record in self:
            try:
                record.best_price = max(record.offer_ids.mapped("price"))
            except ValueError:
                record.best_price = None

    @api.onchange("garage")
    def _on_garden_change(self):
        if self.garage:
            self.gardern_area = 10
            self.gardern_orientation = "north"
        else:
            self.gardern_area = 0
            self.gardern_orientation = None

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError("Sold property can not be canceled")
            else:
                property.state = "canceled"
        return True

    def action_sold_property(self):
        for property in self:
            if property.state == "canceled":
                raise UserError("Canceled property can not be sold")
            else:
                property.state = "sold"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        "Ensure Selling price is not <90% of expected_price"
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue
            if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError(
                    "The Selling Price can not lower than 90% of the expected Price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )
