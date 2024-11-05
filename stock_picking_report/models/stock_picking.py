from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    external_weight = fields.Char(string='External Weight', readonly=True)
    external_unit = fields.Char(string='External Unit', readonly=True)

    def fetch_and_print_report(self):
        """Fetch weight data from the external API and update fields."""
        remote_server_url = 'http://127.0.0.1:5001/balance'  # Adjust URL if necessary

        try:
            response = requests.get(remote_server_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                _logger.info(f"API response: {data}")

                # Extract unit and weight
                unit = data.get('unite', '')
                weight = data.get('value', '')

                # Validate and update fields
                if weight:
                    self.write({
                        'external_weight': weight,
                        'external_unit': unit
                    })
                    _logger.info("Updated fields with external weight and unit.")
                else:
                    _logger.warning("No weight received, fields will remain empty.")
                    self.write({'external_weight': '', 'external_unit': ''})

            else:
                _logger.error(f"Failed to fetch data: {response.status_code}")
                self.write({'external_weight': '', 'external_unit': ''})

        except requests.exceptions.RequestException as e:
            _logger.error(f"Error connecting to API: {e}")
            self.write({'external_weight': '', 'external_unit': ''})

        # Call the report action
        return self.action_print_report()

    def action_print_report(self):
        report_action = self.env.ref('stock_picking_report.action_report_stock_picking', raise_if_not_found=False)
        if report_action:
            return report_action.report_action(self)
        else:
            raise UserError("Report action not found.")
