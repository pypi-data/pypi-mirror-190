.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.pintarito/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.pintarito/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.pintarito/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.pintarito?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.pintarito/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.pintarito

.. image:: https://img.shields.io/pypi/v/collective.pintarito.svg
    :target: https://pypi.python.org/pypi/collective.pintarito/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.pintarito.svg
    :target: https://pypi.python.org/pypi/collective.pintarito
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.pintarito.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.pintarito.svg
    :target: https://pypi.python.org/pypi/collective.pintarito/
    :alt: License


====================
collective.pintarito
====================

An add-on for Plone that changes the color of the default Barceloneta theme.

Features
--------

Installing this product will create a new control panel that allows
you to quickly select a CSS style sheet which controls the barceloneta
CSS color variables.

It provides also an override for the Plone logo to inline the svg image
in order to control its color using CSS.


Should I use it?
----------------

For the time being this is a proof of concept born at the Alpine city sprint 2023.
You are welcome to improve it and make it more useful, but do not rely on its internals.

What the heck is Pintarito?
---------------------------

Pintarito is a word chosen to remind the Catalan word *pintar* (to paint).
I decided to make up that word to avoid stealing some other useful name from the collective namespace.

Possible future plans
---------------------

It *might be* that in the future the possibility to wire up external color schemes will be added.
Also It might be possible that css file uploaded to the site might be picked.


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Installation
------------

Install collective.pintarito by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.pintarito


and then running ``bin/buildout``


Authors
-------

Provided by awesome people ;)


Contributors
------------

Put your name here, you deserve it!

- Alessandro Pisa


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.pintarito/issues
- Source Code: https://github.com/collective/collective.pintarito
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
