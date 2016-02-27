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

class Method(Node):
    def __init__(self, name, comment, body):
        self.name = name
        self.comment = comment
        self.body = body

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.comment is not None: nodelist.append(("comment", self.comment))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ('name', 'comment', 'body',)

class MethodBody(Node):
    def __init__(self, in_args, out_args):
        self.in_args = in_args
        self.out_args = out_args

    def children(self):
        nodelist = []
        if self.in_args is not None: nodelist.append(("in_args", self.in_args))
        if self.out_args is not None: nodelist.append(("out_args", self.out_args))
        return tuple(nodelist)
    
    attr_names = ('in_args','out_args',)

class MethodArgument(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)
    
    attr_names = ('type', 'name',)

class MethodArgumentList(Node):
    def __init__(self, args):
        self.args = args

    def children(self):
        nodelist = []
        for i, child in enumerate(self.args or []):
            nodelist.append(("args[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ('args',)

class MethodOutArguments(Node):
    def __init__(self, args):
        self.args = args
    
    def children(self):
        nodelist = []
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)

    attr_names = ('args',)

class MethodInArguments(Node):
    def __init__(self, args):
        self.args = args
    
    def children(self):
        nodelist = []
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)

    attr_names = ('args',)

class Typename(Node):
    def __init__(self, typename):
        self.typename = typename

    def children(self):
        return tuple()

    attr_names = ('typename',)
