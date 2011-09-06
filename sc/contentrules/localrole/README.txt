.. contents:: Table of Contents
   :depth: 2

sc.contentrules.localrole
**********************************

Overview
--------
    **sc.contentrules.localrole** 

Use case
---------

    In a portal content is created in a folder /post and must be moved to a 
    new location when it is published. This new location will be under another 
    folder /blogs where every user has its own sub folder 
    
    A portal manager will add a content rule that when a Page is published
    inside /post it will lookup the value of the method Creator and then move 
    the published content to a folderish under /blog. The id of this folderish 
    will match the value extracted from the Creator method.
    
    So, a user with username kirk, will add a new Page in /post and wait for 
    publication. When a reviewer publishes the content, it will be moved under 
    /blog/kirk, which **must** already exist.

Requirements
------------

    * Plone 3.3.x and above (http://plone.org/products/plone)
    
    
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

Sponsoring
----------

Development of this product was sponsored by:
    
    * `Simples Consultoria <http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * Erico Andrei (erico at simplesconsultoria dot com dot br)
