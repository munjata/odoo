from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer("Color")

    _order = "name"
