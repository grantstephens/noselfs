NoseLFS
==========


.. image:: https://travis-ci.org/grantstephens/noselfs.svg?branch=master
    :target: https://travis-ci.org/grantstephens/noselfs

This provides a nice little decorator that extends the nose attrib decorator
and adds a git lfs argument which will pull any needed lfs files for the test
if they haven't been fetched already

Usage
-----

Just use the focus decorator in your tests:

.. code-block:: python

    from noselfs import noselfs

    @noselfs('filename.ext', 'data', 'unit')
    def test_my_amazing_feature(file_name):
        with open(file_name) as open_file:
            # Whatever
        assert_is_awesome(my_feature)



How it works
------------



Installation
------------

Use pip!:

.. code-block:: bash

    pip install noselfs

Or if you're developing it:

.. code-block:: bash

    pip install -e .
    pip install -e ".[tests]"

Tests
-----

TODO
