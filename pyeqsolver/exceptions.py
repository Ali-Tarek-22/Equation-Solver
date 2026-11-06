class PyEqSolverError(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidFileFormatException(PyEqSolverError):
    """A line breaks the syntax rules above, or the file has no equations
    """
    pass

class DimensionMismatchException(PyEqSolverError):
    """The number of equations does not match the number of variables."""
    pass

class InconsistentSystemException(PyEqSolverError):
    """InconsistentSystemException"""
    pass

class InfiniteSolutionsException(PyEqSolverError):
    """The system has infinitely many solutions"""
    pass