from odoo import fields, models, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    inclusive_price = fields.Float(string="Inclusive Price")

    @api.onchange("price_unit")
    def _onchange_price_unit(self):
        for line in self:
            line.inclusive_price = line.price_unit * 1.15 if line.price_unit else 0.0

    @api.onchange("inclusive_price")
    def _onchange_inclusive_price(self):
        for line in self:
            line.price_unit = line.inclusive_price * (100/115) if line.inclusive_price else 0.0

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("price_unit"):
                vals["inclusive_price"] = vals["price_unit"] * 1.15
            elif vals.get("inclusive_price"):
                vals["price_unit"] = vals["inclusive_price"] * (100/115)
        return super().create(vals_list)

    def write(self, vals):
        for line in self:
            if "price_unit" in vals:
                vals["inclusive_price"] = vals["price_unit"] * 1.15
            elif "inclusive_price" in vals:
                vals["price_unit"] = vals["inclusive_price"] * (100/115)
        return super().write(vals)
