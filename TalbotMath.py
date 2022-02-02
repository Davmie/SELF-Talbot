import ctypes


class Math(ctypes.Structure):
    _fields_ = [
        ('p', ctypes.c_double),
        ('mode', ctypes.c_int),
        ('n', ctypes.c_int),
        ('b', ctypes.c_double),
        ('l', ctypes.c_double),
        ('omega', ctypes.c_double),
        ('k', ctypes.c_double),
        ('omega_n', ctypes.c_double),
        ('integrals', ctypes.POINTER(ctypes.c_double)),
    ]


lib = ctypes.CDLL('lib/libmath.so')

def create_info(p, mode, n, b=None):
    lib.create.restype = ctypes.POINTER(Math)
    lib.create.argtypes = [ctypes.c_void_p]
    new_p = ctypes.c_double(p)
    new_mode = ctypes.c_int(mode)
    new_n = ctypes.c_int(n)
    new_b = ctypes.c_double(b)
    info = lib.create(new_p, new_mode, new_n, new_b)
    return info


def Intense_wrapper(x, z, info):
    func_intense = lib.Intense
    func_intense.argtypes = (ctypes.POINTER(Math), ctypes.c_double, ctypes.c_double)
    func_intense.restype = ctypes.c_double
    new_x = ctypes.c_double(x)
    new_z = ctypes.c_double(z)
    res = func_intense(info, new_x, new_z)
    return res


def free_info(info):
    free = lib.free
    free.argtypes = (ctypes.POINTER(Math))
    free.restype = None
    free(info)
