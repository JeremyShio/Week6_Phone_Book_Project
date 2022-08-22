import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'l1l1l1ll11l1ll1l1lll111lll1l111lll'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class AuthorSignature:
    # Author info for author signature
    author_info = {
        'authorname': 'Jeremy Shiotani',
        # Hidden alias (ಠ.ಠ)
        'alias': 'Programming Apprentice'}
