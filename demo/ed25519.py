"""Ed25519 signatures (RFC 8032, section 5.1) in pure Python, standard library only, so the board server and the
client script `board_id.py` need no extra package. Slow (a few milliseconds per operation) but enough for a board.
Not constant-time: fine for verifying, and for signing a few posts on one's own machine.

    seed = os.urandom(32); pub = public_key(seed); sig = sign(seed, msg); verify(pub, msg, sig) -> bool
"""
import hashlib

P = 2**255 - 19
L = 2**252 + 27742317777372353535851937790883648493
D = -121665 * pow(121666, P - 2, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)


def _sha512(data):
    return hashlib.sha512(data).digest()


def _add(a, b):
    x1, y1, z1, t1 = a
    x2, y2, z2, t2 = b
    A = (y1 - x1) * (y2 - x2) % P
    B = (y1 + x1) * (y2 + x2) % P
    C = 2 * t1 * t2 * D % P
    Dd = 2 * z1 * z2 % P
    E, F, G, H = B - A, Dd - C, Dd + C, B + A
    return E * F % P, G * H % P, F * G % P, E * H % P


def _mul(s, point):
    q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            q = _add(q, point)
        point = _add(point, point)
        s >>= 1
    return q


def _equal(a, b):
    x1, y1, z1, _ = a
    x2, y2, z2, _ = b
    return (x1 * z2 - x2 * z1) % P == 0 and (y1 * z2 - y2 * z1) % P == 0


def _recover_x(y, sign):
    if y >= P:
        return None
    x2 = (y * y - 1) * pow(D * y * y + 1, P - 2, P)
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P != 0:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P != 0:
        return None
    if (x & 1) != sign:
        x = P - x
    return x


_GY = 4 * pow(5, P - 2, P) % P
_GX = _recover_x(_GY, 0)
G = (_GX, _GY, 1, _GX * _GY % P)


def _compress(point):
    x, y, z, _ = point
    zinv = pow(z, P - 2, P)
    x, y = x * zinv % P, y * zinv % P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _decompress(data):
    if len(data) != 32:
        return None
    y = int.from_bytes(data, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return x, y, 1, x * y % P


def _expand(seed):
    if len(seed) != 32:
        raise ValueError("an Ed25519 private key (seed) is 32 bytes")
    h = _sha512(seed)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def public_key(seed):
    """The 32-byte public key of a 32-byte seed."""
    return _compress(_mul(_expand(seed)[0], G))


def sign(seed, message):
    """The 64-byte signature of `message` (bytes) with the 32-byte seed."""
    a, prefix = _expand(seed)
    pub = _compress(_mul(a, G))
    r = int.from_bytes(_sha512(prefix + message), "little") % L
    R = _compress(_mul(r, G))
    k = int.from_bytes(_sha512(R + pub + message), "little") % L
    return R + int.to_bytes((r + k * a) % L, 32, "little")


def verify(public, message, signature):
    """True if `signature` is a valid signature of `message` by `public`; False for anything else, malformed input
    included."""
    try:
        public, message, signature = bytes(public), bytes(message), bytes(signature)
    except (TypeError, ValueError):
        return False
    if len(public) != 32 or len(signature) != 64:
        return False
    A = _decompress(public)
    R = _decompress(signature[:32])
    if A is None or R is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= L:
        return False
    k = int.from_bytes(_sha512(signature[:32] + public + message), "little") % L
    return _equal(_mul(s, G), _add(R, _mul(k, A)))
