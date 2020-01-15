from app.main import db, sha256_crypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def password_hash(self, password):
        return sha256_crypt.hash(password)

    def verify_hash(self, password):
        return sha256_crypt.verify(password, self.password)
