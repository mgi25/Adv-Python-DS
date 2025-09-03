# Neon Air Hockey — Advanced 2-Player Tkinter Game
# Features: smooth physics, dash, power-ups, particles, countdown serve, pause/reset, optional AI
# Controls:
#   P1: W/A/S/D + Left Shift(dash)
#   P2: Arrow keys + Right Shift(dash)
#   Enter(serve/start), P(pause), R(reset), T(toggle AI for right)

import math, random, time
import tkinter as tk

# ------------------- Config -------------------
W, H = 1000, 600
FIELD_MARGIN = 40
GOAL_WALL = 10
MALLET_R = 36
PUCK_R = 16
BASE_SPEED = 7.0
DASH_SPEED = 15.0
DASH_TIME = 0.20  # seconds
DASH_COOLDOWN = 1.25
PUCK_FRICTION = 0.995
BOUNCE_RESTITUTION = 1.02
FRAME_DT = 1/60  # ~60 FPS
WIN_SCORE = 7
POWERUP_EVERY = (6, 9)  # seconds
MAX_PUCK_SPEED = 22.0
MIN_PUCK_SPEED = 5.0

# Colors
BG = "#0b1221"
MIDLINE = "#1f2a44"
NEON_L = "#34d399"  # left player color
NEON_R = "#60a5fa"  # right player color
NEON_PUCK = "#f8fafc"
NEON_GOAL = "#c084fc"
NEON_TEXT = "#e5e7eb"
NEON_SUB = "#a7b3cc"
NEON_PU = {
    "GROW_SELF": "#31c48d",
    "SHRINK_OPP": "#f05252",
    "PUCK_FAST": "#f59e0b",
    "PUCK_SLOW": "#60a5fa",
    "INVERT_OPP": "#eab308",
    "SHIELD_SELF": "#7c3aed",
}

# ------------------- Helpers -------------------
def clamp(v, lo, hi): return lo if v < lo else hi if v > hi else v
def length(x, y): return math.sqrt(x*x + y*y)
def norm(x, y):
    d = length(x, y)
    return (0.0, 0.0) if d == 0 else (x/d, y/d)

def now():
    return time.time()

# ------------------- Entities -------------------
class ParticleSys:
    def __init__(self, cv):
        self.cv = cv
        self.ps = []  # (id, x,y, vx,vy, life)
        self.maxp = 200

    def add_burst(self, x, y, color, n=14, speed=140):
        for _ in range(n):
            a = random.random()*2*math.pi
            v = speed*(0.5+random.random())
            vx, vy = math.cos(a)*v, math.sin(a)*v
            dot = self.cv.create_oval(x-2, y-2, x+2, y+2, fill=color, width=0)
            self.ps.append([dot, x, y, vx, vy, 0.35])
            if len(self.ps) > self.maxp:
                pid, *_ = self.ps.pop(0)
                self.cv.delete(pid)

    def add_trail(self, x, y, color, life=0.18):
        dot = self.cv.create_oval(x-2, y-2, x+2, y+2, fill=color, width=0)
        self.ps.append([dot, x, y, 0, 0, life])
        if len(self.ps) > self.maxp:
            pid, *_ = self.ps.pop(0); self.cv.delete(pid)

    def tick(self, dt):
        dead = []
        for i, p in enumerate(self.ps):
            pid, x,y, vx,vy, life = p
            life -= dt
            if life <= 0:
                dead.append(i); continue
            x += vx*dt
            y += vy*dt
            self.cv.coords(pid, x-2, y-2, x+2, y+2)
            alpha = clamp(life*3, 0, 1)
            # simulate fade with stipple change (not real alpha, but okay)
            stip = "gray50" if alpha < 0.4 else "gray25" if alpha < 0.7 else ""
            self.cv.itemconfig(pid, stipple=stipple_from_name(stip))
            p[1], p[2], p[5] = x, y, life
        for idx in reversed(dead):
            pid = self.ps[idx][0]
            self.cv.delete(pid)
            self.ps.pop(idx)

def stipple_from_name(name):
    # Tk accepts 'gray12', 'gray25', 'gray50', 'gray75' or '' for solid
    return name

