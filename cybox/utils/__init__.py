# Copyright (c) 2013, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

"""Common utility methods"""

#importlib is imported below
import os

from .caches import *
from .idgen import *
from .nsparser import *

import xml.sax.saxutils


def get_class_for_object_type(object_type):
    return META.get_class_for_object_type(object_type)


ESCAPE_DICT = {',': '&comma;'}
UNESCAPE_DICT = {'&comma;': ','}


def denormalize_from_xml(value):
    # This is probably not necessary since the parser will have removed
    # the CDATA already.
    value = unwrap_cdata(value)

    if ',' in value:
        return [unescape(x).strip() for x in value.split(',')]
    else:
        return unescape(value)


def normalize_to_xml(value):
    if isinstance(value, list):
        value = ",".join([escape(x) for x in value])
    else:
        value = escape(unicode(value))

    if '&comma;' in value:
        value = wrap_cdata(value)
    return value


def escape(value):
    return xml.sax.saxutils.escape(value, ESCAPE_DICT)


def unescape(value):
    return xml.sax.saxutils.unescape(value, UNESCAPE_DICT)


def wrap_cdata(value):
    return "<![CDATA[" + value + "]]>"


def unwrap_cdata(value):
    """Remove CDATA wrapping from `value` if present"""
    if value.startswith("<![CDATA[") and value.endswith("]]>"):
        return value[9:-3]
    else:
        return value


def _import_submodules(pkg):
    import importlib
    filename = pkg.__file__
    if "__init__.py" not in filename:
        return

    print pkg.__name__
    for module in os.listdir(os.path.dirname(filename)):
        if "__init__.py" in module or not module.endswith(".py"):
            continue
        mod_name = "%s.%s" % (pkg.__name__, module[:-3])
        importlib.import_module(mod_name)


def _import_all():
    """Import all modules in the core, common and objects packages.

    This is useful when we want to check all classes for some property.
    """

    # Everything in common should be imported by cybox.common.__init__
    import cybox.common
    # Everything in core should be imported by cybox.core.__init__
    import cybox.core
    import cybox.objects
    _import_submodules(cybox.objects)
