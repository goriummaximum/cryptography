import random
import sys

# c[m][p] <- a[m][n], b[n][p]
def mtx_dot(a, b):
    if len(a[0]) != len(b):
        print("invalid inputs")
        return
        
    m = len(a)
    n = len(a[0])
    p = len(b[0])
    c = [[0 for j in range(p)] for i in range(m)]
    
    for i in range(m):
        for j in range(p):
            for k in range(n):
                c[i][j] = c[i][j] + a[i][k] * b[k][j]
    
    return c

# det <- a[m][m]
def mtx_det(a):
    if len(a) != len(a[0]):
        print("input is not a squared matrix")
        return
    
    if len(a) == 2 and len(a[0]) == 2:
        return (a[0][0]*a[1][1]) - (a[0][1]*a[1][0])
    
    sub_a = [[0 for j in range(len(a)-1)] for i in range(len(a)-1)]
    sign = 1
    det = 0
    for target_a_j in range(0, len(a[0])):
        sub_a_i = 0
        sub_a_j = 0
        for a_i in range(1, len(a)):
            for a_j in range(0, len(a[0])):
                if a_j != target_a_j:
                    sub_a[sub_a_i][sub_a_j] = a[a_i][a_j]
                    sub_a_i = sub_a_i + ((sub_a_j + 1) // len(sub_a[0]))
                    sub_a_j = (sub_a_j + 1) % len(sub_a[0])
        det = det + (sign * a[0][target_a_j] * mtx_det(sub_a))
        sign = -1 if (sign == 1) else 1
    
    return det
    
# adj[m][n] <- a[m][n]
def mtx_adj(a):
    adj_a = [[0 for j in range(len(a))] for i in range(len(a))]
    sub_a = [[0 for j in range(len(a)-1)] for i in range(len(a)-1)]
    sign = 1
    
    for adj_a_i in range(0, len(adj_a)):
        for adj_a_j in range(0, len(adj_a[0])):
            # build sub_a
            sub_a_i = 0
            sub_a_j = 0
            for a_i in range(0, len(a)):
                if a_i != adj_a_j:
                    for a_j in range(0, len(a[0])):
                        if a_j != adj_a_i:
                            sub_a[sub_a_i][sub_a_j] = a[a_i][a_j]
                            sub_a_i = sub_a_i + ((sub_a_j + 1) // len(sub_a[0]))
                            sub_a_j = (sub_a_j + 1) % len(sub_a[0])
            # calculate det(sub_a)
            adj_a[adj_a_i][adj_a_j] = sign*mtx_det(sub_a)
            sign = -1 if (sign == 1) else 1
    
    return adj_a

# b <- a, m
def inv_mod(a, m):
    for i in range(1, m):
        if (i * a) % m == 1:
            return i
    return -1
    
# c[m] <- p[m], k[n][n]
# C = P x K
def encrypt(p, k):
    m = len(p)
    n = len(k)
    c = []
    
    # perform matrix multiplication/dot of each portion of p of length n with matrix k
    for i in range(0, m, n):
        c.extend(mtx_dot([p[i:i+n]], k)[0])
    
    # c % 26
    for i in range(len(c)):
        c[i] = c[i] % 26
        
    return c

# p[m] <- c[m], k[n][n]
# P = C x K^(-1) = C x (1/det(K) * adj(K))
def decrypt(c, k):
    # find det(k) % 26
    det_k = mtx_det(k) % 26
    # find adj(k) % 26
    adj_k = mtx_adj(k)
    for i in range(len(adj_k)):
        for j in range(len(adj_k[0])):
            adj_k[i][j] = adj_k[i][j] % 26
    # find inverse modulo of det_k
    det_k_inv = inv_mod(det_k, 26)
    # find k inverse
    k_inv = [[0 for j in range(len(k[0]))] for i in range(len(k))]
    for i in range(len(k_inv)):
        for j in range(len(k_inv[0])):
            k_inv[i][j] = (det_k_inv * adj_k[i][j]) % 26
    # calculate plaintext p
    m = len(c)
    n = len(k)
    p = []
    for i in range(0, m, n):
        p.extend(mtx_dot([c[i:i+n]], k_inv)[0])
    
    for i in range(len(p)):
        p[i] = p[i] % 26
        
    return p

# str <- str, str
def encrypt_str(p, k_int):
    p_int = [(ord(char) - ord('a')) for char in p]
    c_int = encrypt(p_int, k_int)
    c_str = "".join(chr(val + ord('a')) for val in c_int)
    return c_str
    
# str <- str, str
def decrypt_str(c, k_int):
    c_int = [(ord(char) - ord('a')) for char in c]
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

    p_str = "paymoremoney"
    k_int =[
        [17, 17, 5],
        [21, 18, 21],
        [2, 2, 19]
    ]

    c_str = encrypt_str(p_str, k_int)
    print("p_str = {}".format(p_str))
    print("k_int = {}".format(k_int))
    print("c_str = {}".format(c_str))

    p_str_decr = decrypt_str(c_str, k_int)
    print("p_str_decr = {}".format(p_str_decr))
