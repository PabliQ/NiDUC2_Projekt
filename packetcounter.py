class PacketCounter:

    def __init__(self):
        self.good_bits = 0
        self.fixed_wrong = 0
        self.nonfixed_wrong = 0
        self.nondetected_wrong = 0

    def reset(self):
        self.good_bits = 0
        self.fixed_wrong = 0
        self.nonfixed_wrong = 0
        self.nondetected_wrong = 0

    def get_table(self):
        return [self.good_bits,
                self.fixed_wrong,
                self.nonfixed_wrong,
                self.nondetected_wrong]

    @staticmethod
    def get_column_name():
        return ['Well sent', 'Repaired', 'Unrepaired', 'Undetected']
