import datetime

from flask import (Blueprint,
                    render_template,
                    jsonify,
                    session,
                    request,
                    redirect,
                    Response,
                    url_for,
                    flash,
                    g
                    )

from flask.ext.login import (LoginManager, 
                                login_user,
                                logout_user,
                                login_required)

from webapp.models import User


login_manager = LoginManager()
login_manager.login_view = 'login'

user_blueprint = Blueprint(
    'user',
    __name__,
    static_folder='../static',
    template_folder='../templates/user',
    url_prefix='/user'
)

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None

@user_blueprint.record_once                                             
def on_load(state):                                                
  login_manager.init_app(state.app)  


@user_blueprint.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.index'))

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username)
        if user.count() == 0:
            user = User(username=username, password=password)
            user.save()
            
            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('user.login'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('user.register'))
    else:
        abort(405)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 1:
            login_user(user.one())
            flash('Welcome back {0}'.format(username))
            try:
                next = request.form['next']
                return redirect(next)
            except:
                return redirect(url_for('user.index'))
        else:
            flash('Invalid login')
            return redirect(url_for('user.login'))
    else:
        return abort(405)

@user_blueprint.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',
                            users=users)

@user_blueprint.route('/add_friend/', methods=['POST'])
def add_friend():
    user = g.user

    if not user.is_anonymous and request.method == 'POST':
        username = request.form.get('friendname')
        result = user.add_friend(username)
        if result:
            return '{"result":"ok"}'
        else:
            return '{"result":"failed", "message":"You already have that friend."}'
    return '{"result":"failed"}'
