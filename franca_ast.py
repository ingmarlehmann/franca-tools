import sys

class Node(object):
    def __init__(self):
        print ("node constructor")
    
    def children(self):
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.

            buf:
                Open IO buffer into which the Node is printed.

            offset:
                Initial offset (amount of leading spaces)

            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.

            nodenames:
                True if you want to see the actual node names
                within their parents.

            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)

class Attribute(Node):
    def __init__(self, typename, name):
        self.typename = typename
        self.name = name

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.typename is not None: nodelist.append(("typename", self.typename))
        return tuple(nodelist)

    attr_names = ()

class BroadcastMethod(Node):
    def __init__(self, name, comment, out_args, is_selective=False):
        self.name = name
        self.comment = comment
        self.out_args = out_args
        self.is_selective = is_selective

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.comment is not None: nodelist.append(("comment", self.comment))
        if self.out_args is not None: nodelist.append(("out_args", self.out_args))
        return tuple(nodelist)

    attr_names = ('is_selective',)

class Constant(Node):
    def __init__(self, comment):
        self.value = value

    def children(self):
        return tuple()

    attr_names = ('value',)

class Enum(Node):
    def __init__(self, name, values, comment=None):
        self.name = name
        self.values = values
        self.comment = comment
    
    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.values is not None: nodelist.append(("values", self.values))
        if self.comment is not None: nodelist.append(("comment", self.comment))
        return tuple(nodelist)

    attr_names = ()

class Enumerator(Node):
    def __init__(self, name, value=None, comment=None):
        self.name = name
        self.value = value
        self.comment = comment

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.value is not None: nodelist.append(("value", self.value))
        if self.comment is not None: nodelist.append(("comment", self.comment))
        return tuple(nodelist)

    attr_names = ()

class EnumeratorList(Node):
    def __init__(self, enumerators):
        self.enumerators = enumerators

    def children(self):
        nodelist = []
        for i, child in enumerate(self.enumerators or []):
            nodelist.append(("enumerators[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class FrancaComment(Node):
    def __init__(self, comment):
        self.comment = comment

    def children(self):
        return tuple()

    attr_names = ('comment',)

class ID(Node):
    def __init__(self, id):
        self.id = id

    def children(self):
        return tuple()

    attr_names = ('id',)

class IntegerConstant(Node):
    def __init__(self, value):
        self.value = value

    def children(self):
        return tuple()

    attr_names = ('value',)

class ImportIdentifier(Node):
    def __init__(self, import_identifier):
        self.import_identifier = import_identifier

    def children(self):
        return tuple()

    attr_names = ('import_identifier',)

class Method(Node):
    def __init__(self, name, comment, body, is_fire_and_forget=False):
        self.name = name
        self.comment = comment
        self.body = body
        self.is_fire_and_forget = is_fire_and_forget

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.comment is not None: nodelist.append(("comment", self.comment))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ('is_fire_and_forget',)

class MethodBody(Node):
    def __init__(self, in_args, out_args):
        self.in_args = in_args
        self.out_args = out_args

    def children(self):
        nodelist = []
        if self.in_args is not None: nodelist.append(("in_args", self.in_args))
        if self.out_args is not None: nodelist.append(("out_args", self.out_args))
        return tuple(nodelist)
    
    attr_names = ()

class MethodArgument(Node):
    def __init__(self, type, name, comment=None):
        self.type = type
        self.name = name
        self.comment = comment

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        if self.name is not None: nodelist.append(("name", self.name))
        if self.comment is not None: nodelist.append(("comment", self.comment))
        return tuple(nodelist)
    
    attr_names = ()

class MethodArgumentList(Node):
    def __init__(self, args):
        self.args = args

    def children(self):
        nodelist = []
        for i, child in enumerate(self.args or []):
            nodelist.append(("args[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class MethodOutArguments(Node):
    def __init__(self, args):
        self.args = args
    
    def children(self):
        nodelist = []
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)

    attr_names = ()

class MethodInArguments(Node):
    def __init__(self, args):
        self.args = args
    
    def children(self):
        nodelist = []
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)

    attr_names = ()

class PackageStatement(Node):
    def __init__(self, package_identifier):
        self.package_identifier = package_identifier

    def children(self):
        nodelist = []
        if self.package_identifier is not None: nodelist.append(("package_identifier", self.package_identifier))
        return tuple(nodelist)

    attr_names = ('package_identifier',)

class PackageIdentifier(Node):
    def __init__(self, package_identifier):
        self.package_identifier = package_identifier

    def children(self):
        return tuple()

    attr_names = ('package_identifier',)

class Typename(Node):
    def __init__(self, typename):
        self.typename = typename

    def children(self):
        return tuple()

    attr_names = ('typename',)

class Version(Node):
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def children(self):
        nodelist = []
        if self.major is not None: nodelist.append(("major", self.major))
        if self.minor is not None: nodelist.append(("minor", self.minor))
        return tuple(nodelist)

    attr_names = ()

