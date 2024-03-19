"""Exceptions."""

class NotPrimeError(Exception):
    """Raised when we expect the input value to be prime."""

    def __init__(self, z: int):
        self.z = z

    def __str__(self) -> str:
        return f"Integer: {self.z} is not prime."