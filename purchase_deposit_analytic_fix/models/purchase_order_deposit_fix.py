# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging # Optional: for logging messages during testing
_logger = logging.getLogger(__name__) # Optional

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _prepare_deposit_move_line_vals(self, amount, taxes_vals):
        """
        Override to add analytic distribution from the first PO line
        to the deposit account move line.
        """
        # First, call the original method to get the list of line dictionaries
        lines_vals_list = super(PurchaseOrder, self)._prepare_deposit_move_line_vals(amount, taxes_vals)

        # Ensure there are PO lines to get analytic info from
        if not self.order_line:
            _logger.warning(f"Purchase Order {self.name}: No order lines found to fetch analytic distribution.")
            return lines_vals_list # Return original lines if no PO lines exist

        # Get analytic distribution from the first PO line (simplification)
        # Odoo 17 uses analytic_distribution (JSONB field - dictionary format)
        first_line = self.order_line[0]
        analytic_distribution = first_line.analytic_distribution

        _logger.info(f"Purchase Order {self.name}: First line analytic distribution: {analytic_distribution}") # Optional logging

        # Proceed only if analytic distribution is actually set on the first line
        if not analytic_distribution:
            _logger.warning(f"Purchase Order {self.name}: No analytic distribution found on the first order line ({first_line.name}).")
            return lines_vals_list # Return original lines if no analytic info found

        # Find the deposit account used (use the same logic as the original method)
        deposit_account_id = self._get_deposit_account()
        if not deposit_account_id:
            # This case should ideally be handled by the original method validation,
            # but double-checking doesn't hurt.
             _logger.error(f"Purchase Order {self.name}: Could not determine deposit account.")
             return lines_vals_list # Should not happen if original method works

        # Iterate through the prepared line dictionaries
        line_modified = False
        for line_vals_tuple in lines_vals_list:
            # line_vals_tuple is typically (0, 0, {line_dictionary})
            if len(line_vals_tuple) == 3 and isinstance(line_vals_tuple[2], dict):
                line_dictionary = line_vals_tuple[2]

                # Identify the deposit line:
                # It's the one posting to the deposit_account_id and
                # usually has a specific name like "Deposit Payment"
                # and will have a debit value (for standard deposits)
                if (line_dictionary.get('account_id') == deposit_account_id and
                        line_dictionary.get('debit', 0) > 0): # Check for debit > 0

                    # Add the analytic distribution to this line's dictionary
                    line_dictionary['analytic_distribution'] = analytic_distribution
                    line_modified = True
                    _logger.info(f"Purchase Order {self.name}: Applied analytic distribution {analytic_distribution} to deposit line.") # Optional logging
                    # Assuming only one main deposit line needs it, we can stop searching
                    break

        if not line_modified:
             _logger.warning(f"Purchase Order {self.name}: Could not find the specific deposit line (Account ID: {deposit_account_id}, Debit>0) in prepared move lines to apply analytics.")

        # Return the potentially modified list of line dictionaries
        return lines_vals_list
