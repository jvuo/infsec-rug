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

MESSAGE = """govmywodydromyebcoklyedsxpybwkdsyxcomebsdidrscmyebcoscklyedcomebsxqsxpybwkdsyxsxdrscmyxdohdgodrsxupybohkwzvoklyedrygdyzbofoxddroexkedrybsjonboknsxqypsxpybwkdsyxybklyedrygdyzbofoxddroexkedrybsjonwynspsmkdsyxypsxpybwkdsyxwkxioxmbizdsyxwodryncohscdcywokvboknidryeckxnciokbcyvnsxsdskvvigovvpymecyxcswzvowodryncdyoxmbizdsxpybwkdsyxpyvvygsxqdrscgovvecomrkbkmdobscdsmfkveocsnoxdspisxqsxpybwkdsyxwkusxqsdnsppsmevddywynspisxpybwkdsyxexxydspsonvkdobsxdrscmyebcogovvsxdbynemozobcyxkvoxmbizdsyxkxngovvcdenidyzsmcvsuoleppobyfobpvygohzvysdckxncmbycccsdocmbszdsxqsryzoiyevvoxtyidrscmyebcoklyedsxpybwkdsyxcomebsdi"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def decrypt_message(message, key):
    decrypt = lambda c: ALPHABET[(ord(c) - key) % 26]
    return "".join([decrypt(c) for c in message])


def encrypt_message(message, key):
    encrypt = lambda c: ALPHABET[(ord(c) + key) % 26]
    return "".join([encrypt(c) for c in message])

if __name__ == "__main__":
    for key in range(0, 26):
        message = encrypt_message(MESSAGE, key)
        print(message, key)
