from flask import request
from flask import session
from flask import jsonify
from flask_restful import Resource
from DAO.DataBase.database import db
from Entities.user import User
from Entities.recipe import Recipe
from Entities.ingredients import Ingredient
from Entities.ing_type import IngType
from Entities.rec_type import RecType
from Entities.rec_ing import RecIng
from Entities.comment import Comment
from Entities.favorite import Favorite
from Entities.relation_rec_type import RelRecType
from Entities.relation_ing_type import RelIngType
from Utils.get_time import time_now
from Utils.string_process import pre_process
from Config.config import BASE_DIR
import os
import re


class PublishAPI(Resource):
	allow_file_type = ['bmp', 'jpg', 'png', 'jpg', 'jpeg', 'pdf', 'gif']

	def connect_rec_ing(self, recipe, ing_list):
		for ingredient in ing_list:
			# search ingredient
			ing_name = ingredient['name'].strip().lower()
			ing = Ingredient.query.filter_by(name=ing_name).first()
			# ingredient does not exist, create a new ingredient
			if not ing:
				ing = Ingredient(name=ing_name)
				db.session.add(ing)
			# search this ingredient type
			ing_type_id = IngType.query.filter_by(name=ingredient['cat'].lower()).first().id
			rel_ing_type = RelIngType.query.filter_by(ingredient=ing.id, type=ing_type_id).first()
			# if upload ingredient type for this ingredient does not exist, create a new relation
			if not rel_ing_type:
				rel_ing_type = RelIngType(ingredient=ing.id, type=ing_type_id)
				db.session.add(rel_ing_type)
			# create recipe and ingredient relation
			rec_ing = RecIng(recipe=recipe.id, ingredient=ing.id)
			db.session.add(rec_ing)

	# get published recipe detail
	def get(self):
		u_id = session.get('id')
		r_id = request.args.get('r_id')
		recipe = Recipe.query.filter_by(id=r_id).first()
		# check accuracy and authority
		if not recipe or not u_id or recipe.author != int(u_id):
			return {'res': False}, 400
		# query all ingredients for that recipe
		ing_list = [None]
		for ing_id in [rec.ingredient for rec in RecIng.query.filter_by(recipe=r_id).all()]:
			cat_id = db.session.query(RelIngType.type, RelIngType.ingredient, db.func.count(RelIngType.type)).\
			filter_by(ingredient=ing_id).group_by('type').order_by(db.func.count(RelIngType.type).desc()).first()[0]
			ing_list.append({
				'ingredient': Ingredient.query.filter_by(id=ing_id).first().name,
				'cat': IngType.query.filter_by(id=cat_id).first().name.title()}
			)
		# create return date
		data = {
			'title': recipe.title,
			'describe': recipe.describe,
			'hour': recipe.cook_time//60,
			'minus': recipe.cook_time % 60,
			'img': recipe.img_link if recipe.img_type == 'link' else '/'+recipe.img_link,
			'ingredients': ing_list,
			'steps': [s.split(':', 1)[1] for s in recipe.steps.split('\n')]
		}
		return jsonify(data)

	# post a new recipe
	def post(self):
		# check user authority
		u_id = session.get('id')
		if not u_id:
			return {'res': False}, 400
		# receive uploaded info
		title = pre_process(request.form.get('title'), 'title')
		ingredients = eval(request.form.get('ingredients'))
		categories = eval(request.form.get('select_cat'))
		cook_hour = int(request.form.get('hour'))
		cook_minus = int(request.form.get('minus'))
		describe = request.form.get('describe')
		describe = pre_process(describe)
		steps = eval(request.form.get('steps'))
		img_type = request.form.get('img').rsplit('.')[1]
		# check file type
		if img_type not in self.allow_file_type:
			return {'res': False}, 400
		steps = '\n'.join([f'{i+1}: {step.strip()}' for i, step in enumerate(steps)])
		img_path = f'Static/img/RecipeImg/temp{int(u_id)}.{img_type}'

		# create recipe
		recipe = Recipe(title=title, steps=steps, update_time=time_now(),
						author=session.get('id'), cook_time=cook_hour*60 + cook_minus,
						describe=describe, img_type=img_type)
		db.session.add(recipe)
		categories = [int(re.findall('[0-9]+', c)[0]) for c in categories]
		# connect recipe and its recipe category
		user = User.query.filter_by(id=u_id).first()
		for c in categories:
			rel = RelRecType(r_id=recipe.id, t_id=RecType.query.filter_by(id=c).first().id)
			db.session.add(rel)
		# connect ingredients to recipe
		self.connect_rec_ing(recipe, ingredients)
		db.session.commit()
		# add the img link for this recipe
		new_path = f'Static/img/RecipeImg/recipe_{recipe.id}.{img_type}'
		os.rename(os.path.join(BASE_DIR, img_path), os.path.join(BASE_DIR, new_path))
		recipe.img_link = new_path

		user.exp += 10
		db.session.commit()
		return jsonify({'res': True})

	# update a published recipe
	def put(self):
		u_id = session.get('id')
		r_id = request.form.get('r_id')
		# query recipe
		recipe = Recipe.query.filter_by(id=r_id).first()
		# check correctness and  user authority
		if not u_id or not recipe or recipe.author != int(u_id):
			return {'res': False}, 400
		# update title of recipe
		recipe.title = pre_process(request.form.get('title'), 'title')
		# update ingredients of recipe
		RecIng.query.filter_by(recipe=recipe.id).delete()
		ingredients = eval(request.form.get('ingredients'))
		self.connect_rec_ing(recipe, ingredients)
		# update recipe type
		RelRecType.query.filter_by(r_id=recipe.id).delete()
		categories = eval(request.form.get('select_cat'))
		categories = [int(re.findall('[0-9]+', c)[0]) for c in categories]
		for c in categories:
			rel = RelRecType(r_id=recipe.id, t_id=RecType.query.filter_by(id=c).first().id)
			db.session.add(rel)
		# update cook time
		cook_hour = int(request.form.get('hour'))
		cook_minus = int(request.form.get('minus'))
		recipe.cook_time = cook_hour*60 + cook_minus
		# update update time
		recipe.update_time = time_now()
		# update steps
		steps = eval(request.form.get('steps'))
		steps = '\n'.join([f'{i + 1}: {step.strip()}' for i, step in enumerate(steps)])
		recipe.steps = steps
		# update describe
		describe = request.form.get('describe')
		describe = pre_process(describe)
		recipe.describe = describe
		# update img
		img = request.form.get('img')
		if img:
			img_type = img.rsplit('.')[1]
			if img_type not in self.allow_file_type:
				return {'res': False}, 400
			img_path = f'Static/img/RecipeImg/temp{int(u_id)}.{img_type}'
			new_path = f'Static/img/RecipeImg/recipe_{recipe.id}.{img_type}'
			os.rename(os.path.join(BASE_DIR, img_path), os.path.join(BASE_DIR, new_path))
			recipe.img_link = new_path
			recipe.img_type = img_type
		user = User.query.filter_by(id=u_id).first()
		if user.max_exp <= 30:
			user.exp += 1
			user.max_exp += 1
		db.session.commit()
		return {'res': True}

	# delete a published recipe
	def delete(self):
		# check correctness and authority
		u_id = session.get('id')
		r_id = request.form.get('id')
		recipe = Recipe.query.filter_by(id=r_id).first()
		if not u_id or not r_id or recipe.author != int(u_id):
			return {'res': False}, 400
		# del comments of recipe
		Comment.query.filter_by(recipe=recipe.id).delete()
		# del favorite of recipe
		Favorite.query.filter_by(recipe=recipe.id).delete()
		# del ingredients that correspond to this recipe
		RecIng.query.filter_by(recipe=recipe.id).delete()
		# del img if img save on local
		img_path = f'Static/img/RecipeImg/recipe_{recipe.id}.{recipe.img_type}'
		os.remove(os.path.join(BASE_DIR, img_path))
		# del recipe type that correspond to this recipe
		RelRecType.query.filter_by(r_id=recipe.id).delete()
		# del this recipe
		db.session.delete(recipe)
		db.session.commit()
		return {'res': True}


class PublishFile(Resource):
	allow_file_type = ['bmp', 'jpg', 'png', 'jpg', 'jpeg', 'pdf', 'gif']

	# upload img file save to temp file
	def post(self):
		# check user authority
		u_id = session.get('id')
		img = request.files.get('images')
		if not img or not u_id:
			return {'res': False}, 400
		# check img type
		file_type = img.filename.rsplit('.', 1)[-1]
		if file_type not in self.allow_file_type:
			return {'res': False}, 400
		# if valid img type, save it as a temp file
		path = f'Static/img/RecipeImg/temp{int(u_id)}.{file_type}'
		img.save(os.path.join(BASE_DIR, path))
		return {'url': path}

