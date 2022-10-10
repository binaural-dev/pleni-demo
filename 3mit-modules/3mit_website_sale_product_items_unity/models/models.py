# -*- coding: utf-8 -*-

from asyncio.log import logger
from odoo import models, fields, api
from odoo.exceptions import UserError


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        res = super(ProductTemplateInherit, self)._get_combination_info(combination, product_id, add_qty, pricelist, parent_combination, only_template)
        uom_id = self.env['product.template'].browse(res.get('product_template_id')).uom_id
        res['uom_id'] = uom_id.name
        
        res['wholesale_price'] = None
        product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        if not product or not pricelist: return res
        pricelist_items = self.env['product.pricelist.item'].sudo().search([('pricelist_id','=',pricelist.id),'|',('product_tmpl_id','=',self.id),('product_id','=',product.id)], order= 'min_quantity asc')
        if not pricelist_items: return res
        res['wholesale_price'] = pricelist_items[-1].fixed_price if pricelist_items[-1].fixed_price != res['price'] else None
        if res['wholesale_price']:
            res['discount_rate'] = round(100-((res['price']*100)/res['wholesale_price']))
        return res

