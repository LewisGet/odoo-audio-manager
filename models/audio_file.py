import os
from odoo import models, fields, api


class AudioFile(models.Model):
    _name = 'audio.file'
    _description = 'auido file'

    path = fields.Char()
    tag_ids = fields.Many2many('audio.tag')
    rates = fields.Integer()
    channels = fields.Integer()
    length = fields.Integer()

    pad_p = fields.Float()
    pad_a = fields.Float()
    pad_d = fields.Float()
