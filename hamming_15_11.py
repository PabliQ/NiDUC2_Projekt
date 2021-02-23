class HammingCode15:

    @staticmethod
    def encode(message):
        message_size = len(message)
        message_coded = []
        for i in range(message_size + 4):
            message_coded.append(0)
        for i in range(7):
            message_coded[i] = message[i]
        for i in range(7, 10):
            message_coded[i + 1] = message[i]
        message_coded[12] = message[10]
        parity1 = 0
        for i in range(0, 14, 2):
            parity1 += message_coded[i]
        if parity1 % 2 == 0:
            parity1 = 0
        else:
            parity1 = 1
        message_coded[14] = parity1
        parity2 = 0
        for i in range(0, 14):
            if i == 2 or i == 3 or i == 6 or i == 7 or i == 11 or i == 10:
                continue
            else:
                parity2 += message_coded[i]
        if parity2 % 2 == 0:
            parity2 = 0
        else:
            parity2 = 1
        message_coded[13] = parity2
        parity4 = 0
        for i in range(0, 12):
            if i == 4 or i == 5 or i == 6 or i == 7:
                continue
            else:
                parity4 += message_coded[i]
        if parity4 % 2 == 0:
            parity4 = 0
        else:
            parity4 = 1
        message_coded[11] = parity4
        parity8 = 0
        for i in range(0, 8):
            parity8 += message_coded[i]
        if parity8 % 2 == 0:
            parity8 = 0
        else:
            parity8 = 1
        message_coded[7] = parity8
        return message_coded

    def encode15_11(self, message):
        coded_message = []
        part_size = 11
        while len(message) % part_size != 0:
            message.append(0)
        number_of_parts = int(len(message) / part_size)
        for i in range(number_of_parts):
            part_message = message[part_size * i:part_size * (i + 1)]
            part_message = self.encode(part_message)
            for bit in part_message[:]:
                coded_message.append(bit)
        return coded_message

    @staticmethod
    def decode15_11(message_received, encoded_message, stats_15_11):
        decoded_message = []
        message_size = len(message_received)
        part_size = 15
        number_of_parts = int(message_size / part_size)
        for i in range(number_of_parts):
            part_received_message = message_received[part_size * i:part_size * (i + 1)]
            part_encoded_message = encoded_message[part_size * i:part_size * (i + 1)]

            part_equal = True

            for j in range(part_size):
                if part_received_message[j] != part_encoded_message[j]:
                    part_equal = False

            if not part_equal:

                parity1 = part_received_message[14]
                parity2 = part_received_message[13]
                parity4 = part_received_message[11]
                parity8 = part_received_message[7]

                parity1c = 0
                for j in range(0, 14, 2):
                    parity1c += part_received_message[j]
                if parity1c % 2 == 0:
                    parity1c = 0
                else:
                    parity1c = 1
                parity2c = 0
                for j in range(0, 14):
                    if j == 2 or j == 3 or j == 6 or j == 7 or j == 11 or j == 10 or j == 13 or j == 14:
                        continue
                    else:
                        parity2c += part_received_message[j]
                if parity2c % 2 == 0:
                    parity2c = 0
                else:
                    parity2c = 1
                parity4c = 0
                for j in range(0, 12):
                    if j == 4 or j == 5 or j == 6 or j == 7 or j == 11 or j == 12:
                        continue
                    else:
                        parity4c += part_received_message[j]
                if parity4c % 2 == 0:
                    parity4c = 0
                else:
                    parity4c = 1
                parity8c = 0
                for j in range(0, 8):
                    if j == 7:
                        continue
                    else:
                        parity8c += part_received_message[j]
                if parity8c % 2 == 0:
                    parity8c = 0
                else:
                    parity8c = 1
                if parity1 != parity1c:
                    parity1 = 1
                else:
                    parity1 = 0
                if parity2 != parity2c:
                    parity2 = 1
                else:
                    parity2 = 0
                if parity4 != parity4c:
                    parity4 = 1
                else:
                    parity4 = 0
                if parity8 != parity8c:
                    parity8 = 1
                else:
                    parity8 = 0
                parity_sum = [parity1, parity2, parity4, parity8]
                wrong_bit = 0
                for j in range(len(parity_sum)):
                    if parity_sum[j] == 1:
                        wrong_bit = wrong_bit + 2 ** j
                message_bits = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12]
                sliced_part_received_message = part_received_message[part_size::-1]

                if wrong_bit != 0:
                    wrong_bit = wrong_bit - 1
                    if sliced_part_received_message[wrong_bit] == 0:
                        sliced_part_received_message[wrong_bit] = 1
                    else:
                        sliced_part_received_message[wrong_bit] = 0
                    part_received_message = sliced_part_received_message[part_size::-1]

                    error = False

                    for j in range(part_size):
                        if part_received_message[j] != part_encoded_message[j]:
                            error = True
                            break

                    if error:
                        stats_15_11.nonfixed_wrong += 1
                    else:
                        stats_15_11.fixed_wrong += 1

                else:
                    stats_15_11.nondetected_wrong += 1
            else:
                stats_15_11.good_bits += 1

            part_received_message.pop(14)
            part_received_message.pop(13)
            part_received_message.pop(11)
            part_received_message.pop(7)

            for bit in part_received_message[:]:
                decoded_message.append(bit)
        return decoded_message
