__version__ = '0.0.2.dev3'
__prog_name__ = 'dallspoirpoise'
__version_date__ = 'Oct-23-2019'


def ver2tuple(ver):
    if isinstance(ver, tuple):
        return ver
    # ### This is the initialisation of the dallsporpoise package. Please note this was forked from lkilcher's
    # DOLfYN package as below:

    # __version__ = '0.11.2'
    # __prog_name__ = 'DOLfYN'
    # __version_date__ = 'May-27-2019'

    if isinstance(ver, (float, int)):
        return (0, int(ver), int(round(10 * (ver % 1))))
    # ### Now switched to use pkg_version STRING.
    # Switch to pkg_version STRING (pkg_version 0.6)
    # Now 'old versions' become '0.x.y'
    # ver becomes a tuple.
    
    out = []
    for val in ver.split('.'):
        try:
            val = int(val)
        except ValueError:
            pass
        out.append(val)
    return tuple(out)


version_info = ver2tuple(__version__)
