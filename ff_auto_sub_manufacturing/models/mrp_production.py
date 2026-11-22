from odoo import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _ff_manufacture_rule_for_product(self, product):
        """Return the native manufacture rule for a manufactured component."""
        self.ensure_one()
        routes = product.route_ids | product.categ_id.total_route_ids
        route_rules = routes.rule_ids.filtered(
            lambda rule: rule.action == 'manufacture' and rule.active
        )
        if route_rules:
            return route_rules.sorted(
                key=lambda rule: (rule.route_sequence, rule.sequence)
            )[0]
        warehouse_rule = self.picking_type_id.warehouse_id.manufacture_pull_id
        if warehouse_rule and warehouse_rule.active and warehouse_rule.action == 'manufacture':
            return warehouse_rule
        return self.env['stock.rule']

    def _ff_normal_bom_for_product(self, product):
        self.ensure_one()
        return self.env['mrp.bom']._bom_find(
            product,
            picking_type=self.picking_type_id,
            bom_type='normal',
            company_id=self.company_id.id,
        )[product]

    def _ff_create_sub_manufacturing_orders(self):
        """Create one native child MO for every manufactured raw component."""
        for production in self.filtered(lambda mo: mo.state not in ('cancel', 'done')):
            component_moves = production.move_raw_ids.filtered(
                lambda move: move.state not in ('cancel', 'done')
            )
            if not component_moves:
                continue

            # Serialize confirmations so concurrent confirmations cannot create
            # duplicate child orders for the same parent raw move.
            self.env.cr.execute(
                'SELECT id FROM stock_move WHERE id IN %s FOR UPDATE',
                [tuple(component_moves.ids)],
            )
            procurements = []
            for move in component_moves:
                bom = production._ff_normal_bom_for_product(move.product_id)
                rule = production._ff_manufacture_rule_for_product(move.product_id)
                if not bom or not rule:
                    continue
                if move.move_orig_ids.mapped('production_id').filtered(
                    lambda child: child.state not in ('cancel', 'done')
                ):
                    continue

                shortage_product_qty = max(move.product_qty - move.quantity, 0.0)
                shortage_qty = move.product_id.uom_id._compute_quantity(
                    shortage_product_qty,
                    move.uom_id,
                    rounding_method='HALF-UP',
                )
                if move.uom_id.compare(shortage_qty, 0.0) <= 0:
                    continue

                values = move._prepare_procurement_values()
                values.update({
                    'move_dest_ids': move,
                    'production_group_id': move.production_group_id.id,
                    'date_planned': move.date,
                    'date_deadline': move.date_deadline,
                    'reference_ids': move.reference_ids,
                })
                procurements.append((self.env['stock.rule'].Procurement(
                    move.product_id,
                    shortage_qty,
                    move.uom_id,
                    move.location_id,
                    rule.name,
                    move._prepare_procurement_origin(),
                    move.company_id,
                    values,
                ), rule))
            if procurements:
                self.env['stock.rule'].with_context(
                    manual_replenishment=True,
                )._run_manufacture(procurements)

    def action_confirm(self):
        result = super().action_confirm()
        self._ff_create_sub_manufacturing_orders()
        return result
