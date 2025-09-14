import random                                                                                                                                                                                                                                                                                                                                                                                                                              
import sys

def print_2d_list(l):
    for row in l:
        print(" ".join(f"{num:>4}" for num in row))

# int[][] <- int[]
def key_parse(k):
    rows, cols = (5, 5)
    k_mtx_pos2sym = [[0 for _ in range(cols)] for _ in range(rows)]
    k_mtx_sym2pos = [[0 for _ in range(2)] for _ in range(26)]
    sym_existence = [0]*26
    k_ptr = 0
    k_mtx_row_ptr = 0
    k_mtx_col_ptr = 0
    sym = 0

    # alloc key to matrix first
    while k_ptr < len(k):
        if sym_existence[k[k_ptr]] == 0:
            k_mtx_pos2sym[k_mtx_row_ptr][k_mtx_col_ptr] = k[k_ptr]
            if (k[k_ptr] == 8 or k[k_ptr] == 9):
                k_mtx_sym2pos[8][0] = k_mtx_row_ptr
                k_mtx_sym2pos[8][1] = k_mtx_col_ptr
                k_mtx_sym2pos[9][0] = k_mtx_row_ptr
                k_mtx_sym2pos[9][1] = k_mtx_col_ptr
                sym_existence[8] = 1
                sym_existence[9] = 1
            else:
                k_mtx_sym2pos[k[k_ptr]][0] = k_mtx_row_ptr
                k_mtx_sym2pos[k[k_ptr]][1] = k_mtx_col_ptr
                sym_existence[k[k_ptr]] = 1
            k_mtx_row_ptr = k_mtx_row_ptr + ((k_mtx_col_ptr + 1) // cols)
            k_mtx_col_ptr = (k_mtx_col_ptr + 1) % cols
        k_ptr = k_ptr + 1

    # alloc other symbols to matrix second
    while sym < len(sym_existence):
        if sym_existence[sym] == 0:
            k_mtx_pos2sym[k_mtx_row_ptr][k_mtx_col_ptr] = sym
            if (sym == 8 or sym == 9):
                k_mtx_sym2pos[8][0] = k_mtx_row_ptr
                k_mtx_sym2pos[8][1] = k_mtx_col_ptr
                k_mtx_sym2pos[9][0] = k_mtx_row_ptr
                k_mtx_sym2pos[9][1] = k_mtx_col_ptr
                sym_existence[8] = 1
                sym_existence[9] = 1
            else:
                k_mtx_sym2pos[sym][0] = k_mtx_row_ptr
                k_mtx_sym2pos[sym][1] = k_mtx_col_ptr
                sym_existence[sym] = 1
            k_mtx_row_ptr = k_mtx_row_ptr + ((k_mtx_col_ptr + 1) // cols)
            k_mtx_col_ptr = (k_mtx_col_ptr + 1) % cols
        sym = sym + 1
    return k_mtx_pos2sym, k_mtx_sym2pos

# int[] <- (int[], int[])
def encrypt(p, k):
    # create key matrix
    k_mtx_pos2sym, k_mtx_sym2pos = key_parse(k)

    # create diagram
    diagram = []
    p_ptr = 0
    while (p_ptr + 1) < len(p):
        diagram.append(p[p_ptr])
        # if identical, then insert 'x'
        if (p[p_ptr] == p[p_ptr + 1]) or ((p[p_ptr] == 8 or p[p_ptr] == 9) and (p[p_ptr + 1] == 8 or p[p_ptr + 1] == 9)):
            diagram.append(23) # 'x'
            p_ptr = p_ptr + 1
        else:
            diagram.append(p[p_ptr + 1])
            p_ptr = p_ptr + 2
    # if the last pair lack 1 character, then insert 'x' in the end
    if p_ptr == (len(p) - 1):
        diagram.append(p[p_ptr])
        diagram.append(23) # 'x'
    
    # begin encryption mapping to ciphertext
    c = []
    d_ptr = 0
    while (d_ptr + 1) < len(diagram):
        # if same col, move down (row + 1) wrap around -> ciphertext still same col
        if k_mtx_sym2pos[diagram[d_ptr]][1] == k_mtx_sym2pos[diagram[d_ptr + 1]][1]:
            row = k_mtx_sym2pos[diagram[d_ptr]][0]
            col = k_mtx_sym2pos[diagram[d_ptr]][1]
            c.append(k_mtx_pos2sym[(row + 1) % 5][col])
            row = k_mtx_sym2pos[diagram[d_ptr + 1]][0]
            col = k_mtx_sym2pos[diagram[d_ptr + 1]][1]
            c.append(k_mtx_pos2sym[(row + 1) % 5][col])

        # if same row, move right (col + 1) wrap around -> ciphertext still same row
        elif k_mtx_sym2pos[diagram[d_ptr]][0] == k_mtx_sym2pos[diagram[d_ptr + 1]][0]:
            row = k_mtx_sym2pos[diagram[d_ptr]][0]
            col = k_mtx_sym2pos[diagram[d_ptr]][1]
            c.append(k_mtx_pos2sym[row][(col + 1) % 5])
            row = k_mtx_sym2pos[diagram[d_ptr + 1]][0]
            col = k_mtx_sym2pos[diagram[d_ptr + 1]][1]
            c.append(k_mtx_pos2sym[row][(col + 1) % 5])

        # if rectangle (not same row and not same col), swap col
        else:
            row = k_mtx_sym2pos[diagram[d_ptr]][0]
            col = k_mtx_sym2pos[diagram[d_ptr + 1]][1]
            c.append(k_mtx_pos2sym[row][col])
            row = k_mtx_sym2pos[diagram[d_ptr + 1]][0]
            col = k_mtx_sym2pos[diagram[d_ptr]][1]
            c.append(k_mtx_pos2sym[row][col])

        d_ptr = d_ptr + 2
    return c

# int[] <- (int[], int[])
def decrypt(c, k):
    # create key matrix
    k_mtx_pos2sym, k_mtx_sym2pos = key_parse(k)
    
    # begin decryption mapping to diagram
    diagram = []
    c_ptr = 0
    while (c_ptr + 1) < len(c):
        # if same col, move up (row - 1) wrap around
        if k_mtx_sym2pos[c[c_ptr]][1] == k_mtx_sym2pos[c[c_ptr + 1]][1]:
            row = k_mtx_sym2pos[c[c_ptr]][0]
            col = k_mtx_sym2pos[c[c_ptr]][1]
            diagram.append(k_mtx_pos2sym[(row - 1 + 5) % 5][col])
            row = k_mtx_sym2pos[c[c_ptr + 1]][0]
            col = k_mtx_sym2pos[c[c_ptr + 1]][1]
            diagram.append(k_mtx_pos2sym[(row - 1 + 5) % 5][col])
        
        # if same row, move left (col - 1) wrap around
        elif k_mtx_sym2pos[c[c_ptr]][0] == k_mtx_sym2pos[c[c_ptr + 1]][0]:
            row = k_mtx_sym2pos[c[c_ptr]][0]
            col = k_mtx_sym2pos[c[c_ptr]][1]
            diagram.append(k_mtx_pos2sym[row][(col - 1 + 5) % 5])
            row = k_mtx_sym2pos[c[c_ptr + 1]][0]
            col = k_mtx_sym2pos[c[c_ptr + 1]][1]
            diagram.append(k_mtx_pos2sym[row][(col - 1 + 5) % 5])

        # if rectangle (not same row and not same col), swap col
        else:
            row = k_mtx_sym2pos[c[c_ptr]][0]
            col = k_mtx_sym2pos[c[c_ptr + 1]][1]
            diagram.append(k_mtx_pos2sym[row][col])
            row = k_mtx_sym2pos[c[c_ptr + 1]][0]
            col = k_mtx_sym2pos[c[c_ptr]][1]
            diagram.append(k_mtx_pos2sym[row][col])

        c_ptr = c_ptr + 2
    return diagram

# str <- str, str
def encrypt_str(p, k):
    p_int = [(ord(char) - ord('a')) for char in p]
    k_int = [(ord(char) - ord('a')) for char in k]
    c_int = encrypt(p_int, k_int)
    c_str = "".join(chr(val + ord('a')) for val in c_int)
    return c_str
    
# str <- str, str
def decrypt_str(c, k):
    c_int = [(ord(char) - ord('a')) for char in c]
    k_int = [(ord(char) - ord('a')) for char in k]
    p_int = decrypt(c_int, k_int)
    p_str = "".join(chr(val + ord('a')) for val in p_int)
    return p_str

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seed_int = int(sys.argv[1])
    else:
        seed_int = None

    if seed_int is not None:
        random.seed(seed_int)

    p_str = "nesoapp"
    k_str = "nesoapp"

    c_str = encrypt_str(p_str, k_str)
    print("p_str = {}".format(p_str))
    print("k_str = {}".format(k_str))
    print("c_str = {}".format(c_str))

    p_str_decr = decrypt_str(c_str, k_str)
    print("p_str_decr = {}".format(p_str_decr))
