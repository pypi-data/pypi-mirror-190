class METSLibError(Exception):
    """Base class for other exceptions"""
    pass


class ParseError(METSLibError):
    """Raised when xml file could not be parsed into library objects"""
    pass


class METSVerificationError(METSLibError):
    """Raised when library objects do not contain all information required by METS standard"""
    pass
