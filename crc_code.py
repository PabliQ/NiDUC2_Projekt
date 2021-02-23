'''
Implementacja kodowania, dekodowania oraz naprawy jednego bitu w kodach CRC. Charakterystyka kodów CRC nie pozwala na naprawę wiekszej ilości bitów niz 1,
możemy natomiast w łatwy sposób te błędy wykryć. W celu naprawy błędu wymagane jest spełnienie następujących warunków:
- wielomian generujacy musi być "primitive polynomial"  (nie wiem jak to przetłumaczyć na polski), czyli taki, który nie może być rozłożony na prostsze wielomiany
- wysłana wiadomość powinna mieć maksymalną długość 2^m - 1, gdzie m to ilość bitów w sumie kontrolnej. Ilość bitów sumy kontrolnej to ilość bitów wielomianu generującego minus 1
- w przypadku wystąpienia więcej niz jednego błędu w odebranej wiadomości próba naprawy stworzy kolejne błędy

W poniższym kodzie jako przykładowego wielomianu generującego użyto 1011, dlatego wysyłane wiadomości powinnny być długości 4 bitów
Testowano kod dla wiadomości wysyłanej: 1100
'''
import packetcounter


class CRCCode:
    additional_bits = 0

    @staticmethod
    def crc_remainder(message, polynomial='1011'):
        '''
        Metoda wyznacza sumę kontrolną, wykorzystana w metodzie encode
        '''
        size = len(message)
        extra_bits = "0" * (len(polynomial) - 1)
        message2 = list(message + extra_bits)
        while '1' in message2[:size]:
            place = message2.index('1')
            for i in range(len(polynomial)):
                message2[place + i] = str(int(polynomial[i] != message2[place + i]))
        remainder = message2[size:]
        return ''.join(remainder)

    def encode(self, message, polynomial='1011'):
        message_str = ''
        for bit in message[:len(message)]:
            message_str += str(bit)
        coded_message = message_str + self.crc_remainder(message_str, polynomial)
        coded_array = []
        for bit in coded_message:
            coded_array.append(int(bit))
        return coded_array

    def encode_crc(self, message):
        coded_message = []
        part_size = 4
        while len(message) % part_size != 0:
            message.append(0)
            self.additional_bits = self.additional_bits + 1
        number_of_parts = int(len(message) / part_size)
        for i in range(number_of_parts):
            part_message = message[part_size * i:part_size * (i + 1)]
            part_message = self.encode(part_message)
            for bit in part_message:
                coded_message.append(bit)
        return coded_message

    @staticmethod
    def crc_check(message_received, polynomial='1011'):
        polynomial_size = len(polynomial)
        message_size = len(message_received) - polynomial_size + 1
        message_received1 = list(message_received)
        while '1' in message_received1[:message_size]:
            place = message_received1.index('1')
            for i in range(polynomial_size):
                message_received1[place + i] = str(int(polynomial[i] != message_received1[place + i]))
        crc_checked = message_received1[message_size:]
        return '1' not in crc_checked

    def decode_crc(self, message_received, coded_message, crc_stats, polynomial='1011'):
        decoded_message = []
        message_size = len(message_received)
        part_size = 7
        number_of_parts = int(message_size / part_size)
        for j in range(number_of_parts):
            part_received_message = message_received[part_size * j:part_size * (j + 1)]
            part_coded_message = coded_message[part_size * j:part_size * (j + 1)]
            tmp = []
            message_str = ''
            for bit in part_received_message[:len(part_received_message)]:
                message_str += str(bit)
            if self.crc_check(message_str, polynomial):
                polynomial_size = len(polynomial)
                real_message_size = len(message_str) - polynomial_size + 1
                for bit in message_str:
                    tmp.append(int(bit))

                error = False

                for i in range(part_size):
                    if tmp[i] != part_received_message[i]:
                        error = True
                        break
                if not error:
                    crc_stats.good_bits += 1
                else:
                    crc_stats.nondetected_wrong += 1

                tmp = tmp[:real_message_size]
                for bit in tmp:
                    decoded_message.append(bit)
            else:
                polynomial_size = len(polynomial)
                real_message_size = len(message_str) - polynomial_size + 1
                message_received1 = list(message_str)
                while '1' in message_received1[:real_message_size]:
                    place = message_received1.index('1')
                    for i in range(polynomial_size):
                        message_received1[place + i] = str(int(polynomial[i] != message_received1[place + i]))
                crc_checked = message_received1[real_message_size:]
                hpo2 = 2 ** (polynomial_size - 1)
                checksum = []
                sliced_polynomial = polynomial[polynomial_size::-1]
                polynomial_array = list(sliced_polynomial)
                gp = 0
                while '1' in polynomial_array[:polynomial_size]:
                    index = polynomial_array.index('1')
                    gp = gp + 2 ** index
                    polynomial_array[index] = '0'
                for pos in reversed(range(0, hpo2, 1)):
                    checksum.append(0)
                t = 1
                for pos in reversed(range(1, hpo2, 1)):
                    checksum[t] = pos
                    t *= 2
                    if t >= hpo2:
                        t ^= gp
                crc_checked_size = len(crc_checked)
                sliced_crc_checked = crc_checked[crc_checked_size::-1]
                checked_array = list(sliced_crc_checked)
                cs_wrong = 0
                while '1' in checked_array[:crc_checked_size]:
                    index1 = checked_array.index('1')
                    cs_wrong = cs_wrong + 2 ** index1
                    checked_array[index1] = '0'
                bad_bit_pos = checksum[cs_wrong] - 1
                message_array = list(message_str)
                if message_array[bad_bit_pos] == '0':
                    message_array[bad_bit_pos] = '1'
                else:
                    message_array[bad_bit_pos] = '0'

                for bit in message_array:
                    tmp.append(int(bit))

                error = False

                for i in range(part_size):
                    if tmp[i] != part_coded_message[i]:
                        error = True
                        break

                if error:
                    crc_stats.nonfixed_wrong += 1
                else:
                    crc_stats.fixed_wrong += 1

                tmp = tmp[:real_message_size]
                for bit in tmp:
                    decoded_message.append(bit)
        return decoded_message[:real_message_size * number_of_parts - self.additional_bits]
