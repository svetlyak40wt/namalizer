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

Migration
---------

If you use some library with wierd naming method, this regex will help you to
find all places where wrong names are used:

    git grep -e '\(\.\|def \)[a-z]\+[A-Z]'

Credits
-------

* Alexander Artemenko <<svetlyak.40wt@gmail.com>> — original author.

Fork the project, contribute and send me patches.
