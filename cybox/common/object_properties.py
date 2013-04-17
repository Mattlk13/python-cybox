import cybox
import cybox.utils


class ObjectProperties(cybox.Entity):
    """The Cybox ObjectProperties base class."""

    def __init__(self):
        self.object_reference = None
        self.parent = None

    @property
    def parent(self):
        if not self._parent:
            self._parent = cybox.core.object.Object(self)
        return self._parent

    @parent.setter
    def parent(self, value):
        if value and not isinstance(value, cybox.core.object.Object):
            raise ValueError("Must be an Object")
        self._parent = value

    def add_related(self, related, relationship, inline=True):
        self.parent.add_related(related, relationship, inline)

    def to_obj(self, partial_obj=None):
        """Populate an existing bindings object.

        Note that this is different than to_obj() on most other CybOX types.
        """
        if not partial_obj:
            raise NotImplementedError()

        partial_obj.set_xsi_type("%s:%s" % (self._XSI_NS, self._XSI_TYPE))
        if self.object_reference is not None:
            partial_obj.set_object_reference(self.object_reference)

    def to_dict(self, partial_dict=None):
        """Populate an existing dictionary.

        Note that this is different than to_dict() on most other CybOX types.
        """
        if partial_dict is None:
            raise NotImplementedError()

        partial_dict['xsi:type'] = self._XSI_TYPE
        if self.object_reference is not None:
            partial_dict['object_reference'] = self.object_reference

    @staticmethod
    def from_obj(defobj_obj):
        if not defobj_obj:
            return None

        any_attributes = defobj_obj.get_anyAttributes_()
        xsi_type = any_attributes.get('{http://www.w3.org/2001/XMLSchema-instance}type')
        if not xsi_type:
            raise ValueError("Object has no xsi:type")
        type_value = xsi_type.split(':')[1]

        # Find the class that can parse this type.
        klass = cybox.utils.get_class_for_object_type(type_value)
        defobj = klass.from_obj(defobj_obj)
        defobj.object_reference = defobj_obj.get_object_reference()

        return defobj

    @staticmethod
    def from_dict(defobj_dict):
        if not defobj_dict:
            return None

        xsi_type = defobj_dict.get('xsi:type')
        if not xsi_type:
            raise ValueError('dictionary does not have xsi:type key')

        klass = cybox.utils.get_class_for_object_type(xsi_type)
        defobj = klass.from_dict(defobj_dict)

        defobj.object_reference = dict_.get('object_reference')

        return defobj

