S = [
    [-1,0x00,0x19,0x01,0x32,0x02,0x1a,0xc6,0x4b,0xc7,0x1b,0x68,0x33,0xee,0xdf,0x03],
    [0x64,0x04,0xe0,0x0e,0x34,0x8d,0x81,0xef,0x4c,0x71,0x08,0xc8,0xf8,0x69,0x1c,0xc1],
    [0x7d,0xc2,0x1d,0xb5,0xf9,0xb9,0x27,0x6a,0x4d,0xe4,0xa6,0x72,0x9a,0xc9,0x09,0x78],
    [0x65,0x2f,0x8a,0x05,0x21,0x0f,0xe1,0x24,0x12,0xf0,0x82,0x45,0x35,0x93,0xda,0x8e],
    [0x96,0x8f,0xdb,0xbd,0x36,0xd0,0xce,0x94,0x13,0x5c,0xd2,0xf1,0x40,0x46,0x83,0x38],
    [0x66,0xdd,0xfd,0x30,0xbf,0x06,0x8b,0x62,0xb3,0x25,0xe2,0x98,0x22,0x88,0x91,0x10],
    [0x7e,0x6e,0x48,0xc3,0xa3,0xb6,0x1e,0x42,0x3a,0x6b,0x28,0x54,0xfa,0x85,0x3d,0xba],
    [0x2b,0x79,0x0a,0x15,0x9b,0x9f,0x5e,0xca,0x4e,0xd4,0xac,0xe5,0xf3,0x73,0xa7,0x57],
    [0xaf,0x58,0xa8,0x50,0xf4,0xea,0xd6,0x74,0x4f,0xae,0xe9,0xd5,0xe7,0xe6,0xad,0xe8],
    [0x2c,0xd7,0x75,0x7a,0xeb,0x16,0x0b,0xf5,0x59,0xcb,0x5f,0xb0,0x9c,0xa9,0x51,0xa0],
    [0x7f,0x0c,0xf6,0x6f,0x17,0xc4,0x49,0xec,0xd8,0x43,0x1f,0x2d,0xa4,0x76,0x7b,0xb7],
    [0xcc,0xbb,0x3e,0x5a,0xfb,0x60,0xb1,0x86,0x3b,0x52,0xa1,0x6c,0xaa,0x55,0x29,0x9d],
    [0x97,0xb2,0x87,0x90,0x61,0xbe,0xdc,0xfc,0xbc,0x95,0xcf,0xcd,0x37,0x3f,0x5b,0xd1],
    [0x53,0x39,0x84,0x3c,0x41,0xa2,0x6d,0x47,0x14,0x2a,0x9e,0x5d,0x56,0xf2,0xd3,0xab],
    [0x44,0x11,0x92,0xd9,0x23,0x20,0x2e,0x89,0xb4,0x7c,0xb8,0x26,0x77,0x99,0xe3,0xa5],
    [0x67,0x4a,0xed,0xde,0xc5,0x31,0xfe,0x18,0x0d,0x63,0x8c,0x80,0xc0,0xf7,0x70,0x07]
]
def get(i,j):
    i=int(i,16)
    j=int(j,16)
    if S[i][j] == -1:
        return -1
    else:
        return hex(S[i][j]).lstrip('0x').zfill(2)
if __name__ == "__main__":
   pass
    