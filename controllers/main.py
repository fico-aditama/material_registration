from odoo import http
from odoo.http import request, Response
import json

class MaterialController(http.Controller):
    
    @http.route('/api/materials', type='http', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        try:
            domain = []
            if kwargs.get('material_type'):
                domain.append(('material_type', '=', kwargs.get('material_type')))
                
            materials = request.env['material.registration'].sudo().search(domain)
            data = []
            
            for material in materials:
                data.append({
                    'id': material.id,
                    'material_code': material.material_code,
                    'name': material.name,
                    'material_type': material.material_type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id,
                    'supplier_name': material.supplier_id.name,
                })
                
            return Response(
                json.dumps({'status': 'success', 'data': data}),
                content_type='application/json'
            )
        except Exception as e:
            request.env.cr.rollback()
            return Response(
                json.dumps({'status': 'error', 'message': str(e)}),
                content_type='application/json'
            )
    
    @http.route('/api/materials', type='json', auth='user', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        try:
            data = request.jsonrequest
            material = request.env['material.registration'].sudo().create({
                'material_code': data.get('material_code'),
                'name': data.get('name'),
                'material_type': data.get('material_type'),
                'buy_price': data.get('buy_price'),
                'supplier_id': data.get('supplier_id'),
            })
            request.env.cr.commit()
            
            return {
                'status': 'success',
                'id': material.id,
                'message': 'Material created successfully'
            }
        except Exception as e:
            request.env.cr.rollback()
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @http.route('/api/materials/<int:material_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        try:
            data = request.jsonrequest
            material = request.env['material.registration'].sudo().browse(material_id)
            
            if not material.exists():
                return {
                    'status': 'error',
                    'message': 'Material not found'
                }
                
            material.write({
                'material_code': data.get('material_code', material.material_code),
                'name': data.get('name', material.name),
                'material_type': data.get('material_type', material.material_type),
                'buy_price': data.get('buy_price', material.buy_price),
                'supplier_id': data.get('supplier_id', material.supplier_id.id),
            })
            request.env.cr.commit()
            
            return {
                'status': 'success',
                'message': 'Material updated successfully'
            }
        except Exception as e:
            request.env.cr.rollback()
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @http.route('/api/materials/<int:material_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        try:
            material = request.env['material.registration'].sudo().browse(material_id)
            
            if not material.exists():
                return Response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Material not found'
                    }),
                    content_type='application/json'
                )
                
            material.unlink()
            request.env.cr.commit()
            
            return Response(
                json.dumps({
                    'status': 'success',
                    'message': 'Material deleted successfully'
                }),
                content_type='application/json'
            )
        except Exception as e:
            request.env.cr.rollback()
            return Response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                content_type='application/json'
            )