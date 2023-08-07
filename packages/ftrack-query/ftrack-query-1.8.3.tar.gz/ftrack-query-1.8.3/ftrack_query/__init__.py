# pylint: disable=consider-using-f-string
"""Wrapper over the FTrack API to make it more pythonic to use.
Supports the querying and creation of objects, and a way to build
event listeners.

It's designed to hide the SQL-like syntax in favour of an object
orientated approach. Inspiration was taken from SQLALchemy.
"""

__all__ = ['FTrackQuery', 'exception', 'entity', 'and_', 'or_', 'not_', 'event',
           'select', 'create', 'update', 'delete', 'attr']

__version__ = '1.8.3'

import os

import ftrack_api

from . import exception, utils
from .abstract import AbstractStatement
from .query import Query, entity, and_, or_, not_
from .event import event
from .statement import attr, select, create, update, delete
from .utils import copy_doc


class FTrackQuery(ftrack_api.Session):
    # pylint: disable=arguments-differ
    """Expansion of the ftrack_api.Session class."""

    def __init__(self, page_size=None, logger=utils.logger, debug=False, **kwargs):
        """Attempt to initialise the connection.
        If the debug argument is set, the connection will be ignored.
        """
        self.debug = debug

        if page_size is None:
            try:
                page_size = int(os.environ.get('FTRACK_API_PAGE_SIZE', 0)) or None
            except ValueError:
                pass
        self.page_size = page_size

        self._logger = logger
        self._logger.debug('Connecting...')

        if not self.debug:
            super(FTrackQuery, self).__init__(**kwargs)
        self._logger.debug('New session initialised.')

    def __getattribute__(self, attr):
        """Get an entity type if it exists.
        The standard AttributeError will be raised if not.
        """
        try:
            return super(FTrackQuery, self).__getattribute__(attr)
        except AttributeError:
            if self.debug or attr in super(FTrackQuery, self).__getattribute__('types'):
                return Query(self, attr)
            raise

    def close(self, *args, **kwargs):
        """Avoid error when closing session in debug mode."""
        if not self.debug:
            return super(FTrackQuery, self).close(*args, **kwargs)

    def get(self, value, _value=None, *args, **kwargs):  # pylint: disable=keyword-arg-before-vararg
        """Get any entity from its ID.
        The _value argument is for compatibility with ftrack_api.Session.
        """
        if _value is None:
            entity = 'Context'
        else:
            entity, value = value, _value
        self._logger.debug('Get: %s(%r)', entity, value)
        return super(FTrackQuery, self).get(entity, value, *args, **kwargs)

    def query(self, query, page_size=None, **kwargs):
        """Create an FTrack query object from a string."""
        query = str(query)
        self._logger.debug('Query: %s', query)

        # Set page size
        page_size = page_size or self.page_size
        if page_size:
            kwargs['page_size'] = page_size

        return super(FTrackQuery, self).query(query, **kwargs)

    def create(self, entity, data, *args, **kwargs):
        """Create a new entity."""
        if not kwargs.get('reconstructing', False):
            self._logger.debug('Create: %s(%s)', entity, utils.dict_to_str(data))
        return super(FTrackQuery, self).create(entity, data, *args, **kwargs)

    def delete(self, entity, *args, **kwargs):
        """Delete an FTrack entity."""
        self._logger.debug('Delete: %r', entity)
        return super(FTrackQuery, self).delete(entity, *args, **kwargs)

    def where(self, *args, **kwargs):
        """Set entity type as TypedContext if none provided."""
        return self.TypedContext.where(*args, **kwargs)

    def commit(self, *args, **kwargs):
        """Commit changes."""
        self._logger.debug('Changes saved.')
        return super(FTrackQuery, self).commit(*args, **kwargs)

    def rollback(self, *args, **kwargs):
        """Rollback changes."""
        self._logger.debug('Changes discarded.')
        return super(FTrackQuery, self).rollback(*args, **kwargs)

    def populate(self, entities, projections):
        """Populate new values."""
        if isinstance(projections, (list, tuple, set)):
            projections = ','.join(map(str, projections))
        return super(FTrackQuery, self).populate(entities, projections)

    def execute(self, stmt):
        """Execute a statement."""
        if isinstance(stmt, AbstractStatement):
            return stmt.options(session=self).execute()
        raise NotImplementedError(type(stmt))

    @copy_doc(select)
    def select(self, *items):
        """Generate a select statement with the session attached."""
        return select(*items).options(session=self)