class Mallet:
    def __init__(self, cv, x, y, color, side):
        self.cv = cv
        self.x, self.y = x, y
        self.vx, self.vy = 0.0, 0.0
        self.r = MALLET_R
        self.base_color = color
        self.side = side  # 'L' or 'R'
        self.invert_until = 0.0
        self.dash_until = 0.0
        self.next_dash_at = 0.0
        self.ai = False
        self.ai_target = None
        self.id_shadow = cv.create_oval(0,0,0,0, outline=color, width=10)
        self.id = cv.create_oval(0,0,0,0, fill=color, width=0)
        self.draw()

    def set_ai(self, on=True):
        self.ai = on

    def center(self): return (self.x, self.y)

    def draw(self):
        x, y, r = self.x, self.y, self.r
        self.cv.coords(self.id, x-r, y-r, x+r, y+r)
        # "glow" outline
        self.cv.coords(self.id_shadow, x-(r+6), y-(r+6), x+(r+6), y+(r+6))

    def update_input(self, keys, dt):
        if self.ai:
            self.ai_move(dt)
            return

        up = ("w" if self.side=="L" else "up") in keys
        dn = ("s" if self.side=="L" else "down") in keys
        lf = ("a" if self.side=="L" else "left") in keys
        rt = ("d" if self.side=="L" else "right") in keys
        dash_key = ("shift_l" if self.side=="L" else "shift_r") in keys

        inv = -1 if now() < self.invert_until else 1
        dx = (rt - lf) * inv
        dy = (dn - up) * inv

        spd = DASH_SPEED if now() < self.dash_until else BASE_SPEED
        self.vx, self.vy = dx*spd*60, dy*spd*60  # px/sec

        # dash trigger
        if dash_key and now() >= self.next_dash_at and (dx or dy):
            self.dash_until = now() + DASH_TIME
            self.next_dash_at = now() + DASH_COOLDOWN

    def ai_move(self, dt):
        # simple AI: track nearest puck
        target = self.ai_target() if callable(self.ai_target) else None
        if not target: return
        tx, ty = target
        dx, dy = tx - self.x, ty - self.y
        d = length(dx, dy)
        if d > 1:
            nx, ny = dx/d, dy/d
            spd = BASE_SPEED*0.95
            self.vx, self.vy = nx*spd*60, ny*spd*60
        else:
            self.vx = self.vy = 0

    def tick(self, dt, bounds):
        self.x += self.vx*dt
        self.y += self.vy*dt
        # clamp to half-field
        x0, y0, x1, y1 = bounds
        self.x = clamp(self.x, x0+self.r, x1-self.r)
        self.y = clamp(self.y, y0+self.r, y1-self.r)
        self.draw()

class Puck:
    def __init__(self, cv, x, y):
        self.cv = cv
        self.x, self.y = x, y
        a = random.uniform(-0.6, 0.6)
        self.vx = (random.choice([-1,1]) * 420.0)
        self.vy = math.tan(a) * 320.0
        self.r = PUCK_R
        self.id_shadow = cv.create_oval(0,0,0,0, outline=NEON_PUCK, width=6)
        self.id = cv.create_oval(0,0,0,0, fill=NEON_PUCK, width=0)
        self.last_touch = None  # 'L' or 'R'
        self.draw()

    def center(self): return (self.x, self.y)

    def draw(self):
        x, y, r = self.x, self.y, self.r
        self.cv.coords(self.id, x-r, y-r, x+r, y+r)
        self.cv.coords(self.id_shadow, x-(r+4), y-(r+4), x+(r+4), y+(r+4))

    def speed(self):
        return length(self.vx, self.vy)

    def clamp_speed(self):
        sp = self.speed()
        if sp > MAX_PUCK_SPEED*60:
            f = (MAX_PUCK_SPEED*60)/sp
            self.vx *= f; self.vy *= f
        elif sp < MIN_PUCK_SPEED*60:
            f = (MIN_PUCK_SPEED*60)/max(sp,1)
            self.vx *= f; self.vy *= f

    def tick(self, dt, top, bottom):
        self.x += self.vx*dt
        self.y += self.vy*dt

        # wall bounces
        if self.y < top + self.r:
            self.y = top + self.r
            self.vy = abs(self.vy) * BOUNCE_RESTITUTION
        elif self.y > bottom - self.r:
            self.y = bottom - self.r
            self.vy = -abs(self.vy) * BOUNCE_RESTITUTION

        # friction
        self.vx *= PUCK_FRICTION
        self.vy *= PUCK_FRICTION

        self.clamp_speed()
        self.draw()

    def collide_mallet(self, m: Mallet, psys: ParticleSys):
        # circle-circle collision
        dx = self.x - m.x
        dy = self.y - m.y
        dist = length(dx, dy)
        overlap = (self.r + m.r) - dist
        if overlap > 0:
            nx, ny = norm(dx, dy)
            # separate puck out of mallet
            self.x += nx * (overlap + 0.5)
            self.y += ny * (overlap + 0.5)

            # relative velocity along normal
            rvx = self.vx - m.vx
            rvy = self.vy - m.vy
            vn = rvx * nx + rvy * ny
            if vn < 0:
                j = -(1.05) * vn  # restitution
                self.vx += j * nx
                self.vy += j * ny

            # add "impulse" from mallet motion
            self.vx += 0.25 * m.vx
            self.vy += 0.25 * m.vy

            self.last_touch = m.side
            self.clamp_speed()
            psys.add_burst(self.x, self.y, NEON_PUCK, n=10, speed=180)
            return True
        return False

