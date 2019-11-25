# *****************************************************************************
#
# Copyright (c) 2019, the Perspective Authors.
#
# This file is part of the Perspective library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#


class _PerspectiveStateManager(object):

    TO_PROCESS = {}

    @classmethod
    def set_process(cls, pool, table_id):
        """Queue a `_process` call on the specified pool and table ID.

        Checks whether a `_process()` call has been queued already for the specified
        table, and calls `queue_process`, which MUST be implemented by the caller.

        Args:
            cls (:obj`_PerspectiveStateManager`): an instance of _PerspectiveStateManager
            pool (:obj`libbinding.t_pool`): a `t_pool` object
            table_id (:obj`int`): a unique ID for the Table
        """
        if table_id not in cls.TO_PROCESS:
            cls.TO_PROCESS[table_id] = pool
            cls.queue_process(table_id)

    @classmethod
    def clear_process(cls, table_id):
        """Given a table_id, find the corresponding pool and call `process()`
        on it.

        Args:
            cls (:obj`_PerspectiveStateManager`): an instance of _PerspectiveStateManager
            table_id (:obj`int`): The unique ID of the Table
        """
        pool = cls.TO_PROCESS.get(table_id, None)
        if pool is not None:
            pool._process()
            cls.reset_process(table_id)

    @classmethod
    def reset_process(cls, table_id):
        """Remove a pool from the execution cache, indicating that it should no
        longer be operated on.

        Args:
            table_id (:obj`int`): The unique ID of the Table
        """
        cls.TO_PROCESS.pop(table_id, None)

    @classmethod
    def _queue_process_immediate(cls, table_id):
        """Immediately execute `clear_process` on the pool as soon
        as it is registered with the manager.

        This is the default implementation of `set_process` for environments
        without an event loop.

        Args:
            pool (:obj`libbinding.t_pool`): A `t_pool` object
            table_id (:obj`int`): The unique ID of the Table
        """
        cls.clear_process(table_id)
