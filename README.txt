**************************************
Content Rules: Apply local role
**************************************

.. contents:: Content
   :depth: 2

Overview
--------

**Content Rules: Apply local role** (sc.contentrules.localrole) package
provides a content rule action to apply a local role in a content.

This package is tested with Travis CI:

.. image:: https://secure.travis-ci.org/collective/sc.contentrules.localrole.png
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/sc.contentrules.localrole

.. image:: https://coveralls.io/repos/collective/sc.contentrules.localrole/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/sc.contentrules.localrole

.. image:: https://pypip.in/d/sc.contentrules.localrole/badge.png
    :target: https://pypi.python.org/pypi/sc.contentrules.localrole/
    :alt: Downloads

Use case
---------

A college with descentralized content management and groups dedicated to research. Each group should manage its own content.

In their portal they want to host areas for each research group they sponsor.
All those areas will be under the folder /research/. A research group called
"Environmental Studies" will have an area at /research/environmental-studies.

Every time a new research group is added under /research/ they want asing a local role to users and gropus:

    * Editor local role: Given to users and groups responsible for this area.

    * Reader local role: Group of users with access to this area.

Installation
------------

To enable this product,on a buildout based installation:

1. Edit your buildout.cfg and add ``sc.contentrules.localrole``
   to the list of eggs to install ::

    [buildout]
    ...
    eggs =
        sc.contentrules.localrole

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.


Action
---------

This package provides one content rules action.

Apply local role
^^^^^^^^^^^^^^^^^^^

Used to create a new user group this action have three options:

Username / Group name
    Identifier of the user or group to receive the local role in the current content.
    You are allowed to use ${title} in here to dinamically generate the id of the user
    or group. i.e.: If this field have a value of **${title} Editors** and the action
    is being executed for a folder with title "Environmental Studies", this field will
    be "Environmental Studies Editors"

Roles
    Local roles to be applied in the current content -- the one that triggered the
    content rule -- to the user or group identified on the previous field


Requirements
------------

    * Plone 3.3.x and above (http://plone.org/products/plone)
