# import pygame
# import time
# import os

# # Init controller
# pygame.init()
# pygame.joystick.init()

# if pygame.joystick.get_count() == 0:
#     print("❌ No controller detected")
#     exit()

# joy = pygame.joystick.Joystick(0)
# joy.init()

# print(f"✅ Controller connected: {joy.get_name()}")

# # Initial angles
# shoulder_x = 90
# shoulder_y = 90
# elbow = 90
# wrist = 90

# def clamp(val, min_val=0, max_val=180):
#     return max(min_val, min(max_val, val))

# def deadzone(val, threshold=0.1):
#     return 0 if abs(val) < threshold else val

# while True:
#     pygame.event.pump()

#     # Read joystick with deadzone
#     lx = deadzone(joy.get_axis(0))
#     ly = deadzone(joy.get_axis(1))
#     rx = deadzone(joy.get_axis(2))
#     ry = deadzone(joy.get_axis(3))

#     # Apply movement
#     shoulder_x += lx * 2
#     shoulder_y += ly * 2
#     elbow += ry * 2
#     wrist += rx * 2

#     # Clamp values
#     shoulder_x = clamp(shoulder_x)
#     shoulder_y = clamp(shoulder_y)
#     elbow = clamp(elbow)
#     wrist = clamp(wrist)

#     # Clear screen
#     os.system('cls' if os.name == 'nt' else 'clear')

#     # Print dashboard
#     print("🎮 CONTROLLER INPUT")
#     print(f"LX: {lx:.2f} | LY: {ly:.2f}")
#     print(f"RX: {rx:.2f} | RY: {ry:.2f}")

#     print("\n🦾 SERVO ANGLES")
#     print(f"Shoulder X: {shoulder_x:.1f}")
#     print(f"Shoulder Y: {shoulder_y:.1f}")
#     print(f"Elbow:      {elbow:.1f}")
#     print(f"Wrist:      {wrist:.1f}")

#     # for checking axis
#     # for i in range(6):
#     #     print(f"Axis {i}: {joy.get_axis(i):.2f}")

#     time.sleep(0.1)


# ______________________________________________________________________________________________________________________-


# import pygame
# import time
# import os

# # ---------------- PID CLASS ----------------
# class PID:
#     def __init__(self, kp, ki, kd):
#         self.kp = kp
#         self.ki = ki
#         self.kd = kd
#         self.prev_error = 0
#         self.integral = 0

#     def compute(self, target, current):
#         error = target - current
#         self.integral += error
#         derivative = error - self.prev_error

#         output = (
#             self.kp * error +
#             self.ki * self.integral +
#             self.kd * derivative
#         )

#         self.prev_error = error
#         return output

# # ---------------- INIT ----------------
# pygame.init()
# pygame.joystick.init()

# joy = pygame.joystick.Joystick(0)
# joy.init()

# kp = 0.2
# ki = 0.001
# kd = 0.05


# # PID controllers
# pid_shoulder_x = PID(kp, ki, kd)
# pid_shoulder_y = PID(kp, ki, kd)
# pid_elbow = PID(kp, ki, kd)
# pid_wrist = PID(kp, ki, kd)

# # Current angles
# shoulder_x = 90
# shoulder_y = 90
# elbow = 90
# wrist = 90

# # Target angles
# t_shoulder_x = 90
# t_shoulder_y = 90
# t_elbow = 90
# t_wrist = 90

# def clamp(v): return max(0, min(180, v))

# def deadzone(v): return 0 if abs(v) < 0.1 else v

# # ---------------- LOOP ----------------
# while True:
#     pygame.event.pump()

#     lx = deadzone(joy.get_axis(0))
#     ly = deadzone(joy.get_axis(1))
#     rx = deadzone(joy.get_axis(2))
#     ry = deadzone(joy.get_axis(3))

#     # Update targets (NOT actual position)
#     t_shoulder_x += lx * 3
#     t_shoulder_y += ly * 3
#     t_elbow += ry * 3
#     t_wrist += rx * 3

#     # Clamp targets
#     t_shoulder_x = clamp(t_shoulder_x)
#     t_shoulder_y = clamp(t_shoulder_y)
#     t_elbow = clamp(t_elbow)
#     t_wrist = clamp(t_wrist)

#     # PID compute
#     shoulder_x += pid_shoulder_x.compute(t_shoulder_x, shoulder_x)
#     shoulder_y += pid_shoulder_y.compute(t_shoulder_y, shoulder_y)
#     elbow += pid_elbow.compute(t_elbow, elbow)
#     wrist += pid_wrist.compute(t_wrist, wrist)

#     # Clamp actual
#     shoulder_x = clamp(shoulder_x)
#     shoulder_y = clamp(shoulder_y)
#     elbow = clamp(elbow)
#     wrist = clamp(wrist)

#     # Display
#     os.system('cls' if os.name == 'nt' else 'clear')

#     print("🎯 TARGET")
#     print(t_shoulder_x, t_shoulder_y, t_elbow, t_wrist)

