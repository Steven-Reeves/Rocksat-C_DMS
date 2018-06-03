import threading
import time

CYCLES = 10
NUM_THREADS = 6


# Manage multiple files:
def file_output(filename, delay=.5):
    if (delay < .5):
        delay = .5
    file = open(filename + '.txt', 'w')
    file.write(filename + "\n")
    for n in range(CYCLES):
        file.write(str(time.ctime(time.time())))
        file.write('\n')
        time.sleep(delay)
    file.write("END")


# Print to screen method (for testing and verification)
def print_output(filename, delay=.5):
    if (delay < .5):
        delay = .5
    for n in range(CYCLES):
        print(filename + ": " + str(time.ctime(time.time())))
        time.sleep(delay)
    print(filename + " finished!")


threads = []  # List of threads

# Print-to-screen threads
for i in range(NUM_THREADS):
    t = threading.Thread(target=print_output, args=("Thread-" + str(i + 1), i))
    threads.append(t)
    t.start()

# File-output threads
for i in range(NUM_THREADS):
    t = threading.Thread(target=file_output, args=("Thread-" + str(i + 1), i))
    threads.append(t)
    t.start()

print("Exit main program")