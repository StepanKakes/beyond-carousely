import sys, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps
src, out, per, cols, cell = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
files = sorted(f for f in glob.glob(os.path.join(src, '*')) if f.lower().endswith(('.jpg','.png')))
try: font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
except: font = ImageFont.load_default()
for si in range(0, len(files), per):
    chunk = files[si:si+per]; rows = (len(chunk)+cols-1)//cols
    sheet = Image.new('RGB', (cols*cell, rows*(cell+30)), 'white'); d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = ImageOps.exif_transpose(Image.open(f)).convert('RGB'); im.thumbnail((cell, cell))
        x, y = (i%cols)*cell, (i//cols)*(cell+30)
        sheet.paste(im, (x+(cell-im.width)//2, y+30+(cell-im.height)//2))
        d.text((x+4, y+4), os.path.basename(f), fill='black', font=font)
    sheet.save(f"{out}_{si//per+1}.jpg", quality=80); print(f"{out}_{si//per+1}.jpg", len(chunk))
