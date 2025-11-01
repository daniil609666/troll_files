# alpha_blend_desktop.py
import ctypes
from ctypes import wintypes
from PIL import Image
import sys

# --- Константы ---
BI_RGB = 0
DIB_RGB_COLORS = 0

AC_SRC_OVER = 0x00
AC_SRC_ALPHA = 0x01

# --- Windows API ---
gdi32 = ctypes.WinDLL('gdi32')
user32 = ctypes.WinDLL('user32')
msimg32 = ctypes.WinDLL('msimg32')

# Типы для удобства
LPVOID = ctypes.c_void_p

# Функции
GetDC = user32.GetDC
GetDC.argtypes = [wintypes.HWND]
GetDC.restype = wintypes.HDC

ReleaseDC = user32.ReleaseDC
ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
ReleaseDC.restype = wintypes.INT

CreateCompatibleDC = gdi32.CreateCompatibleDC
CreateCompatibleDC.argtypes = [wintypes.HDC]
CreateCompatibleDC.restype = wintypes.HDC

DeleteDC = gdi32.DeleteDC
DeleteDC.argtypes = [wintypes.HDC]
DeleteDC.restype = wintypes.BOOL

SelectObject = gdi32.SelectObject
SelectObject.argtypes = [wintypes.HDC, wintypes.HGDIOBJ]
SelectObject.restype = wintypes.HGDIOBJ

CreateDIBSection = gdi32.CreateDIBSection
CreateDIBSection.argtypes = [
    wintypes.HDC,
    ctypes.c_void_p,  # BITMAPINFO*
    wintypes.UINT,
    ctypes.POINTER(LPVOID),
    wintypes.HANDLE,
    wintypes.DWORD
]
CreateDIBSection.restype = wintypes.HBITMAP

DeleteObject = gdi32.DeleteObject
DeleteObject.argtypes = [wintypes.HGDIOBJ]
DeleteObject.restype = wintypes.BOOL

# BLENDFUNCTION struct
class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ("BlendOp", ctypes.c_ubyte),
        ("BlendFlags", ctypes.c_ubyte),
        ("SourceConstantAlpha", ctypes.c_ubyte),
        ("AlphaFormat", ctypes.c_ubyte),
    ]

# Определяем argtypes для AlphaBlend — структура передаётся по значению
msimg32.AlphaBlend.argtypes = [
    wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    wintypes.HDC, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    BLENDFUNCTION
]
msimg32.AlphaBlend.restype = wintypes.BOOL

# BITMAPINFOHEADER
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", ctypes.c_uint32 * 3)  # not used for 32-bit
    ]


def premultiply_rgba_to_bgra_premultiplied(img_rgba):
    """
    Принимает PIL Image в режиме 'RGBA'.
    Возвращает bytes в порядке BGRA с premultiplied alpha, top-down (строки сверху вниз).
    """
    w, h = img_rgba.size
    rgba = img_rgba.tobytes()  # RGBA order
    out = bytearray(w * h * 4)
    # RGBA -> premultiplied BGRA
    # for speed, работаем на байтах
    idx_in = 0
    idx_out = 0
    for _ in range(w * h):
        r = rgba[idx_in]
        g = rgba[idx_in + 1]
        b = rgba[idx_in + 2]
        a = rgba[idx_in + 3]
        # premultiply
        if a != 255:
            r = (r * a + 127) // 255
            g = (g * a + 127) // 255
            b = (b * a + 127) // 255
        out[idx_out] = b
        out[idx_out + 1] = g
        out[idx_out + 2] = r
        out[idx_out + 3] = a
        idx_in += 4
        idx_out += 4
    return bytes(out)


def draw_image_alphablend(screen_x, screen_y, pil_image):
    # Ensure RGBA
    img = pil_image.convert("RGBA")
    w, h = img.size
    if w == 0 or h == 0:
        raise ValueError("Image has zero width or height")
    # premultiplied BGRA top-down
    pixel_bytes = premultiply_rgba_to_bgra_premultiplied(img)
    buf_size = len(pixel_bytes)

    # Prepare BITMAPINFO with negative height for top-down DIB
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h  # top-down
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = BI_RGB
    bmi.bmiHeader.biSizeImage = buf_size
    bmi.bmiHeader.biXPelsPerMeter = 0
    bmi.bmiHeader.biYPelsPerMeter = 0
    bmi.bmiHeader.biClrUsed = 0
    bmi.bmiHeader.biClrImportant = 0

    # Get screen DC
    hdc_screen = GetDC(None)
    if not hdc_screen:
        raise OSError("GetDC failed")

    # Create memory DC compatible with screen
    hdc_mem = CreateCompatibleDC(hdc_screen)
    if not hdc_mem:
        ReleaseDC(None, hdc_screen)
        raise OSError("CreateCompatibleDC failed")

    # Create DIBSection
    bits_ptr = LPVOID()
    hbitmap = CreateDIBSection(hdc_screen, ctypes.byref(bmi), DIB_RGB_COLORS, ctypes.byref(bits_ptr), None, 0)
    if not hbitmap:
        DeleteDC(hdc_mem)
        ReleaseDC(None, hdc_screen)
        raise OSError(f"CreateDIBSection failed, GetLastError={ctypes.GetLastError()}")

    # Select bitmap into memory DC
    prev_obj = SelectObject(hdc_mem, hbitmap)
    if not prev_obj:
        DeleteObject(hbitmap)
        DeleteDC(hdc_mem)
        ReleaseDC(None, hdc_screen)
        raise OSError("SelectObject failed")

    # Copy pixel data into DIBSection memory
    if not bits_ptr.value:
        # shouldn't happen, but check
        SelectObject(hdc_mem, prev_obj)
        DeleteObject(hbitmap)
        DeleteDC(hdc_mem)
        ReleaseDC(None, hdc_screen)
        raise OSError("CreateDIBSection returned null bits pointer")

    ctypes.memmove(bits_ptr.value, pixel_bytes, buf_size)

    # Setup blend function (by-value)
    bf = BLENDFUNCTION(AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)

    # Call AlphaBlend to draw onto screen DC
    ok = msimg32.AlphaBlend(
        hdc_screen,
        screen_x, screen_y, w, h,
        hdc_mem,
        0, 0, w, h,
        bf
    )
    if not ok:
        err = ctypes.GetLastError()
        # cleanup before raising
        SelectObject(hdc_mem, prev_obj)
        DeleteObject(hbitmap)
        DeleteDC(hdc_mem)
        ReleaseDC(None, hdc_screen)
        raise OSError(f"AlphaBlend failed, GetLastError={err}")

    # Cleanup: restore selected object, delete bitmap and mem DC, release screen DC
    SelectObject(hdc_mem, prev_obj)
    DeleteObject(hbitmap)
    DeleteDC(hdc_mem)
    ReleaseDC(None, hdc_screen)


if __name__ == "__main__":
    import os
    #img_path = r'C:\1.png'
    temp = os.getenv('temp')
    
    img_path = os.path.join(temp, 'img.png')
    print(img_path)
    img = Image.open(img_path)
    # Draw at coordinates (100, 100) — можно изменить
    while True:
        try:
            draw_image_alphablend(0, 0, img)
            #print("Image drawn")
        except Exception as e:
            print("Error:", e)
