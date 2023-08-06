import struct

cdtypesstru = {
    "char": "c",
    "signed_char": "b",
    "unsigned_char": "B",
    "Bool": "?",
    "short": "h",
    "unsigned_short": "H",
    "int": "i",
    "unsigned_int": "I",
    "long": "l",
    "unsigned_long": "L",
    "long_long": "q",
    "unsigned_long_long": "Q",
    "ssize_t": "n",
    "size_t": "N",
    "float": "f",
    "double": "d",
    "char_array_s": "s",
    "char_array_p": "p",
    "void": "P",
}
cdtypesstru2 = {v: v for k, v in cdtypesstru.items()}
cdtypesstru |= cdtypesstru2

def print_all_dtypes():
    for key,item in cdtypesstru.items():

        print(f'key: {str(key).ljust(25)}   dtype: {item}')

def convert_to_py(dtype, b):
    try:
        convme = cdtypesstru[dtype]
        si = struct.calcsize(convme)
        mply = len(b) // si
        if mply == 0:
            mply = ""
    except KeyError:
        convme = dtype
        mply = ""

    return struct.unpack(f"""{mply}{convme}""", b)


def convert_to_c(dtype, *args):
    largs = len(args)
    argadd = ""

    try:
        convme = cdtypesstru[dtype]
        argadd = str(largs)
    except KeyError:
        convme = dtype
    return struct.pack(f"""{argadd}{convme}""", *args)


def convert_to_c_char(*args):
    return convert_to_c("char", *args)


def convert_to_c_c(*args):
    return convert_to_c("c", *args)


def convert_to_c_signed_char(*args):
    return convert_to_c("signed_char", *args)


def convert_to_c_b(*args):
    return convert_to_c("b", *args)


def convert_to_c_unsigned_char(*args):
    return convert_to_c("unsigned_char", *args)


def convert_to_c_B(*args):
    return convert_to_c("B", *args)


def convert_to_c_Bool(*args):
    return convert_to_c("Bool", *args)


def convert_to_c_bool(*args):
    return convert_to_c("?", *args)


def convert_to_c_short(*args):
    return convert_to_c("short", *args)


def convert_to_c_h(*args):
    return convert_to_c("h", *args)


def convert_to_c_unsigned_short(*args):
    return convert_to_c("unsigned_short", *args)


def convert_to_c_H(*args):
    return convert_to_c("H", *args)


def convert_to_c_int(*args):
    return convert_to_c("int", *args)


def convert_to_c_i(*args):
    return convert_to_c("i", *args)


def convert_to_c_unsigned_int(*args):
    return convert_to_c("unsigned_int", *args)


def convert_to_c_I(*args):
    return convert_to_c("I", *args)


def convert_to_c_long(*args):
    return convert_to_c("long", *args)


def convert_to_c_l(*args):
    return convert_to_c("l", *args)


def convert_to_c_unsigned_long(*args):
    return convert_to_c("unsigned_long", *args)


def convert_to_c_L(*args):
    return convert_to_c("L", *args)


def convert_to_c_long_long(*args):
    return convert_to_c("long_long", *args)


def convert_to_c_q(*args):
    return convert_to_c("q", *args)


def convert_to_c_unsigned_long_long(*args):
    return convert_to_c("unsigned_long_long", *args)


def convert_to_c_Q(*args):
    return convert_to_c("Q", *args)


def convert_to_c_ssize_t(*args):
    return convert_to_c("ssize_t", *args)


def convert_to_c_n(*args):
    return convert_to_c("n", *args)


def convert_to_c_size_t(*args):
    return convert_to_c("size_t", *args)


def convert_to_c_N(*args):
    return convert_to_c("N", *args)


def convert_to_c_float(*args):
    return convert_to_c("float", *args)


def convert_to_c_f(*args):
    return convert_to_c("f", *args)


def convert_to_c_double(*args):
    return convert_to_c("double", *args)


