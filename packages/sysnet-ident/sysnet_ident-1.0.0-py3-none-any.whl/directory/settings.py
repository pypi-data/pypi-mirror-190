import os

PID_PREFIX = os.environ.get('PID_PREFIX', 'SYS')
PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 40
TOKEN_LENGTH = 16
PASSWORD_USE_LOWER = os.getenv("PASSWORD_USE_LOWER", 'True').lower() in ('true', '1', 't')
PASSWORD_USE_UPPER = os.getenv("PASSWORD_USE_UPPER", 'True').lower() in ('true', '1', 't')
PASSWORD_USE_DIGITS = os.getenv("PASSWORD_USE_DIGITS", 'True').lower() in ('true', '1', 't')
PASSWORD_USE_PUNCTUATION = os.getenv("PASSWORD_USE_PUNCTUATION", 'False').lower() in ('true', '1', 't')
JWT_KEY = os.getenv("JWT_KEY", 'SYSNET_AM')
JWT_ALGORITHM = 'HS256'
JWT_OPTIONS = {
    'verify_signature': True,
    'verify_exp': False,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}
JWT_SUBJECT = os.getenv('JWT_SUBJECT', 'SYSNET Identity Platform')
JWT_ISSUER = os.getenv('JWT_ISSUER', 'urn:cz:sysnet:iam')
JWT_IDENTIFIER = os.getenv('JWT_IDENTIFIER', 'iam@sysnet.cz')
CIPHER = (
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
)
