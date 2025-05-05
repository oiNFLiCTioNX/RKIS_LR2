import random
import math
import village

class Player:
    def __init__(self, name, player_class, health, stamina, armor, damage, defending):
        self.name = name
        self.player_class = player_class
        self.max_health = int(health)
        self.health = self.max_health
        self.max_stamina = int(stamina)
        self.stamina = self.max_stamina
        self.armor = int(armor)
        self.damage = int(damage)
        self.defending = bool(defending)
        self.defending_armor = int(self.armor * 1.25)
        self.x = 1  # Начальная координата X
        self.y = 1  # Начальная координата Y

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if game_map[new_y][new_x] == '.':
            self.x = new_x
            self.y = new_y
            health_restored = int(self.max_health * 0.01)
            stamina_restored = int(self.max_stamina * 0.05)
            self.health = min(self.health + health_restored, self.max_health)
            self.stamina = min(self.stamina + stamina_restored, self.max_stamina)
            print(f"{self.name} восстановил здоровье: {health_restored}, Восстановил выносливость: {stamina_restored}")
        elif game_map[new_y][new_x] == 'E':
            self.x = new_x
            self.y = new_y
            combat_cycle(player, enemies)
        elif game_map[new_y][new_x] == 'H':
            if int(input("Вы подошли к хижине. Выберите действие: 1 - войти, 2 - уйти: ")) == 1:
                print(f"Кажется, дверь закрыта!")
        elif game_map[new_y][new_x] == '!':
            if int(input("Вы подошли к жителю деревни. Выберите действие: 1 - взять задание, 2 - уйти: ")) == 1:
                quest_acquire(quests)
                self.x = new_x
                self.y = new_y
        elif game_map[new_y][new_x] == '>':
            if int(input("Вы нашли переход. Выберите действие: 1 - перейти на следующую локацию, 2 - вернуться: ")) == 1:
                print(f"PODVAL")        
        elif game_map[new_y][new_x] == 'H!':
            if int(input("Вы подошли к хижине с подвалом. Выберите действие: 1 - войти в подвал, 2 - уйти: ")) == 1:
                print(f"PODVAL")
        elif game_map[new_y][new_x] == 'W':
            if int(input("Вы подошли к колодцу. Выберите действие: 1 - испить воды, 2 - уйти: ")) == 1:
                w_health_restored = int(self.max_health * 0.25)
                w_stamina_restored = int(self.max_stamina * 0.25)
                print(f"{self.name} утолил жажду и восстановил {w_health_restored} здоровья и {w_stamina_restored} выносливости.")
                self.health = min(self.health + w_health_restored, self.max_health)
                self.stamina = min(self.stamina + w_stamina_restored, self.max_stamina)
        

    def attack(self, enemy):
        stamina_used = int(self.damage * 0.1)
        damage_dealt = self.damage - enemy.get_damage_reduction(self.damage)
        if damage_dealt > 0:
            enemy.take_damage(damage_dealt)
            self.stamina -= stamina_used
        print(f"{self.name} нанес {damage_dealt} урона {enemy.name} и использовал {stamina_used} выносливости.")

    def defend(self):
        self.defending = True
        health_restored = int(self.max_health * 0.05)
        stamina_restored = int(self.max_stamina * 0.1)
        self.health = min(self.health + health_restored, self.max_health)
        self.stamina = min(self.stamina + stamina_restored, self.max_stamina)
        print(f"{self.name} защищается! Восстановлено здоровья: {health_restored}, Восстановлена выносливость: {stamina_restored}")

    def take_damage(self, damage):
        if self.defending:
            damage_received = int(damage - self.get_damage_reduction_defending(damage))
        else:
            damage_received = int(damage - self.get_damage_reduction(damage))
        if damage_received > 0:
            self.health -= damage_received
        print(f"{self.name} получил {damage_received} урона.")
        if self.health <= 0:
            self.health = 0

    def get_damage_reduction(self, damage):
        k = 0.1  # Коэффициент уменьшающейся эффективности
        return int(damage * (1 - math.exp(-k * self.armor)))

    def get_damage_reduction_defending(self, damage):
        k = 0.1  # Коэффициент уменьшающейся эффективности
        return int(damage * (1 - math.exp(-k * self.defending_armor)))

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return (f"Имя игрока: {self.name}\n"
                f"Класс игрока: {self.player_class}\n"
                f"Здоровье игрока: {self.health}/{self.max_health}\n"
                f"Выносливость игрока: {self.stamina}/{self.max_stamina}\n"
                f"Броня игрока: {self.armor}\n"
                f"Урон игрока: {self.damage}")

