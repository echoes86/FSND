# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

import datetime

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
show_to_venues = db.Table('show_to_venues', db.metadata,
                          db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id')),
                          db.Column('show_id', db.Integer, db.ForeignKey('Show.id'))
                          )


class Venue(db.Model):
    __tablename__ = 'Venue'

    default_image = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid" \
                      "=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80 "

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), default=default_image)
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), default='No seeking for new talents now')

    shows = db.relationship('Show', backref="venue")

    def __repr__(self):
        return '<Venue id:{}, city:{}, state:{}>'.format(self.id, self.city, self.state)

    @property
    def past_shows(self):
        return [item for item in self.shows if item.start_time <= datetime.datetime.utcnow()]

    @property
    def upcoming_shows(self):
        return [item for item in self.shows if item.start_time > datetime.datetime.utcnow()]

    @property
    def upcoming_shows_count(self):
        return len([item for item in self.shows if item.start_time > datetime.datetime.utcnow()])

    @property
    def past_shows_count(self):
        return len([item for item in self.shows if item.start_time <= datetime.datetime.utcnow()])


class Artist(db.Model):
    __tablename__ = 'Artist'
    __default_image = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid' \
                      '=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80 '

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), default=__default_image)
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), default='No seeking for new venues now')
    shows = db.relationship('Show', backref='artist')

    @property
    def past_shows(self):
        return [item for item in self.shows if item.start_time <= datetime.datetime.utcnow()]

    @property
    def upcoming_shows(self):
        return [item for item in self.shows if item.start_time > datetime.datetime.utcnow()]

    @property
    def upcoming_shows_count(self):
        return len([item for item in self.shows if item.start_time > datetime.datetime.utcnow()])

    @property
    def past_shows_count(self):
        return len([item for item in self.shows if item.start_time <= datetime.datetime.utcnow()])


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)


