#
# INTEL CONFIDENTIAL
#
# Copyright (c) 2021 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code (Material) are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or
# disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.
#

import struct
import intelhex as ihex

UNCACHED_OFFSET = 0x20000000
DEBUG_HEX_TOOLS = False

# NOTE: Here is the binary_chunk structure format written, please make sure it is
# consistent with its definition in 0_Src/2_DrvSw/flash/flash.h
# typedef struct
# {
#     uint32  target_address;   /** Address where the chunk should be stored in flash */
#     uint32  size;             /** Size of the chunk */
#     void    *next;            /** Pointer to the next chunk in temp RAM */
#     uint8   data[];           /** Data to be stored */
# } binary_chunk_t;


def debug_print(fmt, *kargs):
    if DEBUG_HEX_TOOLS:
        print(fmt, kargs)


def hex_prepare_chunks(hex_file, page_size, chunks_root_address):
    ih = ihex.IntelHex(hex_file)
    chunks = bytearray()
    current_chunk = bytearray()
    current_chunk_start = ih.segments()[0][0]
    current_chunk_end = current_chunk_start
    for segment_start, segment_end in ih.segments():
        segment_size = segment_end - segment_start
        # chunk exceeds segment start boundary
        if current_chunk_end > segment_start:
            print("current_chunk_end(0x%x) > segment_start(0x%x)" % (current_chunk_end, segment_start))
        assert current_chunk_end <= segment_start
        # check for a hole in the memory section
        if current_chunk_end < segment_start:
            # pn0 the current page
            pn0 = current_chunk_end // page_size
            if current_chunk_end % page_size:
                pn0 += 1
            # pn the next page
            pn = segment_start // page_size
            # check if we're on the same page
            if pn > pn0:
                # not the same page, we are on a new chunk - there's a hole!
                misaligned_on_page = segment_start % page_size  # segment_start # current_chunk_start
                # adds 12 for the chunk struct size of 3 x 32bits words
                next_chunk_address = chunks_root_address + 12 + len(current_chunk)
                if next_chunk_address % 4:
                    # the structure shall be 32 bits aligned
                    bytes2add = 4 - next_chunk_address % 4
                    current_chunk += bytearray(bytes2add)
                    next_chunk_address += bytes2add
                    current_chunk_end += bytes2add
                current_chunk_size = current_chunk_end - current_chunk_start
                chunk_header = struct.Struct('<III').pack(current_chunk_start + UNCACHED_OFFSET, current_chunk_size, next_chunk_address)
                chunks += chunk_header
                chunks += current_chunk
                current_chunk = bytearray()
                if misaligned_on_page:
                    debug_print("WARNING: we are misaligned on the page!")
                    debug_print("WARNING: current_chunk_start (0x%x) page_size (0x%x) misaligned (0x%x)" % (current_chunk_start, page_size, misaligned_on_page))
                    current_chunk += bytearray(misaligned_on_page)
                current_chunk_start = segment_start - misaligned_on_page
                debug_print("Chunk of 0x%08x--0x%08x for %08d bytes from 0x%08x to 0x%08x  -- total size: %d bytes" %
                            (chunks_root_address, next_chunk_address - 4, current_chunk_size,
                             current_chunk_start + UNCACHED_OFFSET, current_chunk_end + UNCACHED_OFFSET, len(chunks)))
                chunks_root_address = next_chunk_address
            else:
                # same page, fills with 0 in the interval
                current_chunk += bytearray(segment_start - current_chunk_end)
        # Copy the segment payload into our chunk
        current_chunk += ih.gets(segment_start, segment_size)
        current_chunk_end = segment_end
    if len(current_chunk) != 0:
        current_chunk_size = current_chunk_end - current_chunk_start
        chunk_header = struct.Struct('<III').pack(
            current_chunk_start + UNCACHED_OFFSET,
            current_chunk_size,
            0)  # don't set the next chunk address since this is the last
        debug_print("Last chunk 0x%08x--0x%08x for %08d bytes from 0x%08x to 0x%08x" % (
            chunks_root_address,
            chunks_root_address + current_chunk_size + 12, current_chunk_size,
            current_chunk_start + UNCACHED_OFFSET, current_chunk_end + UNCACHED_OFFSET))
        chunks += chunk_header
        chunks += current_chunk
    last_bytes = len(chunks) % page_size
    if last_bytes != 0:
        # last page is not complete, fill it with 0s
        chunks += bytearray(page_size - last_bytes)
    debug_print("Chunks total size: %d" % len(chunks))
    return chunks
