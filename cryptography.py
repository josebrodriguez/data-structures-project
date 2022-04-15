from collections import defaultdict

class cryptography:
    def __init__(self):
        self.a = 0

    # RC4 Encryption
    def rc4_encryption(self, listToStr, newPassword):
        tempKey = ''
        j = 0
         ## Extend the key if its not long enough
        for i in range(0, len(newPassword)):
             tempKey = tempKey + self.keyStream[j]
             j = j + 1
             if (j == len(self.keyStream)):
                 j = 0


        ## Now xor the string with the keystream
        encrypt_list = [chr( ord(a) ^ ord(b) ) for a,b in zip(newPassword, tempKey)]
        encrypted_string = ''

        # Convert the encrypted_list into characters
        encrypted_string.join(encrypt_list)
        print(encrypted_string)

        return encrypt_list
    
    

   #RC4 Decryption
    ### This will Decrypt the Encrypted string ###
    def rc4_decryption(self, encrypted_string, keyString):
        ## In order to recover the original Password, we need to xor it to the keystream
        # CT xor KS
        tempKey = ''
        j = 0
         ## Extend the key if its not long enough
        for i in range(0, len(encrypted_string)):
             tempKey = tempKey + self.keyStream[j]
             j = j + 1
             if (j == len(self.keyStream)):
                 j = 0

        decrypted_list = [chr( ord(a) ^ ord(b)) for a,b in zip(encrypted_string, tempKey )]

        return decrypted_list

    # Key Generator
    ## This will Generate the Key and the corresponding keyArray ##
    def genKey(self, input_len, fileName, userPassword):
        ## Obtain the frequencies from the generator
        frequency_letters = self.frequency_generator(fileName)

        #Create an empty array that will hold our keyArray
        freq_key_array = []
        for i in userPassword:
            value = int(frequency_letters[i] * 100)

            # If the value is out of our range, then we will shift to it accordingly
            if (value < 32):
                value + 32
            # We really only have to worry about this being the key
            freq_key_array.append(value)

        # Give the new key to a variable that will be used to conver into a 256 bit string
        encrypted_string = ''
        pass_key = freq_key_array


        ## Now we take the key and place it into a 256 array to be used again later
        keyArray = []
        currNum = int(0)
    
        # This will create a key array of size 256 bits
        for i in pass_key:
            keyArray.append(i)

        for i in range(len(pass_key),256):
            keyArray.append(keyArray[currNum])
            currNum = currNum + 1
    
        return keyArray

    # Key Stream
    def keyStream_gen(self, input_len, keyArray):
        # This will generate the keyStream that will encrypt and/or decrypt a string
        # Generate the s[] array
        s = []
        for i in range(0, 256):
            s.append(i)

        ## Key schedualling
        j = 0
        tempVar = 0
        for i in range(0,256):
            j = (j + s[i] + keyArray[i])%256
            tempVar = s[i]
            s[i] = s[j]
            s[j] = tempVar # We are swapping the variables to make is pseudorandom
    

        ## Pseudo - Random Generation Algorithm
        # First set i and j back to 0
        i = 0
        j = 0
        tempVar = 0
        self.keyStream = []

        # Now run a for loop that will encrypt the plaintext
        for i in range (i+1, input_len + 1):
            j =  (j + s[i])% 256
            tempVar = s[i]
            s[i] = s[j]
            s[j] = tempVar

            t = (s[i] + s[j])%256
            self.keyStream.append(s[t])


        # Convert the keyStream into characters
        for i in range(0, len(self.keyStream)):
            self.keyStream[i] = chr(self.keyStream[i])

        #Convert the list to a string
        listToStr = ''.join([str(elem) for elem in self.keyStream])

        return listToStr

    def frequency_generator(self, filename):
        # Load in the default dictionary/file
        f = open(filename, "r")
        d = defaultdict()
        letter_count = 0

        # Initialize the dictionary with ASCII values from 33 to 126
        for i in range(33, 126):
            d[chr(i)] = 0
    
        # Iterate through each character
        for lines in f:
            for letter in lines:
                #Ignore any instance of \r or \n
                if (letter != '\r' and letter != '\n'):
                    # Increment the letter's count and the total count
                    d[letter] += 1
                    letter_count += 1

        # Now load the frequency hash with the default dictionary
        freq_percentages = defaultdict()

        for i in range(33,126):
            freq_percentages[chr(i)] = d[chr(i)] / float(letter_count)

        # Close the file
        f.close()

        return freq_percentages
