def compress(data: bytes) -> bytes:
    """
    Compress data using the LZ78 algorithm as described in Lempel and Ziv's 1978 paper:
    "Compression of Individual Sequences via Variable-Rate Coding" (DOI: 10.1109/TIT.1978.1055934).

    The algorithm builds a dictionary of substrings and outputs a sequence of (index, character) pairs,
    where 'index' refers to the dictionary index of the longest prefix match and 'character' is the next
    character that did not match.

    Args:
        data (bytes): The input data to compress.

    Returns:
        bytes: The compressed data as a sequence of (index, character) pairs.
    """
    import struct

    # Initialize the dictionary with an empty string at index 0
    dictionary = {b'': 0}  # Map substrings to indices
    dict_size = 1  # Next available index for the dictionary
    compressed_data = []  # List to store the output (index, character) pairs

    w = b''  # Current prefix (initialized to empty string)

    for byte in data:
        c = bytes([byte])  # Current character as bytes

        # Check if the concatenation of w and c is in the dictionary
        if w + c in dictionary:
            # If yes, extend the current prefix w
            w = w + c
        else:
            # Output the index of w and the new character c
            index = dictionary[w]
            compressed_data.append((index, byte))
            # Add w + c to the dictionary
            dictionary[w + c] = dict_size
            dict_size += 1
            # Reset w to empty string for the next iteration
            w = b''

    # After processing all input, if w is not empty, output it
    if w != b'':
        index = dictionary[w]
        compressed_data.append((index, 0))  # Use 0 to indicate the end

    # Convert the compressed data to bytes
    output_data = b''
    for index, byte in compressed_data:
        # Pack index as 4 bytes unsigned int (big-endian) and byte as 1 byte
        output_data += struct.pack('>I', index) + bytes([byte])

    return output_data


def decompress(data: bytes) -> bytes:
    """
    Decompress data compressed with the LZ78 algorithm.

    The decompression algorithm rebuilds the dictionary in the same way as compression,
    using the (index, character) pairs to reconstruct the original data.

    Args:
        data (bytes): The compressed data as a sequence of (index, character) pairs.

    Returns:
        bytes: The original uncompressed data.
    """
    import struct

    # Initialize the dictionary with an empty string at index 0
    dictionary = {0: b''}  # Map indices to substrings
    dict_size = 1  # Next available index for the dictionary
    decompressed_data = b''  # To store the output data

    i = 0  # Current position in the compressed data
    data_length = len(data)

    while i < data_length:
        # Read the next (index, character) pair
        # Index is 2 bytes unsigned int (big-endian), character is 1 byte
        if i + 3 > data_length:
            # Not enough data to unpack index and character
            break
        index = struct.unpack('>I', data[i:i+4])[0]
        byte = data[i+4]
        i += 5

        # Reconstruct the original substring
        # If byte is 0, it indicates the end (no character)
        if byte != 0:
            entry = dictionary[index] + bytes([byte])
        else:
            entry = dictionary[index]
        # Append the entry to the decompressed data
        decompressed_data += entry
        # Add the new entry to the dictionary
        dictionary[dict_size] = entry
        dict_size += 1

    return decompressed_data
