import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json


scoreboard = []

def load_scores():
    global scoreboard
    try:
        with open("scores.json", "r") as f:
            scoreboard = json.load(f)
    except FileNotFoundError:
        scoreboard = []

def save_scores():
    with open("scores.json", "w") as f:
        json.dump(scoreboard, f)

# add/del player functions
def add_player():
    name = name_entry.get()

    if not name:
        messagebox.showerror("Input Error", "Player name cannot be empty.")
        return
    
    scoreboard.append({"name": name, "score": 0})
    save_scores()
    update_scoreboard()
    name_entry.delete(0, tk.END)

def delete_player():
    selection = listbox.curselection()
    if not selection:
        messagebox.showerror("Selection Error", "No player selected.")
        return
    
    index = selection[0]
    del scoreboard[index]
    save_scores()
    update_scoreboard()

# score modification function
def change_scoreboard(amount):
    selection = listbox.curselection()
    if not selection:
        messagebox.showerror("Selection Error", "No player selected.")
        return
    
    index = selection[0]
    player = scoreboard[index]
    player['score'] += amount
    save_scores()
    update_scoreboard()

# scoreboard display update function
def update_scoreboard():
    listbox.delete(0, tk.END)
    sorted_players = sorted(scoreboard, key=lambda x: x['score'], reverse=True)
    scoreboard[:] = sorted_players  # keep order in memory
    for player in scoreboard:
        listbox.insert(tk.END, f"{player['name']} — {player['score']}")



# GUI Setup
root = tk.Tk()
root.title("Scoreboard")
root.geometry("450x390")

bg_image = Image.open("toothfairy.jpg")  # or .png
bg_image = bg_image.resize((450, 390))   # resize to fit window
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Player Name:").pack(side=tk.LEFT, padx=5)
name_entry = tk.Entry(input_frame, width=20)
name_entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(input_frame, text="Add Player", command=add_player)
add_button.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(input_frame, text="Delete Player", command=delete_player)
add_button.pack(pady=5)

listbox = tk.Listbox(root, width=40, height=10)
listbox.pack(side=tk.LEFT,pady=10)

# Score control buttons
control_frame = tk.Frame(root)
control_frame.pack(pady=10)

# Add score buttons
for val in [-100, -200, -300, -400, -500, 100, 200, 300, 400, 500]:
    tk.Button(control_frame, text=str(val), command=lambda v=val: change_scoreboard(v)).pack(side=tk.TOP, padx=5)

load_scores()
update_scoreboard()

root.mainloop()