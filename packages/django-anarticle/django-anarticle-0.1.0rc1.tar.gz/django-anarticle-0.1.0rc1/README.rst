====================================
django package of an article
====================================

Anarticle uses tag, catelog, and article models to make article publication easy.
Support for graphQL with pre-defined types and basic resolvers.

------------
Requirements
------------

* Python 3.11+
* django 4.0+
* ariadne 0.16.0+
* ariadne-relay 0.1.0a8+
* pillow 9.4.0+

-------------------
Django admin mixins
-------------------

Use predefined mixins to construct the admin class.

* TagAdminMixin
* CategoryAdminMixin
* ArticleAdminMixin

.. code:: python

    from django.contrib import admin

    from anarticle.models import Tag
    from anarticle.admin.mixins import TagAdminMixin


    @admin.register(Tag)
    class TagAdmin(TagAdminMixin, ModelAdmin):
        ...

---------------------------
Ariadne types and resolvers
---------------------------

Integrate predefined types and resolvers to scheme.

**resolvers**

* resolve_anarticles
* resolve_anarticle_tags
* resolve_anarticle_categories

**types**

* anarticle
* anarticle_paragraph
* anarticle_tag
* anarticle_category

-------
License
-------

django-anarticle is released under the terms of **Apache license**. Full details in LICENSE file.
