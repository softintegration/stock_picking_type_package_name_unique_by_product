# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    unique_product_package_name = fields.Boolean(string='Unique package name by product', default=False,
                                                 help="If this case is checked,we can't attribute the same package reference to different packages with the same product in the same transfer.")

