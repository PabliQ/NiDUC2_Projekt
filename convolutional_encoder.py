class convolutional_encoder:
    def encode(self, message):
        k=len(message)
        encoded=[]
        r1=0
        r2=0
        r3=0
        for i in range(0,k,1):
            r3 = r2
            r2 = r1
            r1=message[i]
            o1=r1^r2^r3
            o2=r1^r3
            encoded.append(o1)
            encoded.append(o2)
        return encoded
