# pylint: disable=W0622
"""cubicweb-vtimeline application packaging information"""

modname = "vtimeline"
distname = "cubicweb-vtimeline"

numversion = (0, 9, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "VeriteCo / TimelineJS cube"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname

__depends__ = {"cubicweb": ">= 3.38.0, < 3.39.0"}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
