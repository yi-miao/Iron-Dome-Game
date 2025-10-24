import pygame, math, sys, random

def compute_intercept_velocity(p_a, v_a, p_i, speed_i):
    dx = p_a[0] - p_i[0]
    dy = p_a[1] - p_i[1]
    dvx = v_a[0]
    dvy = v_a[1]

    a = dvx**2 + dvy**2 - speed_i**2
    b = 2 * (dx * dvx + dy * dvy)
    c = dx**2 + dy**2

    discriminant = b**2 - 4 * a * c
    if discriminant < 0 or a == 0:
        return None

    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    t_candidates = [t for t in [t1, t2] if t > 0]
    if not t_candidates:
        return None

    t = min(t_candidates)
    target_x = p_a[0] + dvx * t
    target_y = p_a[1] + dvy * t
    vx = (target_x - p_i[0]) / t
    vy = (target_y - p_i[1]) / t
    return [vx, vy]

class Attacker(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, target_x, sim):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = list(pos)
        self.gravity = gravity
        angle_deg = random.randint(45, 65)
        angle_rad = math.radians(angle_deg)
        range_x = target_x - pos[0]
        speed = math.sqrt(range_x * gravity / math.sin(2 * angle_rad))
        self.velocity = [speed * math.cos(angle_rad), -speed * math.sin(angle_rad)]
        self.trajectory = []
        self.satellite_timer = 0
        self.interceptor_launched = False
        self.active = True
        self.intercepted = False
        self.interception_attempted = False
        self.sim = sim  # Reference to IronDome instance
        self.hit_ground = False

    def update(self):
        if not self.active:
            return

        self.velocity[1] += self.gravity
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        self.trajectory.append(tuple(self.pos))

        # 💥 Ground impact detection
        if self.pos[1] >= self.sim.ground_y and not self.hit_ground:
            print("💥 Attacker hit the ground")
            self.active = False
            self.hit_ground = True
            self.sim.missed_impacts += 1

