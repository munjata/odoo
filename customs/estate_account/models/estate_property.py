from odoo import models, api


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        print("Action Sold in ... estate_account ")

        return super().action_sold_property()
