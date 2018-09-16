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

from hashlib import sha256


class Feistel:

    def __init__(self, password, rounds=16, block_size=8):
        self.block_size = block_size
        self.rounds = rounds
        self.key_size = self.block_size / 2
        self.keys = self._generate_keys(password)
        self.message = []

    def _generate_keys(self, password):
        n_keys = self.block_size * self.rounds / 2
        keys, current_hash = [], password
        while len(keys) < n_keys:
            current_hash = sha256(str.encode(current_hash)).hexdigest()
            # Iterate new hash using step size 2 to extract hex keys
            for i in range(0, len(current_hash), 2):
                if i != len(current_hash):
                    keys.append(current_hash[i:i+2])
        return keys

    def _convert_message_to_blocks(self, message):
        # Iterate message splitting it into blocks according to block size
        for i in range(0, len(message), self.block_size):
            if i != len(message):
                block = str.encode(message[i:i+self.block_size])
                # Append blocks as L and R
                self.message.append([block[0:self.block_size//2], block[self.block_size//2:]])

    def _key_function(self, key_idx):
        key = bytearray.fromhex(" ".join(self.keys[key_idx:key_idx+(self.block_size//2)]))
        return key

    def _bytes_xor(self, block, key):
        encrypted = []
        for b, k in zip(block, key):
            encrypted.append(bytes([b ^ k]))
        return b''.join(encrypted)

    def _process_block(self, block_idx, key_idx):
        key = self._key_function(key_idx)
        block_l, block_r = self.message[block_idx]
        block_l = self._bytes_xor(block_l, key)
        self.message[block_idx] = [block_r, block_l]

    def _run_round(self, key_idx):
        for block_idx in range(len(self.message)):
            self._process_block(block_idx, key_idx)

    def _reconstruct_message(self):
        message = []
        for m in self.message:
            message.extend([m[0], m[1]])
        return b''.join(message)

    def encrypt(self, message, verbose=False):
        self._convert_message_to_blocks(message)
        key_idx = 0
        for r in range(self.rounds):
            self._run_round(key_idx)
            key_idx += self.block_size//2
            print("Done encryption for round {:2}!".format(r+1))
            if verbose:
                print(self._reconstruct_message())


if __name__ == "__main__":
    pw = "Feistel"
    message = "flapjackhighjackjokinglychipmunk"
    f = Feistel(pw)
    f.encrypt(message, verbose=True)
