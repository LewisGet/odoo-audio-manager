import os
from odoo import models, fields, api


class AudioTag(models.Model):
    _name = 'audio.tag'
    _description = 'audio tag'

    name = fields.Char()
    description = fields.Text()
    audio_ids = fields.Many2many('audio.file')
