from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    label_product_name = fields.Char(string="Product Name", readonly=True)
    label_product_id = fields.Many2one('product.product', string="Product ID", readonly=True)
    label_material_name = fields.Char(string="Material Name", readonly=True)
    label_material_id = fields.Many2one('product.product', string="Material ID", readonly=True)
    label_lot_number = fields.Char(string="Lot Number", readonly=True)
    label_date_printing = fields.Date(string="Date of Printing", default=fields.Date.today)
    label_expiration_date = fields.Date(string="Expiration Date", readonly=True)
    label_expected_weight = fields.Float(string="Expected Weight")
    label_actual_weight = fields.Float(string="Actual Weight", default=0.0)
    label_batch_number = fields.Char(string="Batch Number", readonly=True)

    receiver_signature = fields.Binary(string="Receiver's Signature", help="Signature of the receiver")
    supervisor_signature = fields.Binary(string="Supervisor's Signature", help="Signature of the supervisor")
    can_print_inventory_label = fields.Boolean(compute="_compute_can_print_inventory_label", store=False)

    @api.depends('picking_type_id', 'location_id', 'location_dest_id', 'state')
    def _compute_can_print_inventory_label(self):
        for picking in self:
            picking.can_print_inventory_label = (
                    picking.picking_type_id.id == 19 and
                    picking.location_id.id == 44 and
                    picking.location_dest_id.id == 45 and
                    picking.state == 'assigned'
            )

    @api.depends('move_lines.product_id', 'move_lines.lot_ids')
    def _compute_label_details(self):
        for record in self:
            if record.move_lines:
                first_move = record.move_lines[0]  # Just taking the first move for simplicity
                record.label_product_name = first_move.product_id.name
                record.label_product_id = first_move.product_id.id
                record.label_material_name = first_move.product_id.name
                record.label_material_id = first_move.product_id.id

                if first_move.lot_ids:
                    record.label_lot_number = first_move.lot_ids[0].name
                    record.label_batch_number = first_move.lot_ids[0].name
                    record.label_expiration_date = first_move.lot_ids[0].use_by_date or (fields.Date.today() + timedelta(days=30))
                else:
                    record.label_lot_number = ''
                    record.label_batch_number = ''
                    record.label_expiration_date = fields.Date.today() + timedelta(days=30)
            else:
                record.label_product_name = ''
                record.label_product_id = False
                record.label_material_name = ''
                record.label_material_id = False
                record.label_lot_number = ''
                record.label_batch_number = ''
                record.label_expiration_date = fields.Date.today() + timedelta(days=30)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'label_expiration_date' not in res:
            res['label_expiration_date'] = fields.Date.today() + timedelta(days=30)
        return res
