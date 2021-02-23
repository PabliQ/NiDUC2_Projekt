import math


class HammingCode:

    @staticmethod
    def _encode(message):
        size = len(message)
        # r is number of redundant bits
        r = 1

        while math.pow(2, r) < size + r + 1:
            r += 1

        code_length = size + r + 1
        ar = []

        j = 0
        i = 1
        while i < code_length:
            if (math.ceil(math.log(i) / math.log(2))
                    - math.floor(math.log(i) / math.log(2)) == 0):

                # if i == 2 ^ n for n in (0, 1, 2, .....)
                # then ar[i]=0
                # codeword[i] = 0 ----
                # redundant bits are intialized
                # with value 0
                ar.append(0)
            else:
                # codeword[i] = dataword[j]
                ar.append(message[j])
                j += 1
            i += 1

        # calculating value of redundant bits
        for i in range(r):
            x = int(math.pow(2, i))
            j = 1
            while j < code_length:
                if ((j >> i) & 1) == 1:
                    if x != j:
                        ar[x-1] = ar[x-1] ^ ar[j-1]
                j += 1
        # Coded message, first bit should bo ignored
        return ar

    def encode7_4(self, message):
        coded_message = []
        size_part = 4
        while len(message) % size_part != 0:
            message.append(0)
        number_of_parts = int(len(message) / size_part)
        for i in range(number_of_parts):
            part_message = []
            for j in range(size_part):
                part_message.append(message[i * size_part + j])
            part_message = self._encode(part_message)
            for j in range(len(part_message)):
                coded_message.append(part_message[j])
        return coded_message

    @staticmethod
    def decode7_4(sent_message, coded_message, stats):
        decoded_message = []
        size_part = 7
        size_orginal_part = 4
        number_of_parts = int(len(sent_message) / size_part)
        for i in range(number_of_parts):
            part_sent_message = []
            part_coded_message = []
            part_message = []

            part_equal = True
            for j in range(size_part):
                part_sent_message.append(sent_message[i * size_part + j])
                part_coded_message.append(coded_message[i * size_part + j])
                if part_sent_message[j] != part_coded_message[j]:
                    part_equal = False

            if not part_equal:
                for j in range(size_orginal_part):
                    part_message.append(sent_message[i * size_orginal_part + j])

                # decode
                matrix = []
                for n in range(len(part_sent_message)):
                    if part_sent_message[n] == 1:
                        bit = n + 1
                        for j in range(3):
                            matrix.append(bit % 2)
                            bit >>= 1
                matrix_hight = int(len(matrix)/3)
                parity_bits = []
                column = 0
                while column < 3:
                    parity = 0
                    row = column
                    for j in range(matrix_hight):
                        parity = parity ^ matrix[row]
                        row += 3
                    parity_bits.append(parity)
                    column += 1
                # teoretycznie bity są zapisane odwrotnie np. DEC3 == NB110
                wrong_bit = 0
                j = 2
                while j >= 0:
                    wrong_bit *= 2
                    wrong_bit += parity_bits[j]
                    j -= 1
                if wrong_bit != 0:
                    if part_sent_message[wrong_bit-1] == 1:
                        part_sent_message[wrong_bit-1] = 0
                    else:
                        part_sent_message[wrong_bit-1] = 1
                        # statistics
                    error = False
                    for j in range(len(part_sent_message)):
                        if part_sent_message[j] != part_coded_message[j]:
                            error = True
                            break
                    if error:
                        stats.nonfixed_wrong += 1
                    else:
                        stats.fixed_wrong += 1

                # if wrong_bit = 0 its error, nondetected
                else:
                    stats.nondetected_wrong += 1
            else:
                stats.good_bits += 1
            # usunąć bity kontrolne
            part_decoded_message = [part_sent_message[2], part_sent_message[4], part_sent_message[5],
                                    part_sent_message[6]]
            # end decode
            for j in range(len(part_decoded_message)):
                decoded_message.append(part_decoded_message[j])
        return decoded_message
