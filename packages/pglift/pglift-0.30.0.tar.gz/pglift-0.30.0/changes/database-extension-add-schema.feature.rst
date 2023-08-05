Until now, when an extension was added to a database, the extension's objects were
installed by default on the current schema of the database (usually ``public``
schema).

Now, the name of the ``schema`` in which to install the extension's objects can be
specified when adding or altering extensions, by specifying it in the manifest.
