from app import db
from flask_babel import lazy_gettext


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, name):
        self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {'name': self.name}

    def get_list(self):
        result = [('id', self.id),
                  ('name', self.name)]
        return result

    def get_id(self):
        return self.id

    def has_relationships(self):
        return Scheduler.query.filter_by(room=self).all()

    @staticmethod
    def get_allowed(current_user):
        if current_user.admin:
            return Room.query.all()
        elif not current_user.id_group:
            return []
        else:
            sql_statement = ('select distinct * from rooms '
                             'inner join (select room_id '
                             'from schedule '
                             'where schedule.group_id={}) as table1 '
                             'on rooms.id = table1.room_id').format(current_user.id_group)
            return Room.query.from_statement(sql_statement).all()

    @staticmethod
    def get_by_id(id_entity):
        room = None
        try:
            room = Room.query.get(id_entity)
        except Exception, e:
            print e
        return room


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(10), nullable=False)
    lastname = db.Column(db.String(10), nullable=False)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return self.firstname + ' ' + self.lastname

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {'firstname': self.firstname, 'lastname': self.lastname}

    def get_list(self):
        result = [('id', self.id),
                  ('firstname', self.firstname),
                  ('lastname', self.lastname)]
        return result

    def get_id(self):
        return self.id

    def has_relationships(self):
        return Lesson.query.filter_by(teacher=self).all()

    @staticmethod
    def get_allowed(current_user):
        if current_user.admin:
            return Teacher.query.all()
        elif not current_user.id_group:
            return []
        else:
            sql_statement = ('select distinct * from teachers '
                             'inner join (select id_teacher '
                             'from lessons '
                             'inner join schedule '
                             'on lessons.id = schedule.lesson_id '
                             'and schedule.group_id={}) as table1 '
                             'on teachers.id = table1.id_teacher').format(current_user.id_group)
            return Teacher.query.from_statement(sql_statement).all()

    @staticmethod
    def get_by_id(id_entity):
        teacher = None
        try:
            teacher = Teacher.query.get(id_entity)
        except Exception, e:
            print e
        return teacher


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    id_teacher = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher',
                              backref=db.backref('lessons', lazy='dynamic'))

    def __init__(self, name, teacher):
        self.name = name
        self.teacher = teacher

    def __repr__(self):
        return '%s (%s)' % (self.name, self.teacher)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, name, teacher):
        self.name = name
        self.teacher = teacher
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {'name': self.name, 'teacher': self.teacher}

    def get_list(self):
        result = [('id', self.id),
                  ('name', self.name),
                  ('teacher', self.teacher)]
        return result

    def get_id(self):
        return self.id

    def has_relationships(self):
        return Scheduler.query.filter_by(lesson=self).all()

    @staticmethod
    def get_allowed(current_user):
        if current_user.admin:
            return Lesson.query.all()
        elif not current_user.id_group:
            return []
        else:
            sql_statement = ('select distinct * from lessons '
                             'inner join schedule '
                             'on lessons.id = schedule.lesson_id '
                             'and schedule.group_id={} '
                             'group by id_teacher, lesson_id').format(current_user.id_group)
            return Lesson.query.from_statement(sql_statement).all()

    @staticmethod
    def get_by_id(id_entity):
        lesson = None
        try:
            lesson = Lesson.query.get(id_entity)
        except Exception, e:
            print e
        return lesson


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, name):
        self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {'name': self.name}

    def get_list(self):
        result = [('id', self.id),
                  ('name', self.name)]
        return result

    def get_id(self):
        return self.id

    def has_relationships(self):
        return Scheduler.query.filter_by(group=self).all()

    @staticmethod
    def get_allowed(current_user):
        if current_user.admin:
            return Group.query.all()
        else:
            return current_user.group

    @staticmethod
    def get_by_id(id_entity):
        group = None
        try:
            group = Group.query.get(id_entity)
        except Exception, e:
            print e
        return group


class ClassNumber(db.Model):
    __tablename__ = "class_numbers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    time_start = db.Column(db.String(5), nullable=False)
    time_end = db.Column(db.String(5), nullable=False)

    def __init__(self, name, time_start, time_end):
        self.name = name
        self.time_start = time_start
        self.time_end = time_end

    def __repr__(self):
        return self.name

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, name, time_start, time_end):
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_id(self):
        return self.id

    def get_dict(self):
        return {'name': self.name, 'time_start': self.time_start, 'time_end': self.time_end}

    def get_list(self):
        result = [('id', self.id),
                  ('name', self.name),
                  ('time start', self.time_start),
                  ('time end', self.time_end)]
        return result

    def has_relationships(self):
        return Scheduler.query.filter_by(class_number=self).all()

    @staticmethod
    def get_allowed(current_user):
        return ClassNumber.query.all()

    @staticmethod
    def get_by_id(id_entity):
        number = None
        try:
            number = ClassNumber.query.get(id_entity)
        except Exception, e:
            print e
        return number


