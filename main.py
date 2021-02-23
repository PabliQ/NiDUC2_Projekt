import measurement
import data_analysis as da


def main():
    # measurement.m_hamming1(10, 30, 0.04)
    # measurement.m_crc(1000, 30, 0.04)
    # measurement.m_hamming2(10, 30, 0.04)
    # measurement.m_triple(10, 30, 0.04)
    #da.d_histogram()
    #da.d_boxplot()
    #da.fit_function()
    #da.avg_all()
    #da.sddev_all()
    #da.fivenum_all()
    # da.fitfit()
    da.fit_function()
#     def select_length_and_number():
#         global message_length_input
#         message_length_input = int(input("Podaj długość wiadomości do przesłania: "))
#         global number_of_tests
#         number_of_tests = int(input("Podaj liczbę testów do przeprowadzenia: "))
# #Testowanie
#     print("Wybierz rodzaj kodowania:\n"
#           "1.Kodowanie przez potrajanie bitów\n"
#           "2.Kodowanie metodą Hamminga  7,4\n"
#           "3.Kodowanie metodą Hamminga 15,11\n"
#           "4.Kodowanie metodą CRC\n"
#           "5.Wszystkie rodzaje kodowania\n")
#     case = int(input("Wybór: "))
#     select_length_and_number()
#     if case==1:
#         for i in range(number_of_tests):
#             triple_testing(message_length_input)
#     if case==2:
#         for i in range(number_of_tests):
#             hc7_4_testing(message_length_input)
#     if case==3:
#         for i in range(number_of_tests):
#             hm15_11_testing(message_length_input)
#     if case==4:
#         for i in range(number_of_tests):
#             crc_testing(message_length_input)
#     if case==5:
#         for i in range(number_of_tests):
#             triple_testing(message_length_input)
#             hc7_4_testing(message_length_input)
#             crc_testing(message_length_input)
#             hm15_11_testing(message_length_input)

if __name__ == "__main__":
    main()
