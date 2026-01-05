import tkinter as tk
import sys

lyrics_list = [
    "Kung sinu-sino pang tinatawagan mo",
    "Nandito lang naman ako",
    "At kung saan-saan ka pa naghahanap",
    "Nandito lang naman ako",
    "Kung sinu-sino pang tinatawagan mo",
    "Nandito lang naman ako",
    "At kung saan-saan ka pa naghahanap",
    "Nandito lang naman ako",
    "Ako na lang sana,",
    "tayo na lang dal'wa",
    "Sana nalaman mo pala,",
    "ako na lang sana"
]

typing_delay = 50
delays = [
    600,
    800,
    900,
    1000,
    900,
    1200,
    500,
    1400,
    5000,
    3900,
    2300
]

current_line_index = 0
current_char_index = 0
lyrics_label = None
root = None

def type_next_char():
    global current_char_index, current_line_index

    if current_line_index < len(lyrics_list):
        current_line = lyrics_list[current_line_index]

        if current_char_index < len(current_line):
            new_text = lyrics_label.cget("text") + current_line[current_char_index]
            lyrics_label.config(text=new_text)
            current_char_index += 1
            root.after(typing_delay, type_next_char)
        else:
            current_line_index += 1
            current_char_index = 0
            if current_line_index < len(lyrics_list):
                root.after(delays[current_line_index - 1], next_line)
    else:
        pass

def next_line():
    lyrics_label.config(text="")
    type_next_char()

def create_lyrics_window():
    global lyrics_label, root
    
    root = tk.Tk()
    root.title("Game Over")
    root.geometry("500x400")
    root.configure(bg="#2c3e50")
    root.attributes('-topmost', True)

    lyrics_label = tk.Label(
        root,
        text="",
        font=("Helvetica", 14),
        fg="white",
        bg="#2c3e50",
        justify="center"
    )
    lyrics_label.pack(pady=40, padx=20)

    close_button = tk.Button(
        root,
        text="Close",
        command=root.destroy,
        font=("Helvetica", 12),
        bg="#e74c3c",
        fg="white"
    )
    close_button.pack(pady=20)

    root.after(1000, type_next_char)

    root.mainloop()

if __name__ == "__main__":
    create_lyrics_window()