class Enemy:
    def __init__(self, name, health, armor, damage):
        self.name = name
        self.max_health = int(health)
        self.health = self.max_health
        self.armor = int(armor)
        self.damage = int(damage)
        self.x = 0
        self.y = 0

    def attack(self, player):
        damage_dealt = self.damage
        if damage_dealt > 0:
            player.take_damage(damage_dealt)
        print(f"{self.name} нанес {damage_dealt} урона {player.name}.")

    def take_damage(self, damage):
        damage_received = damage - self.get_damage_reduction(damage)
        if damage_received > 0:
            self.health -= damage_received
        print(f"{self.name} получил {damage_received} урона.")
        if self.health <= 0:
            self.health = 0

    def get_damage_reduction(self, damage):
        k = 0.1  # Коэффициент уменьшающейся эффективности
        return int(damage * (1 - math.exp(-k * self.armor)))

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return (f"Имя врага: {self.name}\n"
                f"Здоровье врага: {self.health}/{self.max_health}\n"
                f"Броня врага: {self.armor}\n"
                f"Урон врага: {self.damage}")

def place_player_on_map(player, game_map):
    game_map[player.y][player.x] = 'P'

def place_enemies_on_map(enemies, game_map):
    for enemy in enemies:
        placed = False
        while not placed:
            x = random.randint(1, len(game_map[0]) - 2)
            y = random.randint(1, len(game_map) - 2)
            if game_map[y][x] == '.':
                game_map[y][x] = 'E'
                enemy.x = x
                enemy.y = y
                placed = True

def print_map(map_, player_info):
    max_map_height = len(map_)
    player_info_lines = player_info.split('\n')
    max_info_height = len(player_info_lines)
    for i in range(max_map_height):
        map_row = ''.join(map_[i])
        info_row = player_info_lines[i] if i < max_info_height else ''
        print(f"{map_row} | {info_row}")

def clear_player_from_map(player, game_map):
    game_map[player.y][player.x] = '.'

def clear_enemy_from_map(enemy, game_map):
    game_map[enemy.y][enemy.x] = '.'

def choose_class():
    classes = {
        1: {'name': 'рыцарь', 'health': 250, 'stamina': 20, 'armor': 7, 'damage': 100},
        2: {'name': 'варвар', 'health': 500, 'stamina': 50, 'armor': 2, 'damage': 100},
        3: {'name': 'самурай', 'health': 150, 'stamina': 35, 'armor': 5, 'damage': 130}
    }
    print("Выберите класс:")
    for key, cls in classes.items():
        print(f"{key}. {cls['name']}")
    while True:
        try:
            choice = int(input("Введите номер класса: ").strip())
            if choice in classes:
                return classes[choice]['name'], classes[choice]
            else:
                print("Неверный номер класса, попробуйте снова.")
        except ValueError:
            print("Введите число.")

def generate_enemies(width, height, num_enemies):
    enemies = []
    for _ in range(num_enemies):
        enemy_type = random.choice(['орк', 'гоблин', 'тролль'])
        if enemy_type == 'орк':
            enemies.append(Enemy(name='Орк', health=500, armor=4, damage=95))
        elif enemy_type == 'гоблин':
            enemies.append(Enemy(name='Гоблин', health=300, armor=2, damage=80))
        elif enemy_type == 'тролль':
            enemies.append(Enemy(name='Тролль', health=700, armor=6, damage=110))
    return enemies

