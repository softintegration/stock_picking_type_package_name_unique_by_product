# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

CHECKED_PACKAGE_FIELD_BY_PICKING_TYPE = {
    'incoming':('result_package_id',),
    'internal':('package_id','result_package_id'),
    'outgoing':('package_id',)
}

class StockPicking(models.Model):
    _inherit = "stock.picking"


    def _check_product_id_package_name_unicity(self):
        for each in self.filtered(lambda pick:pick.picking_type_id.unique_product_package_name):
            package_fields_to_check = CHECKED_PACKAGE_FIELD_BY_PICKING_TYPE[each.picking_type_code]
            for check_field in package_fields_to_check:
                for ml in each.move_line_ids:
                    if not getattr(ml,check_field,False):
                        continue
                    domain = [('picking_id','=',each.id),('product_id','=',ml.product_id.id),('id','!=',ml.id),
                              ('%s_name'%check_field,'=',getattr(ml,'%s_name'%check_field))]
                    if self.env['stock.move.line'].search_count(domain):
                        raise ValidationError(_("Package reference must be unique by product in this type of transfer"))




