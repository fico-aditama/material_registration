from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'material.registration'
    _description = 'Material Registration'

    material_code = fields.Char(string='Material Code', required=True)
    name = fields.Char(string='Material Name', required=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True)
    buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', required=True)
    
    _sql_constraints = [
        ('material_code_unique', 'unique(material_code)', 'Material Code must be unique!')
    ]
    
    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError(_("Material Buy Price cannot be less than 100!"))