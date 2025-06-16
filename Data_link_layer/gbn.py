import random
import time

class Frame:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data
    
    
    def __repr__(self):
        return f"Frame(seq={self.seq_num}, data='{self.data}')"

class GoBackNProtocol:    
    def __init__(self, window_size, timeout_duration, total_frames):
        self.window_size = window_size
        self.timeout_duration = timeout_duration #time to wait before retransmitting
        self.total_frames = total_frames

        self.send_base = 0              # Oldest unacknowledged frame
        self.next_seq_num = 0           # Next frame to be sent
        self.frames_buffer = []         # Buffer storing all frames
        
        self.expected_seq_num = 0       # Next expected frame sequence number
        
        self.frames_sent = 0
        self.frames_retransmitted = 0
        self.frames_lost = 0
        self.frames_corrupted = 0
        self.acks_sent = 0
        self.timeouts_occurred = 0
        
        self.last_send_time = {}        # Track when each frame was sent
        
        self.loss_probability = 0.2     # Frame loss probability
        self.corruption_probability = 0.1  # Frame corruption probability

    def create_frames(self, data_list):
        """Create frames with sequence numbers"""
        self.frames_buffer = [Frame(i, data) for i, data in enumerate(data_list)]
        print("FRAMES CREATED:")
        for frame in self.frames_buffer:
            print(f"   {frame}")
        print()
        
    
    def check_timeouts(self):
        current_time = time.time()
        timeout_occurred = False
        
        for seq_num in range(self.send_base, self.next_seq_num): #frames that have been sent but not yet acknowledged
            if seq_num in self.last_send_time:
                if current_time - self.last_send_time[seq_num] > self.timeout_duration:
                    print(f"\nTIMEOUT OCCURRED for Frame {seq_num}")
                    self.timeouts_occurred += 1
                    timeout_occurred = True
                    break
        
        if timeout_occurred:
            print(f"RETRANSMITTING all frames from {self.send_base} to {self.next_seq_num-1}")
            for i in range(self.send_base, self.next_seq_num): #Starts from send_base (oldest unacked frame) through next_seq_num-1
                if i < len(self.frames_buffer): #Checks bounds to ensure the frame exists in the buffer
                    self.transmit_frame(self.frames_buffer[i], is_retransmission=True) #Calls transmit_frame() with a retransmission flag
            print()
    
    def transmit_frame(self, frame, is_retransmission=False):
        if is_retransmission:
            print(f"RETRANSMITTING: {frame}")
            self.frames_retransmitted += 1
        else:
            print(f"SENDING: {frame}")
            self.frames_sent += 1
        
        self.last_send_time[frame.seq_num] = time.time() #Resets timer for both new transmissions and retransmissions
        
        time.sleep(0.1) # Simulate transmission delay
        
        # Simulate frame loss
        if random.random() < self.loss_probability:
            print(f"Frame {frame.seq_num} LOST during transmission!")
            self.frames_lost += 1
            return False
        
        # Simulate frame corruption
        if random.random() < self.corruption_probability:
            print(f"Frame {frame.seq_num} CORRUPTED during transmission!")
            self.frames_corrupted += 1
            return False
        
        # Frame successfully transmitted - deliver to receiver
        return self.receive_frame(frame)
    
    def receive_frame(self, frame):
        """Receiver processes incoming frame"""
        print(f"RECEIVED: {frame}")
        
        if frame.seq_num == self.expected_seq_num:
            # Frame received in order
            print(f"Frame {frame.seq_num} accepted (in order)")
            self.expected_seq_num += 1
            return self.send_ack(frame.seq_num)
        else:
            # Out-of-order frame - discard and send ACK for last in-order frame
            print(f"Frame {frame.seq_num} discarded (out of order)")
            print(f"Expected: {self.expected_seq_num}, Received: {frame.seq_num}")
            if self.expected_seq_num > 0:
                return self.send_ack(self.expected_seq_num - 1)
            return False
    
    def send_ack(self, ack_num):
        """Send acknowledgment for received frame"""
        print(f"SENDING ACK {ack_num}")
        self.acks_sent += 1
        
        # Simulate ACK transmission delay
        time.sleep(0.05)
        
        # Process ACK at sender (assuming reliable ACK channel)
        return self.process_ack(ack_num)
    
    def process_ack(self, ack_num):
        """Sender processes received ACK"""
        print(f"ACK {ack_num} received by sender")
        
        # Remove timeout tracking for acknowledged frame
        if ack_num in self.last_send_time:
            del self.last_send_time[ack_num]
        
        # Slide window if this ACK advances the window
        if ack_num >= self.send_base:
            old_base = self.send_base
            self.send_base = ack_num + 1
            
            # Clean up timeout tracking for all acknowledged frames
            for seq in list(self.last_send_time.keys()):
                if seq < self.send_base:
                    del self.last_send_time[seq]
            
            if old_base != self.send_base:
                window_start = self.send_base
                window_end = min(self.send_base + self.window_size - 1, self.total_frames - 1)
                old_window = f"{old_base}-{old_base + self.window_size - 1}"
                new_window = f"{window_start}-{window_end}" if window_end >= window_start else "EMPTY"
                print(f"WINDOW SLID: [{old_window}] → [{new_window}]")
            return True
        return False
    
    def can_send_frame(self):
        """Check if sender can send more frames (window not full)"""
        return (self.next_seq_num < self.send_base + self.window_size and 
                self.next_seq_num < self.total_frames)
    
    def all_frames_acknowledged(self):
        """Check if all frames have been acknowledged"""
        return self.send_base >= self.total_frames
    
    def run_protocol(self, data_list):
        """Main protocol execution"""
        print("STARTING GO-BACK-N PROTOCOL\n")
        self.create_frames(data_list)
        
        # Main protocol loop
        max_iterations = 100  # Prevent infinite loops
        iteration = 0
        
        while not self.all_frames_acknowledged() and iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Check for timeouts first
            self.check_timeouts()
            
            # Send new frames within window
            frames_sent_this_iteration = 0
            while self.can_send_frame() and frames_sent_this_iteration < self.window_size:
                frame = self.frames_buffer[self.next_seq_num]
                
                if self.transmit_frame(frame):
                    # Frame was successfully transmitted and ACK received
                    pass
                
                self.next_seq_num += 1
                frames_sent_this_iteration += 1
            
            # Show current state
            print(f"State: send_base={self.send_base}, next_seq_num={self.next_seq_num}")
            print(f"Window: [{self.send_base}-{min(self.send_base + self.window_size - 1, self.total_frames - 1)}]")
            
            # Small delay between iterations
            time.sleep(0.2)
            
            # Check if we're making progress
            if frames_sent_this_iteration == 0 and not self.last_send_time:
                print("No progress detected. Ending simulation.")
                break
        
        # Print results
        self.print_simulation_results()
    
    def print_simulation_results(self):
        """Print detailed simulation statistics"""
        print(f"\n{'='*60}")
        print("SIMULATION RESULTS")
        print(f"{'='*60}")
        
        print(f"TRANSMISSION STATISTICS:")
        print(f"Total Frames Sent: {self.frames_sent}")
        print(f"Frames Retransmitted: {self.frames_retransmitted}")
        print(f"Frames Lost: {self.frames_lost}")
        print(f"Frames Corrupted: {self.frames_corrupted}")
        print(f"ACKs Sent: {self.acks_sent}")
        print(f"Timeouts Occurred: {self.timeouts_occurred}")
        

        
        print(f"\nPROTOCOL STATUS:")
        if self.all_frames_acknowledged():
            print("ALL FRAMES SUCCESSFULLY TRANSMITTED AND ACKNOWLEDGED")
        else:
            acknowledged = self.send_base
            print(f"PARTIAL SUCCESS: {acknowledged}/{self.total_frames} frames acknowledged")
        
        print(f"{'='*60}\n")

