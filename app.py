from flask import render_template, redirect, url_for, session, request, flash, jsonify
from config import app
from functools import wraps

from models import Player, Team
from models import db


def get_admin_from_session():
    return session.get('login_admin', '')


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not get_admin_from_session():
            return redirect(url_for('.login'))
        return func(*args, **kwargs)

    return decorated_view


@app.context_processor
def inject_dict_in_all_templates():
    return dict(admin=get_admin_from_session())


@app.route("/login", methods=["GET", "POST"])
def login():
    form = {}
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        form = request.form
        if not (username and password):
            flash("Username or Password cannot be empty.", "error")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        if username == 'admin' and password == 'pass1234':
            session['login_admin'] = str(username)
            return redirect(url_for(".index"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html", form=form, no_navbar=True)


@app.route("/logout")
def logout():
    if session.get('login_admin'):
        del session['login_admin']
    return redirect(url_for('.index'))


@app.route('/')
def index():
    return render_template('teams.html')
    #return redirect(url_for('.teams'))


@app.route('/add-team', methods=["GET", "POST"])
@admin_required
def add_team():
    form = request.form
    if request.method == "POST":
        team = Team(name=form.get('name'), logo_uri=form.get('logo_uri'))
        try:
            db.session.add(team)
            db.session.commit()
            flash("Added team {}".format(form.get('name')), "success")
        except Exception as e:
            db.session.rollback()
            flash("Could not add team {}".format(form.get('name')), "error")
        return redirect(url_for('.index'))
    return render_template('add_team.html', form=form)


@app.route('/edit-team/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_team(id):
    team = Team.query.filter_by(id=id).first_or_404()
    if request.method == "POST":
        team.name = request.form.get('name')
        team.logo_uri = request.form.get('logo_uri')
        try:
            db.session.commit()
            flash("Successfully edited {}".format(request.form.get('name')), "success")
        except Exception as e:
            db.session.rollback()
            flash("Could not edit team {}".format(request.form.get('name')), "error")
        return redirect(url_for('.index'))
    return render_template('add_team.html', form=team)


@app.route('/delete-team/<int:id>', methods=['GET'])
@admin_required
def delete_team(id):
    Team.query.filter_by(id=id).delete()
    try:
        db.session.commit()
        flash("Successfully deleted ", "success")
    except Exception as e:
        db.session.rollback()
        flash("Could not delete ", "error")
    return redirect(url_for('.index'))


@app.route('/add-player', methods=["GET", "POST"])
@admin_required
def add_player():
    form = request.form
    if request.method == "POST":

        player = Player(firstname=request.form.get('firstname'),
                        lastname=request.form.get('lastname'),
                        image_uri=request.form.get('image_uri'),
                        team_id=request.form.get('team_id'))
        try:
            db.session.add(player)
            db.session.commit()
            flash("Added player {}".format(form.get('firstname')), "success")
        except Exception as e:
            db.session.rollback()
            flash("Could not add player {}".format(form.get('firstname')), "error")
        return redirect(url_for('.index'))
    return render_template('add_player.html', form=form, teams=Team.query.all())


@app.route('/edit-player/<int:id>', methods=["GET", "POST"])
@admin_required
def edit_player(id):
    player = Player.query.filter_by(id=id).first_or_404()
    if request.method == "POST":
        print(request.form)
        player.firstname = request.form.get('firstname')
        player.lastname = request.form.get('lastname')
        player.image_uri = request.form.get('image_uri')
        player.team_id = request.form.get('team_id')
        try:
            db.session.commit()
            flash("Successfully edited {}".format(request.form.get('firstname')), "success")
        except Exception as e:
            db.session.rollback()
            flash("Could not edit player {}".format(request.form.get('firstname')), "error")
        return redirect(url_for('.players', team_id=id))
    return render_template('add_player.html', form=player, teams=Team.query.all())


@app.route('/delete-player/<int:id>', methods=['GET'])
@admin_required
def delete_player(id):
    Player.query.filter_by(id=id).delete()
    try:
        db.session.commit()
        flash("Successfully deleted ", "success")
    except Exception as e:
        db.session.rollback()
        flash("Could not delete ", "error")
    return redirect(url_for('.index'))


@app.route('/teams')
def teams():
    return render_template('teams.html')


@app.route('/team/<int:team_id>/players')
def players(team_id):
    return render_template('players.html', team_id=team_id)


@app.route('/api/team/<int:team_id>/players/')
def api_players(team_id):
    return jsonify([player.as_dict() for player in Player.query.filter_by(team_id=team_id).all()]), 200


@app.route('/api/teams/', methods=["GET"])
def api_teams():
    return jsonify([team.as_dict() for team in Team.query.all()]), 200


if __name__ == "__main__":
    app.run(port=5008, host='0.0.0.0')