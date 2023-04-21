from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, abort, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SubmitField, PasswordField
from wtforms.validators import Email, DataRequired
from . import db
import sqlite3
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
ad = Blueprint('ad', __name__)

class AdminForm(FlaskForm):
    def account_check(self, field):
        if field.data != 'mayData0426@gmail.com':
            raise ValidationError('Wrong Administrator')

    def password_check(self, field):
        if field.data != 'mayISOM4007':
            raise ValidationError('Wrong Administrator')

    email = StringField("Admin Email", validators=[DataRequired(message=''),
                                                   Email(message=u'Not an Email'), account_check])
    password = PasswordField("Admin Password", validators=[DataRequired(message=''), password_check])
    login = SubmitField("Login")

class AdminAddForm(FlaskForm):
    def email_unique(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Existing Email")

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), email_unique])
    password = StringField('Password', validators=[DataRequired()])
    add = SubmitField('Add User')


@ad.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        session['admin'] = True
        return redirect(url_for('ad.control'))
    return render_template('form.html', form=form)

@ad.route('/control', methods=['GET', 'POST'])
def control():
    if not session.get('admin'):
        abort(400)
    users = User.query.all()
    return render_template('control.html', users=users)

@ad.route('/add', methods=['GET', 'POST'])
def admin_add():
    if not session.get('admin'):
        abort(400)
    form = AdminAddForm()
    if form.validate_on_submit():
        # n = []
        # for i in range(10):
        #     n.append(str(random.randint(0, 9)))
        # active_code = ''.join(n)
        user = User(username=request.form.get('username'), email=request.form.get('email'),
                    password= generate_password_hash(request.form.get('password'), method='sha256'))
        db.session.add(user)
        db.session.commit()
        flash('Add user successfully')
        return redirect(url_for('ad.admin_add'))
    return render_template('adminadd.html', form=form)

@ad.route('/delete', methods=['GET', 'POST'])
def admin_delete():
    if session.get('admin'):
        user = User.query.filter_by(id=request.form.get('id')).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        return 'ok'
    abort(400)

@ad.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code='404'), 404

@ad.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code='500'), 500

@ad.errorhandler(400)
def bad_request(e):
    return render_template('error.html', code = '400'), 400

@ad.route('/db_mangement')
def db_management():
    con = sqlite3.connect("project/data/data.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Sheet1")
    data = cur.fetchall()
    return render_template("db_management.html", datas=data)

@ad.route('/add_db', methods=["POST", "GET"])
def add_db():
    con = sqlite3.connect('project/data/data.db')

    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # cur.execute("select * from Sheet1 where id=?",(id,))
    # data = cur.fetchall()

    if request.form == 'POST':
        ID = request.form['id']
        Streamer_Name = request.form['liveStreamer_name']
        sex = request.form['sex']
        product_interest = request.form['product_interest']
        fans_number = request.form['fans_number']
        totalSales_revenue = request.form['totalSales_revenue']
        # con = sqlite3.connect('project/data/data.db')
        # cur = con.cursor()
        cur.execute("""
                    INSERT INTO Sheet1
                    id = ?,
                    liveStreamer_name = ?,
                    sex = ?, 
                    product_interest = ?,
                    fans_number = ?,
                    totalSales_revenue = ?""",
                    (ID, Streamer_Name, sex, product_interest, fans_number, totalSales_revenue))
        con.commit()
        flash('User Added successfully')
        con.close()
        return redirect(url_for('ad.control'))
    return render_template("add_db.html")

