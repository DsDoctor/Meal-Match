from flask_restful import Resource
from flask import request
from flask import session
from flask import jsonify
from Entities.recipe import Recipe
from Entities.relation_ing_type import RelIngType
from Entities.relation_rec_type import RelRecType
from Entities.ingredients import Ingredient
from Entities.rec_ing import RecIng
from Entities.rec_type import RecType
from Entities.user_pre import UserPre
from Utils.gen_card import card
from Utils.string_process import pre_process, get_num
import re


class SearchAPI(Resource):
    @staticmethod
    def _select_rec(query):
        return [rec.id for rec in query]

    @staticmethod
    def _filter_rec(rec_list, filters):
        if not filters:
            return rec_list
        valid_rec = []
        first = True
        for f in filters:
            if f <= 3 or f > 26:
                continue
            temp_set = set()
            for r in RelRecType.query.filter_by(t_id=f).all():
                if first:
                    valid_rec.append(r.r_id)
                else:
                    temp_set.add(r.r_id)
            if first:
                first = False
            else:
                valid_rec = list(set(valid_rec) & temp_set)
        if not valid_rec and first:
            return rec_list
        valid_rec = list(set(valid_rec))
        res = []
        for rec in rec_list:
            if rec in valid_rec:
                res.append(rec)
        return res

    @staticmethod
    def _sort_list(rec_list, filters, keywords):
        sort_method = [f for f in filters if f <= 3]
        preferences = [f for f in filters if f > 26]
        ingredients = eval(session.get('list')) if session.get('list') else []
        keywords = [k.lower() for k in keywords if k]
        keywords = list(set(keywords).difference(set([ing['name'] for ing in ingredients])))
        if ingredients:
            ingredients = [ing['id'] for ing in ingredients]
        for i, rec in enumerate(rec_list):
            score = 0
            filter_ing = RecIng.query.filter(RecIng.recipe == rec, RecIng.ingredient.in_(ingredients)).all()
            score += len(filter_ing)
            filter_pre = RelRecType.query.filter(RelRecType.r_id == rec, RelRecType.t_id.in_(preferences)).all()
            score += len(filter_pre)
            filter_key = [len(Recipe.query.filter(Recipe.id == rec, Recipe.title.contains(k)).all()) for k in keywords]
            score += sum(filter_key)
            rec_list[i] = (rec_list[i], score)
        if sort_method:
            f = sort_method.pop()
            if f == 1:
                for i, rec in enumerate(rec_list):
                    rec_list[i] = (rec_list[i], Recipe.query.filter_by(id=rec[0]).first().update_time)
                rec_list.sort(key=lambda x: (x[1], x[0][1]), reverse=True)
            elif f == 2:
                for i, rec in enumerate(rec_list):
                    rec_list[i] = (rec_list[i], Recipe.query.filter_by(id=rec[0]).first().like)
                rec_list.sort(key=lambda x: (x[1], x[0][1]), reverse=True)
            else:
                for i, rec in enumerate(rec_list):
                    rec_list[i] = (rec_list[i], Recipe.query.filter_by(id=rec[0]).first().cook_time)
                rec_list.sort(key=lambda x: (x[1], x[0][1]))
            rec_list = list(map(lambda x: x[0][0], rec_list))
        else:
            rec_list.sort(key=lambda x: x[1], reverse=True)
            rec_list = list(map(lambda x: x[0], rec_list))
        return jsonify([card(rec) for rec in rec_list])

    def get(self):
        search_result = []
        redundancy_dic = {}
        string = request.args.get('string').strip()
        string = re.sub(r'[,.!?\-]', ' ', string)
        running_list = session.get('list')
        running_list = eval(running_list) if running_list else []
        filters = session.get('filter')
        filters = [f['id'] for f in eval(filters)] if filters else []
        filter_args = request.args.get('filter')
        if filter_args is not None and filter_args != 'None':
            filters.extend([int(f) for f in filter_args.split(',') if f])
        if not string and not running_list:
            search_result = self._select_rec(Recipe.query.all())
            search_result = self._filter_rec(search_result, filters)
            return self._sort_list(search_result, filters, '')
        string = ' '.join(ing['name'] for ing in running_list) + ' ' + string if running_list else string
        string = string.split(' ')
        for s in string:
            if s:
                recipes = Recipe.query.filter(Recipe.title.contains(s.lower())).all()
                for recipe in recipes:
                    if not redundancy_dic.get(recipe.id) and s in recipe.title.lower().split(' '):
                        search_result.append(recipe.id)
                        redundancy_dic[recipe.id] = True
                ingredient = Ingredient.query.filter_by(name=s.lower()).first()
                if ingredient:
                    recipe_ids = RecIng.query.filter_by(ingredient=ingredient.id).all()
                    for r in recipe_ids:
                        recipes = self._select_rec(Recipe.query.filter_by(id=r.recipe).all())
                        for recipe in recipes:
                            if not redundancy_dic.get(recipe):
                                search_result.append(recipe)
                                redundancy_dic[recipe] = True
        search_result = self._filter_rec(search_result, filters)
        return self._sort_list(search_result, filters, string)


