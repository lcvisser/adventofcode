def extended_gcd(a, b):
    """ Extended Euclidean algorithm

    Returns q, s, t such that q = gcd(a, b) and s and t are such that as + bt = gcd(a, b)
    """
    rp, rc = a, b
    sp, sc = 1, 0
    tp, tc = 0, 1
    while rc:
        rp, rc, q = rc, rp % rc, rp // rc
        sp, sc = sc, sp - q * sc
        tp, tc = tc, tp - q * tc

    return rp, sp, tp


def crt(a1, m1, a2, m2):
    """ Chinese Remainder Theorem

    Solves for x:
     x = a1 mod m1
     x = a2 mod m2
    """
    g, n1, n2 = extended_gcd(m1, m2)
    assert g == 1
    assert m1 * n1 + m2 * n2 == 1
    return a2 * m1 * n1 + a1 * m2 * n2
