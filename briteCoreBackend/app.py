import flask
import json
from flask import Flask
from flask_restplus import Api, Resource
from resources.risk_types import RiskType
from resources.field_risk_type import FieldRiskType


app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Insurance Services',
    description='A series services needed to aid insurance bussiness.'
)


insurance_ns = api.namespace(
    'insurances',
    description='Services to aid in finding a insurer type risks.'
)


@insurance_ns.route('risktypes/<int:risk_type_key>/detail')
@api.doc(params={'risk_type_key': 'Risk Type ID'})
class RiskTypeDetail(Resource):

    @api.response(200, 'Success')
    @api.response(404, 'Risk Type not found')
    @api.response(409, 'Conflict')
    def get(self, risk_type_key):
        """
        Get a risk type  information by risk_type_key

        * Send an risk_type_key  as required field and returns type risk information.

        """
        try:
            result = FieldRiskType().find_risktype_fields(risk_type_key)
            return flask.Response(json.dumps(result), status=200, mimetype='application/json')
        except Exception as e:
            raise e


@insurance_ns.route('/risktypes/<int:insurer_key>')
@api.doc(params={'insurer_key': 'Insurer ID'})
class RiskTypesInsurer(Resource):

    def get(self, insurer_key):
        """
        Get a all risks types  information by insurer

        * Send an insurer_key  as required field and returns all risk types  information.
        ```
        {
            "insurer": "insurer associated with this risk",
            "number": "risk id,shown in this exercise with the only purpose that serves as data to consume the detail service"
            "name": "Risk name"
            "description": "Risk detail information",
            "created_at": "Creation Date",
            "updated_at": "Last Update Date"
            
        }

        ```

        """

        try:
            result = RiskType().find_by_insurer_id(insurer_key)
            return flask.Response(json.dumps(result), status=200, mimetype='application/json')
        except Exception as e:
            raise e


if __name__ == "__main__":
    app.run(debug=True)