class SearchIngType(Resource):
    def get(self):
        running_list = [ing['id'] for ing in eval(session.get('list'))] if session.get('list') else []
        ingredients = RelIngType.query.filter_by(type=request.args.get('ing_type_id')).all()
        if ingredients:
            ing_ids = [ing.ingredient for ing in ingredients]
            ingredients = Ingredient.query.filter(Ingredient.id.in_(ing_ids)).all()
            return jsonify([{'id': ing.id, 'ingredient': ing.name, 'check': 'true' if ing.id in running_list else 'false'} for ing in ingredients])
        else:
            return {'res': False}, 400


class RunningList(Resource):
    # 读取running list
    def get(self):
        if not session.get('list'):
            session['list'] = str([])
        return jsonify(eval(session['list']))

    # 添加至 running list
    def post(self):
        if not session.get('list'):
            session['list'] = str([])
        ing_id = re.findall('[0-9]+', request.form.get('id'))
        if not ing_id:
            return jsonify(eval(session['list']))
        lis = eval(session['list'])
        ing_id = int(ing_id[0])
        if ing_id not in [ing['id'] for ing in lis]:
            ing = Ingredient.query.filter_by(id=ing_id).first()
            lis.append({'id': ing.id, 'name': ing.name, 'check': True})
            session['list'] = str(lis)
        return jsonify(eval(session['list']))

    # 从running list中删除
    def delete(self):
        if not session.get('list'):
            session['list'] = str([])
        ing_id = re.findall('[0-9]+', request.form.get('id'))
        if not ing_id:
            return jsonify(eval(session['list']))
        ing_id = int(ing_id[0])
        lis = eval(session['list'])
        if not len(lis):
            return jsonify(eval(session['list']))
        for i, ing in enumerate(lis):
            if ing['id'] == ing_id:
                lis.pop(i)
                break
        session['list'] = str(lis)
        return jsonify(eval(session['list']))


class ClearRunningList(Resource):
    def delete(self):
        lis = [ing['id'] for ing in eval(session['list'])]
        session['list'] = str([])
        return jsonify(lis)


class AddToList(Resource):
    def post(self):
        running_list = session.get('list')
        if not running_list:
            running_list = []
        else:
            running_list = eval(running_list)
        string = request.form.get('ing_string')
        if not string:
            return {'res': False}
        r_list = [ing['id'] for ing in running_list]
        ingredients = pre_process(string, 'search')
        for ing in ingredients:
            ing = Ingredient.query.filter_by(name=ing).first()
            if ing:
                if ing.id not in r_list:
                    running_list.append({'id': ing.id, 'name': ing.name, 'check': True})
        session['list'] = str(running_list)
        return jsonify(running_list)


class Filter(Resource):
    def get(self):
        filters = session.get('filter')
        filters = eval(filters) if filters else []
        res = []
        for rec_type in RecType.query.all():
            res.append({
                'id': rec_type.id,
                'name': rec_type.name,
                'checked': True if rec_type.id in filters else False
            })
        return jsonify(res)

    def post(self):
        filters = session.get('filter')
        filters = eval(filters) if filters else []
        f_id = get_num(request.form.get('id'))
        if not f_id:
            return jsonify(filters)
        f = RecType.query.filter_by(id=f_id).first()
        if f.id not in [r_type['id'] for r_type in filters]:
            filters.append({
                'id': f.id,
                'f_name': f.name
                # 'checked': True
            })
        session['filter'] = str(filters)
        return jsonify(filters)

    def delete(self):
        filters = session.get('filter')
        filters = eval(filters) if filters else []
        f_id = get_num(request.form.get('id'))
        if not f_id:
            return jsonify(filters)
        f = RecType.query.filter_by(id=f_id).first()
        if not len(filters):
            return jsonify(filters)
        for i, k in enumerate(filters):
            if k['id'] == f.id:
                filters.pop(i)
                break
        session['filter'] = str(filters)
        return jsonify(filters)


class ClearFilter(Resource):
    def delete(self):
        session['filter'] = str([])
        return jsonify({'res': True})
