#!/usr/bin/env python3
"""
    Copyright (C) 2018  J. Vuopionpera [jvuopionpera@gmail.com]

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FREQS = {"a": 8.167, "b": 1.492, "c": 2.782, "d": 4.253,
         "e": 12.702, "f": 2.228, "g": 2.015, "h": 6.094,
         "i": 6.966, "j": 0.153, "k": 0.772, "l": 4.025,
         "m": 2.406, "n": 6.749, "o": 7.507, "p": 1.929,
         "q": 0.095, "r": 5.987, "s": 6.327, "t": 9.056,
         "u": 2.758, "v": 0.978, "w": 2.360, "x": 0.150,
         "y": 1.974, "z": 0.074}


def calculate_occurences(txt, depth=50):
    distribution = []
    # Iterate the rows until depth is reached
    for i in range(1, depth):
        counter = 0
        # Loop two version of the same string
        for j in range(i, len(txt)-i):
            # Original string moved one to the right
            if txt[j] == txt[j-i]:
                counter += 1
        distribution.append(counter)
    return distribution


def decrypt(txt, key):
    decrypted, key_index = [], 0
    for i in range(len(txt)):
        if key_index > len(key) - 1:
            key_index = 0
        decrypted.append(ALPHABET[ord(txt[i]) - 97 - key[key_index]])
        key_index += 1
    return "".join(decrypted)


def multiply_frequencies(freqs):
    shift_index, f = 0, 0
    for i in range(0, 26):
        m = []
        for j in range(0, 26):
            shift_i = j + i
            if shift_i > 25:
                shift_i -= 26
            x = FREQS[ALPHABET[j]] * freqs[shift_i]
            m.append(x)
        f_ = sum(m)
        if f_ > f:
            f = f_
            shift_index = i
    #print(shift_index, f)
    return shift_index


def get_key_shifts(txt, size):
    key = []
    for i in range(size):
        freqs = get_letter_frequencies(txt, 9, offset=i)
        shift_number = multiply_frequencies(freqs)
        key.append(shift_number)
    return key


def get_letter_frequencies(txt, size, offset = 0):
    distribution = []
    for i in range(0, len(txt), size):
        try:
            distribution.append(txt[i + offset])
        except IndexError:
            pass
    # Calculate frequencies
    freq = [distribution.count(a)*100/len(distribution) for a in ALPHABET]
    return freq


def calculate_std_devs(freq):
    std = math.sqrt(sum([f**2 for f in freq]) / 26 - math.sqrt(sum(freq) / 26))
    return std


def try_key_sizes(lower_limit, upper_limit):
    for k in range(lower_limit, upper_limit+1):
        freqs = get_letter_frequencies(txt, k)
        std = calculate_std_devs(freqs)
        print("Sum of {:2} std. devs.: {:2.1f}".format(k, std))


def get_text(path):
    with open(path, "r") as fh:
        txt = fh.readlines()
        return "".join([line.strip() for line in txt])


if __name__ == "__main__":
    txt = get_text("schneier.encrypted.txt")
    key = get_key_shifts(txt, 9)
    decrypted = decrypt(txt, key)
    print(decrypted)
