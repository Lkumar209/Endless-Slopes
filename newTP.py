from cmu_graphics import *
import math
import random
import time

class Weather:
    def __init__(self, width, height):
        
        self.clouds = []
        self.cloudSpeeds = [0.2, 0.4, 0.6]
        self.cloudLayers = 3
        self.width = width
        self.height = height
        
        
        for layer in range(self.cloudLayers):
            for _ in range(4):
                x = random.randint(0, width)
                y = 30 + layer * 30
                width_cloud = random.randint(60, 100)
                height_cloud = random.randint(30, 50)
                self.clouds.append([x, y, width_cloud, height_cloud, layer])
        
        
        self.dayTime = 0
        self.daySpeed = 0.9
        self.sunX = width
        self.sunY = 50
        self.isNight = False
        self.isRaining = False
        self.timeSinceNight = 0
        self.nightDuration = 600
        
        
        self.raindrops = []
        self.maxRaindrops = 100
        self.transitionDuration = 300  
        self.transitionProgress = 0    
        self.isTransitioning = False
        self.transitionType = None 

        self.dayColor = rgb(135, 206, 235)    
        self.nightColor = rgb(50, 50, 100)    
        self.sunsetColor = rgb(255, 150, 50)  
        self.horizonColor = rgb(220, 240, 255)  
        
    def lerp(self, start, end, t):
        return start + (end - start) * t
    
    def createRaindrop(self):
        x = random.randint(0, self.width)
        y = random.randint(-50, 0)
        speed = random.randint(5, 10)
        return [x, y, speed]
    

    def updateDayNightCycle(self):
        self.sunX -= self.daySpeed
        
        
        if self.sunX < 400 and not self.isNight and not self.isTransitioning:
            self.isTransitioning = True
            self.transitionType = 'sunset'
            self.transitionProgress = 0
        
        
        if self.timeSinceNight >= self.nightDuration and self.isNight and not self.isTransitioning:
            self.isTransitioning = True
            self.transitionType = 'sunrise'
            self.transitionProgress = 0
        
        
        if self.isTransitioning:
            self.transitionProgress += 1/self.transitionDuration
            
            if self.transitionProgress >= 1:
                self.isTransitioning = False
                if self.transitionType == 'sunset':
                    self.isNight = True
                    self.isRaining = True
                    self.timeSinceNight = 0
                else:  
                    self.sunX = self.width + 30
                    self.isNight = False
                    self.isRaining = False
                    self.timeSinceNight = 0
        
        if self.isNight:
            self.timeSinceNight += 1
    
    def updateRain(self):
        if self.isRaining:
            if len(self.raindrops) < self.maxRaindrops:
                self.raindrops.append(self.createRaindrop())
            
            for drop in self.raindrops:
                drop[1] += drop[2]
            
            self.raindrops = [drop for drop in self.raindrops if drop[1] < self.height]
    
    def updateClouds(self, velocity_x):
        for cloud in self.clouds:
            cloud[0] -= self.cloudSpeeds[cloud[4]] * velocity_x
            if cloud[0] + cloud[2] < 0:
                cloud[0] = self.width + cloud[2]
                cloud[1] = 30 + cloud[4] * 30 + random.randint(-10, 10)
                cloud[2] = random.randint(60, 100)
                cloud[3] = random.randint(30, 50)
    
    def draw(self):
        
        dayColor = (135, 206, 235)     
        nightColor = (50, 50, 100)     
        sunsetColor = (255, 150, 50)   

        if self.isTransitioning:
            if self.transitionType == 'sunset':
                
                if self.transitionProgress < 0.5:
                    
                    progress = self.transitionProgress * 2
                    skyColor = rgb(
                        int(self.lerp(dayColor[0], sunsetColor[0], progress)),
                        int(self.lerp(dayColor[1], sunsetColor[1], progress)),
                        int(self.lerp(dayColor[2], sunsetColor[2], progress))
                    )
                else:
                    
                    progress = (self.transitionProgress - 0.5) * 2
                    skyColor = rgb(
                        int(self.lerp(sunsetColor[0], nightColor[0], progress)),
                        int(self.lerp(sunsetColor[1], nightColor[1], progress)),
                        int(self.lerp(sunsetColor[2], nightColor[2], progress))
                    )
            else:  
                if self.transitionProgress < 0.5:
                    
                    progress = self.transitionProgress * 2
                    skyColor = rgb(
                        int(self.lerp(nightColor[0], sunsetColor[0], progress)),
                        int(self.lerp(nightColor[1], sunsetColor[1], progress)),
                        int(self.lerp(nightColor[2], sunsetColor[2], progress))
                    )
                else:
                    
                    progress = (self.transitionProgress - 0.5) * 2
                    skyColor = rgb(
                        int(self.lerp(sunsetColor[0], dayColor[0], progress)),
                        int(self.lerp(sunsetColor[1], dayColor[1], progress)),
                        int(self.lerp(sunsetColor[2], dayColor[2], progress))
                    )
        else:
            
            skyColor = rgb(
                max(50, min(135, 135 - (self.isNight * 85))),
                max(50, min(206, 206 - (self.isNight * 156))),
                max(100, min(235, 235 - (self.isNight * 135)))
            )

            

        drawRect(0, 0, self.width, self.height, fill=skyColor)

        
        if not self.isNight:
            sunOpacity = 100
            if self.isTransitioning:
                if self.transitionType == 'sunset':
                    sunOpacity = 100 * (1 - self.transitionProgress)
                elif self.transitionType == 'sunrise':
                    sunOpacity = 100 * self.transitionProgress
            
            
            for r in range(60, 20, -10):
                drawCircle(self.sunX, self.sunY, r, 
                        fill=rgb(255, 255, 200), opacity=15 * sunOpacity/100)
            
            drawCircle(self.sunX, self.sunY, 25, 
                    fill=rgb(255, 255, 220), opacity=90 * sunOpacity/100)
            drawCircle(self.sunX, self.sunY, 20, 
                    fill=rgb(255, 255, 240), opacity=sunOpacity)

        
        for cloud in self.clouds:
            x, y, width, height, layer = cloud
            cloudOpacity = 90 - (layer * 10)
            
            
            drawOval(x, y, width, height, fill='white', opacity=cloudOpacity)
            
            drawOval(x + width*0.2, y - height*0.2, width*0.6, height*0.8, 
                    fill='white', opacity=cloudOpacity)
            
            drawOval(x + width*0.1, y + height*0.1, width*0.4, height*0.6, 
                    fill='white', opacity=cloudOpacity-10)
            drawOval(x + width*0.5, y + height*0.2, width*0.4, height*0.5, 
                    fill='white', opacity=cloudOpacity-10)

        
        if self.isRaining:
            rainOpacity = 100
            if self.isTransitioning:
                if self.transitionType == 'sunrise':
                    rainOpacity = 100 * (1 - self.transitionProgress)
                elif self.transitionType == 'sunset':
                    rainOpacity = 100 * self.transitionProgress
            
            for drop in self.raindrops:
                drawLine(drop[0], drop[1],
                        drop[0], drop[1] + 10,
                        fill='lightBlue', lineWidth=1,
                        opacity=rainOpacity)


