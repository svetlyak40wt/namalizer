Namalizer — smart method name normalizer
========================================

It allows you to keep PEP8 naming style, using libraries like `Twisted` or `unittest`.

Here is example:

    #!/usr/bin/python
    import unittest
    from namalizer import pep8


    class MyTests(unittest.TestCase):
        def set_up(self):
            self.a = 'blah'

        def test_example(self):
            self.assert_equal(self.a, 'blah')


    pep8(**locals())
    # or
    pep8(MyTests)


    if __name__ == '__main__':
        unittest.main()

Namalizer creates aliases for method with wrong names. In this case,
it will create aliazes in `unittest.TestCase` for methods like `setUp`,
`assertEqual`, etc..

Then, it will see that you created method `set_up` to override base class's
functionality and will create alias `setUp` for this method, this way
when `unittest` will call `setUp`, you version will be called.

Migration
---------

If you use some library with ugly naming method, this regex will help you to
find all places where wrong names are used:

    git grep -e '\(\.\|def \)[a-z]\+[A-Z]'

Credits
-------

* Alexander Artemenko <<svetlyak.40wt@gmail.com>> — original author.

Fork the project, contribute and send me patches.
