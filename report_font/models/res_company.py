# Copyright 2022 Amin Cheloh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    font = fields.Selection(
        selection_add=[
            ("Pyidaungsu Bold", "Pyidaungsu Bold"),
            ("Pyidaungsu Number", "Pyidaungsu Number"),
            ("Pyidaungsu Regular", "Pyidaungsu Regular"),
            ("Pyidaungsu Book Bold", "Pyidaungsu Book Bold"),
            ("Pyidaungsu Book Regular", "Pyidaungsu Book Regular"),
            ("Zawgyi", "Zawgyi"),
        ]
    )
