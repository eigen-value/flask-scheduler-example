from flask import Blueprint, request, redirect, render_template, flash
from flask_login import login_required, current_user
from .models import ENTITIES
from app.decorators import only_for_admin
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

mod = Blueprint('entity', __name__)


@mod.route('/<href>', methods=['GET'])
@login_required
def show_entity(href):
    if href not in ENTITIES:
        return render_template('404.html')
    entity = ENTITIES.get(href)
    if not current_user.admin and not current_user.id_group:
        message = 'Please enter your group in the user settings.'
        return render_template('entity.html', name=entity['href'],
                               title=entity['title'], message=message)
    else:
        refs = entity['class'].get_allowed(current_user)
        return render_template('entity.html', name=entity['href'],
                               title=entity['title'], entities=refs)


@mod.route('/<href>/add', methods=['GET', 'POST'])
@only_for_admin
def add_entity(href):
    if href not in ENTITIES:
        return render_template('404.html')
    entity = ENTITIES.get(href)
    form = entity['form'](request.form)
    new_ref = entity['class'](**form.get_dict())
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_ref.add()
            return redirect('/' + entity['href'])
        except IntegrityError:
            flash('You entered non-unique values', 'error')
        except SQLAlchemyError:
            flash('An error occurred while writing to the database', 'error')
        return redirect('/%s/add' % href)
    else:
        form.fill(**new_ref.get_dict())
        return render_template('entity_update.html', title='New %s' % entity['name_unit'],
                               text_button='Add', form=form)


@mod.route('/<href>/<id_entity>/update', methods=['GET', "POST"])
@only_for_admin
def update_entity(href, id_entity):
    if href not in ENTITIES:
        return render_template('404.html')
    entity = ENTITIES.get(href)
    found_ref = entity['class'].get_by_id(id_entity)
    form = entity['form'](request.form)
    if request.method == "POST" and form.validate_on_submit():
        try:
            found_ref.edit(**form.get_dict())
            return redirect('/' + entity['href'])
        except IntegrityError:
            flash('You entered non-unique values', 'error')
        except SQLAlchemyError:
            flash('An error occurred while writing to the database', 'error')
        return redirect('/%s/%s/update' % (href, id_entity))
    else:
        form.fill(**found_ref.get_dict())
        return render_template('entity_update.html', text_button='Update', form=form,
                               title='Update %s %s' % (entity['name_unit'], found_ref))


@mod.route('/<href>/<id_entity>/delete', methods=['GET'])
@only_for_admin
def delete_entity(href, id_entity):
    if href not in ENTITIES:
        return render_template('404.html')
    entity = ENTITIES.get(href)
    found_ref = entity['class'].get_by_id(id_entity)
    if found_ref.has_relationships():
        flash('You can\'t delete %s that used' % entity['name_unit'], 'error')
        return redirect('/' + entity['href'])
    try:
        found_ref.delete()
    except SQLAlchemyError:
        flash('An error occurred while writing to the database', 'error')
    return redirect('/' + entity['href'])
