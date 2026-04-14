# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# L1, L2, L3 = 220, 200, 40

# def rot_z(t):
#     return np.array([
#         [np.cos(t), -np.sin(t), 0],
#         [np.sin(t),  np.cos(t), 0],
#         [0, 0, 1]
#     ])

# def rot_y(t):
#     return np.array([
#         [ np.cos(t), 0, np.sin(t)],
#         [0, 1, 0],
#         [-np.sin(t), 0, np.cos(t)]
#     ])

# def fk(yaw, pitch, elbow, wrist, base):
#     base = np.array(base)

#     # Shoulder rotation
#     R = rot_z(yaw) @ rot_y(pitch)

#     # Arm now extends along X-axis (IMPORTANT FIX)
#     p1 = base + R @ np.array([L1, 0, 0])

#     R2 = R @ rot_y(elbow)
#     p2 = p1 + R2 @ np.array([L2, 0, 0])

#     R3 = R2 @ rot_y(wrist)
#     p3 = p2 + R3 @ np.array([L3, 0, 0])

#     return np.array([base, p1, p2, p3])


# def lerp(a, b, t):
#     return a + (b - a) * t


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.set_xlim(-400, 400)
# ax.set_ylim(-400, 400)
# ax.set_zlim(0, 600)

# left_line, = ax.plot([], [], [], 'o-', lw=4, color='blue')
# right_line, = ax.plot([], [], [], 'o-', lw=4, color='red')

# left_base = [120, 0, 300]
# right_base = [-120, 0, 300]


# def update(frame):
#     hold = 20
#     transition = 40

#     # ✅ TRUE T-POSE
#     tpose = {
#         "yaw_L": 0,          # straight out left
#         "yaw_R": np.pi,      # straight out right
#         "pitch": 0,
#         "elbow": 0,
#         "wrist": 0
#     }

#     # ✅ CORRECT NAMASKAR (forward + inward)
#     target = {
#         "yaw_L": 1,
#         "yaw_R": np.pi - 1,
#         "pitch": -1,   # bring forward
#         "elbow": -1.9,   # fold
#         "wrist": 0.4
#     }

#     if frame < hold:
#         alpha = 0
#     elif frame < hold + transition:
#         alpha = (frame - hold) / transition
#     else:
#         alpha = 1

#     yaw_L = lerp(tpose["yaw_L"], target["yaw_L"], alpha)
#     yaw_R = lerp(tpose["yaw_R"], target["yaw_R"], alpha)
#     pitch = lerp(tpose["pitch"], target["pitch"], alpha)
#     elbow = lerp(tpose["elbow"], target["elbow"], alpha)
#     wrist = lerp(tpose["wrist"], target["wrist"], alpha)

#     left = fk(yaw_L, pitch, elbow, wrist, left_base)
#     right = fk(yaw_R, pitch, elbow, wrist, right_base)

#     left_line.set_data(left[:,0], left[:,1])
#     left_line.set_3d_properties(left[:,2])

#     right_line.set_data(right[:,0], right[:,1])
#     right_line.set_3d_properties(right[:,2])

#     return left_line, right_line


# anim = FuncAnimation(fig, update, frames=120, interval=50)

# plt.title("FIXED: True T-Pose → Correct Namaskar")
# plt.show()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

L1, L2, L3 = 220, 200, 40

def rot_z(t):
    return np.array([
        [np.cos(t), -np.sin(t), 0],
        [np.sin(t),  np.cos(t), 0],
        [0, 0, 1]
    ])

def rot_y(t):
    return np.array([
        [ np.cos(t), 0, np.sin(t)],
        [0, 1, 0],
        [-np.sin(t), 0, np.cos(t)]
    ])

def fk(yaw, pitch, elbow, wrist, base, mirror=False):
    base = np.array(base)

    #mirror
    if mirror:
        mirror_mat = np.diag([-1,1,1])
    else:
        mirror_mat = np.eye(3)

    R = mirror_mat @ (rot_z(-yaw) @ rot_y(-pitch))

    p1 = base + R @ np.array([L1, 0, 0])

    R2 = R @ rot_y(-elbow)
    p2 = p1 + R2 @ np.array([L2, 0, 0])

    R3 = R2 @ rot_y(-wrist)
    p3 = p2 + R3 @ np.array([L3, 0, 0])

    return np.array([base, p1, p2, p3])


# Bases
left_base  = [120, 0, 300]
right_base = [-120, 0, 300]

# Figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

plt.subplots_adjust(left=0.25, bottom=0.35)

ax.set_xlim(-400, 400)
ax.set_ylim(-400, 400)
ax.set_zlim(0, 600)

left_line, = ax.plot([], [], [], 'o-', lw=4, color='blue')
right_line, = ax.plot([], [], [], 'o-', lw=4, color='red')


def update_plot(val):
    # Read slider values (convert to radians)
    yaw_L = np.radians(s_yaw_L.val)
    pitch_L = np.radians(s_pitch_L.val)
    elbow_L = np.radians(s_elbow_L.val)
    wrist_L = np.radians(s_wrist_L.val)

    yaw_R = -np.radians(s_yaw_R.val)
    pitch_R = np.radians(s_pitch_R.val)
    elbow_R = np.radians(s_elbow_R.val)
    wrist_R = np.radians(s_wrist_R.val)

    left = fk(yaw_L, pitch_L, elbow_L, wrist_L, left_base)
    right = fk(yaw_R, pitch_R, elbow_R, wrist_R, right_base,mirror=True)

    left_line.set_data(left[:,0], left[:,1])
    left_line.set_3d_properties(left[:,2])

    right_line.set_data(right[:,0], right[:,1])
    right_line.set_3d_properties(right[:,2])

    fig.canvas.draw_idle()


# === SLIDERS ===
axcolor = 'lightgoldenrodyellow'

def make_slider(pos, label, vmin, vmax, vinit):
    ax_s = plt.axes(pos, facecolor=axcolor)
    return Slider(ax_s, label, vmin, vmax, valinit=vinit)

# Left arm
s_yaw_L   = make_slider([0.25, 0.25, 0.65, 0.02], 'Yaw L', -180, 180, 0)
s_pitch_L = make_slider([0.25, 0.22, 0.65, 0.02], 'Pitch L', -90, 90, 0)
s_elbow_L = make_slider([0.25, 0.19, 0.65, 0.02], 'Elbow L', -150, 0, 0)
s_wrist_L = make_slider([0.25, 0.16, 0.65, 0.02], 'Wrist L', -90, 90, 0)

# Right arm
s_yaw_R   = make_slider([0.25, 0.12, 0.65, 0.02], 'Yaw R', -180, 180, 0)
s_pitch_R = make_slider([0.25, 0.09, 0.65, 0.02], 'Pitch R', -90, 90, 0)
s_elbow_R = make_slider([0.25, 0.06, 0.65, 0.02], 'Elbow R', -150, 0, 0)
s_wrist_R = make_slider([0.25, 0.03, 0.65, 0.02], 'Wrist R', -90, 90, 0)

# Attach update
for s in [s_yaw_L, s_pitch_L, s_elbow_L, s_wrist_L,
          s_yaw_R, s_pitch_R, s_elbow_R, s_wrist_R]:
    s.on_changed(update_plot)

update_plot(None)

plt.title("Full DOF Control (Use sliders)")
plt.show()