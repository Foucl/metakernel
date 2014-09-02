from jupyter_kernel import Magic, option
from jupyter_kernel.tests.utils import get_kernel, get_log_text


class Dummy(Magic):

        @option(
        '-s', '--size', action='store',
        help='Pixel size of plots, "width,height"'
         )
        def line_dummy(self, foo, size=None):
            """%dummy [options] foo - Perform dummy operation on foo"""
            self.foo = foo
            self.size = size

        def cell_spam(self):
            """%spam - Cook some spam"""
            pass

        def line_eggs(self, style):
            """%eggs STYLE - cook some eggs in the given style"""
            pass


def test_get_magics():
    kernel = get_kernel()
    d = Dummy(kernel)
    line = d.get_magics('line')
    cell = d.get_magics('cell')

    assert 'dummy' in line
    assert 'spam' in cell
    assert 'eggs' in line


def test_get_help():
    kernel = get_kernel()
    d = Dummy(kernel)

    dummy_help = d.get_help('line', 'dummy', 0)
    assert dummy_help == d.line_dummy.__doc__.lstrip().split("\n", 1)[0]

    dummy_help = d.get_help('line', 'dummy', 1)
    assert dummy_help == d.line_dummy.__doc__.lstrip()

    spam_help = d.get_help('cell', 'spam', 0)
    assert spam_help == d.cell_spam.__doc__.lstrip().split("\n", 1)[0]

    spam_help = d.get_help('cell', 'spam', 1)
    assert spam_help == d.cell_spam.__doc__.lstrip()


def test_option():
    kernel = get_kernel()
    d = Dummy(kernel)
    assert 'Options:' in d.line_dummy.__doc__
    assert '--size' in d.line_dummy.__doc__

    ret = d.call_magic('line', 'dummy', '', 'hey -s400,200')
    assert ret == d
    assert d.foo == 'hey'
    assert d.size == '400,200'