import base64
import hashlib
import secrets
import string
import uuid
from datetime import datetime, timezone
from random import randint

import deprecation
import jwt
import shortuuid

from ident.settings import PID_PREFIX, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, TOKEN_LENGTH, PASSWORD_USE_LOWER, \
    PASSWORD_USE_UPPER, PASSWORD_USE_DIGITS, PASSWORD_USE_PUNCTUATION, JWT_KEY, JWT_ALGORITHM, JWT_OPTIONS, JWT_ISSUER, \
    JWT_IDENTIFIER, CIPHER


def check_pid(pid: str):
    """
    Kontroluje spravnost PID
    :param pid:     Dvanáctímíský kód PID ke kontrole
    :return:        True/False
    """
    if pid is None:
        return False
    if len(pid) == 12:
        w = pid.upper()
        c1 = w[-1]
        w = w[0:11]
        c2 = code39_mod_36(w, return_type=2)
        if c1 == c2:
            return True
    return False


def correct_pid(pid: str):
    """
    Zkontroluje a opravi PID.
    :param pid:     dvanactimistny PID
    :return:        dvanactimistny PID s opravenym poslednim znakem
    """
    out = pid.upper()
    if not check_pid(pid=pid.upper()):
        if len(out) == 12:
            out = out[0:11]
        if len(out) == 11:
            out = code39_mod_36(data_to_encode=out, return_type=1)
    return out


def generate_short_uuid():
    """
    Vygeneruje dvanactimistne UUID s poslednim kontrolnim znakem
    :return:    dvanactimistny náhodný UUID s kontrolnim poslednim znakem
    """
    alphabet = string.digits + string.ascii_uppercase
    shortuuid.set_alphabet(alphabet)
    out = shortuuid.random(length=12)
    return correct_pid(out)


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def generate_uuid4():
    return uuid.uuid4()


def generate_uuid1():
    return uuid.uuid1()


def generate_uuid4_string():
    return str(uuid.uuid4())


def generate_uuid1_string():
    return str(uuid.uuid1())


def next_uuid(uuid_type=1):
    if uuid_type == 1:
        out = uuid.uuid1()
    else:
        out = uuid.uuid4()
    return out


def generate_token(length=TOKEN_LENGTH):
    return secrets.token_urlsafe(length)


def next_token(length=TOKEN_LENGTH):
    return generate_token(length=length)


def next_api_key(name='X-API-KEY', length=16):
    """
    Vytvoří nový API Key

    :param name:
    :param length:
    :return:
    """
    out = {generate_api_key(length=length): name}
    return out


def generate_api_key(length: int):
    return secrets.token_urlsafe(length)


def generate_pid():
    """
    Vygeneruje PID s implicitnim trimistnym prefixem
    :return:
    """
    return generate_id12()


def next_pid(prefix=PID_PREFIX):
    """
    Vytvoří nový PID

    :param prefix:
    :return:
    """
    return generate_id12(three_char_prefix=prefix)


@deprecation.deprecated(details="Use the sha256 function instead")
def hash_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


@deprecation.deprecated(details="Use the sha256 function instead")
def hash_sha1(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def hash_sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def hash_sha224(text):
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def hash_sha384(text):
    return hashlib.sha384(text.encode('utf-8')).hexdigest()


def hash_sha512(text):
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


@deprecation.deprecated(details="Use the hash_files_sha256 function instead")
def hash_files_md5(file_name_list):
    """
    Vyrobí kontrolní součet pro seznam souborů

    :param file_name_list:  Seznam cest k souborům
    :return: hash
    """
    out = [
        (fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.md5())) for fname in file_name_list
    ]
    return out


@deprecation.deprecated(details="Use the hash_files_sha256 function instead")
def hash_files_sha1(file_name_list):
    """
    Vyrobí kontrolní součet pro seznam souborů

    :param file_name_list:  Seznam cest k souborům
    :return: hash
    """
    out = [
        (fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha1())) for fname in file_name_list
    ]
    return out


def hash_files_sha256(file_name_list):
    """
    Vyrobí kontrolní součet pro seznam souborů

    :param file_name_list:  Seznam cest k souborům
    :return: hash
    """
    out = [
        (fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha256())) for fname in file_name_list
    ]
    return out


def hash_files_sha384(file_name_list):
    """
    Vyrobí kontrolní součet pro seznam souborů

    :param file_name_list:  Seznam cest k souborům
    :return: hash
    """
    out = [
        (fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha384())) for fname in file_name_list
    ]
    return out


def hash_files_sha512(file_name_list):
    """
    Vyrobí kontrolní součet pro seznam souborů

    :param file_name_list:  Seznam cest k souborům
    :return: hash
    """
    out = [
        (fname, hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha512())) for fname in file_name_list
    ]
    return out


