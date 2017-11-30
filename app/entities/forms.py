from models import get_teachers, get_groups, get_lessons, get_rooms, get_class_numbers
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.fields import StringField, DateField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class RoomForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    def get_dict(self):
        form_dict = self.__dict__
        return {key: form_dict[key].data for key in form_dict.keys()
                if isinstance(form_dict[key], Field) and key != 'csrf_token'}

    def fill(self, name):
        self.name.data = name


class TeacherForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])

    def get_dict(self):
        form_dict = self.__dict__
        return {key: form_dict[key].data for key in form_dict.keys()
                if isinstance(form_dict[key], Field) and key != 'csrf_token'}

    def fill(self, lastname, firstname):
        self.lastname.data = lastname
        self.firstname.data = firstname


class LessonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    teacher = QuerySelectField('Teacher', query_factory=get_teachers, allow_blank=False)

    def get_dict(self):
        form_dict = self.__dict__
        return {key: form_dict[key].data for key in form_dict.keys()
                if isinstance(form_dict[key], Field) and key != 'csrf_token'}

    def fill(self, name, teacher):
        self.name.data = name
        self.teacher.data = teacher


class GroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    def get_dict(self):
        form_dict = self.__dict__
        return {key: form_dict[key].data for key in form_dict.keys()
                if isinstance(form_dict[key], Field) and key != 'csrf_token'}

    def fill(self, name):
        self.name.data = name


class ClassNumberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    time_start = StringField('Time start', validators=[DataRequired()])
    time_end = StringField('Time end', validators=[DataRequired()])

    def get_dict(self):
        form_dict = self.__dict__
        return {key: form_dict[key].data for key in form_dict.keys()
                if isinstance(form_dict[key], Field) and key != 'csrf_token'}

    def fill(self, name, time_start, time_end):
        self.name.data = name
        self.time_start.data = time_start
        self.time_end.data = time_end


class SchedulerForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    class_number = QuerySelectField('Class number', query_factory=get_class_numbers, allow_blank=False)
    room = QuerySelectField('Room', query_factory=get_rooms, allow_blank=False)
    lesson = QuerySelectField('Lesson', query_factory=get_lessons, allow_blank=False)
    group = QuerySelectField('Group', query_factory=get_groups, allow_blank=False)

    def get_dict(self):
        form_dict = self.__dict__
        return {key: form_dict[key].data for key in form_dict.keys()
                if isinstance(form_dict[key], Field) and key != 'csrf_token'}

    def fill(self, date, class_number, room, lesson, group):
        self.date.data = date
        self.class_number.data = class_number
        self.room.data = room
        self.lesson.data = lesson
        self.group.data = group