#     print("\n🤖 ACTUAL (PID)")
#     print(round(shoulder_x,1), round(shoulder_y,1),
#           round(elbow,1), round(wrist,1))

#     time.sleep(0.05)

# ________________________________________________________________________________________________________________________

import pygame
import tkinter as tk
from tkinter import ttk
import time

# ---------------- PID ----------------
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, target, current):
        error = target - current
        self.integral += error
        derivative = error - self.prev_error

        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )

        self.prev_error = error
        return output

# ---------------- INIT ----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No controller")
    exit()

joy = pygame.joystick.Joystick(0)
joy.init()

kp = 0.2
ki = 0.001
kd = 0.05

# PID controllers
pid_sx = PID(kp, ki, kd)
pid_sy = PID(kp, ki, kd)
pid_el = PID(kp, ki, kd)
pid_wr = PID(kp, ki, kd)

# Angles
sx = sy = el = wr = 90
t_sx = t_sy = t_el = t_wr = 90

def clamp(v): return max(0, min(180, v))
def deadzone(v): return 0 if abs(v) < 0.1 else v

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Robotic Arm Control Panel")

frame = ttk.Frame(root, padding=10)
frame.grid()



# Labels
labels = {}

control_mode = tk.StringVar(value="joystick")

ttk.Radiobutton(frame, text="Joystick", variable=control_mode, value="joystick").grid(column=0, row=12)
ttk.Radiobutton(frame, text="Manual", variable=control_mode, value="manual").grid(column=1, row=12)

def create_row(name, row):
    ttk.Label(frame, text=name).grid(column=0, row=row)
    labels[name] = ttk.Label(frame, text="0")
    labels[name].grid(column=1, row=row)

create_row("LX", 0)
create_row("LY", 1)
create_row("RX", 2)
create_row("RY", 3)

create_row("Target SX", 4)
create_row("Target SY", 5)
create_row("Target EL", 6)
create_row("Target WR", 7)

create_row("Actual SX", 8)
create_row("Actual SY", 9)
create_row("Actual EL", 10)
create_row("Actual WR", 11)

# Sliders (manual override)
sliders = {}

def create_slider(name, row):
    var = tk.DoubleVar(value=90)
    slider = ttk.Scale(frame, from_=0, to=180, variable=var, orient="horizontal")
    slider.grid(column=2, row=row)
    sliders[name] = var

create_slider("SX", 4)
create_slider("SY", 5)
create_slider("EL", 6)
create_slider("WR", 7)

# ---------------- LOOP ----------------
def update():
    global sx, sy, el, wr
    global t_sx, t_sy, t_el, t_wr

    pygame.event.pump()

    lx = deadzone(joy.get_axis(0))
    ly = deadzone(joy.get_axis(1))
    rx = deadzone(joy.get_axis(2))
    ry = deadzone(joy.get_axis(3))

    # Update targets (controller + slider)
    t_sx = clamp(t_sx + lx * 2)
    t_sy = clamp(t_sy + ly * 2)
    t_el = clamp(t_el + ry * 2)
    t_wr = clamp(t_wr + rx * 2)

    # # Slider override
    # t_sx = sliders["SX"].get()
    # t_sy = sliders["SY"].get()
    # t_el = sliders["EL"].get()
    # t_wr = sliders["WR"].get()

    if control_mode.get() == "joystick":
        t_sx = clamp(t_sx + lx * 2)
        t_sy = clamp(t_sy + ly * 2)
        t_el = clamp(t_el + ry * 2)
        t_wr = clamp(t_wr + rx * 2)
    
    else:  # manual mode
        t_sx = sliders["SX"].get()
        t_sy = sliders["SY"].get()
        t_el = sliders["EL"].get()
        t_wr = sliders["WR"].get()

    # PID
    sx += pid_sx.compute(t_sx, sx)
    sy += pid_sy.compute(t_sy, sy)
    el += pid_el.compute(t_el, el)
    wr += pid_wr.compute(t_wr, wr)

    sx = clamp(sx)
    sy = clamp(sy)
    el = clamp(el)
    wr = clamp(wr)

    # Update GUI
    labels["LX"].config(text=f"{lx:.2f}")
    labels["LY"].config(text=f"{ly:.2f}")
    labels["RX"].config(text=f"{rx:.2f}")
    labels["RY"].config(text=f"{ry:.2f}")

    labels["Target SX"].config(text=f"{t_sx:.1f}")
    labels["Target SY"].config(text=f"{t_sy:.1f}")
    labels["Target EL"].config(text=f"{t_el:.1f}")
    labels["Target WR"].config(text=f"{t_wr:.1f}")

    labels["Actual SX"].config(text=f"{sx:.1f}")
    labels["Actual SY"].config(text=f"{sy:.1f}")
    labels["Actual EL"].config(text=f"{el:.1f}")
    labels["Actual WR"].config(text=f"{wr:.1f}")

    root.after(50, update)

# Start loop
update()
root.mainloop()