class OptimizedSnowboardingGame:
    def __init__(self, width=1200, height=800):
        
        self.width = width
        self.height = height
        
        
        self.seed = random.randint(0, 10000)
        self.terrain_cache = {}
        self.terrain_width = width * 2

        self.flip_speed = 0.30  
        self.flip_direction = 0  
        self.total_rotation = 0  
        self.max_safe_landing_angle = 45  

        self.trees = []  
        self.tree_spacing = 100
        self.tree_chance = 0.5
        self.last_tree_x = 0  


        
        
        self.sky_color = rgb(135, 206, 235)
        self.terrain_base = rgb(255, 255, 255)  
        self.terrain_shadow = rgb(230, 230, 230)  
        self.terrain_highlight = rgb(255, 255, 255)  
        self.weather = Weather(width, height)
        self.screens = Screens(width, height, self)
        self.currentScreen = 'start'

        
        
        self.init_game_state()
        
        
        self.terrain = self.generate_terrain(0, self.terrain_width)

        
        
        self.generate_trees(self.terrain)
    
    def init_game_state(self):
        
        self.rider_width = 40
        self.rider_height = 40
        self.rider_x = 200
        self.rider_y = self.height // 3
        
        
        self.gravity = 0.8       
        self.air_gravity = 0.9    
        self.velocity_x = 32      
        self.velocity_y = 0
        
        
        self.ground_friction = 0.995  
        self.air_resistance = 0.995   
        self.max_speed = 40           
        self.base_speed = 28     
        self.snap_distance = 12
        
        
        self.jump_force = -15
        self.jump_cooldown = 0
        self.max_jump_cooldown = 10
        
        
        self.is_grounded = False
        self.on_curve = False
        self.char_angle = 0
        self.camera_x = 0

        self.jump_buffer_time = 0
        self.coyote_time = 0
        self.MAX_JUMP_BUFFER = 5
        self.MAX_COYOTE_TIME = 5
        self.game_over = False

        self.coins = []
        self.coin_width = 20
        self.coin_height = 20
        self.score = 0
        self.coin_spacing = 400  
        self.last_coin_x = 0
        self.coin_cache = {}  

        self._rotation_cache = {}
        self._terrain_cache = {}
        self.MAX_CACHE_SIZE = 1000

        self.frame_times = []
        self.last_frame_time = time.time()
        self.fps = 0
        self.difficulty = 'easy'
        
        
        if len(self._terrain_cache) > self.MAX_CACHE_SIZE:
            self._terrain_cache.clear()


    def generate_coins(self, terrain):
        while self.last_coin_x < len(terrain) - self.coin_spacing:
            if random.random() < 0.2:  
                num_coins = random.randint(3, 5)  
                base_y = self.height - terrain[int(self.last_coin_x)]
                
                for i in range(num_coins):
                    x = self.last_coin_x + i * 40  
                    y = base_y - 50
                    self.coins.append([x, y, True])
            
            self.last_coin_x += self.coin_spacing

    def resetGame(app):
        
        app.gameOver = False
        app.maxLandingAngle = 45  
        app.currentScreen = 'start'
        
        
        app.charWidth = 30
        app.charHeight = 40
        app.charX = 20
        app.charY = 150
        app.charAngle = 0
        
        
        app.gravity = 0.8
        app.airGravity = 0.9
        app.friction = 0.0003
        app.maxSpeed = 25
        app.baseSpeed = 15
        app.velocityX = app.baseSpeed
        app.velocityY = 0
        app.onCurve = False
        
        
        app.snowboarderWidth = 40
        app.snowboarderHeight = 50
        
        
        app.clouds = []
        app.cloudSpeeds = [0.2, 0.4, 0.6]
        app.cloudLayers = 3
        
        
        for layer in range(app.cloudLayers):
            for _ in range(4):
                x = random.randint(0, 400)
                y = 30 + layer * 30
                width = random.randint(60, 100)
                height = random.randint(30, 50)
                app.clouds.append([x, y, width, height, layer])
        
        
        app.dayTime = 0
        app.daySpeed = 0.5
        app.sunX = 1200
        app.sunY = 50
        app.isNight = False
        app.isRaining = False
        app.timeSinceNight = 0
        app.nightDuration = 300
        
        
        app.raindrops = []
        app.maxRaindrops = 100
        
        
        app.trees = []
        app.treeSpacing = 100
        app.treeChance = 0.3
        app.treeWidth = 20
        app.treeHeight = 30
        
        
        app.buttonWidth = 200
        app.buttonHeight = 50    
    
    def lerp(self, start, end, t):
        """function for linear interpolation"""
        return start + (end - start) * t
    
    
    def generate_terrain(self, start_x, width):
        terrain = [self.height / 2] * width
        


        seed_multipliers = [
            (self.seed, 800, 150),
            (self.seed * 2, 400, 80),
            (self.seed * 3, 300, 60)
        ]

        for x in range(width):
            adjusted_x = x + start_x
            terrain[x] += sum(
                math.sin((adjusted_x + seed) / freq) * amplitude
                for seed, freq, amplitude in seed_multipliers
            )
        
        
        for i in range(1, len(terrain)):
            terrain[i] = (terrain[i] + terrain[i-1]) / 2
        
        return terrain
    
    def get_terrain_height(self, x):
        cache_key = int(x)
        
        
        if cache_key in self.terrain_cache:
            return self.terrain_cache[cache_key]
        
        
        x = max(0, min(x, len(self.terrain) - 2))
        
        
        index = int(x)
        t = x - index
        height = self.lerp(self.terrain[index], self.terrain[index + 1], t)
        
        
        self.terrain_cache[cache_key] = height
        return height
    
    def get_terrain_normal(self, x):
        h1 = self.get_terrain_height(x - 1)
        h2 = self.get_terrain_height(x + 1)
        dx = 2
        dy = h2 - h1
        
        
        length = math.hypot(dx, dy)
        return (-dy/length, dx/length)
    

    def extend_terrain(self):
        if self.rider_x + self.width > len(self.terrain):
            new_segment = self.generate_terrain(len(self.terrain), self.width//2) 
            self.terrain.extend(new_segment)
            self.generate_trees(self.terrain)  
            
    def update_physics(self):
        current_time = time.time()
        dt = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        self.frame_times.append(dt)
        if len(self.frame_times) > 30:  
            self.frame_times.pop(0)
        
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = int(1 / avg_frame_time)
        
        self.camera_x = self.rider_x - 200
        
        
        self.jump_cooldown = max(0, self.jump_cooldown - 1)
        
        
        terrain_height = self.get_terrain_height(self.rider_x)
        ground_y = self.height - terrain_height
        
        if not self.on_curve:
            
            self.velocity_y += self.air_gravity
            self.rider_y += self.velocity_y
            self.rider_x += self.velocity_x
            
            
            if self.flip_direction != 0:
                self.char_angle += self.flip_speed * self.flip_direction
                self.total_rotation += self.flip_speed * self.flip_direction
            
            
            if self.rider_y + self.rider_height / 2 > ground_y - self.snap_distance and self.velocity_y > 0:
                landing_angle = math.degrees(self.char_angle) % 360
                if landing_angle > 180:
                    landing_angle = landing_angle - 360
                landing_angle = abs(landing_angle)
                
                if landing_angle > 135:  
                    self.rider_y = ground_y - self.rider_height / 2
                    self.game_over = True
                elif landing_angle < 45:  
                    self.rider_y = ground_y - self.rider_height / 2
                    self.on_curve = True
                    self.char_angle = 0
                    self.total_rotation = 0
                else:  
                    self.rider_y = ground_y - self.rider_height / 2
                    self.game_over = True
        else:
            
            next_height = self.get_terrain_height(self.rider_x + self.velocity_x)
            dx = self.velocity_x
            dy = terrain_height - next_height
            
            
            target_angle = math.atan2(dy, dx)
            
            
            self.char_angle = self.lerp(self.char_angle, target_angle, 0.15)
            
            
            slope_effect = math.sin(target_angle)
            self.velocity_x += self.gravity * slope_effect
            self.velocity_x *= (1 - self.ground_friction)
            self.velocity_x = max(self.base_speed, min(self.velocity_x, self.max_speed))
            
            
            self.rider_x += self.velocity_x
            self.rider_y = ground_y - self.rider_height / 2

        if not self.game_over:
            
            visible_start = self.camera_x - 100
            visible_end = self.camera_x + self.width + 100
            
            
            nearby_coins = [coin for coin in self.coins 
                        if coin[2] and visible_start <= coin[0] <= visible_end]
            
            
            for coin in nearby_coins:
                dx = self.rider_x - coin[0]
                dy = self.rider_y - coin[1]
                
                if dx * dx + dy * dy < (self.coin_width * 1.5) ** 2:
                    coin[2] = False
                    self.score += 10

        self.extend_terrain()
        self.weather.updateDayNightCycle()
        self.weather.updateRain()
        self.weather.updateClouds(self.velocity_x)

    def handleScreenClick(self, mouseX, mouseY):
        buttonX = self.width//2 - 150  
        
        if self.currentScreen == 'start':
            if (buttonX <= mouseX <= buttonX + 300 and 350 <= mouseY <= 410):
                self.currentScreen = 'menu'
            elif (buttonX <= mouseX <= buttonX + 300 and 430 <= mouseY <= 490):
                self.currentScreen = 'help'
            elif (buttonX <= mouseX <= buttonX + 300 and 510 <= mouseY <= 570):
                pass  
        
        elif self.currentScreen == 'menu':
            if (buttonX <= mouseX <= buttonX + 300 and 350 <= mouseY <= 410):
                self.currentScreen = 'game'
                self.init_game_state()
            elif (buttonX <= mouseX <= buttonX + 300 and 430 <= mouseY <= 490):
                self.currentScreen = 'modes'
            elif (buttonX <= mouseX <= buttonX + 300 and 510 <= mouseY <= 570):
                self.currentScreen = 'start'
        
        elif self.currentScreen == 'help':
            if (buttonX <= mouseX <= buttonX + 300 and 700 <= mouseY <= 760):
                self.currentScreen = 'start'
        
        elif self.currentScreen == 'modes':
            if (buttonX <= mouseX <= buttonX + 300 and 280 <= mouseY <= 360):
                self.difficulty = 'easy'
                self.currentScreen = 'menu'
            elif (buttonX <= mouseX <= buttonX + 300 and 380 <= mouseY <= 460):
                self.difficulty = 'medium'
                self.currentScreen = 'menu'
            elif (buttonX <= mouseX <= buttonX + 300 and 480 <= mouseY <= 560):
                self.difficulty = 'hard'
                self.currentScreen = 'menu'
            elif (buttonX <= mouseX <= buttonX + 300 and 600 <= mouseY <= 660):
                self.currentScreen = 'menu'
        
        elif self.currentScreen == 'crash':
            if (buttonX <= mouseX <= buttonX + 300 and 400 <= mouseY <= 460):
                self.currentScreen = 'start'
                self.init_game_state()  
                self.game_over = False  
            elif (buttonX <= mouseX <= buttonX + 300 and 480 <= mouseY <= 540):
                pass 

    def draw(self):
        if self.currentScreen == 'start':
            self.screens.drawStartScreen()
        elif self.currentScreen == 'menu':
            self.screens.drawMenuScreen()
        elif self.currentScreen == 'help':
            self.screens.drawHelpScreen()
        elif self.currentScreen == 'modes':
            self.screens.drawModesScreen() 
        elif self.currentScreen == 'crash':
            self.screens.drawCrashScreen(self.score)
        else:
            
            drawRect(0, 0, self.width, self.height, fill=self.sky_color)
            self.weather.draw()
            
            
            start_x = int(self.camera_x)
            end_x = min(start_x + self.width + 1, len(self.terrain))
            step = 4  
            
            for i in range(start_x, end_x, step):
                if i >= len(self.terrain) - step:
                    break
                    
                screen_x = i - start_x
                height = self.terrain[i]
                next_height = self.terrain[min(i + step, len(self.terrain) - 1)]
                
                
                drawPolygon(
                    screen_x, self.height - height,
                    screen_x + step, self.height - next_height,
                    screen_x + step, self.height,
                    screen_x, self.height,
                    fill='white'
                )
                
                
                if i % 120 == 0:
                    drawLine(
                        screen_x, self.height - height,
                        screen_x, self.height,
                        fill=self.terrain_highlight,
                        lineWidth=2
                    )
            visible_start = self.camera_x - self.coin_width
            visible_end = self.camera_x + self.width + self.coin_width
            
            
            camera_offset = self.camera_x
            coin_half_width = self.coin_width / 2
            coin_half_height = self.coin_height / 2
            
            
            visible_coins = [coin for coin in self.coins 
                            if coin[2] and visible_start <= coin[0] <= visible_end]
            
            for coin in visible_coins:
                screen_x = coin[0] - camera_offset
                drawImage('coin.png',
                        screen_x - coin_half_width,
                        coin[1] - coin_half_height,
                        width=self.coin_width,
                        height=self.coin_height)
            
            self.draw_trees(self.camera_x)
            
            
            screen_x = self.rider_x - self.camera_x
            drawImage('newSnowboarder.png',
                    screen_x - self.rider_width/2,
                    self.rider_y - self.rider_height/2,
                    width=self.rider_width,
                    height=self.rider_height,
                    rotateAngle=math.degrees(self.char_angle))
            
            drawLabel(f'FPS: {self.fps}', 50, 20, 
                size=16, bold=True, fill='white')
            
            if self.game_over:
                drawRect(0, 0, self.width, self.height,
                        fill='black', opacity=50)
                drawLabel('GAME OVER', self.width/2, self.height/2,
                        size=64, bold=True, fill='white')
                drawLabel('Press E to Exit', self.width/2, self.height/2 + 80,
                        size=32, fill='white')



    def handle_flip(self, keys):
        if not self.on_curve:
            if 'left' in keys:
                self.flip_direction = -1
            elif 'right' in keys:
                self.flip_direction = 1
            else:
                self.flip_direction = 0
    
    def handle_jump(self, keys):
       
        
        if 'space' in keys:
            self.jump_buffer_time = self.MAX_JUMP_BUFFER
        else:
            self.jump_buffer_time = max(0, self.jump_buffer_time - 1)
        
        
        can_jump = (
            (self.on_curve and self.jump_cooldown == 0) or  
            (self.coyote_time > 0 and self.jump_cooldown == 0)  
        )
        
        
        if self.jump_buffer_time > 0 and can_jump:
            self.velocity_y = self.jump_force
            self.on_curve = False
            self.jump_cooldown = self.max_jump_cooldown
            self.char_angle = 0
            self.jump_buffer_time = 0
            self.coyote_time = 0
    
 
    def interpolate_color(self, color1, color2, t):
        return rgb(
            int(self.lerp(color1.red, color2.red, t)),
            int(self.lerp(color1.green, color2.green, t)),
            int(self.lerp(color1.blue, color2.blue, t))
        )
    

    def generate_trees(self, terrain):
       
        while self.last_tree_x < len(terrain):
            if random.random() < self.tree_chance:
                
                terrain_y = self.height - terrain[int(self.last_tree_x)]  
                self.trees.append(('small', self.last_tree_x, terrain_y))
            
            
            if random.random() < 0.05:  
                terrain_y = self.height - terrain[int(self.last_tree_x)]  
                self.trees.append(('large', self.last_tree_x, terrain_y))
            
            self.last_tree_x += self.tree_spacing  


    def draw_trees(self, camera_x):
       
        for tree_type, x, y in self.trees:
            screen_x = x - camera_x
            if -self.tree_spacing <= screen_x <= self.width + self.tree_spacing:  
                self.draw_tree(screen_x, y, tree_type)

    def draw_tree(self, x, y, tree_type="small"):
        
        if tree_type == "small":
            trunk_width = 8
            trunk_height = 30
            drawRect(x - trunk_width // 2, y - trunk_height, trunk_width, trunk_height, fill="saddleBrown")

            
            for i in range(3):
                layer_height = 40 - i * 10
                layer_width = 30 - i * 8
                drawPolygon(
                    x, y - trunk_height - layer_height,
                    x - layer_width // 2, y - trunk_height - i * 10,
                    x + layer_width // 2, y - trunk_height - i * 10,
                    fill="darkGreen"
                )
        
        elif tree_type == "large":
            trunk_width = 20  
            trunk_height = 50  
            drawRect(x - trunk_width // 2, y - trunk_height, trunk_width, trunk_height + 3, fill="saddleBrown")
            
            
            for i in range(4):
                layer_height = 60 - i * 15
                layer_width = 50 - i * 12
                drawPolygon(
                    x, y - trunk_height - layer_height,
                    x - layer_width // 2, y - trunk_height - i * 15,
                    x + layer_width // 2, y - trunk_height - i * 15,
                    fill="darkGreen"
                )

class Screens:
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.buttonWidth = 200
        self.buttonHeight = 50
        self.game = game
    
    def lerp(self, start, end, t):
        """Linear interpolation helper function"""
        return start + (end - start) * t
        
    def drawStartScreen(self):
        skyColor = rgb(200, 220, 235)
        drawRect(0, 0, self.width, self.height, fill=skyColor)
        
        
        drawLabel('Endless Slopes', self.width//2 + 3, 203, 
                size=80, bold=True, fill='grey', opacity=50)  
        drawLabel('Endless Slopes', self.width//2, 200, 
                size=80, bold=True, fill='white')
        
        
        drawLabel('Conquer the Mountains, Master the Slopes', 
                self.width//2, 280, size=24, italic=True, fill='white')
        
        
        buttonWidth = 300  
        buttonHeight = 60  
        buttonX = self.width//2 - buttonWidth//2  
        
        
        drawRect(buttonX, 350, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('PLAY', self.width//2, 380, size=32, bold=True, fill='white')
        
        drawRect(buttonX, 430, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('HELP', self.width//2, 460, size=32, bold=True, fill='white')
        
        drawRect(buttonX, 510, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('QUIT', self.width//2, 540, size=32, bold=True, fill='white')
        
        
        for x in range(-20, self.width + 20, 40):
            drawPolygon(x, self.height, x+20, 750, x+40, self.height, 
                    fill='darkGreen')
        
        
        if not hasattr(self, 'snowflakes'):
            self.snowflakes = []
            for _ in range(100):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                self.snowflakes.append([x, y])
        #MAKE FUNCTION FOR THIS
        for snowflake in self.snowflakes:
            snowflake[0] += random.randint(-1, 1)
            snowflake[1] += random.randint(1, 3)
            
            if snowflake[1] > self.height:
                snowflake[1] = 0
                snowflake[0] = random.randint(0, self.width)
            
            drawCircle(snowflake[0], snowflake[1], 2, fill='white')

    def drawMenuScreen(self):
        skyColor = rgb(200, 220, 235)
        drawRect(0, 0, self.width, self.height, fill=skyColor)
        
        
        drawLabel('Endless Slopes', self.width//2 + 3, 203, 
                size=80, bold=True, fill='grey', opacity=50)  
        drawLabel('Endless Slopes', self.width//2, 200, 
                size=80, bold=True, fill='white')
        
        
        drawLabel('Conquer the Mountains, Master the Slopes', 
                self.width//2, 280, size=24, italic=True, fill='white')
        
        
        buttonWidth = 300  
        buttonHeight = 60  
        buttonX = self.width//2 - buttonWidth//2  
        
        
        drawRect(buttonX, 350, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('BEGIN GAME', self.width//2, 380, 
                size=32, bold=True, fill='white')
        
        drawRect(buttonX, 430, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('MODES', self.width//2, 460, 
                size=32, bold=True, fill='white')
        
        drawRect(buttonX, 510, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('BACK', self.width//2, 540, 
                size=32, bold=True, fill='white')
        
        
        drawLabel(f'You are in {self.game.difficulty} mode', 
                150, self.height - 100, 
                size=20, bold=True, fill='white')
        
        
        for x in range(-20, self.width + 20, 40):
            drawPolygon(x, self.height, x+20, 750, x+40, self.height, 
                    fill='darkGreen')
        
        
        for snowflake in self.snowflakes:
            snowflake[0] += random.randint(-1, 1)  
            snowflake[1] += random.randint(1, 3)   
            
            if snowflake[1] > self.height:
                snowflake[1] = 0
                snowflake[0] = random.randint(0, self.width)
            
            drawCircle(snowflake[0], snowflake[1], 2, fill='white')
    
    def drawHelpScreen(self):
        
        skyColor = rgb(200, 220, 235)
        drawRect(0, 0, self.width, self.height, fill=skyColor)
        
        
        drawLabel('HOW TO PLAY', self.width/2, 80, size=64, bold=True, fill='white')
        
        
        drawLabel('CONTROLS', self.width/2, 180, size=36, bold=True, fill='white')
        drawLabel('SPACE - Press to jump, hold longer for higher jumps', self.width/2, 220, size=20, fill='white')
        drawLabel('LEFT ARROW - Hold to perform backflips in the air', self.width/2, 250, size=20, fill='white')
        drawLabel('RIGHT ARROW - Hold to perform frontflips in the air', self.width/2, 280, size=20, fill='white')
        drawLabel('R - Press to restart after game over', self.width/2, 310, size=20, fill='white')
        
        
        drawLabel('GAMEPLAY', self.width/2, 380, size=36, bold=True, fill='white')
        drawLabel('• Build speed by riding down slopes', self.width/2, 420, size=20, fill='white')
        drawLabel('• Collect coins to increase your score', self.width/2, 450, size=20, fill='white')
        drawLabel('• Perform tricks for style points', self.width/2, 480, size=20, fill='white')
        
        
        drawLabel('TIPS & TRICKS', self.width/2, 550, size=36, bold=True, fill='white')
        drawLabel('• Land straight to avoid crashing', self.width/2, 590, size=20, fill='white')
        drawLabel('• Avoid landing upside down or at sharp angles', self.width/2, 620, size=20, fill='white')
        drawLabel('• Use slopes to gain momentum for bigger jumps', self.width/2, 650, size=20, fill='white')
        
        
        drawRect(500, 700, self.buttonWidth, self.buttonHeight, 
                fill=None, border='white', borderWidth=2)
        drawLabel('BACK', self.width/2, 725, size=24, bold=True, fill='white')
        
        
        for x in range(-20, self.width + 20, 40):
            drawPolygon(x, self.height, x+20, self.height-50, x+40, self.height, 
                    fill='darkGreen')
        
        if not hasattr(self, 'snowflakes'):
            self.snowflakes = []
            for _ in range(100):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                self.snowflakes.append([x, y])
        
        
        for snowflake in self.snowflakes:
            snowflake[0] += random.randint(-1, 1)  
            snowflake[1] += random.randint(1, 3)   
            
            if snowflake[1] > self.height:
                snowflake[1] = 0
                snowflake[0] = random.randint(0, self.width)
            
            drawCircle(snowflake[0], snowflake[1], 2, fill='white')
    def drawCrashScreen(self, score):
        
        skyColor = rgb(200, 220, 235)
        drawRect(0, 0, self.width, self.height, fill=skyColor)
        
        
        drawLabel('GAME OVER', self.width//2, 150, 
                size=100, bold=True, fill='white')
        
        
        drawLabel(f'Your Score: {score}', self.width//2, 300, 
                size=40, fill='white')
        
        
        buttonWidth = 300
        buttonHeight = 60
        buttonX = self.width//2 - buttonWidth//2
        
        
        drawRect(buttonX, 400, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('START AGAIN', self.width//2, 430, 
                size=32, bold=True, fill='white')
        
        
        drawRect(buttonX, 480, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('QUIT', self.width//2, 510, 
                size=32, bold=True, fill='white')
        
        
        for x in range(-20, self.width + 20, 40):
            drawPolygon(x, self.height, x+20, 750, x+40, self.height, 
                    fill='darkGreen')
        
        
        for snowflake in self.snowflakes:
            snowflake[0] += random.randint(-1, 1)  
            snowflake[1] += random.randint(1, 3)   
            
            if snowflake[1] > self.height:
                snowflake[1] = 0
                snowflake[0] = random.randint(0, self.width)
            
            drawCircle(snowflake[0], snowflake[1], 2, fill='white')
    
    def drawModesScreen(self):
        
        skyColor = rgb(200, 220, 235)
        drawRect(0, 0, self.width, self.height, fill=skyColor)
        
        drawLabel('SELECT DIFFICULTY', self.width//2 + 3, 153, 
                size=64, bold=True, fill='grey', opacity=50)
        drawLabel('SELECT DIFFICULTY', self.width//2, 150, 
                size=64, bold=True, fill='white')
        
        
        drawLabel('Choose your terrain style:', self.width//2, 230, 
                size=24, italic=True, fill='white')
        
        
        buttonWidth = 300
        buttonHeight = 80
        buttonX = self.width//2 - buttonWidth//2
        
        
        drawRect(buttonX, 280, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('EASY', self.width//2, 305, size=32, bold=True, fill='white')
        drawLabel('Gentle slopes, smooth terrain', self.width//2, 335, 
                size=20, fill='white')
        
        
        drawRect(buttonX, 380, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('MEDIUM', self.width//2, 405, size=32, bold=True, fill='white')
        drawLabel('Balanced mix of slopes', self.width//2, 435, 
                size=20, fill='white')
        
        
        drawRect(buttonX, 480, buttonWidth, buttonHeight, 
                fill=None, border='white', borderWidth=3)
        drawLabel('HARD', self.width//2, 505, size=32, bold=True, fill='white')
        drawLabel('Steep slopes, challenging terrain', self.width//2, 535, 
                size=20, fill='white')
        
        
        drawRect(buttonX, 600, buttonWidth, buttonHeight-20, 
                fill=None, border='white', borderWidth=3)
        drawLabel('BACK', self.width//2, 630, size=32, bold=True, fill='white')
        
        
        for x in range(-20, self.width + 20, 40):
            drawPolygon(x, self.height, x+20, 750, x+40, self.height, 
                    fill='darkGreen')
        
        
        for snowflake in self.snowflakes:
            snowflake[0] += random.randint(-1, 1)  
            snowflake[1] += random.randint(1, 3)   
            
            if snowflake[1] > self.height:
                snowflake[1] = 0
                snowflake[0] = random.randint(0, self.width)
            
            drawCircle(snowflake[0], snowflake[1], 2, fill='white')

def onAppStart(app):
    app.game = OptimizedSnowboardingGame(app.width, app.height)

def onStep(app):
    if not app.game.game_over:  
        app.game.update_physics()

def onKeyHold(app, keys):
    app.game.handle_jump(keys)
    app.game.handle_flip(keys)

def onKeyPress(app, key):
    if key == 'e' and app.game.game_over:
        app.game.currentScreen = 'crash'

def onMousePress(app, mouseX, mouseY):
    app.game.handleScreenClick(mouseX, mouseY)

def redrawAll(app):
    app.game.draw()


runApp(width=1200, height=800)


'''
Citations:
Snowboarder: https://depositphotos.com/vectors/skiboard.html?qview=563929798

https://www.geeksforgeeks.org/how-to-implement-linear-interpolation-in-python/

 Matt DesL (@mattdesl). "Linear interpolation (lerp) is one of the most fundamental building blocks of animation and graphics programming." Twitter, Aug 19, 2018.
2
 GeeksforGeeks. "How to implement linear interpolation in Python?" GeeksforGeeks, May 10, 2022.
https://x.com/mattdesl/status/1031305279227478016?prefetchTimestamp=1733176692934

'''
