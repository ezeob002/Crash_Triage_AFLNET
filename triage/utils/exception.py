import attr

@attr.s
class FMIFailure(Exception):

    message = attr.ib(type=str, default="")
    pass

class FMIError(Exception):
    pass


class FMIRestartFailedError(FMIError):
    pass


class FMITargetConnectionFailedError(FMIError):
    pass

class FMIOutOfAvailableSockets(FMIError):
    pass

class FMIPaused(FMIError):
    pass


class FMITestCaseAborted(FMIError):
    pass


class FMITargetConnectionReset(FMIError):
    pass


class FMITargetRecvTimeout(FMIError):
    pass


@attr.s
class FMITargetConnectionAborted(FMIError):
    """
    Raised on `errno.ECONNABORTED`.
    """
    socket_errno = attr.ib()
    socket_errmsg = attr.ib()


class FMIRpcError(FMIError):
    pass


class FMIRuntimeError(Exception):
    pass


class SizerNotUtilizedError(Exception):
    pass


class MustImplementException(Exception):
    pass

class FMINonDeterministicError(FMIError):
    def __init__(self):
        self.message = "Non-deterministic behavior detected"

class FMITableError(FMIError):
    def __init__(self):
        self.message = "Observation Table needs to be updated"

class FMIRepeatedNonDeterministicError(FMIError):
    def __init__(self):
        self.message = "Repeated non-deterministic error detected"
