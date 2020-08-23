from flask import request
from flask import jsonify
from flask import session
from flask_restful import Resource
from DAO.DataBase.database import db
from Entities.ingredients import Ingredient
from Entities.relation_ing_type import RelIngType
from Entities.ing_type import IngType
from Entities.rec_ing import RecIng
from Entities.search_s import SearchS
from gensim.models import Word2Vec
from Utils.string_process import pre_process
from Config.config import BASE_DIR
import os


# recommend ingredient type
class RecIngType(Resource):
    def get(self):
        # string preprocess
        ingredient = pre_process(request.args.get('ingredient'), 'ingredient')
        # not an ingredient return 400
        if len(ingredient) <= 2 or not ingredient.replace(' ', '').isalpha():
            return {'msg': 'Maybe not an ingredient?'}, 400
        # try to find ingredient in db, if db does not have this ingredient return type=''
        ing = Ingredient.query.filter_by(name=ingredient).first()
        if ing:
            # select (type_id, ingredient_id, count(type))
            res = db.session.query(RelIngType.type, RelIngType.ingredient, db.func.count(RelIngType.type)).\
                filter_by(ingredient=ing.id).group_by('type').order_by(db.func.count(RelIngType.type).desc()).first()
            if res:
                ing_type_id = res[0]
                # find type name and return
                ing = IngType.query.filter_by(id=ing_type_id).first()
                return jsonify({'type': ing.name})
        else:
            return jsonify({'type': ''})


# recommend ingredient to running list
class RecIngToList(Resource):
    model = Word2Vec.load(os.path.join(BASE_DIR, 'DAO/data/w2v_model.model'))

    def get(self):
        result = []
        rec_list = []
        # search string pre process
        strings = pre_process(request.args.get('string'), 'search')
        # read running list
        running_list = session.get('list')
        running_list = eval(session.get('list')) if running_list else []
        running_list = [ing['id'] for ing in running_list]
        rec_list.extend(running_list)
        # for each searched ingredient
        for ing in strings:
            ing = Ingredient.query.filter_by(name=ing).first()
            # if searched ingredient in db, recommend user add it to running list
            if ing:
                if ing.id not in rec_list:
                    result.append({
                        'id': ing.id,
                        'ingredient': ing.name
                    })
                    rec_list.append(ing.id)
        # recommend next ingredients
        for ex_ing in rec_list[::-1]:
            # maximum of 6 recommend ingredients
            if len(result) < 6:
                temp_list = []
                # query all recipe including that ingredient
                recipes = RecIng.query.filter_by(ingredient=ex_ing).all()
                for recipe in recipes:
                    #
                    next_ing_list = RecIng.query.filter_by(recipe=recipe.recipe).all()
                    for next_ing in next_ing_list:
                        ing = Ingredient.query.filter_by(id=next_ing.ingredient).first()
                        if ing.id not in rec_list:
                            temp_list.append(ing)
                            rec_list.append(ing.id)
                for i, ing in enumerate(temp_list):
                    try:
                        temp_list[i] = (ing, self.model.wv.similarity(ing.name, Ingredient.query.filter_by(id=ex_ing).first().name))
                    except KeyError:
                        temp_list[i] = (ing, 0)
                temp_list.sort(key=lambda x: x[1], reverse=True)
                temp_list = list(map(lambda x: {'id': x[0].id, 'ingredient': x[0].name}, temp_list))
                result.extend(temp_list[:6 - (len(result))])
            else:
                return jsonify(result)
        return jsonify(result)


class RecIngSet(Resource):
    with open(os.path.join(BASE_DIR, 'DAO/data/ingredients_data.txt'), 'r') as f:
        ing_data = f.read().split('\n')

    def valid(self, string):
        if not string.strip():
            return False
        strings = string.strip().split(',')
        # 判断每个字串都为ingredient
        for s in strings:
            if s.strip().lower() not in self.ing_data:
                return False
        # 有一个不是则返回False
        return True

    @staticmethod
    def has_recipe(string):
        strings = string.strip().split(',')
        recipe_list = []
        for i, s in enumerate(strings):
            ing = Ingredient.query.filter_by(name=s.strip().lower()).first()
            if ing:
                rec_ing = RecIng.query.filter_by(ingredient=ing.id).all()
                if i == 0:
                    recipe_list.extend([r.recipe for r in rec_ing])
                elif rec_ing:
                    recipe_list = list(set(recipe_list) & set([r.recipe for r in rec_ing]))
                else:
                    return False
            else:
                return False
        return bool(recipe_list)

    # 获取ing推荐
    def get(self):
        k = 3
        res = []
        # 数据库读取search字符串 has_recipe== False order_by frequency 倒序
        search_s_list = SearchS.query.filter_by(has_recipe=False).order_by(SearchS.frequency.desc()).all()
        # 每一个search string 查 是否有recipe
        for s in search_s_list:
            # 是则变更has_recipe 为True
            if self.has_recipe(s.string):
                s.has_recipe = True
                db.session.commit()
            else:
                res.append(s.string.replace(',', ', '))
        # 否则res.append(s.string)
        return jsonify(res[:k])

    # 搜索时上传字符串
    def post(self):
        # 接受search字符串
        string = request.form.get('string')
        # 判断搜索字符串有效 无效直接返回
        if not self.valid(string):
            return {'res': False}
        string = ','.join([s.strip().lower() for s in string.split(',')])
        # 搜索字符串存在db fre+1 否则创建
        search_s = SearchS.query.filter_by(string=string).first()
        if not search_s:
            search_s = SearchS(string=string)
            db.session.add(search_s)
        else:
            search_s.frequency += 1
        db.session.commit()
        return {'res': True}
