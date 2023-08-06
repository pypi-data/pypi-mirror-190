from flatten_everything import flatten_everything
import numpy as np
from tolerant_isinstance import isinstance_tolerant

notex = [
    "q8",
    "q64",
    "q32",
    "q256",
    "q16",
    "q128",
    "l8",
    "l64",
    "l32",
    "l256",
    "l16",
    "l128",
    "i64",
    "i32",
    "i256",
    "i16",
    "i128",
    "h8",
    "h64",
    "h32",
    "h256",
    "h16",
    "h128",
    "g8",
    "g64",
    "g32",
    "g256",
    "g16",
    "g128",
    "f64",
    "f32",
    "f256",
    "f16",
    "f128",
    "e8",
    "e64",
    "e32",
    "e256",
    "e16",
    "e128",
    "d8",
    "d64",
    "d32",
    "d256",
    "d16",
    "d128",
    "b8",
    "b64",
    "b32",
    "b256",
    "b16",
    "b128",
    "Q8",
    "Q64",
    "Q32",
    "Q256",
    "Q16",
    "Q128",
    "L8",
    "L64",
    "L32",
    "L256",
    "L16",
    "L128",
    "I8",
    "I64",
    "I32",
    "I256",
    "I16",
    "I128",
    "H8",
    "H64",
    "H32",
    "H256",
    "H16",
    "H128",
    "G8",
    "G64",
    "G32",
    "G256",
    "G16",
    "G128",
    "F8",
    "F64",
    "F32",
    "F256",
    "F16",
    "F128",
    "D8",
    "D64",
    "D32",
    "D256",
    "D16",
    "D128",
    "B8",
    "B64",
    "B32",
    "B256",
    "B16",
    "B128",
    "?8",
    "?16",
    "?32",
    "?64",
    "?256",
    "?128",
    "M8",
    "M16",
    "M32",
    "M64",
    "M128",
    "M256",
    "m8",
    "m16",
    "m32",
    "m64",
    "m128",
    "m256",
    "O8",
    "O16",
    "O32",
    "O64",
    "O128",
    "O256",
]

numpydtypes = {
    "b": """numpy.byte signed integer type, compatible with C char.""",
    "h": """numpy.short Signed integer type, compatible with C short.""",
    "i": """numpy.intc Signed integer type, compatible with C int.""",
    "l": """numpy.int_ Signed integer type, compatible with Python int and C long.""",
    "q": """class numpy.longlong Signed integer type, compatible with C long long.""",
    "B": """numpy.ubyte Unsigned integer type, compatible with C unsigned char.""",
    "H": """numpy.ushort Unsigned integer type, compatible with C unsigned short.""",
    "I": """Unsigned integer type, compatible with C unsigned int.""",
    "L": """Unsigned integer large enough to fit pointer, compatible with C uintptr_t.""",
    "Q": """Signed integer type, compatible with C unsigned long long.""",
    "e": """16-bit-precision floating-point number type: sign bit, 5 bits exponent, 10 bits mantissa.""",
    "f": """32-bit-precision floating-point number type: sign bit, 8 bits exponent, 23 bits mantissa.""",
    "d": """64-bit precision floating-point number type: sign bit, 11 bits exponent, 52 bits mantissa.""",
    "g": """128-bit extended-precision floating-point number type.""",
    "F": """Complex number type composed of 2 32-bit-precision floating-point numbers.""",
    "D": """Complex number type composed of two double-precision floating-point numbers, compatible with Python complex.""",
    "G": """Complex number type composed of 2 128-bit extended-precision floating-point numbers.""",
    "?": """The bool_ type is not a subclass of the int_ type (the bool_ is not even a number type). This is different than Python’s default implementation of bool as a sub-class of int.""",
    "M": """numpy.datetime64""",
    "m": """A timedelta stored as a 64-bit integer.""",
    "O": """Any Python object""",
    "S": """When used in arrays, this type strips trailing null bytes.""",
    "U": """Unlike the builtin str, this supports the Buffer Protocol, exposing its contents as UCS4:""",
    "V": """Create a new structured or unstructured void scalar.""",
}


def print_alldtypes():
    for key, item in numpydtypes.items():
        print(f"{key}  -  {item}")


def convert_to_all_possible_dtypes(
    a,
    with_bit_variations=False,
    continous_array=True,
    ignore_dtypes=("M", "m", "O"),
    ignore_bit=(128, 256),
):
    results = {}
    bit = [8, 16, 32, 64, 128, 256]
    bit = list(sorted(set(bit) - set(ignore_bit)))
    for key, item in numpydtypes.items():
        if key in ignore_dtypes:
            continue
        try:
            results[key] = la_to_ndarray(
                a, continous_array=continous_array, dtype=key, return_first=True
            )
            if with_bit_variations:
                for bi in bit:
                    try:
                        biva = f"{key}{bi}"
                        if biva in notex:
                            continue
                        results[biva] = la_to_ndarray(
                            a,
                            continous_array=continous_array,
                            dtype=biva,
                            return_first=True,
                        )
                    except Exception as fax:
                        continue

        except Exception as fe:
            results[key] = str(fe)
            continue
    return results


def la_to_ndarray(a, continous_array=True, dtype=None, return_first=True):
    x = a
    if not isinstance_tolerant(a, np.recarray):
        x = np.core.records.fromarrays(a)
    alldtypes = []
    for daxs in [x for x in list(flatten_everything(x.dtype.fields.items()))]:
        try:
            alldtypes.append(daxs.descr)
        except Exception as fe:
            continue
    deldt = [x for x in (flatten_everything(alldtypes)) if len(x) > 0]
    deldt = list(reversed(sorted(deldt, key=lambda z: len(z))))

    fields = x.dtype.names
    allna = len(fields)
    allconverts = []
    if isinstance_tolerant(dtype, None):
        alldone = []
        for da in deldt:
            if da in alldone:
                continue
            alldone.append(da)
            try:
                v = x.view((da, allna))
                if continous_array:
                    if return_first:
                        return np.ascontiguousarray(v)
                    else:
                        allconverts.append(np.ascontiguousarray(v))
                else:
                    if return_first:
                        return v
                    else:
                        allconverts.append(v)
            except Exception as fe:
                continue
        return allconverts
    else:
        try:
            v = x.view((dtype, allna))
        except Exception:

            try:
                ara = np.dstack([x[field] for field in fields])
                aran = ara.astype(dtype)
            except Exception:
                aran = x.astype(dtype)
            if continous_array:
                return np.ascontiguousarray(aran)
            else:
                return aran

        if continous_array:
            return np.ascontiguousarray(v)
        else:
            return v



