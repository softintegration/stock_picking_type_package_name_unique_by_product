# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError



class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    unique_product_package_name = fields.Boolean(compute='_compute_unique_product_package_name')
    package_id_name = fields.Char(compute='_compute_package_id_name',store=True)
    result_package_id_name = fields.Char(compute='_compute_result_package_id_name',store=True)

    @api.depends('picking_id.picking_type_id.unique_product_package_name')
    def _compute_unique_product_package_name(self):
        for each in self:
            each.unique_product_package_name = each.picking_id.picking_type_id.unique_product_package_name

    @api.depends('package_id')
    def _compute_package_id_name(self):
        for each in self:
            each.package_id_name = each.package_id and each.package_id.name or False

    @api.depends('result_package_id')
    def _compute_result_package_id_name(self):
        for each in self:
            each.result_package_id_name = each.result_package_id and each.result_package_id.name or False

    def create(self, vals):
        move_lines = super(StockMoveLine, self).create(vals)
        move_lines.mapped('picking_id')._check_product_id_package_name_unicity()
        return move_lines

    def write(self, vals):
        res = super(StockMoveLine, self).write(vals)
        self.mapped('picking_id')._check_product_id_package_name_unicity()
        return res


