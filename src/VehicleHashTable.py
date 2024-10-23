"""
VehicleHashTable.py
DSA [COMP1002] Assignment
Author: Jai Dutta
Student ID: 22073372
This file contains the VehicleHashTable class, which is used to store vehicles in a hash table,
as well as the HashEntry class, which is used to store the vehicles in the hash table.
"""

import numpy as np


class HashEntry:
    def __init__(self, key="", value=None):
        self.key = key
        self.value = value
        self.state = 0 if key == "" else 1

    # Getters
    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_state(self):
        return self.state

    def set_as_removed(self):
        self.state = -1


class VehicleHashTable:
    def __init__(self, size):
        init_size = self._find_next_prime(size)
        self.hash_array = np.empty(init_size, dtype=HashEntry)
        self.count = 0

        for i in range(self.hash_array.size):
            self.hash_array[i] = HashEntry()

    def __str__(self):
        output = ""
        for i in self.hash_array:
            if i.get_state() == 1:
                output += (f"{i.get_value()}\n")
        return output

    def put(self, key, value):
        # Prevent size change infinite loop
        self.size_up_check()

        hash_index = self._hash(key)
        original_index = hash_index

        inserted = False
        give_up = False

        while not inserted and not give_up:
            if self.hash_array[hash_index].get_key() == key:
                raise DuplicateVehicleFound(f"Could not insert vehicle ID: [{key}]. Duplicate ID found.")
            elif self.hash_array[hash_index].get_state() == 0:
                self.hash_array[hash_index] = HashEntry(key, value)
                self.count += 1
                inserted = True
            else:
                hash_index = (hash_index + 1) % self.hash_array.size
                if self.hash_array[hash_index].get_state() != 1:
                    self.hash_array[hash_index] = HashEntry(key, value)
                    self.count += 1
                    inserted = True
                if hash_index == original_index:
                    give_up = True
        if not inserted:
            print(f"Could not insert {key}:{value}")
        else:
            pass
            # print(f"Successfully inserted {key}:{value}")

    def get(self, key):
        hash_index = self._find(key)
        if hash_index:
            return self.hash_array[hash_index].get_value()
        else:
            raise VehicleNotFoundError(f"ID [{key}] was not found.")

    def remove(self, key):
        self.size_down_check()
        hash_index = self._find(key)
        if hash_index:
            self.hash_array[hash_index] = HashEntry()
            self.hash_array[hash_index].set_as_removed()
            self.count -= 1
        else:
            raise VehicleNotFoundError(f"ID [{key}] was not found for deletion.")

    def get_lf(self):
        lf = self.count / self.hash_array.size
        return round(lf, 1)

    def has_key(self, key) -> bool:
        hash_index = self._find(key)
        if self.hash_array[hash_index].get_key() == key:
            return True
        return False

    def _find(self, key):

        hash_index = self._hash(key)
        original_index = hash_index

        found = False
        give_up = False

        while not found and not give_up:
            if self.hash_array[hash_index].get_state() == 0:
                give_up = True
            elif self.hash_array[hash_index].get_key() == key:
                found = True
            else:
                hash_index = (hash_index + 1) % self.hash_array.size
                if hash_index == original_index:
                    give_up = True

        if not found:
            raise VehicleNotFoundError(f"ID [{key}] was not found.")

        return hash_index

    def export_to_file(self, filename):
        with open(filename, "w") as file:
            for entry in self.hash_array:
                if entry.get_state() == 1:
                    s = str(entry.get_key()) + "," + str(entry.get_value()) + "\n"
                    file.write(s)

    def export_to_array(self):
        arr = np.empty(self.count, dtype=object)
        count = 0
        for vehicle in self.hash_array:
            if vehicle.get_state() == 1:
                arr[count] = vehicle.get_value()
                count += 1
        return arr

    def import_hash_table(self, filename):
        with open(filename, "r") as file:
            line = file.readline()
            while line:
                line_contents = line.strip().split(",")
                self.put(line_contents[0], line_contents[1])
                line = file.readline()

    def size_down_check(self):
        if self.get_lf() < 0.2 and 100 < self.count:
            new_size = self._find_next_prime(self.hash_array.size // 2)
            self.count = 0
            self._resize(new_size)

    def size_up_check(self):
        if 0.75 < self.get_lf():
            new_size = self._find_next_prime(self.hash_array.size * 2)
            self.count = 0
            self._resize(new_size)

    def _resize(self, size: int):
        temp = self.hash_array
        self.hash_array = np.empty(size, dtype=HashEntry)

        # init new table
        for i in range(self.hash_array.size):
            self.hash_array[i] = HashEntry()

        # copy existing entries to new table
        for entry in temp:
            if entry.get_state() == 1:
                self.put(entry.get_key(), entry.get_value())

    def _hash(self, key):
        hash_gen = 0
        for i in key:
            hash_gen += (31 * hash_gen) + ord(i)
        return hash_gen % self.hash_array.size

    def _find_next_prime(self, start_val: int) -> int:
        """
        Returns the next prime number from the start_val
        :param start_val:
        :return: prime_number:
        """

        if start_val % 2 == 0:
            prime_val = start_val + 1
        else:
            prime_val = start_val

        prime_val = prime_val - 2

        is_prime = False
        while not is_prime:
            prime_val = prime_val + 2

            ii = 3
            is_prime = True
            while ii * ii <= prime_val and is_prime:
                if prime_val % ii == 0:
                    is_prime = False
                else:
                    ii += 2
        return prime_val


class VehicleNotFoundError(Exception):
    pass


class DuplicateVehicleFound(Exception):
    pass
