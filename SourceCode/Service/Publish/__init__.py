from flask import Blueprint
from flask_restful import Api
from flask import render_template
from Service.Publish import publish

publish_bp = Blueprint('publish', __name__)
publish_api = Api(publish_bp)

# publish api for creating new recipe, getting published recipe and deleting published recipe
publish_api.add_resource(publish.PublishAPI, '/publish_api')
# for receiving uploaded images
publish_api.add_resource(publish.PublishFile, '/publish/file')


# route for publish page
@publish_bp.route('/publish')
def publish():
    return render_template('publish.html')


# route for edit publish page
@publish_bp.route('/edit_publish/<r_id>')
def get_published(r_id):
    data = {'r_id': r_id}
    return render_template('edit_publish.html', **data)