# ------------------- PowerUps -------------------
class PowerUp:
    TYPES = ("GROW_SELF","SHRINK_OPP","PUCK_FAST","PUCK_SLOW","INVERT_OPP","SHIELD_SELF")
    LABEL = {
        "GROW_SELF": "+P",
        "SHRINK_OPP": "-O",
        "PUCK_FAST": "F+",
        "PUCK_SLOW": "F-",
        "INVERT_OPP": "INV",
        "SHIELD_SELF": "SHD",
    }
    def __init__(self, cv, x, y, kind=None):
        self.cv = cv
        self.kind = kind or random.choice(PowerUp.TYPES)
        self.x, self.y = x, y
        self.r = 16
        c = NEON_PU[self.kind]
        self.id = cv.create_oval(x-self.r, y-self.r, x+self.r, y+self.r, fill=c, width=0)
        self.tx = cv.create_text(x, y, text=PowerUp.LABEL[self.kind], fill="#0b1221", font=("Segoe UI", 10, "bold"))

    def remove(self):
        self.cv.delete(self.id); self.cv.delete(self.tx)

    def hit_by(self, puck: Puck):
        dx = puck.x - self.x
        dy = puck.y - self.y
        return length(dx, dy) <= (puck.r + self.r)

# ------------------- Game -------------------
class Game:
    def __init__(self, root):
        self.root = root
        root.title("Neon Air Hockey — Tkinter")
        self.cv = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
        self.cv.pack()

        # Field: center line & goals
        self.cv.create_line(W/2, FIELD_MARGIN, W/2, H-FIELD_MARGIN, fill=MIDLINE, dash=(10,10), width=2)
        self.left_goal = self.cv.create_rectangle(0, FIELD_MARGIN, GOAL_WALL, H-FIELD_MARGIN, fill=NEON_GOAL, width=0)
        self.right_goal= self.cv.create_rectangle(W-GOAL_WALL, FIELD_MARGIN, W, H-FIELD_MARGIN, fill=NEON_GOAL, width=0)

        # Shields (inactive)
        self.left_shield = None
        self.right_shield = None
        self.left_shield_until = 0.0
        self.right_shield_until = 0.0

        # Players
        self.left = Mallet(self.cv, W*0.25, H*0.5, NEON_L, "L")
        self.right = Mallet(self.cv, W*0.75, H*0.5, NEON_R, "R")

        # Puck
        self.puck = Puck(self.cv, W/2, H/2)

        # Particles
        self.psys = ParticleSys(self.cv)

        # HUD
        self.hud = self.cv.create_text(W/2, 40, fill=NEON_TEXT, font=("Segoe UI", 22, "bold"))
        self.sub = self.cv.create_text(W/2, 70, fill=NEON_SUB, font=("Segoe UI", 12))
        self.score_id = self.cv.create_text(W/2, 110, fill=NEON_TEXT, font=("Consolas", 28, "bold"))

        # State
        self.state = "menu"  # menu|serve|play|paused|over
        self.serve_to = random.choice(["L","R"])
        self.lscore = 0
        self.rscore = 0
        self.keys = set()
        self.countdown_until = 0.0
        self.power = None
        self.schedule_next_power()

        # Bounds per side
        self.left_bounds  = (FIELD_MARGIN, FIELD_MARGIN, W/2 - 20, H-FIELD_MARGIN)
        self.right_bounds = (W/2 + 20, FIELD_MARGIN, W-FIELD_MARGIN, H-FIELD_MARGIN)

        # AI targeting
        self.right.ai_target = lambda: self.puck.center()

        # Input
        root.bind("<KeyPress>", self.on_key)
        root.bind("<KeyRelease>", self.on_key)

        self.update_hud()
        self.loop()

    # ---------- UI ----------
    def update_hud(self, msg=None, sub=None):
        if msg is None:
            if self.state=="menu": msg="Neon Air Hockey"
            elif self.state=="serve": msg="Get Ready..."
            elif self.state=="play": msg=""
            elif self.state=="paused": msg="Paused"
            elif self.state=="over": msg="Game Over"
        if sub is None:
            if self.state=="menu":
                sub="WASD + Shift (P1) | Arrow Keys + Shift (P2) — Enter: Start/Serve  •  P: Pause  •  R: Reset  •  T: AI Toggle"
            elif self.state=="paused": sub="Press P to resume"
            elif self.state=="over": sub="Press R to restart"
            else: sub=""
        self.cv.itemconfigure(self.hud, text=msg)
        self.cv.itemconfigure(self.sub, text=sub)
        self.cv.itemconfigure(self.score_id, text=f"{self.lscore}  :  {self.rscore}")

    # ---------- Input ----------
    def on_key(self, e):
        is_down = (e.type == "2")  # KeyPress
        k = e.keysym.lower()
        if is_down: self.keys.add(k)
        else: self.keys.discard(k)

        if is_down and k == "return":
            if self.state in ("menu","serve"):
                self.start_countdown()
        if is_down and k == "p" and self.state in ("play","paused"):
            self.state = "paused" if self.state=="play" else "play"
            self.update_hud()
        if is_down and k == "r":
            self.reset()
        if is_down and k == "t":
            self.right.set_ai(not self.right.ai)
            self.flash_message(f"AI {'ON' if self.right.ai else 'OFF'} for Right")

    def flash_message(self, text, ms=1000):
        tip = self.cv.create_text(W/2, H-28, text=text, fill=NEON_TEXT, font=("Segoe UI", 12))
        self.root.after(ms, lambda: self.cv.delete(tip))

    def start_countdown(self):
        self.state = "serve"
        self.countdown_until = now() + 3.0  # 3..2..1
        self.update_hud()

    # ---------- PowerUps ----------
    def schedule_next_power(self):
        delay = random.randint(*POWERUP_EVERY)
        self.root.after(int(delay*1000), self.spawn_power)

    def spawn_power(self):
        if self.state != "play" or self.power is not None:
            self.schedule_next_power(); return
        x = random.randint(int(W*0.35), int(W*0.65))
        y = random.randint(int(H*0.25), int(H*0.75))
        self.power = PowerUp(self.cv, x, y)
        self.schedule_next_power()

    def apply_power(self, owner_side, kind):
        mine = self.left if owner_side=="L" else self.right
        opp  = self.right if owner_side=="L" else self.left
        if kind=="GROW_SELF":
            mine.r = clamp(mine.r+6, 26, 60)
        elif kind=="SHRINK_OPP":
            opp.r = clamp(opp.r-6, 26, 60)
        elif kind=="PUCK_FAST":
            self.puck.vx *= 1.25; self.puck.vy *= 1.25
        elif kind=="PUCK_SLOW":
            self.puck.vx *= 0.8; self.puck.vy *= 0.8
        elif kind=="INVERT_OPP":
            opp.invert_until = now() + 3.5
        elif kind=="SHIELD_SELF":
            if owner_side=="L":
                self.left_shield_until = now() + 5.0
            else:
                self.right_shield_until = now() + 5.0
        mine.draw(); opp.draw()
        self.puck.clamp_speed()

    # ---------- Scoring & Serve ----------
    def score(self, who):  # who scored the point
        if who=="L": self.lscore += 1
        else: self.rscore += 1
        self.update_hud()
        self.psys.add_burst(self.puck.x, self.puck.y, NEON_PUCK, n=28, speed=240)
        # reset puck
        self.cv.delete(self.puck.id); self.cv.delete(self.puck.id_shadow)
        self.puck = Puck(self.cv, W/2, H/2)
        # stop shields that expired
        self.state = "over" if (self.lscore>=WIN_SCORE or self.rscore>=WIN_SCORE) else "serve"
        self.serve_to = "R" if who=="L" else "L"
        if self.state != "over":
            self.start_countdown()
        else:
            self.update_hud()

    # ---------- Reset ----------
    def reset(self):
        self.lscore = self.rscore = 0
        self.left.x, self.left.y, self.left.r = W*0.25, H*0.5, MALLET_R
        self.right.x, self.right.y, self.right.r = W*0.75, H*0.5, MALLET_R
        self.left.invert_until = self.right.invert_until = 0.0
        self.left.draw(); self.right.draw()
        self.cv.delete(self.puck.id); self.cv.delete(self.puck.id_shadow)
        self.puck = Puck(self.cv, W/2, H/2)
        if self.power: self.power.remove(); self.power = None
        self.left_shield_until = self.right_shield_until = 0.0
        self.state = "menu"
        self.update_hud()

    # ---------- Shields ----------
    def shields_tick(self):
        # draw/remove shield visuals
        nowt = now()
        # Left shield
        if nowt < self.left_shield_until:
            if not self.left_shield:
                self.left_shield = self.cv.create_rectangle(GOAL_WALL+4, FIELD_MARGIN+40, GOAL_WALL+10, H-FIELD_MARGIN-40,
                                                            fill="#7c3aed", width=0)
        else:
            if self.left_shield: self.cv.delete(self.left_shield); self.left_shield = None
        # Right shield
        if nowt < self.right_shield_until:
            if not self.right_shield:
                self.right_shield = self.cv.create_rectangle(W-GOAL_WALL-10, FIELD_MARGIN+40, W-GOAL_WALL-4, H-FIELD_MARGIN-40,
                                                            fill="#7c3aed", width=0)
        else:
            if self.right_shield: self.cv.delete(self.right_shield); self.right_shield = None

        # puck bounce off shields
        if self.left_shield and self.puck.x - self.puck.r <= GOAL_WALL+10:
            if FIELD_MARGIN+40 <= self.puck.y <= H-FIELD_MARGIN-40:
                self.puck.x = GOAL_WALL+10 + self.puck.r + 1
                self.puck.vx = abs(self.puck.vx)*BOUNCE_RESTITUTION
        if self.right_shield and self.puck.x + self.puck.r >= W-GOAL_WALL-10:
            if FIELD_MARGIN+40 <= self.puck.y <= H-FIELD_MARGIN-40:
                self.puck.x = W-GOAL_WALL-10 - self.puck.r - 1
                self.puck.vx = -abs(self.puck.vx)*BOUNCE_RESTITUTION

    # ---------- Main Loop ----------
    def loop(self):
        dt = FRAME_DT

        # countdown serve numbers
        if self.state == "serve":
            tleft = self.countdown_until - now()
            n = math.ceil(tleft)
            if tleft <= 0:
                self.state = "play"
                # direct puck toward receiver
                if self.serve_to == "L":
                    self.puck.vx = -abs(self.puck.vx)
                else:
                    self.puck.vx = abs(self.puck.vx)
                self.update_hud()
            else:
                self.cv.itemconfigure(self.hud, text=str(n))

        if self.state == "play":
            # controls
            self.left.update_input(self.keys, dt)
            self.right.update_input(self.keys, dt)

            # move players
            self.left.tick(dt, self.left_bounds)
            self.right.tick(dt, self.right_bounds)

            # puck physics
            self.puck.tick(dt, FIELD_MARGIN, H-FIELD_MARGIN)

            # particles trail
            self.psys.add_trail(self.puck.x, self.puck.y, NEON_PUCK)

            # collisions with mallets
            self.puck.collide_mallet(self.left, self.psys)
            self.puck.collide_mallet(self.right, self.psys)

            # powerup spawn/hit
            if self.power and self.power.hit_by(self.puck):
                owner = self.puck.last_touch or random.choice(["L","R"])
                self.apply_power(owner, self.power.kind)
                self.power.remove(); self.power = None

            # shields tick
            self.shields_tick()

            # goals (if puck fully crosses)
            if self.puck.x - self.puck.r <= GOAL_WALL:
                if not (self.left_shield and FIELD_MARGIN+40 <= self.puck.y <= H-FIELD_MARGIN-40):
                    self.score("R")
            elif self.puck.x + self.puck.r >= W-GOAL_WALL:
                if not (self.right_shield and FIELD_MARGIN+40 <= self.puck.y <= H-FIELD_MARGIN-40):
                    self.score("L")

        # paused/menu/over: still animate particles & shields visuals
        self.psys.tick(dt)
        self.shields_tick()

        # update score readout every frame
        self.cv.itemconfigure(self.score_id, text=f"{self.lscore}  :  {self.rscore}")

        self.root.after(int(FRAME_DT*1000), self.loop)

# ------------------- Run -------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