def generate_id12(three_char_prefix=PID_PREFIX):
    """
    Vygeneruje dvanáctimístný identifikátor typu PID

    :param three_char_prefix:
    :return:
    """
    alphabet = string.digits + string.ascii_uppercase
    shortuuid.set_alphabet(alphabet)
    out = three_char_prefix.upper() + shortuuid.random(length=9)
    return correct_pid(out)


def double_to_mod_36(double_num):
    a = double_num
    s = ''
    while a > 0:
        r = round(a - int(a / 36) * 36)
        a = int(a / 36)
        s = CIPHER[int(r)] + s
    return s


def generate_password(
        use_lower=PASSWORD_USE_LOWER,
        use_upper=PASSWORD_USE_UPPER,
        use_digits=PASSWORD_USE_DIGITS,
        use_punctuation=PASSWORD_USE_PUNCTUATION,
        length=0):
    alphabet = ''
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_punctuation:
        alphabet += string.punctuation

    if length == 0:
        length = randint(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)
    elif length < PASSWORD_MIN_LENGTH:
        length = PASSWORD_MIN_LENGTH
    elif length > PASSWORD_MAX_LENGTH:
        length = PASSWORD_MAX_LENGTH
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def code39_mod_36(data_to_encode: str, return_type=1):
    """
    Zpracuje vstupni data do kodu 3z9 na zaklade parametru return_type
    :param data_to_encode: Vstupni data. Oriznou se vsechny znaky krome cislic a pismen.
    :param return_type: 0 - vystup je formatovan pro tisk carovym fontem
                        1 - vystup je formatovan pro ulozeni hodnoty
                        2 - vytupem je pouze kontrolni cislice (posledni znak kodu)
    :return:            viz returnType
    """
    if (return_type != 0) and (return_type != 1) and (return_type != 2):
        return_type = 0
    data_to_encode = data_to_encode.upper()
    data_to_print = ""
    only_correct_data = ""
    current_value = 0

    # Only pass correct data
    for c in data_to_encode:  # Get each character one at a time
        cnum = ord(c)
        # Get the value of c according to MOD36
        if ((cnum < 58) and (cnum > 47)) or ((cnum < 91) and (cnum > 64)):
            only_correct_data += c
    data_to_encode = only_correct_data
    weighted_total = 0
    for c in data_to_encode:
        cnum = ord(c)
        # Get the value of c according to MOD36
        if (cnum < 58) and (cnum > 47):
            current_value = cnum - 48  # 0 - 9
        if (cnum < 91) and (cnum > 64):
            current_value = cnum - 55  # A - Z
        data_to_print += chr(cnum)  # Gather data to print
        weighted_total += current_value  # Add the values together

    # Divide the weighted_total by 36 and get the remainder, this is the check_digit
    check_digit_value = weighted_total % 36

    # Assign values to characters
    check_digit = check_digit_value
    if check_digit_value < 10:
        check_digit += 48
    if (check_digit_value < 36) and (check_digit_value > 9):
        check_digit += 55
    out = ''
    if return_type == 0:  # ReturnType 0 returns data formatted to the barcode font
        out = '!' + data_to_print + chr(check_digit) + '! '
    elif return_type == 1:  # ReturnType 1 returns data formatted for human-readable text
        out = data_to_print + chr(check_digit)
    elif return_type == 2:  # ReturnType 2 returns the  check digit for the data supplied
        out = chr(check_digit)
    return out


def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest() if ashexstr else hasher.digest()


def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def jwt_decode(jwt_token, options=None):
    key = base64.b64decode(JWT_KEY)
    algorithms = [JWT_ALGORITHM]
    if options is None:
        options = JWT_OPTIONS
    return jwt.decode(jwt_token, key=key, algorithms=algorithms, options=options)


def jwt_encode(identifier=JWT_IDENTIFIER, ttl_sec=3600):
    date_now = datetime.now(tz=timezone.utc)
    timestamp_now = int(date_now.timestamp())
    timestamp_exp = timestamp_now + ttl_sec
    jwt_data = {
        'jti': identifier,
        'iat': timestamp_now,
        'sub': generate_uuid4_string(),
        'iss': JWT_ISSUER,
        'exp': timestamp_exp,
    }
    key = base64.b64decode(JWT_KEY)
    out = jwt.encode(payload=jwt_data, key=key, algorithm=JWT_ALGORITHM)
    return out


def is_identifier_uuid(identifier):
    if identifier is None:
        return False
    if is_valid_uuid(uuid_to_test=identifier, version=4):
        return True
    if is_valid_uuid(uuid_to_test=identifier, version=1):
        return True
    return False


def is_identifier_pid(identifier):
    if identifier is None:
        return False
    if len(identifier) == 12:
        return True
    return False


def is_identifier_unid(identifier):
    if identifier is None:
        return False
    if len(identifier) == 32:
        if all(c in string.hexdigits for c in identifier):
            return True
    return False
