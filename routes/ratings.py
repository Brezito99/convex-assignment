import requests
import pandas as pd
from flask import Blueprint, json, Response, current_app
from utils.rating_adapter import RatingAdapter

MIME_JSON = 'application/json'


ratings_blueprint = Blueprint("ratings", __name__)


@ratings_blueprint.route('/api', methods=["GET"])
def get_authorities() -> Response:
    """Fetch authorities and return a list of their IDs and name."""
    uri = current_app.config['FSA_API_URI'] + '/Authorities'
    resp = requests.get(uri, headers={'x-api-version': '2'})

    if resp.status_code != requests.codes.ok:
        raise requests.HTTPError('FSA API call to {} returned error {}'.format(uri, resp.status_code))

    authorities = []
    for authority in resp.json()['authorities']:
        authorities.append(
            {
                'id': authority['LocalAuthorityId'],
                'name': authority['Name'],
                'region': authority['RegionName']
            }
        )

    return Response(json.dumps(authorities), mimetype=MIME_JSON)


@ratings_blueprint.route('/api/?id=<int:authority_id>&region=<string:authority_region>', methods=["GET"])
def get_authority(authority_id: int, authority_region: str) -> Response:
    """Fetch establishments under a specific authority"""
    # This is just sample data to demonstrate what the front-end is expecting

    if authority_id == 0:
        return Response(json.dumps(RatingAdapter.loading_value()), mimetype=MIME_JSON)

    try:
        uri = current_app.config['FSA_API_URI'] + current_app.config['ESTABLISHMENT_URI_PATH'] + str(authority_id)

        resp = requests.get(uri, headers={'x-api-version': '2'})

        # convert data to dataframe for faster grouping and aggregation
        df = pd.DataFrame(resp.json()['establishments'])

        # prepare rating format for frontend
        output_list = df['RatingValue'].value_counts().__truediv__(len(df)).__mul__(100).sort_index().reset_index() \
            .rename(columns={'RatingValue': 'name', 'count': 'value'}).to_dict(orient='records')

        # postprocess rating according to region (i.e. Scotland doesn't use the star system)
        demo = RatingAdapter.prepare_rating_output(output_list, authority_region)
    except Exception as e:
        print(str(e))
        # default value in case of communication error
        demo = RatingAdapter.default_value()

    return Response(json.dumps(demo), mimetype=MIME_JSON)
