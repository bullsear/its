class ItsException( Exception ):
    pass

class ItsUsageException( Exception ):
    pass

class ItsSpecException( Exception ):
    pass

class ItsReservationRetryException( Exception ):
    pass

class ItsServerSpecNotFoundException( Exception ):
    pass

class ItsAssertionException( Exception ):
    pass

class ItsSuiteAssertion( Exception ):
    pass

class ItsReservationUsageException ( Exception ):
    pass

class ItsTestbedNotFree( Exception ):
    pass

class ItsServerSshConnectionException ( Exception ):
    pass

class ItsEmptyCLITableException ( Exception ):
    pass
