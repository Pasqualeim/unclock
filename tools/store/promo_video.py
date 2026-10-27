"""Draws Unclock's motion-design promo video and the stills for social posts (1920x1080).

    python3 -m venv /tmp/promo && /tmp/promo/bin/pip install pillow imageio-ffmpeg numpy
    /tmp/promo/bin/python tools/store/promo_video.py           # it and en, video and stills
    /tmp/promo/bin/python tools/store/promo_video.py it --stills

Writes marketing/video/unclock_promo_<lang>.mp4 (H.264, 30 fps, music from promo_music.py) and
marketing/images/post_<lang>_<n>_<scene>.png (the last frame of each scene).
Pictures come from the site (app screenshots, lake scenes) and docs/store/icon-512.png;
type as in the store screenshots: Fraunces 600 for titles (tools/store/fonts), the site's
Inter for the rest. Pace: one idea per scene, 4.5-7 s each, entrances of about a second,
0.7 s cross-fades: calm on purpose. The copy follows docs/IDEA.md and was checked with humanizer.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import promo_music  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT.parent / "nook-site/public/assets"
IMG = SITE / "img"
FRAUNCES = ROOT / "tools/store/fonts/fraunces-normal.woff2"
INTER = SITE / "fonts/inter-normal.woff2"
ICON = ROOT / "docs/store/icon-512.png"
OUT_VIDEO = ROOT / "marketing/video"
OUT_STILLS = ROOT / "marketing/images"

W, H, FPS = 1920, 1080, 30
XFADE = 0.7

BG = (247, 239, 230, 255)
INK = (45, 32, 28)
MUTED = (112, 92, 82)
CREAM = (255, 248, 240)
PEACH = (246, 196, 166)
SOFT = (240, 226, 214)
CARD = (255, 251, 246, 255)

COPY = {
    "it": {
        "intro": ("Tante app contano le ore di lavoro.", "Unclock conta il tempo che ti riprendi."),
        "work": ("Dici quando lavori.", "Giorni e orari. Il resto è pausa."),
        "pause": ("Fuori orario, le notifiche di lavoro vanno in pausa da sole.", "Non devi avviare niente."),
        "stats": ("Vedi quanto tempo libero ti sei ripreso.", "Anche quanto ne hai passato con la luce del giorno."),
        "privacy": ("Tutto resta sul telefono.", "Non usa internet.", "Non chiede un account."),
        "end": ("Unclock", "App per Android, in test.", "getunclock.app/it/prova"),
        "notes": [
            ("M", "Mail di lavoro", "Puoi guardare il report prima di domani?", (196, 120, 92)),
            ("T", "Chat del team", "Riunione spostata alle 8:30", (110, 140, 120)),
            ("C", "Calendario", "Promemoria: call con il cliente", (120, 130, 170)),
        ],
    },
    "en": {
        "intro": ("Every app counts your work hours.", "Unclock counts the time you get back."),
        "work": ("Tell it when you work.", "Days and hours. The rest is a break."),
        "pause": ("Off work, work notifications pause on their own.", "Nothing to start."),
        "stats": ("See how much free time you got back.", "Even how much of it had daylight."),
        "privacy": ("Everything stays on the phone.", "No internet permission.", "No account."),
        "end": ("Unclock", "An Android app, in testing.", "getunclock.app/en/try"),
        "notes": [
            ("M", "Work email", "Can you check the report before tomorrow?", (196, 120, 92)),
            ("T", "Team chat", "Meeting moved to 8:30", (110, 140, 120)),
            ("C", "Calendar", "Reminder: client call", (120, 130, 170)),
        ],
    },
}

# (scene, seconds). Scenes overlap by XFADE.
# Scenes with little to read are a touch shorter.
SCENES = [("intro", 5.6), ("work", 5.2), ("pause", 7.0), ("stats", 5.6), ("privacy", 4.6), ("end", 6.0)]


# ---- drawing helpers -------------------------------------------------------

def font(path: Path, size: int, weight: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(path), size)
    # Fraunces has Optical Size then Weight; Inter only Weight.
    f.set_variation_by_axes([min(size, 144) if a["name"] == b"Optical Size" else weight for a in f.get_variation_axes()])
    return f


def wrap(text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        probe = f"{line} {word}".strip()
        if f.getlength(probe) <= width or not line:
            line = probe
        else:
            lines.append(line)
            line = word
    return lines + [line]


def text_block(text: str, f, fill, width: int = 1600, align: str = "left", leading: float = 1.18) -> Image.Image:
    lines = wrap(text, f, width)
    asc, desc = f.getmetrics()
    step = round(f.size * leading)
    w = max(round(f.getlength(l)) for l in lines) + 4
    h = step * (len(lines) - 1) + asc + desc
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (w - f.getlength(l)) / 2 if align == "center" else 0
        d.text((x, i * step), l, font=f, fill=fill)
    return im


def rounded(im: Image.Image, radius: int) -> Image.Image:
    im = im.convert("RGBA")
    mask = Image.new("L", im.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *im.size), radius=radius, fill=255)
    im.putalpha(mask)
    return im


def shadowed(im: Image.Image, blur: int = 36, dy: int = 26, strength: int = 70) -> Image.Image:
    """The picture on a soft drop shadow, with room around it for the blur."""
    pad = blur * 2
    out = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2))
    sh = Image.new("RGBA", out.size, (40, 24, 18, 0))
    sh.putalpha(Image.new("L", out.size))
    alpha = Image.new("L", out.size)
    alpha.paste(im.getchannel("A").point(lambda a: a * strength // 255), (pad, pad + dy))
    sh.putalpha(alpha.filter(ImageFilter.GaussianBlur(blur)))
    out.alpha_composite(sh)
    out.alpha_composite(im, (pad, pad))
    return out


def phone(shot: Path, height: int) -> Image.Image:
    screen = Image.open(shot).convert("RGB")
    sw = round(screen.width * height / screen.height)
    screen = rounded(screen.resize((sw, height), Image.LANCZOS), round(sw * 0.11))
    bezel = round(sw * 0.035)
    body = Image.new("RGBA", (sw + bezel * 2, height + bezel * 2))
    ImageDraw.Draw(body).rounded_rectangle((0, 0, *body.size), radius=round(sw * 0.14), fill=(24, 20, 19, 255))
    body.alpha_composite(screen, (bezel, bezel))
    return shadowed(body)


def icon(size: int) -> Image.Image:
    return rounded(Image.open(ICON).convert("RGBA").resize((size, size), Image.LANCZOS), size // 4)


def cover(path: Path) -> Image.Image:
    scene = Image.open(path).convert("RGB")
    scale = max(W / scene.width, H / scene.height) * 1.06  # room for the slow zoom
    return scene.resize((round(scene.width * scale), round(scene.height * scale)), Image.LANCZOS)


def note_card(letter: str, title: str, body: str, color, lang: str) -> Image.Image:
    cw, ch = 700, 128
    card = Image.new("RGBA", (cw, ch))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, cw, ch), radius=32, fill=CARD)
    d.ellipse((28, 34, 88, 94), fill=color)
    fl = font(INTER, 30, 700)
    d.text((58, 64), letter, font=fl, fill=CREAM, anchor="mm")
    d.text((112, 26), title, font=font(INTER, 28, 600), fill=INK)
    d.text((112, 68), body, font=font(INTER, 27, 400), fill=MUTED)
    d.text((cw - 30, 28), "19:42", font=font(INTER, 24, 400), fill=MUTED, anchor="ra")
    return shadowed(card, blur=18, dy=10, strength=45)


# ---- motion ------------------------------------------------------------------

def clamp(x: float) -> float:
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def ease_out(x: float) -> float:
    return 1 - (1 - clamp(x)) ** 3


def ease_in_out(x: float) -> float:
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def enter(t: float, start: float, dur: float = 1.0) -> float:
    return ease_out((t - start) / dur)


def put(frame: Image.Image, layer: Image.Image, x: float, y: float, alpha: float = 1.0, scale: float = 1.0) -> None:
    """Composites layer with its top-left corner at (x, y), faded and scaled around its centre."""
    if alpha <= 0.003:
        return
    if scale != 1.0:
        w, h = layer.size
        layer = layer.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.BICUBIC)
        x += (w - layer.width) / 2
        y += (h - layer.height) / 2
    if alpha < 0.997:
        layer = layer.copy()
        layer.putalpha(layer.getchannel("A").point(lambda a: round(a * alpha)))
    frame.alpha_composite(layer, (round(x), round(y)))


def rise(frame, layer, x, y, t, start, dur=1.0, dist=34):
    p = enter(t, start, dur)
    put(frame, layer, x, y + (1 - p) * dist, p)


# ---- scenes -----------------------------------------------------------------

class Promo:
    def __init__(self, lang: str):
        c = COPY[lang]
        self.lang = lang
        title = font(FRAUNCES, 84, 600)
        sub = font(INTER, 40, 450)
        self.lake = cover(IMG / "lake_golden.webp")
        shade = Image.new("L", (W, H))
        shade.putdata([round(175 * max(0.0, 1 - x / (W * 0.9)) + 55) for _ in range(H) for x in range(W)])
        self.shade = Image.new("RGBA", (W, H), (28, 20, 18, 255))
        self.shade.putalpha(shade)
        self.night = Image.new("RGBA", (W, H), (22, 16, 15, 200))

        big = font(FRAUNCES, 84, 600)
        self.intro = [text_block(c["intro"][0], big, CREAM, 1550), text_block(c["intro"][1], big, PEACH, 1550)]
        self.mark = icon(64)
        self.mark_name = text_block("Unclock", font(INTER, 34, 600), CREAM)

        self.work = [text_block(c["work"][0], title, INK, 760), text_block(c["work"][1], sub, MUTED, 700)]
        self.work_phone = phone(IMG / f"breaks-{lang}.webp", 900)

        self.pause = [text_block(c["pause"][0], font(FRAUNCES, 74, 600), INK, 760), text_block(c["pause"][1], sub, MUTED, 700)]
        self.notes = [note_card(*n, lang) for n in c["notes"]]
        notif = Image.open(IMG / f"notif-{lang}.webp").convert("RGBA")
        notif = notif.resize((760, round(notif.height * 760 / notif.width)), Image.LANCZOS)
        self.notif = shadowed(rounded(notif, 40), blur=30, dy=18, strength=60)

        self.stats = [text_block(c["stats"][0], title, INK, 760), text_block(c["stats"][1], sub, MUTED, 700)]
        self.stats_phone = phone(IMG / f"stats-{lang}.webp", 900)

        self.lock = shadowed(icon(220), blur=24, dy=14, strength=55)
        self.privacy = [text_block(c["privacy"][0], font(FRAUNCES, 88, 600), INK, 1500, "center"),
                        text_block(c["privacy"][1], font(INTER, 42, 450), MUTED, 1200, "center"),
                        text_block(c["privacy"][2], font(INTER, 42, 450), MUTED, 1200, "center")]

        self.end_icon = icon(170)
        self.end = [text_block(c["end"][0], font(FRAUNCES, 104, 600), CREAM, 1200, "center"),
                    text_block(c["end"][1], font(INTER, 42, 450), SOFT, 1200, "center"),
                    text_block(c["end"][2], font(INTER, 46, 600), PEACH, 1200, "center")]

    def lake_frame(self, t: float, dur: float) -> Image.Image:
        z = 1.0 + 0.045 * clamp(t / dur)  # slow push-in
        lw, lh = self.lake.size
        bw, bh = round(lw / z), round(lh / z)
        left, top = (lw - bw) // 2, (lh - bh) // 2
        img = self.lake.crop((left, top, left + bw, top + bh)).resize((W, H), Image.BILINEAR)
        return img.convert("RGBA")

    def scene(self, name: str, t: float, dur: float) -> Image.Image:
        if name in ("intro", "end"):
            f = self.lake_frame(t, dur)
        else:
            f = Image.new("RGBA", (W, H), BG)

        if name == "intro":
            f.alpha_composite(self.shade)
            a, b = self.intro
            y = (H - a.height - b.height - 30) // 2
            rise(f, a, 170, y, t, 0.6, 1.2)
            rise(f, b, 170, y + a.height + 30, t, 2.2, 1.2)
            p = enter(t, 3.4, 1.0)
            put(f, self.mark, 170, H - 150, p)
            put(f, self.mark_name, 250, H - 140, p)

        elif name == "work":
            a, b = self.work
            y = (H - a.height - b.height - 36) // 2
            rise(f, a, 170, y, t, 0.35)
            rise(f, b, 170, y + a.height + 36, t, 0.9)
            ph = self.work_phone
            p = enter(t, 0.5, 1.3)
            put(f, ph, 1360 - ph.width / 2, (H - ph.height) / 2 + 40 + (1 - p) * 70 - 14 * clamp(t / dur), p)

        elif name == "pause":
            a, b = self.pause
            y = (H - a.height - b.height - 36) // 2
            rise(f, a, 170, y, t, 0.35)
            rise(f, b, 170, y + a.height + 36, t, 3.9)
            cx = 1440
            for i, card in enumerate(self.notes):
                cy = 300 + i * 150 - card.height / 2
                p_in = enter(t, 0.6 + i * 0.35, 0.9)
                p_out = ease_in_out((t - (3.0 + i * 0.3)) / 0.8)
                put(f, card, cx - card.width / 2 + p_out * 160, cy + (1 - p_in) * 30, p_in * (1 - p_out))
            p = enter(t, 4.2, 1.1)
            put(f, self.notif, cx - self.notif.width / 2, (H - self.notif.height) / 2, p, 0.94 + 0.06 * p)

        elif name == "stats":
            a, b = self.stats
            y = (H - a.height - b.height - 36) // 2
            ph = self.stats_phone
            p = enter(t, 0.3, 1.3)
            put(f, ph, 520 - ph.width / 2, (H - ph.height) / 2 + 40 + (1 - p) * 70 - 14 * clamp(t / dur), p)
            rise(f, a, 1000, y, t, 0.7)
            rise(f, b, 1000, y + a.height + 36, t, 1.3)

        elif name == "privacy":
            lock, (a, b, c) = self.lock, self.privacy
            p = enter(t, 0.2, 1.1)
            put(f, lock, (W - lock.width) / 2, 150, p, 0.86 + 0.14 * p)
            rise(f, a, (W - a.width) / 2, 470, t, 0.7)
            rise(f, b, (W - b.width) / 2, 620, t, 1.3)
            rise(f, c, (W - c.width) / 2, 690, t, 1.8)

        elif name == "end":
            f.alpha_composite(self.night)
            a, b, c = self.end
            ic = self.end_icon
            p = enter(t, 0.4, 1.2)
            put(f, ic, (W - ic.width) / 2, 190, p, 0.88 + 0.12 * p)
            rise(f, a, (W - a.width) / 2, 410, t, 1.0)
            rise(f, b, (W - b.width) / 2, 570, t, 1.7)
            rise(f, c, (W - c.width) / 2, 650, t, 2.4)
            fade = clamp((t - (dur - 0.8)) / 0.8)  # to dark at the very end
            if fade:
                put(f, Image.new("RGBA", (W, H), (16, 12, 11, 255)), 0, 0, ease_in_out(fade))
        return f

    def starts(self) -> list[float]:
        out, t = [], 0.0
        for _, d in SCENES:
            out.append(t)
            t += d - XFADE
        return out

    def frame(self, t: float) -> Image.Image:
        starts = self.starts()
        live = [(n, t - s, d) for (n, d), s in zip(SCENES, starts) if s <= t < s + d]
        base = self.scene(*live[0])
        if len(live) > 1:
            put(base, self.scene(*live[1]), 0, 0, ease_in_out(live[1][1] / XFADE))
        return base

    def length(self) -> float:
        return sum(d for _, d in SCENES) - XFADE * (len(SCENES) - 1)


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def render(lang: str, stills_only: bool) -> None:
    promo = Promo(lang)
    OUT_STILLS.mkdir(parents=True, exist_ok=True)
    for i, (name, d) in enumerate(SCENES, 1):
        hold = d - 0.9 if name == "end" else d - XFADE - 0.05  # the settled frame, before the fade
        promo.scene(name, hold, d).convert("RGB").save(OUT_STILLS / f"post_{lang}_{i}_{name}.png")
    if stills_only:
        return
    OUT_VIDEO.mkdir(parents=True, exist_ok=True)
    out = OUT_VIDEO / f"unclock_promo_{lang}.mp4"
    wav = Path(tempfile.gettempdir()) / f"unclock_promo_{lang}.wav"
    promo_music.save(str(wav), promo.length())
    cmd = [ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = round(promo.length() * FPS)
    for n in range(frames):
        enc.stdin.write(promo.frame(n / FPS).convert("RGB").tobytes())
    enc.stdin.close()
    assert enc.wait() == 0, "ffmpeg failed"
    print(f"{out.relative_to(ROOT)}: {frames} frames, {promo.length():.1f} s")


if __name__ == "__main__":
    args = sys.argv[1:]
    langs = [a for a in args if a in COPY] or list(COPY)
    for lang in langs:
        render(lang, "--stills" in args)
