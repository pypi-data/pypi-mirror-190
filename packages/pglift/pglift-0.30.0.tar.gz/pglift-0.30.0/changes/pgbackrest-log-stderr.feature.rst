Log messages from pgBackRest commands: ``pgbackrest`` commands are now invoked
with ``--log-level-stderr=info`` and respective messages are forwarded to
pglift's logger at ``DEBUG`` level (as are all ``stderr`` messages from
subprocesses).
