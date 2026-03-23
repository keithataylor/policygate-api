"""
Exceptions for PolicyGate.
"""

class PolicySemanticError(ValueError):
    pass


class DuplicateRuleIdError(PolicySemanticError):
    pass


class InvalidPriorityError(PolicySemanticError):
    pass


class InvalidRationaleCodesError(PolicySemanticError):
    pass


class ConflictingEqualPriorityOverlapError(PolicySemanticError):
    pass


class RedundantEqualPriorityOverlapError(PolicySemanticError):
    pass