import re
#import logbook
from inspect import isroutine, getmro
from itertools import chain

import unittest

_CAMEL_RE = re.compile(r'(?<=[a-z])([A-Z])')

def _normalize(name):
    return _CAMEL_RE.sub(lambda x: '_' + x.group(1).lower(), name).lower()


def _defined_in(obj, name, value):
    if hasattr(obj, '__bases__'):
        mro = getmro(obj)
        if len(mro) > 1:
            return getattr(mro[1], name, None) != value
    return True


def pep8(*args, **kwargs):
    def objects():
        for obj in chain(args, kwargs.values()):
            if hasattr(obj, '__bases__'):
                try:
                    for parent in reversed(getmro(obj)):
                        yield parent
                except:
                    import pdb;pdb.set_trace()
            else:
                if hasattr(obj, '__class__'):
                    yield obj.__class__

    for obj in objects():
        try:
            for name in dir(obj):
                if not name.startswith('_'):
                    value = getattr(obj, name)
                    if isroutine(value):
                        norm_name = _normalize(name)

                        if norm_name != name:
                            try:
                                norm_value = getattr(obj, norm_name, None)

                                if norm_value is None or not _defined_in(obj, norm_name, norm_value):
                                    # no method with normalized name
                                    #logbook.Logger('pep8').info(
                                    #    'writing from %s(%s) to %s(%s) for %r' % (name, hash(value), norm_name, hash(norm_value), obj)
                                    #)
                                    setattr(obj, norm_name, value)
                                else:
                                    # set new value back because, probably it is
                                    # overridden method
                                    if norm_value != value:
                                        #logbook.Logger('pep8').info(
                                        #    'writing back from %s(%s) to %s(%s) for %r' % (
                                        #        norm_name, hash(norm_value),
                                        #        name, hash(value),
                                        #        obj
                                        #    )
                                        #)
                                        setattr(obj, name, norm_value)
                            except TypeError:
                                pass
        except:
            import pdb;pdb.set_trace()
            raise

    #return cls

class TestCase(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual('ugly_method', _normalize('uglyMethod'))
        self.assertEqual('another_ugly_method', _normalize('AnotherUglyMethod'))
        self.assertEqual('listen_tcp', _normalize('listenTCP'))

    def test_inheritance1(self):
        class A:
            def badMethod(self):
                return 'A'
        class B(A): pass
        pep8(B)
        self.assertEqual('A', B().bad_method())

    def test_inheritance2(self):
        class A(object):
            def badMethod(self):
                return 'A'
        class B(A):
            def badMethod(self):
                return 'B'

        pep8(B)
        self.assertEqual('A', A().badMethod())
        self.assertEqual('A', A().bad_method())

        self.assertEqual('B', B().badMethod())
        self.assertEqual('B', B().bad_method())

    def test_inheritance3(self):
        class A(object):
            def badMethod(self):
                return 'A'
        class B(A):
            def bad_method(self):
                return 'B'

        pep8(B)
        self.assertEqual('A', A().badMethod())
        self.assertEqual('A', A().bad_method())

        self.assertEqual('B', B().badMethod())
        self.assertEqual('B', B().bad_method())

    def test_inheritance4(self):
        class A(object):
            def badMethod(self):
                return 'A'

        class B(A):
            def badMethod(self):
                return 'B'

        b = B()
        pep8(A, b)

        self.assertEqual('B', b.badMethod())
        self.assertEqual('B', b.bad_method())

    def test_on_object(self):
        class A(object):
            def badMethod(self):
                return 'A'

        a = A()
        pep8(A)

        self.assertEqual('A', a.badMethod())
        self.assertEqual('A', a.bad_method())

    def test_class_and_function(self):
        class FakeModule:
            class Random:
                pass
            def random():
                pass
        pep8(FakeModule)
        self.assert_(FakeModule.Random != FakeModule.random)

    def test_defined_in(self):
        class A:
            def foo(self): return 'A.foo'
            def bar(self): return 'A.bar'

        class B(A):
            def foo(self): return 'B.foo'
            def blah(self): return 'B.blah'

        self.assertEqual(True, _defined_in(A, 'foo', A.foo))
        self.assertEqual(True, _defined_in(A, 'bar', A.bar))

        self.assertEqual(True, _defined_in(B, 'foo', B.foo))
        self.assertEqual(False, _defined_in(B, 'bar', B.bar))
        self.assertEqual(True, _defined_in(B, 'blah', B.blah))


if __name__ == '__main__':
    unittest.main()

