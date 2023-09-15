from datetime import timedelta
from odoo import api, fields, models


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
        ],
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="SalesPerson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Total Area", compute="_compute_total", help="The Total surface Area")
    best_price = fields.Float(string="Price Price", compute="_best_price", help="Highest Price Offered")

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
