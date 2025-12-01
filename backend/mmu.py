
def translate_address(virtual_hex, page_size_kb):
    try:
        virtual_addr = int(virtual_hex, 16)
        
        # Determine offset bits (4KB=12 bits, 8KB=13 bits)
        offset_bits = 13 if page_size_kb == 8 else 12 
        
        # Bitwise shift to get Page Number
        page_number = virtual_addr >> offset_bits
        
        # Bitwise AND to get Offset
        mask = (1 << offset_bits) - 1
        offset = virtual_addr & mask
        
        # Create Binary Strings for Visualization
        full_binary = bin(virtual_addr)[2:].zfill(16)
        # Split binary string based on offset bits
        page_bin = full_binary[:-offset_bits]
        offset_bin = full_binary[-offset_bits:]
        
        return {
            "valid": True,
            "page_num": page_number,
            "offset_dec": offset,
            "offset_hex": hex(offset).upper(),
            "binary_full": full_binary,
            "binary_page": page_bin,
            "binary_offset": offset_bin,
            "offset_bits": offset_bits
        }
    except:
        return {"valid": False}