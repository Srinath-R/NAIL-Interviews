# Set ith bit
x |= (1 << i)

# Clear ith bit
x &= ~(1 << i)

# Toggle ith bit
x ^= (1 << i)

# Check if ith bit is set
(x >> i) & 1 == 1

# Isolate lowest set bit
x & -x

# Remove lowest set bit
x & (x - 1)

# Count 1s in binary
bin(x).count('1')

# Get binary representation
bin(x)[2:]  # as string without '0b'

# Check power of two
x > 0 and (x & (x - 1)) == 0

# Iterate all subsets of mask
# This trick is useful when:
#     Mask represents a specific set, and you want all its subsets.
#     Efficient subset iteration is needed (e.g. in DP on subsets).
#     You want to skip all combinations outside the original mask (e.g. not iterate over 1 << n unnecessarily).
# Eg: you have 10110 and want to generate 10110, 10100, 10010 10000 00110 00100 00010. 00000 ← This one is excluded (loop ends before this)
def all_subsets(mask):
    subset = mask
    while subset:
        # process subset
        subset = (subset - 1) & mask

# Count Number of 1s (Hamming Weight)
def count_ones(n):
    """Why it works: Each iteration removes the lowest 1. So total iterations = number of 1s."""
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count

#  Is Power of Four
def is_power_of_four(n):
    """
     Why it works:

        n & (n - 1) == 0 checks power of 2.

        0x55555555 ensures 1 is in even position (power of 4)
    """
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0

# Reverse Bits (32-bit)
def reverse_bits(n):
    """Why it works: Collect the LSB each time and shift it into the result."""
    res = 0
    for _ in range(32):
        res = (res << 1) | (n & 1)
        n >>= 1
    return res