def combat_cycle(player, enemies):
    for enemy in enemies[:]:  # Используем enemies[:] для итерации по копии списка
            if enemy.x == player.x and enemy.y == player.y:
                print(f"\nВы встретили {enemy.name}!")
                while player.is_alive() and enemy.is_alive():
                    player_info = str(player)
                    enemy_info = str(enemy)
                    player_info_lines = player_info.split('\n')
                    enemy_info_lines = enemy_info.split('\n')
                    max_player_info_height = len(player_info_lines)
                    max_enemy_info_height = len(enemy_info_lines)
                    for i in range(max(max_player_info_height, max_enemy_info_height)):
                        player_info_row = player_info_lines[i] if i < max_player_info_height else ''
                        enemy_info_row = enemy_info_lines[i] if i < max_enemy_info_height else ''
                        print(f"{player_info_row} | {enemy_info_row}")
                    action = input(f"Введите действие (a - атаковать, d - защищаться, r - убежать): ").strip().lower()
                    if action == 'a':
                        player.attack(enemy)
                        if enemy.is_alive():
                            enemy.attack(player)
                    elif action == 'r':
                        print(f"{player.name} сбежал от {enemy.name}.")
                        break
                    elif action == 'd':
                        print(f"{player.name} защищается от атак {enemy.name}. Временная броня: +{player.defending_armor - player.armor}.")
                        player.defend()
                        enemy.attack(player)
                        player.defending = False
                    else:
                        print("Неизвестное действие")
                    if not player.is_alive():
                        print(f"{player.name} проиграл.")
                        exit()
                    elif not enemy.is_alive():
                        print(f"{player.name} победил {enemy.name}!")
                        clear_enemy_from_map(enemy, game_map)
                        enemies.remove(enemy)
                        break

def quest_acquire(quests):
    for i in range(len(quests)):
        if not quests[i]:
            quests[i] = True
            print(f"Квест {i+1} выдан!")
            return quests
    print("У жителя больше нет заданий!")
    return quests

if __name__ == "__main__":
    game_map = village.load_village()
    width = len(game_map[0]) - 2  # Учитываем границы карты
    height = len(game_map) - 2  # Учитываем границы карты
    
    quests = [False, False, False]
    
    # Выбор класса игрока
    player_class, bonuses = choose_class()
    
    # Создание игрока с бонусами
    player = Player(
        name=input("Введите имя игрока: "),
        player_class=player_class,
        health=500 + bonuses['health'],
        stamina=100 + bonuses['stamina'],
        armor=5 + bonuses['armor'],
        damage=20 + bonuses['damage'],
        defending=False
    )
    
    # Генерация врагов
    num_enemies = 5
    enemies = generate_enemies(width, height, num_enemies)
    
    # Размещение игрока и врагов на карте
    place_player_on_map(player, game_map)
    place_enemies_on_map(enemies, game_map)

    # Основной цикл игры
    while True:
        player_info = str(player)
        print_map(game_map, player_info)

        command = input("Введите команду (w/a/s/d для движения, q для выхода): ").strip().lower()
        if command == 'q':
            break
        elif command == 'w':
            clear_player_from_map(player, game_map)
            player.move(0, -1, game_map)
            place_player_on_map(player, game_map)
        elif command == 'a':
            clear_player_from_map(player, game_map)
            player.move(-1, 0, game_map)
            place_player_on_map(player, game_map)
        elif command == 's':
            clear_player_from_map(player, game_map)
            player.move(0, 1, game_map)
            place_player_on_map(player, game_map)
        elif command == 'd':
            clear_player_from_map(player, game_map)
            player.move(1, 0, game_map)
            place_player_on_map(player, game_map)
        else:
            print("Неизвестная команда")
        
        # Очистка экрана для обновления карты
#        print("\033[H\033[J", end="")