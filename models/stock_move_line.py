# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from odoo.addons.stock_picking_type_package_name_unique_by_product.models.stock_picking import CHECKED_PACKAGE_FIELD_BY_PICKING_TYPE



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
        # if the write doesn't touch any of the fields that must be controled for package unicity we have to avoid the check
        # this is because the check is very costly in the case of picking with many move_line_ids and this is even when no
        # field that must be controlled are modified,so we have sacrified the code simplicity for the sake of performance
        # it is always tradeoff choice!!!
        try:
            package_fields_to_check = CHECKED_PACKAGE_FIELD_BY_PICKING_TYPE[self.mapped("picking_code")[0]]
            fields_to_edit = tuple(vals.keys())
            if not set(package_fields_to_check).intersection(set(fields_to_edit)):
                return res
        except IndexError:
            return res
        self.mapped('picking_id')._check_product_id_package_name_unicity()
        return res


