from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy

# Data model for User
db = SQLAlchemy()
class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), nullable=True)

        def to_dict(self):
            return {"id": self.id, "name": self.name, "group_id": self.group_id}
        
# Data model for User Group
class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='group', lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name}
        
# Function to create a Flask application
def create_app(test_config=None):
    app = Flask(__name__)
    # Configuration for the SQLite database
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    else:
        app.config.update(test_config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

 
    

    # Initialize the database
    with app.app_context():
        db.create_all()

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # POST create user
    @app.route("/user", methods=['POST'])
    def create_user():
        data = request.get_json()
        name = data.get('name')
        group_id = data.get('group_id')

        if not name:
            return jsonify({'error': 'Name is required'}), 400

        if group_id is not None:  # check group exist or not.
            group = UserGroup.query.get(group_id)
            if group is None:
                return jsonify({'error': 'Group with provided ID does not exist'}), 400

        new_user = User(name=name, group_id=group_id)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    # DELETE delete user
    @app.route("/user/<int:user_id>", methods=['DELETE'])
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200

    # GET read specific user
    @app.route("/user/<int:user_id>", methods=['GET'])
    def get_user(user_id):
        user = db.session.get(User, user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200

    # GET user list with optional filtering by partial name match
    @app.route("/users", methods=['GET'])
    def get_users():
        
    # Check if 'name' query parameter is present
        name_filter = request.args.get('name')

    # If name filter is provided, filter users by partial name match
        if name_filter:
            users = User.query.filter(User.name.like(f'%{name_filter}%')).all()
        else:
            users = User.query.all()
    
        return jsonify([user.to_dict() for user in users]), 200

    # POST create user group
    @app.route("/group", methods=['POST'])
    def create_group():
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({'error': 'Name is required'}), 400

        new_group = UserGroup(name=name)
        db.session.add(new_group)
        db.session.commit()
        return jsonify(new_group.to_dict()), 201
    
    # DELETE delete user group
    @app.route("/group/<int:group_id>", methods=['DELETE'])
    def delete_group(group_id):
        group = db.session.get(UserGroup, group_id)
        if not group:
            return jsonify({'error': 'Group not found'}), 404

        # Check if the group has any users
        if group.users:
            return jsonify({'error': 'Group cannot be deleted as it has users associated with it'}), 400

        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': 'Group deleted'}), 200
    
    # GET read single user group
    @app.route("/group/<int:group_id>", methods=['GET'])
    def get_group(group_id):
        group = db.session.get(UserGroup, group_id)
        if not group:
            return jsonify({'error': 'Group not found'}), 404
        
        return jsonify(group.to_dict()), 200
    
    # GET read all user groups
    @app.route("/groups", methods=['GET'])
    def get_groups():
        groups = UserGroup.query.all()
        return jsonify([group.to_dict() for group in groups]), 200
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
