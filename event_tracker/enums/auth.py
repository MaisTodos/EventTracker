from enum import Enum


class AuthStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    TOKEN_EXPIRED = "token_expired"