db.create_all()

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []

    for single_venue in db.session.query(Venue).all():
        single_item = {}

        city_state_already_added = False
        for single_data_item in data:
            if single_data_item['city'] == single_venue.city and single_data_item['state'] == single_venue.state:
                single_venue_item = {
                    'id': single_venue.id,
                    'name': single_venue.name,
                    'num_upcoming_shows': single_venue.upcoming_shows_count
                }
                single_data_item.get('venues', []).append(single_venue_item)
                city_state_already_added = True
                break

        if not city_state_already_added:
            single_item['city'] = single_venue.city
            single_item['state'] = single_venue.state
            single_venue_item = {
                'id': single_venue.id,
                'name': single_venue.name,
                'num_upcoming_shows': single_venue.upcoming_shows_count
            }
            single_item['venues'] = list()
            single_item['venues'].insert(0, single_venue_item)
            data.append(single_item)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    response = {'count': 0, 'data': {}}
    search_term = request.form.get('search_term', '')
    query_results = db.session.query(Venue).filter(Venue.name.ilike("%{}%".format(search_term)))

    if query_results:
        response['count'] = query_results.count()
        response['data'] = [
            {'id': item.id, 'name': item.name, 'num_upcoming_shows': item.upcoming_shows_count} for item in query_results
        ]

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    try:
        query_venue = db.session.query(Venue).get(venue_id)
        query_venue_dict = query_venue.__dict__

        query_venue_dict['past_shows'] = [
            {
                'artist_id': item.artist.id,
                'artist_name': item.artist.name,
                'artist_image_link': item.artist.image_link,
                'start_time': item.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            for item in query_venue.past_shows
        ]

        query_venue_dict['upcoming_shows'] = [
            {
                'artist_id': item.artist.id,
                'artist_name': item.artist.name,
                'artist_image_link': item.artist.image_link,
                'start_time': item.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            for item in query_venue.upcoming_shows
        ]

        query_venue_dict['past_shows_count'] = query_venue.past_shows_count
        query_venue_dict['upcoming_shows_count'] = query_venue.upcoming_shows_count
        data = query_venue_dict
    except Exception as exc:
        logging.debug(exc.args)
        data = []

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venue = {}
        venue['name'] = request.form.get('name', 'no_data')
        venue['city'] = request.form.get('city', 'no_data')
        venue['state'] = request.form.get('state', 'no_data')
        venue['address'] = request.form.get('address', 'no_data')
        venue['phone'] = request.form.get('phone', 'no_data')
        venue['genres'] = dict(request.form).get('genres', 'no_data')
        venue['facebook_link'] = request.form.get('facebook_link', 'no_data')

        db.session.add(Venue(**venue))
        db.session.commit()
    except Exception as exc:
        logging.critical(exc.args)
        db.session.rollback()
        flash('Venue ' + request.form['name'] + ' insertion was wrong!')
    else:
        flash('Venue ' + request.form['name'] + ' was successfully inserted!')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    query_results = db.session.query(Artist).filter(Artist.name.ilike("%{}%".format(search_term)))
    response = {}

    if query_results:
        response['count'] = query_results.count()
        response['data'] = [
            {'id': item.id, 'name': item.name, 'num_upcoming_shows': item.upcoming_shows_count} for item in
            query_results
        ]

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    try:
        query_artist = db.session.query(Artist).get(artist_id)
        query_artist_dict = query_artist.__dict__

        query_artist_dict['past_shows'] = [
            {
                'venue_id': item.venue.id,
                'venue_name': item.venue.name,
                'venue_image_link': item.venue.image_link,
                'start_time': item.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            for item in query_artist.past_shows
        ]

        query_artist_dict['upcoming_shows'] = [
            {
                'venue_id': item.venue.id,
                'venue_name': item.venue.name,
                'venue_image_link': item.venue.image_link,
                'start_time': item.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            for item in query_artist.upcoming_shows
        ]

        query_artist_dict['past_shows_count'] = query_artist.past_shows_count
        query_artist_dict['upcoming_shows_count'] = query_artist.upcoming_shows_count
        data = query_artist_dict

    except Exception as exc:
        logging.debug(exc.args)
        data = []
    finally:
        db.session.close()

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    try:
        artist = Artist.query.get(artist_id)
    except Exception as exc:
        logging.critical(exc.args)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist_updated_dict = {}
    for single_field in request.form:
        artist_updated_dict[single_field] = request.form.get(single_field)

    try:
        db.session.add(Artist(**artist_updated_dict))
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logging.critical(exc.args)
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    try:
        venue = Venue.query.get(venue_id)
    except Exception as exc:
        logging.critical(exc.args)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue_updated_dict = {}
    for single_field in request.form:
        venue_updated_dict[single_field] = request.form.get(single_field)

    try:
        db.session.add(Venue(**venue_updated_dict))
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        logging.critical(exc.args)
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        artist_dict = {}
        artist_dict['name'] = request.form.get('name', 'no_data')
        artist_dict['city'] = request.form.get('city', 'no_data')
        artist_dict['state'] = request.form.get('state', 'no_data')
        artist_dict['phone'] = request.form.get('phone', 'no_data')
        artist_dict['genres'] = dict(request.form).get('genres', 'no_data')
        artist_dict['facebook_link'] = request.form.get('facebook_link', 'no_data')

        db.session.add(Artist(**artist_dict))
        db.session.commit()
    except Exception as exc:
        logging.critical(exc.args)
        db.session.rollback()
        flash('Artist ' + request.form['name'] + ' insertion was wrong!')
    else:
        flash('Artist ' + request.form['name'] + ' was successfully inserted!')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = [
        {
            "venue_id": item.venue.id,
            "venue_name": item.venue.name,
            "artist_id": item.artist.id,
            "artist_name": item.artist.name,
            "artist_image_link": item.artist.image_link,
            "start_time": item.start_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        for item in Show.query.all()
    ]

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show_dict = {}
        show_dict['start_time'] = request.form.get('start_time', 'no_data')
        show_dict['artist_id'] = request.form.get('artist_id', 'no_data')
        show_dict['venue_id'] = request.form.get('venue_id', 'no_data')

        db.session.add(Show(**show_dict))
        db.session.commit()
    except Exception as exc:
        logging.critical(exc.args)
        db.session.rollback()
        flash('Show insertion was wrong!')
    else:
        flash('Show was successfully inserted!')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