@ad.route('/edit_db/<string:id>', methods=['POST', 'GET'])
def edit_db(id):
    conn = sqlite3.connect('project/data/data.db')
    cursor = conn.cursor()

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from Sheet1 where id=?",(id,))
    data = cursor.fetchall()


    if request.method == 'POST':
        print("Inside POST method")

        liveStreamer_name = request.form['liveStreamer_name']
        print(f"liveStreamer_name: {liveStreamer_name}")

        # liveStreamer_name	sex	product_interest	fans_number	member_number	total_live_number	live_number_within30
        # totalSales_revenue	totalSales_volume	average_living_time(s)	live_number_within30	averageViewer_number
        # totalProductConversion_rate	average_sales_volume	average_sales_revenue	average_uv_value	total_product_number
        # total_fans_change	total_video_number	average_videoLike_number	average_videoViewe_number	average_videoComment_number
        # average_videoShare_number
        # average_videoCollect_number	average_femaleFans_rate	average_maleFans_rate
        sex = request.form['sex']
        product_interest = request.form['product_interest']
        fans_number = request.form['fans_number']
        member_number = request.form['member_number']
        total_live_number = request.form['total_live_number']
        totalSales_revenue = request.form['totalSales_revenue']
        totalSales_volume = request.form['totalSales_volume']
        average_uv_value = request.form['average_uv_value']
        live_number_within30 = request.form['live_number_within30']
        averageViewer_number = request.form['averageViewer_number']
        totalProductConversion_rate = request.form['totalProductConversion_rate']
        # average_sales_volume = request.form['average_sales_volume']
        # average_sales_revenue = request.form['average_sales_revenue']
        # average_uv_value = request.form['average_uv_value']
        # total_product_number = request.form['total_product_number']
        # total_fans_change = request.form['total_fans_change']
        # total_video_number = request.form['total_video_number']
        # average_videoLike_number = request.form['average_videoLike_number']
        # average_videoViewe_number = request.form['average_videoViewe_number']
        # average_videoComment_number = request.form['average_videoComment_number']
        # average_videoShare_number = request.form['average_videoShare_number']
        # average_videoCollect_number = request.form['average_videoCollect_number']
        # average_femaleFans_rate = request.form['average_femaleFans_rate']
        # average_maleFans_rate = request.form['average_maleFans_rate']

        cursor.execute("""
            UPDATE sheet1
            SET liveStreamer_name = ?,
                sex = ?,
                product_interest = ?,
                fans_number = ?,
                member_number = ?,
                total_live_number = ?,
                totalSales_revenue = ?,
                totalSales_volume = ?,
                average_uv_value = ?,
                live_number_within30 = ?,
                averageViewer_number = ?,
                totalProductConversion_rate = ?
            WHERE id = ?""",
                       (liveStreamer_name,
                        sex,
                        product_interest,
                        fans_number,
                        member_number,
                        total_live_number,
                        totalSales_revenue,
                        totalSales_volume,
                        average_uv_value,
                        live_number_within30,
                        averageViewer_number,
                        totalProductConversion_rate,
                        id))
                    #	average_sales_volume = ?, average_sales_revenue = ?, average_uv_value = ?, "
                    #"total_product_number = ?, total_fans_change = ?, total_video_number = ?, average_videoLike_number = ?, average_videoViewe_number = ?,"
                    #"average_videoComment_number = ?, average_videoShare_number = ?, average_videoCollect_number = ?, average_femaleFans_rate = ?, average_maleFans_rate = ?"
                    #"where id = ?" # average_sales_volume, average_sales_revenue, average_uv_value, total_product_number,
                                                    #total_fans_change, total_video_number, average_videoLike_number, average_videoViewe_number, average_videoComment_number,
                                                    #average_videoShare_number, average_videoCollect_number, average_femaleFans_rate, average_maleFans_rate, id))
        conn.commit()
        flash('Database Edited')
        conn.close()
        return redirect(url_for('ad.control'))



    return render_template("edit_db.html", Sheet1 = data)

@ad.route('/delete_db/<string:id>', methods=['GET', 'POST'])
def delete_db(id):
    con = sqlite3.connect("project/data/data.db")
    cur = con.cursor()
    cur.execute("delete from Sheet1 where id=?",(id,))
    con.commit()
    flash("Record deleted")
    return redirect(url_for('ad.control'))