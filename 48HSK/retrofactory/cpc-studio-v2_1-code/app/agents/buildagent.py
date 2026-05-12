"""Compatibility shim for legacy buildagent imports."""

from .build_agent import *  # noqa: F401,F403
from .build_agent import CPCTELERA_HOME as CPCTELERAHOME
from .build_agent import CPCT_MKPROJECT as CPCTMKPROJECT
from .build_agent import sanitize_project_name as sanitizeprojectname
