import base64
import struct

# CRC16-XMODEM implementation
def crc16_xmodem(data: bytes) -> int:
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def raw_to_friendly(raw_address: str, bounceable: bool = True, testnet: bool = False) -> str:
    workchain_str, hex_addr = raw_address.split(":")
    workchain = int(workchain_str)

    addr_bytes = bytes.fromhex(hex_addr)

    tag = 0x11 if bounceable else 0x51
    if testnet:
        tag |= 0x80

    data = struct.pack(">b", tag)
    data += struct.pack(">b", workchain)
    data += addr_bytes

    checksum = crc16_xmodem(data)
    data += struct.pack(">H", checksum)
    
    return base64.urlsafe_b64encode(data).decode().rstrip("=")