def convert_to_c_d(*args):
    return convert_to_c("d", *args)


def convert_to_c_char_array_s(*args):
    return convert_to_c("char_array_s", *args)


def convert_to_c_s(*args):
    return convert_to_c("s", *args)


def convert_to_c_char_array_p(*args):
    return convert_to_c("char_array_p", *args)


def convert_to_c_p(*args):
    return convert_to_c("p", *args)


def convert_to_c_void(*args):
    return convert_to_c("void", *args)


def convert_to_c_P(*args):
    return convert_to_c("P", *args)


def convert_char_to_py(b):
    return convert_to_py(dtype="char", b=b)


def convert_c_to_py(b):
    return convert_to_py(dtype="c", b=b)


def convert_signed_char_to_py(b):
    return convert_to_py(dtype="signed_char", b=b)


def convert_b_to_py(b):
    return convert_to_py(dtype="b", b=b)


def convert_unsigned_char_to_py(b):
    return convert_to_py(dtype="unsigned_char", b=b)


def convert_B_to_py(b):
    return convert_to_py(dtype="B", b=b)


def convert_Bool_to_py(b):
    return convert_to_py(dtype="Bool", b=b)


def convert_bool_to_py(b):
    return convert_to_py(dtype="?", b=b)


def convert_short_to_py(b):
    return convert_to_py(dtype="short", b=b)


def convert_h_to_py(b):
    return convert_to_py(dtype="h", b=b)


def convert_unsigned_short_to_py(b):
    return convert_to_py(dtype="unsigned_short", b=b)


def convert_H_to_py(b):
    return convert_to_py(dtype="H", b=b)


def convert_int_to_py(b):
    return convert_to_py(dtype="int", b=b)


def convert_i_to_py(b):
    return convert_to_py(dtype="i", b=b)


def convert_unsigned_int_to_py(b):
    return convert_to_py(dtype="unsigned_int", b=b)


def convert_I_to_py(b):
    return convert_to_py(dtype="I", b=b)


def convert_long_to_py(b):
    return convert_to_py(dtype="long", b=b)


def convert_l_to_py(b):
    return convert_to_py(dtype="l", b=b)


def convert_unsigned_long_to_py(b):
    return convert_to_py(dtype="unsigned_long", b=b)


def convert_L_to_py(b):
    return convert_to_py(dtype="L", b=b)


def convert_long_long_to_py(b):
    return convert_to_py(dtype="long_long", b=b)


def convert_q_to_py(b):
    return convert_to_py(dtype="q", b=b)


def convert_unsigned_long_long_to_py(b):
    return convert_to_py(dtype="unsigned_long_long", b=b)


def convert_Q_to_py(b):
    return convert_to_py(dtype="Q", b=b)


def convert_ssize_t_to_py(b):
    return convert_to_py(dtype="ssize_t", b=b)


def convert_n_to_py(b):
    return convert_to_py(dtype="n", b=b)


def convert_size_t_to_py(b):
    return convert_to_py(dtype="size_t", b=b)


def convert_N_to_py(b):
    return convert_to_py(dtype="N", b=b)


def convert_float_to_py(b):
    return convert_to_py(dtype="float", b=b)


def convert_f_to_py(b):
    return convert_to_py(dtype="f", b=b)


def convert_double_to_py(b):
    return convert_to_py(dtype="double", b=b)


def convert_d_to_py(b):
    return convert_to_py(dtype="d", b=b)


def convert_char_array_s_to_py(b):
    return convert_to_py(dtype="char_array_s", b=b)


def convert_s_to_py(b):
    return convert_to_py(dtype="s", b=b)


def convert_char_array_p_to_py(b):
    return convert_to_py(dtype="char_array_p", b=b)


def convert_p_to_py(b):
    return convert_to_py(dtype="p", b=b)


def convert_void_to_py(b):
    return convert_to_py(dtype="void", b=b)


def convert_P_to_py(b):
    return convert_to_py(dtype="P", b=b)


