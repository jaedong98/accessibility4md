class ElememntVisitor(object):
    """
    A visitor class for ElementTree objects. Subclasses can define methods for
    specific elements to customize their behavior.
    """

    def visit(self, element):
        """
        Visit the specified element, calling the appropriate visit method for
        the element type.

        :param element: The element to visit.
        :return: The result of the visit method.
        """
        methodname = 'visit_' + element.tag
        method = getattr(self, methodname, self.generic_visit)
        return method(element)

    def generic_visit(self, element):
        """
        Visit the specified element and its children, visiting child elements
        recursively.

        :param element: The element to visit.
        """
        for child in element:
            self.visit(child)
        return