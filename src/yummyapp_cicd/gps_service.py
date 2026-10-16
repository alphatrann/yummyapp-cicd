class GPSSignalLostError(Exception):
    """Exception raised when GPS signal is lost."""


def get_current_location():
    """
    Simulate accessing the phone's GPS hardware.
    Automated tests can mock this function.
    """
    return (10.0, 105.0)
