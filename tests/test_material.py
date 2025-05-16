from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError

class TestMaterial(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestMaterial, cls).setUpClass()
        # Use setUpClass for test data that can be shared across all tests
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Test Supplier',
            'email': 'supplier@test.com',
        })
        
    def test_create_material(self):
        """Test creating a valid material record."""
        material = self.env['material.registration'].create({
            'material_code': 'M001',
            'name': 'Test Material',
            'material_type': 'fabric',
            'buy_price': 150.0,
            'supplier_id': self.supplier.id,
        })
        self.assertEqual(material.material_code, 'M001')
        self.assertEqual(material.name, 'Test Material')
        
    def test_buy_price_constraint(self):
        """Test that buy_price < 100 raises ValidationError."""
        with self.assertRaises(ValidationError):
            self.env['material.registration'].create({
                'material_code': 'M002',
                'name': 'Test Material 2',
                'material_type': 'jeans',
                'buy_price': 50.0,  # Less than 100, should raise ValidationError
                'supplier_id': self.supplier.id,
            })