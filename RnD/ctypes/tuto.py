import ctypes

path = (
    r"C:\Users\Lenny\Documents\CODE_MesProjets\dev\0020_lbx_pipeline\RnD\ctypes\tuto.so"
)
# Load the shared library
lib = ctypes.CDLL(path)
lib.display()
