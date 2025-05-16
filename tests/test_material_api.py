from odoo.tests.common import HttpCase
import json
import base64
import logging

_logger = logging.getLogger(__name__)

class TestMaterialAPI(HttpCase):
    """Tests for the Material Registration API endpoints."""
    
    @classmethod
    def setUpClass(cls):
        super(TestMaterialAPI, cls).setUpClass()
        try:
            # Create test data that will be shared across all test methods
            cls.supplier = cls.env['res.partner'].create({
                'name': 'API Test Supplier',
                'email': 'api_supplier@test.com',
            })
            
            cls.material = cls.env['material.registration'].create({
                'material_code': 'API001',
                'name': 'API Test Material',
                'material_type': 'fabric',
                'buy_price': 200.0,
                'supplier_id': cls.supplier.id,
            })
            
            # Create test user with specific access rights
            cls.api_user = cls.env['res.users'].create({
                'name': 'API Test User',
                'login': 'api_test_user',
                'password': 'test_password',
                'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])]
            })
            
            # Force commit to ensure data is available for HTTP tests
            cls.env.cr.commit()
        except Exception as e:
            _logger.error("Error in setUpClass: %s", e)
            cls.env.cr.rollback()
            raise

    def setUp(self):
        super(TestMaterialAPI, self).setUp()
        # Authentication credentials
        self.credentials = base64.b64encode(
            f"{self.api_user.login}:test_password".encode()
        ).decode()
        self.headers = {
            'Authorization': f'Basic {self.credentials}',
            'Content-Type': 'application/json'
        }
    
    def test_get_materials(self):
        """Test GET /api/materials endpoint."""
        try:
            # Use URL with authentication to avoid connection issues
            url = f"/api/materials"
            
            # Make the request with proper error handling
            response = self.url_open(url, headers=self.headers)
            self.assertEqual(response.status_code, 200)
            
            # Parse and validate response
            result = json.loads(response.text)
            self.assertEqual(result.get('status'), 'success')
            self.assertIsInstance(result.get('data'), list)
            
            # Verify our test material is in the results
            material_found = False
            for material in result.get('data', []):
                if material.get('material_code') == 'API001':
                    material_found = True
                    break
            self.assertTrue(material_found, "Test material not found in API response")
            
        except Exception as e:
            _logger.error("Error in test_get_materials: %s", e)
            self.env.cr.rollback()
            raise
    
    def test_filter_by_material_type(self):
        """Test filtering materials by material_type."""
        try:
            # Create materials with different types to ensure filtering works
            fabric_material = self.env['material.registration'].create({
                'material_code': 'FABRIC001',
                'name': 'Fabric Test',
                'material_type': 'fabric',
                'buy_price': 200.0,
                'supplier_id': self.supplier.id,
            })
            
            jeans_material = self.env['material.registration'].create({
                'material_code': 'JEANS001',
                'name': 'Jeans Test',
                'material_type': 'jeans',
                'buy_price': 300.0,
                'supplier_id': self.supplier.id,
            })
            
            # Force commit to ensure data is available for HTTP tests
            self.env.cr.commit()
            
            # Test fabric filter
            response = self.url_open(
                "/api/materials?material_type=fabric", 
                headers=self.headers
            )
            self.assertEqual(response.status_code, 200)
            
            result = json.loads(response.text)
            self.assertEqual(result.get('status'), 'success')
            
            # Verify all returned materials are fabric type
            for material in result.get('data', []):
                self.assertEqual(material.get('material_type'), 'fabric')
            
            # Test jeans filter
            response = self.url_open(
                "/api/materials?material_type=jeans", 
                headers=self.headers
            )
            self.assertEqual(response.status_code, 200)
            
            result = json.loads(response.text)
            self.assertEqual(result.get('status'), 'success')
            
            # Verify all returned materials are jeans type
            for material in result.get('data', []):
                self.assertEqual(material.get('material_type'), 'jeans')
                
        except Exception as e:
            _logger.error("Error in test_filter_by_material_type: %s", e)
            self.env.cr.rollback()
            raise
    
    def test_create_material(self):
        """Test POST /api/materials endpoint."""
        try:
            # Prepare payload
            data = {
                'material_code': 'TEST_CREATE_001',
                'name': 'Created Via API Test',
                'material_type': 'cotton',
                'buy_price': 150.0,
                'supplier_id': self.supplier.id,
            }
            
            # Make the request with controller_activate
            # This uses xml-rpc instead of direct HTTP which is more stable
            response = self.url_open(
                "/api/materials",
                headers=self.headers,
                data=json.dumps(data),
                method='POST'
            )
            
            # Verify the response
            self.assertEqual(response.status_code, 200)
            result = json.loads(response.text)
            self.assertEqual(result.get('status'), 'success')
            
            # Verify the material was actually created
            created_material = self.env['material.registration'].search([
                ('material_code', '=', 'TEST_CREATE_001')
            ])
            self.assertTrue(created_material.exists())
            self.assertEqual(created_material.name, 'Created Via API Test')
            
        except Exception as e:
            _logger.error("Error in test_create_material: %s", e)
            self.env.cr.rollback()
            raise
    
    def test_update_material(self):
        """Test PUT /api/materials/{id} endpoint."""
        try:
            # Create a material to update
            material_to_update = self.env['material.registration'].create({
                'material_code': 'UPDATE001',
                'name': 'Material To Update',
                'material_type': 'jeans',
                'buy_price': 150.0,
                'supplier_id': self.supplier.id,
            })
            self.env.cr.commit()
            
            # Prepare update data
            update_data = {
                'name': 'Updated Material Name',
                'buy_price': 250.0,
            }
            
            # Make the request
            response = self.url_open(
                f"/api/materials/{material_to_update.id}",
                headers=self.headers,
                data=json.dumps(update_data),
                method='PUT'
            )
            
            # Verify the response
            self.assertEqual(response.status_code, 200)
            result = json.loads(response.text)
            self.assertEqual(result.get('status'), 'success')
            
            # Refresh from database and verify updates
            material_to_update.invalidate_cache()
            updated_material = self.env['material.registration'].browse(material_to_update.id)
            self.assertEqual(updated_material.name, 'Updated Material Name')
            self.assertEqual(updated_material.buy_price, 250.0)
            
        except Exception as e:
            _logger.error("Error in test_update_material: %s", e)
            self.env.cr.rollback()
            raise
    
    def test_delete_material(self):
        """Test DELETE /api/materials/{id} endpoint."""
        try:
            # Create a material to delete
            material_to_delete = self.env['material.registration'].create({
                'material_code': 'DELETE001',
                'name': 'Material To Delete',
                'material_type': 'jeans',
                'buy_price': 150.0,
                'supplier_id': self.supplier.id,
            })
            material_id = material_to_delete.id
            self.env.cr.commit()
            
            # Make the request
            response = self.url_open(
                f"/api/materials/{material_id}",
                headers=self.headers,
                method='DELETE'
            )
            
            # Verify the response
            self.assertEqual(response.status_code, 200)
            result = json.loads(response.text)
            self.assertEqual(result.get('status'), 'success')
            
            # Verify the material was deleted
            deleted_material = self.env['material.registration'].browse(material_id)
            self.assertFalse(deleted_material.exists())
            
        except Exception as e:
            _logger.error("Error in test_delete_material: %s", e)
            self.env.cr.rollback()
            raise

    @classmethod
    def tearDownClass(cls):
        try:
            # Clean up created test data to prevent interference with other tests
            if hasattr(cls, 'material') and cls.material.exists():
                cls.material.unlink()
            if hasattr(cls, 'supplier') and cls.supplier.exists():
                cls.supplier.unlink()
            if hasattr(cls, 'api_user') and cls.api_user.exists():
                cls.api_user.unlink()
        except Exception as e:
            _logger.error("Error in tearDownClass: %s", e)
        finally:
            super(TestMaterialAPI, cls).tearDownClass()