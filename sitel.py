import pygame
import math
import sys

# تنظیمات پنجره
WIDTH, HEIGHT = 800, 600
FPS = 60
BG_COLOR = (30, 30, 30)
HEX_COLOR = (100, 200, 100)
BALL_COLOR = (200, 100, 100)
HEX_RADIUS = 200
BALL_RADIUS = 10
GRAVITY = 0.5
FRICTION = 0.99
RESTITUTION = 0.8
ROTATION_SPEED = 1  # درجه بر فریم

# مقداردهی اولیه Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0

def draw_hexagon(surface, color, radius, angle):
    center = (WIDTH//2, HEIGHT//2)
    points = []
    for i in range(6):
        theta = math.radians(60 * i + angle)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    pygame.draw.lines(surface, color, True, points, 2)

def distance_point_to_line(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1), (x1, y1)
    t = ((px - x1)*dx + (py - y1)*dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    dist = math.hypot(px - closest_x, py - closest_y)
    return dist, (closest_x, closest_y)

def check_collision(ball, hex_radius, angle):
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    collision = False
    
    for i in range(6):
        theta1 = math.radians(60 * i + angle)
        x1 = center_x + hex_radius * math.cos(theta1)
        y1 = center_y + hex_radius * math.sin(theta1)
        
        theta2 = math.radians(60 * (i+1) + angle)
        x2 = center_x + hex_radius * math.cos(theta2)
        y2 = center_y + hex_radius * math.sin(theta2)
        
        dist, closest = distance_point_to_line(ball.x, ball.y, x1, y1, x2, y2)
        if dist < ball.radius:
            dx = x2 - x1
            dy = y2 - y1
            nx = -dy
            ny = dx
            vec_to_center = (center_x - closest[0], center_y - closest[1])
            dot = vec_to_center[0] * nx + vec_to_center[1] * ny
            if dot < 0:
                nx = -nx
                ny = -ny
            length = math.hypot(nx, ny)
            if length == 0:
                continue
            nx /= length
            ny /= length
            
            dir_x = closest[0] - center_x
            dir_y = closest[1] - center_y
            tangent_x = -dir_y
            tangent_y = dir_x
            length_tangent = math.hypot(tangent_x, tangent_y)
            if length_tangent == 0:
                v_wall_x = 0
                v_wall_y = 0
            else:
                tangent_x /= length_tangent
                tangent_y /= length_tangent
                omega = math.radians(ROTATION_SPEED)
                v_wall = omega * math.hypot(dir_x, dir_y)
                v_wall_x = tangent_x * v_wall
                v_wall_y = tangent_y * v_wall
            
            rel_vx = ball.vx - v_wall_x
            rel_vy = ball.vy - v_wall_y
            dot_velocity = rel_vx * nx + rel_vy * ny
            
            if dot_velocity < 0:
                j = -(1 + RESTITUTION) * dot_velocity
                new_rel_vx = rel_vx + j * nx
                new_rel_vy = rel_vy + j * ny
                tangent_vel = new_rel_vx * (-ny) + new_rel_vy * nx
                tangent_vel *= 0.9
                new_rel_vx = tangent_vel * (-ny)
                new_rel_vy = tangent_vel * nx
                ball.vx = new_rel_vx + v_wall_x
                ball.vy = new_rel_vy + v_wall_y
                overlap = ball.radius - dist
                ball.x += nx * overlap
                ball.y += ny * overlap
                collision = True
                break
    return collision

# ایجاد توپ و تنظیمات اولیه
ball = Ball(WIDTH//2, HEIGHT//2 - 100, BALL_RADIUS)
current_angle = 0

# حلقه اصلی
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # اعمال گرانش و اصطکاک
    ball.vy += GRAVITY
    ball.vx *= FRICTION
    ball.vy *= FRICTION
    ball.x += ball.vx
    ball.y += ball.vy
    
    # به‌روزرسانی زاویه چرخش
    current_angle += ROTATION_SPEED
    current_angle %= 360
    
    # بررسی برخورد
    check_collision(ball, HEX_RADIUS, current_angle)
    
    # رسم اجزای بازی
    screen.fill(BG_COLOR)
    draw_hexagon(screen, HEX_COLOR, HEX_RADIUS, current_angle)
    pygame.draw.circle(screen, BALL_COLOR, (int(ball.x), int(ball.y)), BALL_RADIUS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()