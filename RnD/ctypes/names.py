import ctypes

path = (
    r"C:\Users\Lenny\Documents\CODE_MesProjets\dev\0020_lbx_plumber\RnD\ctypes\names.so"
)
# Load the shared library
lib = ctypes.CDLL(path)
lib.get_unique_name.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_int,
]
lib.get_unique_name.restype = ctypes.c_char_p

# body work


def add_name(name, data_type="Node"):
    global assigned_names

    c_names = [ctypes.c_char_p(s.encode("utf-8")) for s in assigned_names]
    items_count = len(c_names)
    c_array = (ctypes.c_char_p * (items_count))(*c_names)
    name = lib.get_unique_name(
        bytes(name, "utf-8"), bytes(data_type, "utf-8"), c_array, items_count
    ).decode("utf-8")
    assigned_names.append(name)
    print(assigned_names)


assigned_names = ["name", "name1", "name2"]
add_name("name")
add_name(None)
add_name(None)
add_name("totossimo")
add_name(None)
add_name("name3")
add_name("name2")
add_name(
    "qbdlqgldbhqosfgcpoqhslfiugqOIBDSJKQSGCOHJBQZD4Q5647D4QS12S4DF765SFQJSIUDGQIHSDIQBDIJKSGQUYDCX3"
)
