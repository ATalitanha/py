import pygame
import pymunk
import pymunk.pygame_util
import math

# تنظیمات اولیه
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)

# ایجاد شش ضلعی در حال گردش
hexagon_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
hexagon_shape = pymunk.Poly.create_box(hexagon_body, (100, 100), 0.5)
hexagon_shape.elasticity = 1.0
space.add(hexagon_body, hexagon_shape)

# ایجاد توپ
ball_body = pymunk.Body(mass=1, moment=10)
ball_body.position = (300, 100)
ball_shape = pymunk.Circle(ball_body, radius=10)
ball_shape.elasticity = 0.9
space.add(ball_body, ball_shape)

def draw_hexagon(surface, body, shape):
    points = shape.get_vertices()
    points = [body.position + p.rotated(body.angle) for p in points]
    points = [(int(p.x), int(p.y)) for p in points]
    pygame.draw.polygon(surface, (0, 255, 0), points)

# چرخش شش ضلعی
def rotate_hexagon(body, angle):
    body.angle += angle

# حلقه اصلی
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # رسم شش ضلعی
    draw_hexagon(screen, hexagon_body, hexagon_shape)

    # رسم توپ
    pygame.draw.circle(screen, (0, 0, 255), (int(ball_body.position.x), int(ball_body.position.y)), 10)

    # بروز رسانی فیزیک
    rotate_hexagon(hexagon_body, 0.05)
    space.step(1/60.0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
