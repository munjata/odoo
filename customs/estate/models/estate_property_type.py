from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to sort Type. Lower is better")

    _order = "name"
    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "Tag name already exists!"),
    ]
