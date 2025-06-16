import random

class CRC:
    def __init__(self, generator="1011"):  # Default polynomial (CRC-3)
        self.generator = generator

    def xor(self, a, b): # 10111, 11110
        """Perform XOR operation for CRC division."""
        return "".join("0" if i == j else "1" for i, j in zip(a, b)) #[(1,1), (1,1),(1,0)...] => ["0", "0", "1"...] => 001

    def crc_encode(self, data):
        """Encode data using CRC by appending the remainder."""
        data_augmented = data + "0" * (len(self.generator) - 1)  # Append zero bits
        remainder = self.crc_division(data_augmented)
        return data + remainder  # Append remainder as CRC => codeword

    def crc_division(self, data):
        """Perform binary division (mod-2) for CRC calculation."""
        if len(data) < len(self.generator):
            return data  # If data is shorter than the generator, return the data as the remainder

        divisor = self.generator
        temp = data[: len(divisor)] #first bits == no. of bits in divisor

        for i in range(len(data) - len(divisor) + 1):
            if temp[0] == "1":
                temp = self.xor(temp, divisor) + (data[len(divisor) + i] if len(divisor) + i < len(data) else "")
            else:
                temp = self.xor(temp, "0" * len(divisor)) + (data[len(divisor) + i] if len(divisor) + i < len(data) else "")
            temp = temp[1:]  # Remove processed bit

        return temp  # Remainder

    def crc_check(self, received_data):
        """Verify CRC at the receiver side."""
        remainder = self.crc_division(received_data)
        return all(bit == "0" for bit in remainder)  # No errors if remainder is all zeros

    def introduce_error(self, data):
        """Introduce a random error for testing."""
        if random.random() < 0.3:  # 30% chance of error
            index = random.randint(0, len(data) - 1) 
            corrupted_data = data[:index] + ("1" if data[index] == "0" else "0") + data[index + 1:] # flip bit at random index
            print(f"Error introduced at index {index}")
            return corrupted_data
        return data


def crc_simulation():
    crc = CRC()
    
    # Get binary message from the user
    message = input("Enter a binary message: ").strip() # Remove leading/trailing spaces
    
    # Validate input
    if not message: #empty
        print("Empty input! Please enter a binary string.")
        return
    if not all(bit in "01" for bit in message): #check if all bits are 0 or 1
        print("Invalid input! Please enter a binary string (only 0s and 1s).")
        return

    # **Encoding**
    encoded_crc = crc.crc_encode(message)
    corrupted_crc = crc.introduce_error(encoded_crc)  # Simulating error
    
    print(f"\nTransmitting (CRC): {encoded_crc}")
    print(f"Received    (CRC): {corrupted_crc}")
    print("CRC Check:", "No Errors" if crc.crc_check(corrupted_crc) else "Error Detected - Retransmit!")


if __name__ == "__main__":
    crc_simulation()