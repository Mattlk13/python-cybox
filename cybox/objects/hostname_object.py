# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.


import cybox
import cybox.bindings.hostname_object as hostname_binding
from cybox.common import String

class Hostname(ObjectProperties):
    _binding = hostname_binding
    _binding_class = hostname_binding.HostnameObjectType
    _namespace = "http://cybox.mitre.org/objects#HostnameObject-1"
    _XSI_NS = "HostnameObj"
    _XSI_TYPE = "HostnameObjectType"

    hostname_value = cybox.TypedField("Hostname_Value", String)
    naming_system = cybox.TypedField("Naming_System", String, multiple=True)