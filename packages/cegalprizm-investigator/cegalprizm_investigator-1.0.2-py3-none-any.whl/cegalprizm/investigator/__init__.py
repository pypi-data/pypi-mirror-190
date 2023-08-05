# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""The cegalprizm.investigator module provides the API to allow Blueback Investigations to be accessed from Python.
"""

__version__ = '1.0.2'
__git_hash__ = 'd87faed9'

import logging
logger = logging.getLogger(__name__)

# pylint: disable=wrong-import-position

from .constants import *
from .connection import InvestigatorConnection
from .decorators import InvestigatorPyFunction1D
from .decorators import InvestigatorPyFunction2D
from .named_tuples import *
from .pickling import *
from .plotting import *
from .statistics import *

from .inv.investigation import Investigation

from .views import *

from .utils_pythontoolpro import *
