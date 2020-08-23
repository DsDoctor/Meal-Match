from flask import Blueprint, request
from flask_restful import Api
from flask import render_template
from flask import session
from Service.Search import search

search_bp = Blueprint('search', __name__)
search_api = Api(search_bp)

# main search function
search_api.add_resource(search.SearchAPI, '/search/recipes')
# running list functions
search_api.add_resource(search.RunningList, '/running_list')
# api for add a set of ingredients to running list
search_api.add_resource(search.AddToList, '/running_list/add')
# api for clear all ingredients from running list
search_api.add_resource(search.ClearRunningList, '/running_list/clear')
# Get all ingredient types, rendering to ingredient selector
search_api.add_resource(search.SearchIngType, '/search/ing_type')
# filter functions
search_api.add_resource(search.Filter, '/search/filters')
# clear all filters
search_api.add_resource(search.ClearFilter, '/search/clear')


@search_bp.route('/search')
def ingredients():
    filter_args = request.args.get('filter')
    data = {'string': request.args.get('string'),
            'filter': filter_args if filter_args else '',
            'user': session.get('user'),
            'login': 'true' if session.get('id') else 'false'}
    f_check = session.get('filter')
    if not f_check:
        f_check = []
    else:
        f_check = eval(f_check)
        f_check = [f['id'] for f in f_check]
    if filter_args:
        f_check.extend([int(f) for f in filter_args.split(',') if f])
    for i in range(1, 38):
        data[f'f{i}_check'] = 'checked' if i in f_check else ''
    return render_template('search.html', **data)
