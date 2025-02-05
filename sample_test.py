import pygame
import pymunk
import pymunk.pygame_util
import math

# تنظیمات اولیه
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)  # گرانش به سمت پایین

# تنظیمات شش‌ضلعی
num_sides = 6
radius = 200
center = (width // 2, height // 2)
angle_offset = 0  # زاویه چرخش شش‌ضلعی

# ایجاد شش‌ضلعی
def create_hexagon(center, radius, num_sides, angle_offset):
    points = []
    for i in range(num_sides):
        angle = 2 * math.pi * i / num_sides + angle_offset
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points

# اضافه کردن دیواره‌های شش‌ضلعی به فضای فیزیکی
def add_hexagon_walls(space, center, radius, num_sides, angle_offset):
    points = create_hexagon(center, radius, num_sides, angle_offset)
    for i in range(num_sides):
        p1 = points[i]
        p2 = points[(i + 1) % num_sides]
        segment = pymunk.Segment(space.static_body, p1, p2, 5)
        segment.elasticity = 0.8  # کشسانی برخورد
        segment.friction = 0.5    # اصطکاک
        space.add(segment)

# اضافه کردن توپ به فضای فیزیکی
def add_ball(space, position, radius, mass):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9  # کشسانی برخورد
    shape.friction = 0.7    # اصطکاک
    space.add(body, shape)
    return body

# ایجاد شش‌ضلعی و توپ
add_hexagon_walls(space, center, radius, num_sides, angle_offset)
ball = add_ball(space, (center[0], center[1] - 100), 20, 10)

# تنظیمات نمایش
draw_options = pymunk.pygame_util.DrawOptions(screen)

# حلقه اصلی
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # چرخش شش‌ضلعی
    angle_offset += 0.01
    space.remove(space.static_body)  # حذف دیواره‌های قبلی
    add_hexagon_walls(space, center, radius, num_sides, angle_offset)

    # به‌روزرسانی فیزیک
    space.step(1 / 60.0)

    # رسم صحنه
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()