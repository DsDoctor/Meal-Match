from flask import request
from flask import jsonify
from flask import session
from flask_restful import Resource
from Entities.comment import Comment
from Entities.user import User
from Utils.get_time import time_now
from Utils.string_process import pre_process
from DAO.DataBase.database import db


class CommentsApi(Resource):
    def get(self):
        res = []
        # get all comments with that recipe
        comments = Comment.query.filter_by(recipe=request.args.get('r_id')).all()
        for c in comments:
            # loading user info from that comment
            user = User.query.filter_by(id=c.user).first()
            res.append({'id': user.id,
                        'c_id': c.id,
                        'content': c.content,
                        'username': user.username,
                        'lv': user.exp//100 + 1,
                        'update_time': c.update_time})
        return jsonify(res)

    def post(self):
        # get user id
        user = session.get('id')
        # if not login
        if not user:
            return {'res': False}, 400
        # preprocess string
        string = pre_process(request.form.get('comment'), 'comment')
        comment = Comment(content=string, user=user, recipe=request.form.get('r_id'),
                          update_time=time_now())
        user = User.query.filter_by(id=user).first()
        if user.max_exp <= 30:
            user.exp += 1
            user.max_exp += 1
        db.session.add(comment)
        db.session.commit()
        return jsonify({'res': True})

    def delete(self):
        # get comment id
        c_id = request.form.get('c_id')
        # query comment
        comment = Comment.query.filter_by(id=c_id).first()
        if not comment:
            return {'res': False}, 400
        # delete from database
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'res': True})
