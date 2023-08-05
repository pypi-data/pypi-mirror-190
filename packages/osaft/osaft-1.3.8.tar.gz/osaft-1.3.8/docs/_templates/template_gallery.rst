..
   this creates automatically links to all the classes; the naming is e.g. for
   the ActiveVariable --> ref-src.core.variable-ActiveVariable

{% set split_fullname = fullname.split('.') %}
{% set ref_name = split_fullname[0]~'.'~split_fullname[1]~'.'~split_fullname[2]~'.'~name %}

.. _ref-{{module}}-{{name}}:

{{ name | escape | underline}}

.. currentmodule:: {{ module }}


Examples using this class are:

.. _sphx_glr_backref_{{ref_name}}:

.. minigallery:: {{ ref_name }}

.. autoclass:: {{ objname }}
   :show-inheritance:
   :members:
   :inherited-members:

   .. autoclasstoc::
