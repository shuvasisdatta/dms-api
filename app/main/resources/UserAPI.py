from app.main import db, sha256_crypt, request, jsonify, Resource
from app.main.model import User


class UsersResource(Resource):
    # @token_required
    def get(self, current_user):
        users = User.query.all()
        res = []

        for user in users:
            user_data = {
                'public_id': user.public_id,
                'username': user.username,
                'password': user.password,
                'admin': user.admin
            }
            res.append(user_data)

        return jsonify({'users': res})

    # @token_required
    def post(self):
        data = request.get_json()
        user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            password=sha256_crypt.hash(data['password']),
            admin=data['admin']
        )

        res = {
            'public_id': user.public_id,
            'username': user.username,
            'password': user.password,
            'admin': user.admin
        }

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'New user created', 'user': res})


class UserResource(Resource):
    # @token_required
    def get(self, current_user, public_id):
        user = User.query.filter_by(public_id=public_id).first_or_404(
            description='User not found')

        res = {
            'public_id': user.public_id,
            'username': user.username,
            'password': user.password,
            'admin': user.admin
        }

        return jsonify({'user': res})

    # @token_required
    def put(self, public_id):
        user = User.query.filter_by(public_id=public_id).first_or_404(
            description='User not found')

        data = request.get_json()

        if 'username' in data:
            user.username = data['username']

        if 'password' in data:
            user.password = sha256_crypt.hash(data['password'])

        if 'admin' in data:
            user.admin = data['admin']

        db.session.commit()

        res = {
            'public_id': user.public_id,
            'username': user.username,
            'password': user.password,
            'admin': user.admin
        }

        return jsonify({'message': 'User has been updated', 'user': res})

    # @token_required
    def delete(self, public_id):
        user = User.query.filter_by(public_id=public_id).first_or_404(
            description='User not found')

        db.session.delete(user)
        db.session.commit()

        return '', 204
