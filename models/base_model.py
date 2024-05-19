#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import models
from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """A base class for all hbnb models"""
    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True, unique=True)
        created_at = Column(DateTime,
                            nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime,
                            nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in {'created_at', 'updated_at'}:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
            # if os.getenv('HBNB_TYPE_STORAGE') in ('db')
            if not hasattr(kwargs, 'id'):
                setattr(self, 'id', str(uuid.uuid4()))
            if not hasattr(kwargs, 'created_at'):
                setattr(self, 'created_at', datetime.now())
            if not hasattr(kwargs, 'updated_at'):
                setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """delete the current instance from storage"""
        from models.storage import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        res = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    res[key] = value.isoformat()
                else:
                    res[key] = value
        res['__class__'] = self.__class__.__name__
        return res