def get_user_input():
    """Get protocol parameters from user"""

    while True:
        try:
            window_size = int(input("Enter Window Size (1-8): "))
            if 1 <= window_size <= 8:
                break
            print("Window size must be between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            timeout = float(input("Enter Timeout Duration (seconds, 1-5): "))
            if 1 <= timeout <= 5:
                break
            print("Timeout must be between 1 and 5 seconds.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            num_frames = int(input("Enter Number of Frames (1-12): "))
            if 1 <= num_frames <= 12:
                break
            print("Number of frames must be between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    return window_size, timeout, num_frames


def main():
    """Main function to run the Go-Back-N simulation"""
    print("GO-BACK-N ARQ PROTOCOL SIMULATOR")
    
    # Get user input
    window_size, timeout, num_frames = get_user_input()
    
    # Create data to transmit
    data_list = [f"DATA_{i+1}" for i in range(num_frames)]
    
    # Initialize and run protocol
    protocol = GoBackNProtocol(window_size, timeout, num_frames)
    protocol.run_protocol(data_list)
    
    print("SIMULATION COMPLETED!")

def simulate_go_back_n():
    print("GO-BACK-N ARQ PROTOCOL SIMULATOR")
    window_size, timeout, num_frames = get_user_input()
    data_list = [f"DATA_{i+1}" for i in range(num_frames)]
    protocol = GoBackNProtocol(window_size, timeout, num_frames)
    protocol.run_protocol(data_list)
    print("SIMULATION COMPLETED!")
