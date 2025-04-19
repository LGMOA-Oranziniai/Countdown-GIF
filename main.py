#=== Nustatymai ===#
NAME = "countdown.gif"      # GIF failo pavadinimas
DURATION = 60               # Trukmė, sekundėmis

DARKMODE = False                                                    # Ar naudoti tamsųjį rėžimą
BACKGROUND_COLOR = (255, 255, 255) if not DARKMODE else (0, 0, 0)   # Fono spalva
TEXT_COLOR = (0, 0, 0) if not DARKMODE else (255, 255, 255)         # Teksto spalva

FADING = True               # Ar paskutines sekundes keisti teksto spalvą
FADE_COLOR = (255, 0, 0)    # Spalva, į kurią keisti teksto spalvą
FADE_START = 10             # Sekundė, kada prasideda spalvos keitimas
FADE_END = 0                # Sekundė, kada baigiasi spalvos keitimas

PADDING = 50                # Atstumas nuo teksto iki paveikslėlio krašto
FONT_SIZE = 96              # Šrifto dydis
FONT = None
# Šrifto failo pavadinimas (pvz. "arial.ttf" arba .otf)
# Jei None, naudomas Pillow numatytasis šriftas
# Šrifto failas turi būti tame pačiame aplanke kaip ir šis failas

#===== Kodas ======#
from PIL import Image, ImageDraw, ImageFont

def format_time(seconds: int) -> str:
    return f"{seconds // 60:02}:{seconds % 60:02}"

def max_text_size(texts: list[str], font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    widths, heights = zip(*(font.getbbox(t)[2:] for t in texts))
    return max(widths), max(heights)

def text_color(seconds: int) -> tuple[int, int, int]:
    if FADING and seconds <= FADE_START:
        fade_ratio = max(0, (seconds - FADE_END) / (FADE_START - FADE_END + 1))
        return (
            int(TEXT_COLOR[0] * fade_ratio + FADE_COLOR[0] * (1 - fade_ratio)),
            int(TEXT_COLOR[1] * fade_ratio + FADE_COLOR[1] * (1 - fade_ratio)),
            int(TEXT_COLOR[2] * fade_ratio + FADE_COLOR[2] * (1 - fade_ratio)))
        
    return TEXT_COLOR

def create_frame(text: str, size: tuple[int, int], color: tuple[int, int, int], font: ImageFont.FreeTypeFont) -> Image.Image:
    img = Image.new("RGB", size, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    draw.text((size[0] // 2, size[1] // 2), text, fill=color, font=font, anchor="mm")
    return img

def create_gif(duration: int, filename: str) -> None:    
    try:
        font = ImageFont.truetype(FONT, FONT_SIZE)
    except:
        if FONT is not None:
            print(f"ĮSPĖJIMAS! Šriftas '{FONT}' aplanke nerastas. Naudojamas numatytasis šriftas.")
        font = ImageFont.load_default(FONT_SIZE)
        
    texts = [format_time(i) for i in range(duration + 1)]
    width, height = max_text_size(texts, font)
    size = (width + 2 * PADDING, height + 2 * PADDING)
    
    frames = [create_frame(text, size, text_color(i), font) for i, text in enumerate(texts)]
    frames.reverse()
    frames[0].save(filename, append_images=frames[1:], duration=1000, format="GIF", optimize=True, save_all=True)
    
if __name__ == "__main__":
    create_gif(DURATION, NAME)