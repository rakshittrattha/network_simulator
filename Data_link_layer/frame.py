class Frame:
    def __init__(self, src_mac, dest_mac, payload):
        """Initialize a frame with source and destination MAC addresses and data."""
        self.src_mac = src_mac
        self.dest_mac = dest_mac
        self.payload = payload

    def __str__(self):
        """String representation of the frame for debugging."""
        return f"Frame(SRC: {self.src_mac}, DEST: {self.dest_mac}, Payload: {self.payload})"

    def display(self):
        """Print the frame details."""
        print("\n===========================")
        print("      FRAME DETAILS       ")
        print("===========================")
        print(f"Source MAC: {self.src_mac}")
        print(f"Destination MAC: {self.dest_mac}")
        print(f"Payload: {self.payload}")
        print("===========================\n")






























































# import random

# class Frame:
#     def __init__(self, src_mac, dest_mac, data):
#         self.src_mac = src_mac
#         self.dest_mac = dest_mac
#         self.data = data
#         self.error_check = self.calculate_parity()

#     def calculate_parity(self):
#         # simple parity bit error check
#         binary_data = ''.join(format(ord(char), '08b') for char in self.data)
#         parity = binary_data.count('1') % 2  # even parity
#         return parity

#     def is_corrupt(self):
#         # check if frame has been corrupted
#         return self.calculate_parity() != self.error_check

#     def inject_error(self):
#         # randomly flip a bit in the data to simulate an error
#         if len(self.data) > 0:
#             error_index = random.randint(0, len(self.data) - 1)
#             char_list = list(self.data)
#             char_list[error_index] = chr(ord(char_list[error_index]) ^ 0b00000001)  # flip the least significant bit
#             self.data = ''.join(char_list)

#     def __str__(self):
#         return f"Frame[{self.src_mac} → {self.dest_mac}] Data: {self.data}"

# # Example usage:
# frame = Frame("00:11:22:33:44:55", "66:77:88:99:AA:BB", "Hello")
# print(frame)
# frame.inject_error()
# print(frame)
# print("Is corrupt:", frame.is_corrupt())