from odoo import Command
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestAutoSubManufacturing(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.finished, cls.component = cls.env['product.product'].create([
            {'name': 'FF ASM Finished', 'type': 'consu', 'is_storable': True},
            {'name': 'FF ASM Component', 'type': 'consu', 'is_storable': True},
        ])
        cls.component_bom = cls.env['mrp.bom'].create({
            'product_id': cls.component.id,
            'product_tmpl_id': cls.component.product_tmpl_id.id,
            'product_qty': 1.0,
            'uom_id': cls.component.uom_id.id,
        })
        cls.parent_bom = cls.env['mrp.bom'].create({
            'product_id': cls.finished.id,
            'product_tmpl_id': cls.finished.product_tmpl_id.id,
            'product_qty': 1.0,
            'uom_id': cls.finished.uom_id.id,
            'bom_line_ids': [Command.create({
                'product_id': cls.component.id,
                'product_qty': 2.0,
            })],
        })

    def _new_mo(self):
        form = Form(self.env['mrp.production'])
        form.product_id = self.finished
        form.bom_id = self.parent_bom
        form.product_qty = 1.0
        return form.save()

    def test_confirm_creates_one_linked_child_mo(self):
        parent = self._new_mo()
        parent.action_confirm()
        move = parent.move_raw_ids.filtered(
            lambda raw_move: raw_move.product_id == self.component
        )
        children = move.move_orig_ids.mapped('production_id').filtered(
            lambda child: child.state not in ('cancel', 'done')
        )
        self.assertEqual(len(children), 1)
        self.assertEqual(children.product_id, self.component)
        self.assertEqual(children.product_qty, 2.0)
        self.assertIn(parent.production_group_id, children.production_group_id.parent_ids)

    def test_confirm_is_idempotent_for_existing_child(self):
        parent = self._new_mo()
        parent.action_confirm()
        parent._ff_create_sub_manufacturing_orders()
        move = parent.move_raw_ids.filtered(
            lambda raw_move: raw_move.product_id == self.component
        )
        self.assertEqual(len(move.move_orig_ids.mapped('production_id')), 1)

    def test_component_without_bom_is_ignored(self):
        component = self.env['product.product'].create({
            'name': 'FF ASM Stock Component', 'type': 'consu', 'is_storable': True,
        })
        bom = self.env['mrp.bom'].create({
            'product_id': self.finished.id,
            'product_tmpl_id': self.finished.product_tmpl_id.id,
            'product_qty': 1.0,
            'uom_id': self.finished.uom_id.id,
            'bom_line_ids': [Command.create({
                'product_id': component.id,
                'product_qty': 1.0,
            })],
        })
        form = Form(self.env['mrp.production'])
        form.product_id = self.finished
        form.bom_id = bom
        parent = form.save()
        parent.action_confirm()
        move = parent.move_raw_ids.filtered(
            lambda raw_move: raw_move.product_id == component
        )
        self.assertFalse(move.move_orig_ids.mapped('production_id'))
