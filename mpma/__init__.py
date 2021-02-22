"""mpma - mon petit monde amoureux

just a fancy library to display polyamorist graphs

just a toy project really. leave it alone.

"""
from graphviz import Digraph
import hashlib

import json


class MissingCenterException(Exception):
    pass


class MissingIDException(Exception):
    pass


class Person(object):
    BAG_OF_ITEMS = {}
    @classmethod
    def get(cls, id):
        return cls.BAG_OF_ITEMS.get(id)

    @classmethod
    def get_all(cls):
        return cls.BAG_OF_ITEMS.items()

    def __init__(self, id=None, aliases=None, notes=None):
        if id is None:
            raise MissingIDException
        self.id = id
        self.aliases = aliases
        self.notes = notes
        self.BAG_OF_ITEMS[self.id] = self
        self._relationships = set()

    @property
    def relationships(self):
        return list(self._relationships)

    def render_relationships(self, graph: Digraph):
        for r in self.relationships:
            graph.edge(
                r.left_person.id,
                r.right_person.id, 
                label=r.relationship_type.icon)

    def load_data(self, data):
        self.id = data['id']
        self.aliases = data['aliases']
        self.notes = data['notes']

    def load_relationships(self, relationships):
        for r in relationships:
            if r['id_left'] == self.id:
                self.add_relationship(r['id_right'], r['relationship_type'])

    def add_relationship(self, other, reltype_id):
        r = Relationship(self, Person.get(other), 
                         RelationshipType.get(reltype_id))
        self._relationships.add(r)

    def __str__(self):
        s = "{}:\n".format(self.id)
        s += "\tmy aliases: {}\n".format(', '.join(self.aliases))
        s += "\tnotes about me:\n\t\t{}\n".format(self.notes)
        for r in self._relationships:
            s += "\tI {} {} (aliases: {})\n".format(
                r.relationship_type, 
                r.right_person.id,
                ', '.join(r.right_person.aliases))
        return s


class RelationshipType(object):
    BAG_OF_TYPES = {}

    @classmethod
    def get_all(cls):
        return cls.BAG_OF_TYPES.items()

    @classmethod
    def get(cls, id):
        return cls.BAG_OF_TYPES.get(id)

    def __init__(self, id=None, icon=None, oriented=False, description=None):
        if id is None:
            raise MissingIDException
        self.id = id
        self.icon = icon
        self.oriented = oriented
        self.description = description
        self.BAG_OF_TYPES[id] = self

    def __str__(self):
        return '{} [{}]'.format(self.icon, self.description)


class Relationship(object):
    def __init__(self, left_person, right_person, relationship_type):
        self.left_person = left_person
        self.right_person = right_person
        self.relationship_type = relationship_type

    def __str__(self):
        return '{}__{}__{}'.format(
            self.left_person.id,
            self.right_person.id,
            self.relationship_type.id
        )

    def __hash__(self):
        d = int(hashlib.sha1(str(self).encode('utf-8')).hexdigest(), 16)
        return d

    def __eq__(self, other):
        return (
            self.left_person == other.left_person and
            self.right_person == other.right_person and
            self.relationship_type == other.relationship_type
        )


class RelationshipGraph(object):
    def __init__(self):
        self._data = None
        self._persons = {}
        self._reltypes = {}
        self.center = None
    
    def load_file(self, path):
        try:
            with open(path, 'r') as fh:
                self._data = json.load(fh)
        except IOError:
            raise
        except json.JSONDecodeError:
            raise
        self.parse_data()
    
    def load_string(self, json_data):
        try:
            self._data = json.loads(json_data)
        except json.JSONDecodeError:
            raise
        self.parse_data()

    def parse_data(self):
        Person.BAG_OF_ITEMS.clear()
        RelationshipType.BAG_OF_TYPES.clear()
        for e in self._data['entities']:
            Person(e['id'], e['aliases'], e.get('notes', None))
        for r in self._data['relationship_types']:
            RelationshipType(id=r['id'], icon=r['icon'], oriented=r['oriented'], description=r['description'])
        for _, p in Person.get_all():
            p.load_relationships(self._data['relationships'])
        self.center = self._data['center']
            
    def render_relationships_from_center(self, tf=None):
        c = Person.get(self.center)
        d = Digraph(name='polycule-{}'.format(c.id))
        for _, p in Person.get_all():
            d.node(p.id, ', '.join(p.aliases))
        for _, p in Person.get_all():
            p.render_relationships(d)
        return d