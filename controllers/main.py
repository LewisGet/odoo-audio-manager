from odoo import http
from odoo.http import request
from odoo.http import Response
import json


class Regedit(http.Controller):

    @http.route('/audio/get/<int:object_id>', type='http', auth='public', methods=['GET'])
    def audio_file_get(self, object_id, **get):
        request.session.authenticate(get['db'], login=get['username'], password=get['password'])

        obj = request.env['audio.file'].sudo().browse(object_id)

        if not obj.exists():
            return Response(
                {"error": "Record not found"},
                status=404
            )

        data = dict()

        for field_index, field_object in obj._fields.items():
            field_value = getattr(obj, field_index)
            data[field_index] = field_index

            if field_object.type == "many2many":
                data[field_index] = [related.id for related in field_value]

            if field_object.type == "many2one":
                data[field_index] = field_value.id if field_value else None

        return Response(json.dumps({"respond": data}), status=200)


    @http.route('/audio/set/<int:object_id>', type='http', auth='public', methods=['GET'])
    def audio_set_get(self, object_id, **get):
        request.session.authenticate(get['db'], login=get['username'], password=get['password'])

        obj = request.env['audio.file'].sudo().browse(object_id)

        if not obj.exists():
            return {"respond": "404"}

        fields = obj._fields
        updates = []
        passing = []

        for field in fields:
            try:
                obj.write({field: get[field]})
                updates.append(field)
            except:
                passing.append(field)

        return Response(json.dumps({
            "updates": updates,
            "passing": passing
        }), status=200)
