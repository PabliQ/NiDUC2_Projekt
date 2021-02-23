##################################################
#           SKRYPT DO POMIARÓW FUNKCJI           #
##################################################

import hamming_15_11
import hamming_code
import message_generator as mg
import crc_code
import triplebitscode
import packetcounter
import csv

'''
Funkcja wykonująca pomiary na kodzie hamminga(4,7)
Przyjmuje liczbę wyników jakie należy uzyskać, liczbę pakietów i prawdopodobieństwo zakłóceń
Zapisuje wyniki w pliku csv, nie zwraca nic

The function which makes measurements on hamming code 4,7
It takes numbers of scores, which should be getting, number of packets and probability of interferences
The function save scores in csv file, return nothing
'''


def m_hamming1(num_of_score, packets, probability_interference):
    message = mg.MessageGenerator()
    hc_7_4 = hamming_code.HammingCode()
    stats = []
    for i in range(num_of_score):
        hc4_7_stats = packetcounter.PacketCounter()
        message.generate(packets * 4)
        cm = hc_7_4.encode7_4(message.get_data())
        send = message.chanel_interference(cm, probability_interference)
        hc_7_4.decode7_4(send, cm, hc4_7_stats)
        stats.append(hc4_7_stats.get_table())

    # Saving the results
    write_to_file('hamming_7_4_score.csv', stats)


def m_crc(number_of_tests, packets, interference):
    msg = mg.MessageGenerator()
    crc = crc_code.CRCCode()
    cstats = []
    for i in range(number_of_tests):
        crc_stats = packetcounter.PacketCounter()
        msg.generate(packets * 4)
        crc_encoded = crc.encode_crc(msg.get_data())
        crc_interfered = msg.chanel_interference(crc_encoded, interference)
        crc.decode_crc(crc_interfered, crc_encoded, crc_stats)
        cstats.append(crc_stats.get_table())

    write_to_file('crc_score.csv', cstats)


def m_hamming2(number_of_tests, packets, interference):
    msg = mg.MessageGenerator()
    hm15_11 = hamming_15_11.HammingCode15()
    hstats = []
    for i in range(number_of_tests):
        hm15_11_stats = packetcounter.PacketCounter()
        msg.generate(packets * 11)
        hm15_11_encoded = hm15_11.encode15_11(msg.get_data())
        hm15_11_interfered = msg.chanel_interference(hm15_11_encoded, interference)
        hm15_11.decode15_11(hm15_11_interfered, hm15_11_encoded, hm15_11_stats)
        hstats.append(hm15_11_stats.get_table())

    write_to_file('hamming_15_11_score.csv', hstats)


def m_triple(number_of_tests, packets, interference):
    msg = mg.MessageGenerator()
    triple_coding = triplebitscode.TripleBitsCode()
    triple_packet = packetcounter.PacketCounter()
    triple_stats = []
    for i in range(number_of_tests):
        triple_packet.reset()
        msg.generate(packets*4)
        triple_encoded = triple_coding.encode(msg.get_data())
        triple_interfered = msg.chanel_interference(triple_encoded, interference)
        triple_coding.decode(msg.get_data(), triple_interfered, triple_packet)
        triple_stats.append(triple_packet.get_table())
    write_to_file('triple_bits_score.csv', triple_stats)


def write_to_file(file_name, stats):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(packetcounter.PacketCounter.get_column_name())
        for packet_stats in stats:
            writer.writerow(packet_stats)