class Interceptor(pygame.sprite.Sprite):
    def __init__(self, pos, gravity, velocity):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.pos = list(pos)
        self.gravity = gravity
        self.velocity = velocity
        self.active = True

    def update(self):
        if not self.active:
            return

        self.velocity[1] += self.gravity
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        
class IronDome:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Iron Dome in Pygame")
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("assets/battlefield.png").convert()
        self.bg = pygame.transform.scale(self.bg, (self.WIDTH, self.HEIGHT))

        self.fireball_sheet = pygame.image.load("assets/fireball.png").convert_alpha()
        self.fireball_frames = []
        for i in range(8):
            w = self.fireball_sheet.get_width() // 8
            h = self.fireball_sheet.get_height()
            frame = self.fireball_sheet.subsurface((i * w, 0, w, h))
            self.fireball_frames.append(frame)

        self.explosion_frame_index = 0
        self.explosion_pos = None
        self.explosion_active = False

        self.launcher_pos = (100, 480)
        self.target_pos = (700, 480)
        self.satellite_pos = (400, 40)

        self.gravity = 0.5
        self.satellite_delay = 12
        self.signal_active = False
        self.signal_timer = 0
        self.signal_duration = 15

        self.attackers = pygame.sprite.Group()
        self.interceptors = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.attacker_launch_timer = 0
        self.attacker_launch_interval = random.randint(120, 240)
        
        self.attacker_objects = []
        
        self.score_success = 0
        self.score_failed = 0
        self.missed_impacts = 0
        self.ground_y = self.screen.get_height() - 50

    def launch_missile(self):
        attacker = Attacker(self.launcher_pos, self.gravity, self.target_pos[0], self)
        self.attackers.add(attacker)
        self.all_sprites.add(attacker)
        self.attacker_objects.append(attacker)
        print("🚀 Attacker launched")

    def launch_interceptor(self, attacker):
        intercept_velocity = compute_intercept_velocity(
            attacker.pos, attacker.velocity,
            self.target_pos, speed_i=15
        )
        if intercept_velocity:
            interceptor = Interceptor(self.target_pos, self.gravity, intercept_velocity)
            self.interceptors.add(interceptor)
            self.all_sprites.add(interceptor)
            print("🎯 Interceptor launched")
            self.signal_active = True
            self.signal_timer = self.signal_duration

    def draw_explosion(self):
        if self.explosion_active and self.explosion_frame_index < len(self.fireball_frames):
            frame = self.fireball_frames[self.explosion_frame_index]
            rect = frame.get_rect(center=(int(self.explosion_pos[0]), int(self.explosion_pos[1])))
            self.screen.blit(frame, rect)
            self.explosion_frame_index += 1
        elif self.explosion_active:
            self.explosion_active = False

    def draw_signal_flash(self):
        if self.signal_active and self.signal_timer > 0:
            alpha = int(255 * (self.signal_timer / self.signal_duration))
            signal_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(signal_surface, (255, 255, 0, alpha), self.satellite_pos, self.target_pos, 3)
            self.screen.blit(signal_surface, (0, 0))
            self.signal_timer -= 1
        elif self.signal_active:
            self.signal_active = False

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)

        for attacker in self.attacker_objects:
            if attacker.active and not attacker.intercepted:
                for point in attacker.trajectory:
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(point[0]), int(point[1])), 2)

        # 🧮 Score HUD
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(
            f"✅ Success: {self.score_success}  ❌ Failed: {self.score_failed}  💥 Impacts: {self.missed_impacts}",
            True, (255, 255, 255)
        )
        self.screen.blit(score_text, (10, 10))

        pygame.draw.circle(self.screen, (255, 255, 255), self.satellite_pos, 4)
        pygame.draw.circle(self.screen, (255, 0, 0), self.launcher_pos, 4)
        pygame.draw.circle(self.screen, (0, 0, 255), self.target_pos, 4)

        self.draw_signal_flash()
        self.draw_explosion()
        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.attacker_launch_timer += 1                
            if self.attacker_launch_timer >= self.attacker_launch_interval:
                for _ in range(random.randint(2, 4)):  # Launch 2–4 attackers per wave
                    self.launch_missile()
                self.attacker_launch_timer = 0
                self.attacker_launch_interval = random.randint(180, 300)

            for attacker in list(self.attackers):
                attacker.update()
                attacker.satellite_timer += 1
                if attacker.satellite_timer >= self.satellite_delay and not attacker.interceptor_launched:
                    self.launch_interceptor(attacker)
                    attacker.interceptor_launched = True

            for interceptor in list(self.interceptors):
                interceptor.update()

            for attacker in list(self.attackers):
                for interceptor in list(self.interceptors):
                    dx = attacker.pos[0] - interceptor.pos[0]
                    dy = attacker.pos[1] - interceptor.pos[1]
                    dist = math.hypot(dx, dy)

            for attacker in list(self.attackers):
                for interceptor in list(self.interceptors):
                    dx = attacker.pos[0] - interceptor.pos[0]
                    dy = attacker.pos[1] - interceptor.pos[1]
                    dist = math.hypot(dx, dy)

                    if dist < 20 and not attacker.intercepted:
                        if random.random() < 0.85:  # 85% chance of success
                            print("💥 Interception successful")
                            self.score_success += 1
                            
                            self.explosion_active = True
                            self.explosion_pos = list(attacker.pos)
                            self.explosion_frame_index = 0

                            attacker.intercepted = True
                            attacker.active = False
                            if attacker.trajectory:
                                attacker.trajectory = attacker.trajectory[:-1]

                            self.attackers.remove(attacker)
                            self.interceptors.remove(interceptor)
                            attacker.kill()
                            interceptor.kill()
                        else:
                            print("❌ Interception failed")
                            self.score_failed += 1
                            
                            if attacker.trajectory:
                                attacker.trajectory = attacker.trajectory[:-1]
                            self.interceptors.remove(interceptor)
                            interceptor.kill()

            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
                    
if __name__ == "__main__":
    app = IronDome()
    app.run()