from random import randint
from random import random


class MessageGenerator:
    _originalData = []

    def generate(self, size):
        counter = 0
        self._originalData.clear()
        while counter < size:
            self._originalData.append(randint(0, 1))
            counter += 1

    # Sprawdzenie ile bitów po odczycie wiadomości jest prawidłowych
    def read_validation(self, read_message):
        counter_good_bit = 0
        if len(read_message) > len(self._originalData):
            counter_good_bit += len(read_message) - len(self._originalData)
        for i in range(len(self._originalData)):
            if self._originalData[i] != read_message[i]:
                counter_good_bit += 1
        return counter_good_bit

    # Zakłócenia na kanale
    @staticmethod
    def chanel_interference(coded_data, probability_of_error):
        sent_message = []
        for bit in range(len(coded_data)):
            if random() < probability_of_error:
                if coded_data[bit] == 1:
                    sent_message.append(0)
                else:
                    sent_message.append(1)
            else:
                sent_message.append(coded_data[bit])
        return sent_message

    def get_data(self):
        return self._originalData[:]

    def set_data(self, message):
        self._originalData.clear()
        for i in range(len(message)):
            self._originalData.append(int(message[i]))
    # end_def