class Scheduler(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    room = db.relationship('Room',
                           backref=db.backref('schedules', lazy='dynamic'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    lesson = db.relationship('Lesson',
                             backref=db.backref('schedules', lazy='dynamic'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship('Group',
                            backref=db.backref('schedules', lazy='dynamic'))
    date = db.Column(db.Date, nullable=False)
    class_number_id = db.Column(db.Integer, db.ForeignKey('class_numbers.id'))
    class_number = db.relationship('ClassNumber',
                            backref=db.backref('schedules', lazy='dynamic'))

    def __init__(self, room, lesson, group, date, class_number):
        self.room = room
        self.lesson = lesson
        self.group = group
        self.date = date
        self.class_number = class_number

    def __repr__(self):
        return '%s %s %s' % (self.room, self.group, self.lesson)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, room, lesson, group, date, class_number):
        self.room = room
        self.lesson = lesson
        self.group = group
        self.date = date
        self.class_number = class_number
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {'date': self.date, 'class_number': self.class_number,
                'room': self.room, 'lesson': self.lesson, 'group': self.group}

    def get_list(self):
        result = [('id', self.id),
                  ('date', self.date),
                  ('class number', self.class_number),
                  ('room', self.room),
                  ('lesson', self.lesson),
                  ('group', self.group)]
        return result

    def get_id(self):
        return self.id

    @staticmethod
    def has_relationships():
        return False

    @staticmethod
    def get_allowed(current_user):
        if current_user.admin:
            return Scheduler.query.all()
        elif not current_user.id_group:
            return []
        else:
            return Scheduler.query.filter_by(group=current_user.group).all()

    @staticmethod
    def get_by_id(id_entity):
        scheduler = None
        try:
            scheduler = Scheduler.query.get(id_entity)
        except Exception, e:
            print e
        return scheduler

    @staticmethod
    def get_resources_data():
        groups = Group.query.all()
        result = []
        for g in groups:
            result.append({'text': g.name,
                           'id': g.id,
                           'color': '#1e90ff'})
        return result

    @staticmethod
    def get_data_group(user):
        if user.admin:
            schedule = Scheduler.query.all()
        else:
            schedule = Scheduler.query.filter_by(group=user.group).all()
        result = []
        for s in schedule:
            if user.admin:
                text_cell = s.room.name + ' ' + s.group.name + ' ' + s.lesson.name
            else:
                text_cell = s.room.name + ' ' + s.lesson.name
            result.append({'id': s.id,
                           'text': text_cell,
                           'group': s.group.name,
                           'room': s.room.name,
                           'lesson': s.lesson.name,
                           'teacher': s.lesson.teacher.__repr__(),
                           'class_number': s.class_number.name,
                           'ownerId': s.group.id,
                           'startDate': str(s.date)+'T'+s.class_number.time_start +':00.000000',
                           'endDate': str(s.date)+'T'+s.class_number.time_end +':00.000000'})
        return result


def get_teachers():
    return Teacher.query.all()


def get_groups():
    return Group.query.all()


def get_lessons():
    return Lesson.query.all()


def get_rooms():
    return Room.query.all()


def get_class_numbers():
    return ClassNumber.query.all()


from .forms import RoomForm, TeacherForm, LessonForm, GroupForm, ClassNumberForm, SchedulerForm
ENTITIES = {'rooms': {'name_unit': lazy_gettext('room'), 'href': 'rooms', 'title': lazy_gettext('Rooms'), 'class': Room, 'form': RoomForm},
            'teachers': {'name_unit': lazy_gettext('teacher'), 'href': 'teachers', 'title': lazy_gettext('Teachers'), 'class': Teacher, 'form': TeacherForm},
            'lessons': {'name_unit': lazy_gettext('lesson'), 'href': 'lessons', 'title': lazy_gettext('Lessons'), 'class': Lesson, 'form': LessonForm},
            'groups': {'name_unit': lazy_gettext('group'), 'href': 'groups', 'title': lazy_gettext('Groups'), 'class': Group, 'form': GroupForm},
            'schedule': {'name_unit': lazy_gettext('schedule'), 'href': 'schedule', 'title': lazy_gettext('Schedule'), 'class': Scheduler, 'form': SchedulerForm},
            'class_numbers': {'name_unit': lazy_gettext('class number'), 'href': 'class_numbers', 'title': lazy_gettext('Class numbers'),
                              'class': ClassNumber, 'form': ClassNumberForm}}