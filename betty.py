import tkinter as tk
import tkinter.font as tkfont
import os
import pygame
import math
from PIL import Image, ImageDraw, ImageFont, ImageTk

class LyricSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()

        self.lyrics = [
            {
                "words": [
                    {"time": 0.0, "text": "The"},
                    {"time": 0.5, "text": "worst"},
                    {"time": 1.2, "text": "thing"},
                    {"time": 1.2, "text": "\n"},
                    {"time": 1.5, "text": "that"},
                    {"time": 2.5, "text": "I"},
                    {"time": 3.0, "text": "ever"},
                    {"time": 3.8, "text": "did"},
                ]
            },
            {
                "words": [
                    {"time": 5.3, "text": "Was"},
                    {"time": 5.5, "text": "what"},
                    {"time": 6.4, "text": "i"},
                    {"time": 6.9, "text": "did"},
                    {"time": 7.5, "text": "to"},
                    {"time": 7.8, "text": "you"},
                ]
            },
            {
                "words": [
                    {"time": 12.2, "text": "But"},
                    {"time": 12.3, "text": "if"},
                    {"time": 12.5, "text": "i"},
                    {"time": 12.5, "text": "\n"},
                    {"time": 12.8, "text": "just"},
                    {"time": 13.0, "text": "showed"},
                    {"time": 13.6, "text": "up"},
                    {"time": 13.8, "text": "at"},
                    {"time": 14.0, "text": "your"},
                    {"time": 14.2, "text": "party"},
                ]
            },
            {
                "words": [
                    {"time": 15.0, "text": "Would"},
                    {"time": 15.3, "text": "you"},
                    {"time": 15.4, "text": "have"},
                    {"time": 15.9, "text": "me"},
                    {"time": 16.2, "text": "would"},
                    {"time": 16.5, "text": "you"},
                    {"time": 16.8, "text": "want"},
                    {"time": 17.3, "text": "me"},
                ]
            },
            {
                "words": [
                    {"time": 17.5, "text": "Would"},
                    {"time": 17.8, "text": "you"},
                    {"time": 17.8, "text": "\n"},
                    {"time": 18.0, "text": "tell"},
                    {"time": 18.5, "text": "me"},
                    {"time": 18.7, "text": "to"},
                    {"time": 19.0, "text": "go"},
                    {"time": 19.2, "text": "fuck"},
                    {"time": 19.6, "text": "my"},
                    {"time": 20.0, "text": "self"},
                ]
            },
            {
                "words": [
                    {"time": 20.3, "text": "or"},
                    {"time": 20.6, "text": "lead"},
                    {"time": 20.8, "text": "me"},
                    {"time": 21.1, "text": "to"},
                    {"time": 21.1, "text": "\n"},
                    {"time": 21.5, "text": "the"},
                    {"time": 21.7, "text": "garden"},
                ]
            },
            {
                "words": [
                    {"time": 22.6, "text": "in"},
                    {"time": 22.7, "text": "the"},
                    {"time": 22.9, "text": "garden"},
                    {"time": 23.7, "text": "would"},
                    {"time": 24.0, "text": "you"},
                    {"time": 24.0, "text": "\n"},
                    {"time": 24.2, "text": "trust"},
                    {"time": 24.6, "text": "me"},
                ]
            },
            {
                "words": [
                    {"time": 24.8, "text": "if"},
                    {"time": 25.2, "text": "I"},
                    {"time": 25.5, "text": "told"},
                    {"time": 25.8, "text": "you"},
                    {"time": 26.1, "text": "it"},
                    {"time": 26.2, "text": "was"},
                    {"time": 26.7, "text": "just"},
                    {"time": 26.7, "text": "\n"},
                    {"time": 27.1, "text": "a"},
                    {"time": 27.4, "text": "summer"},
                    {"time": 28.1, "text": "thing"},
                ]
            },
            {
                "words": [
                    {"time": 28.4, "text": "im"},
                    {"time": 28.7, "text": "only"},
                    {"time": 29.4, "text": "seventeen"},
                    {"time": 30.4, "text": "I"},
                    {"time": 30.7, "text": "dont"},
                    {"time": 30.8, "text": "know"},
                    {"time": 31.2, "text": "anything"},
                ]
            },
            {
                "words": [
                    {"time": 32.0, "text": "but"},
                    {"time": 32.4, "text": "I"},
                    {"time": 32.5, "text": "know"},
                ]
            },
            {
                "words": [
                    {"time": 32.7, "text": "I"},
                    {"time": 32.7, "text": "\n"},
                    {"time": 33.1, "text": "miss"},
                    {"time": 33.1, "text": "\n"},
                    {"time": 33.7, "text": "u"},
                    {"time": 33.8, "text": "u"},
                    {"time": 33.9, "text": "u"},
                    {"time": 34.0, "text": "u"},
                    {"time": 34.1, "text": "u"},
                    {"time": 34.2, "text": "u"},
                    {"time": 34.3, "text": "u"},
                    {"time": 34.4, "text": "u"},
                    {"time": 34.5, "text": "koin"},
                ]
            },
        ]

        self.audio_path = "betty.mp3"

        # Window size for each lyric square GUI
        screen_h = self.root.winfo_screenheight()
        if screen_h < 700:
            self.win_size = 350
        elif screen_h < 900:
            self.win_size = 400
        else:
            self.win_size = 500
        self.margin = 6
        self.pixel_scale = 4  # Higher = more pixelated

        # Track state
        self.windows = {}          # block_index -> {"win": Toplevel, "canvas": Canvas}
        self.window_positions = {} # block_index -> {"x": x, "y": y}
        self.last_word_counts = {} # block_index -> last visible word count
        self.music_started = False

        # Pre-compute layouts for each block
        self.block_font_sizes = []
        self.block_layouts = []    # block_index -> list of visual lines
        for block_idx in range(len(self.lyrics)):
            font_size = self._calc_font_size(block_idx)
            self.block_font_sizes.append(font_size)
            layout = self._build_layout(block_idx, font_size)
            self.block_layouts.append(layout)

        # Initialize Audio & Load (but do not play yet)
        pygame.mixer.init()
        if os.path.exists(self.audio_path):
            pygame.mixer.music.load(self.audio_path)

        # Create first window immediately and start music when it opens
        self.create_window(0)
        self.windows[0]["win"].bind("<Map>", lambda e: self.start_music() if e.widget == self.windows[0]["win"] else None)

        # Start tick cycle
        self.tick()

    # ── Layout helpers ──────────────────────────────────────────────

    def _get_real_words(self, block_index):
        """Extract paragraphs of real words (non-\\n) with their sequential index.
        Returns list of paragraphs, each a list of (real_index, text)."""
        block = self.lyrics[block_index]
        paragraphs = []
        current = []
        real_idx = 0
        for w in block["words"]:
            if w["text"] == "\n":
                if current:
                    paragraphs.append(current)
                    current = []
            else:
                current.append((real_idx, w["text"]))
                real_idx += 1
        if current:
            paragraphs.append(current)
        return paragraphs

    def _wrap_paragraph(self, para_words, font, available_width):
        """Wrap a paragraph's words into visual lines based on word + space width.
        para_words: list of (real_index, text).
        Returns list of visual lines, each a list of (real_index, text)."""
        space_width = font.measure(" ")
        lines = []
        current_line = []
        current_width = 0

        for idx, text in para_words:
            w = font.measure(text)
            if current_line:
                # Need space + word to fit
                test_width = current_width + space_width + w
                if test_width > available_width:
                    lines.append(current_line)
                    current_line = [(idx, text)]
                    current_width = w
                else:
                    current_line.append((idx, text))
                    current_width = test_width
            else:
                # First word on line
                current_line.append((idx, text))
                current_width = w

        if current_line:
            lines.append(current_line)
        return lines

    def _build_layout(self, block_index, font_size, font_family="Arial"):
        """Build the complete visual layout: list of visual lines with word positions."""
        available = self.win_size - 2 * self.margin
        f = tkfont.Font(family=font_family, size=font_size, weight="normal")
        paragraphs = self._get_real_words(block_index)
        visual_lines = []
        for para in paragraphs:
            wrapped = self._wrap_paragraph(para, f, available)
            visual_lines.extend(wrapped)
        return visual_lines

    def _count_visual_lines(self, block_index, font, available_width):
        """Count total visual lines after wrapping for a block with a given font."""
        paragraphs = self._get_real_words(block_index)
        total = 0
        for para in paragraphs:
            wrapped = self._wrap_paragraph(para, font, available_width)
            total += len(wrapped)
        return total

    def _calc_font_size(self, block_index, font_family="Arial"):
        """Binary search for the largest font size where all words fit
        (with wrapping) inside the window."""
        min_size = 10
        max_size = 500
        optimal = min_size
        usable = self.win_size - 2 * self.margin

        while min_size <= max_size:
            mid = (min_size + max_size) // 2
            f = tkfont.Font(family=font_family, size=mid, weight="normal")
            line_height = f.metrics("linespace")

            # Every individual word must fit in width
            all_fit = True
            for para in self._get_real_words(block_index):
                for _, text in para:
                    if f.measure(text) > usable:
                        all_fit = False
                        break
                if not all_fit:
                    break

            if not all_fit:
                max_size = mid - 1
                continue

            # Count visual lines (with wrapping) and check height
            num_lines = self._count_visual_lines(block_index, f, usable)
            total_height = line_height * num_lines

            if total_height <= usable:
                optimal = mid
                min_size = mid + 1
            else:
                max_size = mid - 1

        return optimal

    # ── Visibility ──────────────────────────────────────────────────

    def get_visible_count(self, block_index, current_time):
        """Count how many real (non-\\n) words are visible at current_time."""
        block = self.lyrics[block_index]
        count = 0
        for w in block["words"]:
            if current_time >= w["time"]:
                if w["text"] != "\n":
                    count += 1
            else:
                break
        return count

    # ── Window management ───────────────────────────────────────────

    def create_window(self, block_index):
        """Spawn a new square Toplevel window for a lyric block, cascaded."""
        win = tk.Toplevel(self.root)
        win.title(f"Betty")
        win.configure(bg="#ffffff")
        win.resizable(False, False)

        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        
        # Max bounds for top-left corner
        max_x = max(0, screen_w - self.win_size)
        max_y = max(0, screen_h - self.win_size - 60)
        
        # Min pixels of an existing window that must remain visible if they overlap
        min_visible = 120
        
        import random
        for _ in range(100):
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            
            # Check overlap with existing active windows
            too_much_overlap = False
            for ex_idx, ex_pos in self.window_positions.items():
                if ex_idx in self.windows and self.windows[ex_idx]["win"].winfo_exists():
                    ex_x = ex_pos["x"]
                    ex_y = ex_pos["y"]
                    # If they cover each other too much (leaving less than min_visible visible on both dimensions)
                    if abs(x - ex_x) < (self.win_size - min_visible) and abs(y - ex_y) < (self.win_size - min_visible):
                        too_much_overlap = True
                        break
            if not too_much_overlap:
                break
                
        self.window_positions[block_index] = {"x": x, "y": y}
        win.geometry(f"{self.win_size}x{self.win_size}+{x}+{y}")

        canvas = tk.Canvas(
            win,
            width=self.win_size,
            height=self.win_size,
            bg="#ffffff",
            highlightthickness=0,
        )
        canvas.pack(fill="both", expand=True)

        win.protocol("WM_DELETE_WINDOW", self.quit_app)
        win.lift()
        win.focus_force()

        self.windows[block_index] = {"win": win, "canvas": canvas}
        self.last_word_counts[block_index] = 0

    # ── Drawing ─────────────────────────────────────────────────────

    def draw_block(self, block_index, visible_count):
        """Draw the layout at low resolution, then upscale with nearest-neighbor
        for a pixelated look. Only words with index < visible_count are drawn."""
        info = self.windows[block_index]
        canvas = info["canvas"]
        canvas.delete("all")

        layout = self.block_layouts[block_index]
        font_size = self.block_font_sizes[block_index]
        scale = self.pixel_scale

        # Render at reduced resolution
        small_size = self.win_size // scale
        small_font_size = max(font_size // scale, 6)
        small_margin = max(self.margin // scale, 2)

        img = Image.new("RGB", (small_size, small_size), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            pil_font = ImageFont.truetype("arial.ttf", small_font_size)
        except Exception:
            pil_font = ImageFont.load_default(small_font_size)

        ascent, descent = pil_font.getmetrics()
        line_height = ascent + descent
        space_width = draw.textlength(" ", font=pil_font)

        total_height = line_height * len(layout)
        start_y = (small_size - total_height) / 2

        for i, line_words in enumerate(layout):
            y = start_y + i * line_height
            x = small_margin
            for j, (idx, text) in enumerate(line_words):
                if idx < visible_count:
                    draw.text((x, y), text, fill=(0, 0, 0), font=pil_font)
                word_w = draw.textlength(text, font=pil_font)
                x += word_w + space_width

        # Upscale with nearest-neighbor for pixelated effect
        pixelated = img.resize((self.win_size, self.win_size), Image.NEAREST)

        photo = ImageTk.PhotoImage(pixelated)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        info["photo"] = photo  # Keep reference to prevent garbage collection

    def start_music(self):
        """Start audio playback once the GUI is mapped."""
        if not self.music_started:
            self.music_started = True
            if os.path.exists(self.audio_path):
                pygame.mixer.music.play()

    # ── Main loop ───────────────────────────────────────────────────

    def tick(self):
        """Background callback running every 50ms to advance clock and sync lyrics."""
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000.0

            for block_idx, block in enumerate(self.lyrics):
                first_word_time = block["words"][0]["time"]
                if current_time < first_word_time:
                    continue

                if block_idx not in self.windows:
                    self.create_window(block_idx)

                visible_count = self.get_visible_count(block_idx, current_time)
                if visible_count != self.last_word_counts.get(block_idx, 0):
                    self.last_word_counts[block_idx] = visible_count
                    if visible_count > 0:
                        self.draw_block(block_idx, visible_count)

        self.root.after(50, self.tick)

    def quit_app(self):
        """Stop audio and close the application."""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LyricSyncApp(root)
    root.mainloop()
