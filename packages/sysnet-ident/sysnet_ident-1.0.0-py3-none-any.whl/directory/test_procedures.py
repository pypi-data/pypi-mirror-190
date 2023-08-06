import unittest
from unittest import TestCase

from ident.procedures import check_pid, correct_pid, hash_md5, hash_sha1, hash_sha256, hash_sha384, hash_sha512, \
    jwt_encode, jwt_decode, next_uuid
from ident.settings import JWT_ISSUER

PID_TO_CHECK = "HVN12345678Z"
PID_TO_CORRECT = "HVN123456789"

INPUT_STRING = "Testovací textíček"
HASH_MD5 = "f71377e66b24b65aab3161c2cf4b694a"
HASH_SHA1 = "00721fb8a3d8d11d5ff702ff22ad6c0074277a80"
HASH_SHA256 = "97affb930df96dee98e21bcd22550da182ff573508b1e220403c860889c3fd3b"
HASH_SHA384 = "b1dc78e75fed2ddde79061f29be45b4c6800c5061e2017bb07359ea3d6d4bccd67e910a3c9482bf41fd2b7ce46e5a856"
HASH_SHA512 = "e1ab5e5b14a4aeb0466590809c4474a6376eaa364fce5db7ba94e4482ef82739983fdf5f8305b74d3e59228a7b2f60672527a02164d53baa992d69e77e7cae62"


class Test(unittest.TestCase):
    def test_check_pid(self):
        self.assertTrue(check_pid(PID_TO_CHECK))

    def test_correct_pid(self):
        corrected = correct_pid(PID_TO_CORRECT)
        self.assertEqual(corrected, PID_TO_CHECK)

    def test_hash(self):
        self.assertEqual(hash_md5(INPUT_STRING), HASH_MD5)
        self.assertEqual(hash_sha1(INPUT_STRING), HASH_SHA1)
        self.assertEqual(hash_sha256(INPUT_STRING), HASH_SHA256)
        self.assertEqual(hash_sha384(INPUT_STRING), HASH_SHA384)
        self.assertEqual(hash_sha512(INPUT_STRING), HASH_SHA512)

    def test_jwt(self):
        jwt = jwt_encode()
        self.assertFalse(jwt is None)
        decoded = jwt_decode(jwt)
        self.assertFalse(decoded is None)
        self.assertEqual(decoded['iss'], JWT_ISSUER)

    def test_next_uuid(self):
        uuid1 = next_uuid(1)
        self.assertFalse(uuid1 is None)


if __name__ == '__main__':
    unittest.main()


