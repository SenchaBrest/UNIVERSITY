import math
from collections import deque

addresses = [4, 8, 20, 24, 28, 36, 44, 20, 24, 28, 36, 40, 44, 68, 72, 92, 96, 100, 104, 108, 112, 100, 112, 116, 120, 128, 140]
address_size = 16
instruction_size = 32

block_size = 4
number_of_rows = 16
max_storage_bits = 816

miss_cost = 18 + (3 * block_size)
hit_cost = 1


def checkFullyAssociative():
    index_bits = math.ceil(math.log(block_size, 2))  
    tag_bits = address_size - index_bits  
    LRU_bits = math.ceil(math.log(number_of_rows, 2))  
    valid_bits = 1  
    row_size = tag_bits + (8 * block_size) + valid_bits + LRU_bits  
    table_size = row_size * number_of_rows  
    if table_size > max_storage_bits:  
        print("Cache is too large, change your numbers: " + str(table_size))
    else:
        print("Cache is within size constraints: " + str(table_size) + "/" + str(max_storage_bits))


def missTime():
    print("A cache miss will cost you: " + str(miss_cost) + " cycles")


def simulateFullyAssociative():
    tags = [-1] * number_of_rows
    valid = [0] * number_of_rows
    LRU = deque()

    miss_count = 0
    total_instructions = 0

    for i in range(0, 3):
        for addr in addresses:
            offset = addr % block_size
            tag = addr // (block_size)

            print("Address: " + str(addr) + ", tag: " + str(tag) + ", offset: " + str(offset), end="\t")

            if tag in tags:
                # Get the index of the row containing the tag
                location = tags.index(tag)

                # If the row is already in the LRU queue, remove it
                if location in LRU:
                    LRU.remove(location)

                # Add the row to the end of the LRU queue
                LRU.append(location)

                # Print message indicating cache hit
                print("Cache Hit")

            # Check if there is an invalid row - miss, add the current tag to it
            elif 0 in valid:
                # Get the index of the first invalid row
                location = valid.index(0)

                # Update the tag and valid bit for the row
                tags[location] = tag
                valid[location] = 1

                # If this is not the first iteration, increment the cache miss count
                if i > 0:
                    miss_count += 1

                # If the row is already in the LRU queue, remove it
                if location in LRU:
                    LRU.remove(location)

                # Add the row to the end of the LRU queue
                LRU.append(location)

                # Print message indicating cache miss and addition of new row
                print("Cache Miss - adding to empty row")

            # Otherwise, find the least recently used row and replace it with the current tag - miss
            else:
                # Get the index of the least recently used row (the first item in the LRU queue)
                leastUsedLoc = LRU.popleft()

                # Update the tag for the row
                tags[leastUsedLoc] = tag

                # If this is not the first iteration, increment the cache miss count
                if i > 0:
                    miss_count += 1

                # If the row is already in the LRU queue, remove it
                if leastUsedLoc in LRU:
                    LRU.remove(leastUsedLoc)

                # Add the row to the end of the LRU queue
                LRU.append(leastUsedLoc)

                # Print message indicating cache miss and replacement of row
                print("Cache Miss - replacing row")

            # If this is not the first iteration, increment the total instructions count
            if i > 0:
                total_instructions += 1

    # Print the tag and valid information for each row in the cache
    print("row\tvalid\ttag")
    for j in range(0, number_of_rows):
        print(str(j) + "\t" + str(valid[j]) + "\t" + str(tags[j]))

    # Calculate the CPI
    cpi = ((miss_cost * miss_count) + (total_instructions - miss_count)) / total_instructions
    print("CPI: " + str(cpi))
    print("SIMULATION COMPLETE")

def main():
    checkFullyAssociative()  # checks if the cache size is within the specified constraints

    missTime()  # prints the cost of a cache miss in cycles

    simulateFullyAssociative()  # simulates the cache access using a fully associative mapping


if __name__ == "__main__":
    main()
