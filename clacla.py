#encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Video,Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'videos': Video.query.order_by('create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/detail/<video_id>/')
def detail(video_id):
    video_model = Video.query.filter(Video.id == video_id).first()
    return render_template('detail.html',video=video_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    video_id = request.form.get('video_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    video = Video.query.filter(Video.id == video_id).first()
    answer.video = video
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',video_id =video_id ))



@app.route('/ashore/',methods=['GET','POST'])
def ashore():
    if request.method == 'GET':
        return render_template('ashore.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        print(user)
        if user:
            session['user_id'] = user.id
            session.permant = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码错误'


@app.route('/update/',methods=['GET','POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        telephone = request.form.get('telephone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone,User.password == password1).first()
        if user:
            session['user_id'] = user.id
            user.password = password2
            #User.password == password2
            ###############################################################################################
            from sqlalchemy import create_engine
            # 创建的数据库引擎
            engine = create_engine("mysql+mysqldb://root:@127.0.0.1:3306/clacla_demo?charset=utf8")
            #from my_create_table import User, engine
            from sqlalchemy.orm import sessionmaker
            Session = sessionmaker(engine)
            db_session = Session()
            res = db_session.query(User).filter(User.telephone == telephone).update({"password": password2})
            db_session.commit()
            db_session.close()

            print(res)  # 1 res就是我们当前这句更新语句所更新的行数
            return redirect(url_for('ashore'))
        else:
            return u'手机号码或密码错误'



@app.route('/install/',methods=['GET','POST'])
def install():
    if request.method == 'GET':
        return render_template('install.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #手机号码验证，不可重复
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码！'
        else:
            #password1要和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核对再填写！'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                #file = request.files.get('file')
                # user_id = session.get('user_id')
                # user = User.query.filter(User.id == user_id).first()
                # filename = user_id
                # file.save('static/image/%s.jpg' % user.username)
                db.session.add(user)
                db.session.commit()
                #如果注册成功，就让页面跳转
                return redirect(url_for('ashore'))

@app.route('/release/',methods=['GET','POST'])
@login_required
def release():
    if request.method == 'GET':
        return render_template('release.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        video = Video(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        video.author = user
        db.session.add(video)
        db.session.commit()
        file = request.files.get('file')
        filename = user_id
        file.save('static/vedio/%s.mp4' %video.author.username)
        return redirect(url_for('index'))

# @app.route('/useinner/',methods=['GET','POST'])
# @login_required
# def useinner():
#     return render_template('useinner.html')

@app.route('/useinner/',methods=['GET','POST'])
@login_required
def useinner():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        file = request.files.get('file')
        filename = user_id
        file.save('static/image/%s.jpg' % user_id)
        return redirect(url_for('index'))


@app.route('/search/')
def search():
    q= request.args.get('q')
    #or
    videos = Video.query.filter(or_(Video.title.contains(q),Video.content.contains(q))).order_by('create_time')
    return render_template('index.html',videos=videos)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('ashore'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )
