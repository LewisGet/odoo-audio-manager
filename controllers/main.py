from odoo import http
from odoo.http import request
from odoo.http import Response
from datetime import datetime, date
import json
import glob

from pydub import AudioSegment


class Regedit(http.Controller):

    @http.route('/api/<string:model_name>/get/<int:object_id>', type='http', auth='public', methods=['GET'])
    def model_get(self, model_name, object_id, **get):
        request.session.authenticate(get['db'], login=get['username'], password=get['password'])

        obj = request.env[model_name].sudo().browse(object_id)

        if not obj.exists():
            return Response(
                {"error": "Record not found"},
                status=404
            )

        data = dict()

        for field_index, field_object in obj._fields.items():
            field_value = getattr(obj, field_index)
            data[field_index] = field_value

            if field_object.type == "many2many":
                data[field_index] = [related.id for related in field_value]

            if field_object.type == "many2one":
                data[field_index] = field_value.id if field_value else None

            if isinstance(field_value, (datetime, date)):
                data[field_index] = field_value.isoformat()

        return Response(json.dumps({"respond": data}), status=200)


    @http.route('/api/<string:model_name>/set/<int:object_id>', type='http', auth='public', methods=['GET'])
    def model_set(self, model_name, object_id, **get):
        request.session.authenticate(get['db'], login=get['username'], password=get['password'])

        obj = request.env[model_name].sudo().browse(object_id)

        if not obj.exists():
            return {"respond": "404"}

        fields = obj._fields
        updates = []
        passing = []

        for field in fields:
            try:
                value = get[field]

                if fields[field].type == "many2one":
                    value = int(get[field])

                if fields[field].type == "many2many":
                    value = [int(i) for i in get[field].split(",")]

                if isinstance(fields[field], (datetime, date)):
                    value = datetime.fromisoformat(get[field])

                obj.write({field: value})
                updates.append(field)
            except:
                passing.append(field)

        return Response(json.dumps({
            "updates": updates,
            "passing": passing
        }), status=200)


    @http.route('/audio_file/batch', type='http', auth='public', methods=['GET'])
    def batch_init_audio_file(self, **get):
        request.session.authenticate(get['db'], login=get['username'], password=get['password'])

        create_audio_files = []

        for path in glob.glob(get['path']):
            audio = AudioSegment.from_file(path)

            create_audio_files.append({
                "path" : path,
                "tag_ids" : [int(i) for i in get['tag_ids'].split(",")],
                "rates" : audio.frame_rate,
                "channels" : audio.channels,
                "length" : len(audio.get_array_of_samples())
            })

        try:
            request.env["audio.file"].sudo().create(create_audio_files)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500
            )

        return Response({"message": "done"}, status=200)
