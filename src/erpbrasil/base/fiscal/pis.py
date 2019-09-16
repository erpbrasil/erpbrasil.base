# coding=utf-8
# Copyright (C) 2013  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def validar(pis_pasep):
    digits = []
    for c in pis_pasep:
        if c == '.' or c == ' ' or c == '\t':
            continue
        if c == '-':
            if len(digits) != 10:
                return False
            continue
        if c.isdigit():
            digits.append(int(c))
            continue
        return False
    if len(digits) != 11:
        return False
    height = [int(x) for x in "3298765432"]
    total = 0
    for i in range(10):
        total += digits[i] * height[i]
    rest = total % 11
    if rest != 0:
        rest = 11 - rest
    if rest == digits[10]:
        return True
    return False
