Configure pgBackRest on standby instances, even in ``repository.path``
mode, removing a previous limitation from the implementation.

In addition, when calling ``instance backup <instance>`` with ``<instance>``
being a standby, ``pgbackrest`` is now invoked with ``--backup-standby``
option.
