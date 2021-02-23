class TripleBitsCode:

    def encode(self, message):
        length = len(message)
        encoded = []
        for i in range(length):
            for j in range(3):
                encoded.append(message[i])
        return encoded

    def decode(self, message, encoded, stats):  # oryginalna wiadomosc do porownywania
        length = len(encoded)
        packet_length = 4
        notfull_length = 0  # dlugosc niepelnego pakietu
        stats.reset()
        if length % (packet_length * 3) == 0:
            number_of_packets = length / (packet_length * 3)
        else:
            number_of_packets = (length // (packet_length * 3)) + 1  # niepelny pakiet
            notfull_length = len(message) % packet_length  # dlugosc niepelnego pakietu
            for i in range(packet_length - notfull_length):
                message.append(0)  # dopisuje odpowiednia ilosc zer do wiadmosci w celu dopelnienia pakietu
                for j in range(3):
                    encoded.append(0)  # dopisuje odpowiednia ilosc zer do zakodowanej wiadomosci
        decoded = []
        for k in range(int(number_of_packets)):
            good_bits = 0
            fixed_wrong = 0
            nonfixed_wrong = 0
            nondetected_wrong = 0
            for l in range(packet_length):
                # dekodowanie
                suma = 0
                suma = encoded[k * packet_length * 3 + 3 * l] + encoded[k * packet_length * 3 + 3 * l + 1] + encoded[
                    k * packet_length * 3 + 3 * l + 2]
                if suma < 2:
                    decoded.append(0)
                if suma > 1:
                    decoded.append(1)
                # sprawdzenie statystyk pakietu
                decoded_bit = k * packet_length + l
                if message[decoded_bit] == decoded[decoded_bit]:
                    if (message[decoded_bit] == 1 and suma == 3) or (message[decoded_bit] == 0 and suma == 0):
                        good_bits += 1
                    else:
                        fixed_wrong += 1
                if message[decoded_bit] != decoded[decoded_bit]:
                    if (message[decoded_bit] == 1 and suma == 0) or (message[decoded_bit] == 0 and suma == 3):
                        nondetected_wrong += 1
                    else:
                        nonfixed_wrong += 1
                # sprawdzenie status calego pakietu
            if good_bits == packet_length:
                stats.good_bits += 1
            if fixed_wrong > 0 and nonfixed_wrong == 0 and nondetected_wrong == 0:
                stats.fixed_wrong += 1
            if nonfixed_wrong > 0 and nondetected_wrong == 0:
                stats.nonfixed_wrong += 1
            if nondetected_wrong > 0:
                stats.nondetected_wrong += 1
        return decoded
