from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    label_product_name = fields.Char(string="Product Name", compute="_compute_label_details")
    label_product_id = fields.Many2one('product.product', string="Product ID", compute="_compute_label_details")
    label_material_name = fields.Char(string="Material Name", compute="_compute_label_details")
    label_material_id = fields.Many2one('product.product', string="Material ID", compute="_compute_label_details")
    label_lot_number = fields.Char(string="Lot Number", compute="_compute_label_details")
    label_date_printing = fields.Date(string="Date of Printing", default=fields.Date.today)
    label_expiration_date = fields.Date(string="Expiration Date", compute="_compute_label_details")
    label_expected_weight = fields.Float(string="Expected Weight")
    label_actual_weight = fields.Float(string="Actual Weight", default=0.0)

    @api.depends('move_line_ids.product_id', 'move_line_ids.lot_id', 'move_line_ids.product_id.expiration_date')
    def _compute_label_details(self):
        for picking in self:
            if picking.move_line_ids:
                move = picking.move_line_ids[0]  # Get details from the first move line
                picking.label_product_name = move.product_id.name
                picking.label_product_id = move.product_id.id
                picking.label_material_name = move.product_id.name  # Adjust if different material
                picking.label_material_id = move.product_id.id  # Adjust if different material
                picking.label_lot_number = move.lot_id.name if move.lot_id else ''
                picking.label_expiration_date = move.product_id.expiration_date
                # Add logic for expected weight if needed
            else:
                # Reset values if there are no move lines
                picking.label_product_name = ''
                picking.label_product_id = False
                picking.label_material_name = ''
                picking.label_material_id = False
                picking.label_lot_number = ''
                picking.label_expiration_date = False

    def action_print_label(self):
        return self.env.ref('custom_inventory_label.inventory_label_report').report_action(self)
