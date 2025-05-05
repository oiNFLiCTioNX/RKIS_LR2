import random
import math
import village
import basement
import lake
import forest

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

    def move(self, dx, dy, game_map, map_type, player, enemies):
     new_x = self.x + dx
     new_y = self.y + dy

     # Проверка границы карты
     if not (0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map)):
        print("Невозможно выйти за пределы карты.")
        return game_map, map_type, enemies
     
     # Логика для разных объектов
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
            for index, enemy in enumerate(enemies[:]):
             if enemy.x == self.x and enemy.y == self.y:
              combat_cycle(self, enemy)
              break
     elif game_map[new_y][new_x] == '!':
            if input("Вы подошли к жителю деревни. Выберите действие: 1 - взять задание, 2 - уйти: ") == '1':
                quest_acquire(quests)
                self.x = new_x
                self.y = new_y
     elif game_map[new_y][new_x] == 'W':
            if (input("Вы подошли к колодцу. Выберите действие: 1 - испить водицы, 2 - уйти: ")) == '1':
             w_health_restored = int(self.max_health * 0.25)
             w_stamina_restored = int(self.max_stamina * 0.25)
             print(f"{self.name} утолил жажду и восстановил {w_health_restored} здоровья и {w_stamina_restored} выносливости.")
             self.health = min(self.health + w_health_restored, self.max_health)
             self.stamina = min(self.stamina + w_stamina_restored, self.max_stamina)
     elif game_map[new_y][new_x] == 'H':
            if input("Вы подошли к хижине. Выберите действие: 1 - войти, 2 - уйти: ") == '1':
             print("Закрыто!")
     elif game_map[new_y][new_x] == 'T':
            if input("Вы подошли к дереву. Выберите действие: 1 - осмотреть, 2 - уйти: ") == '1':
             print("Перед вами стоит величественная сосна.")
     elif game_map[new_y][new_x] == 'P':
            if input("Вы подошли к себе. Выберите действие: 1 - поговорить, 2 - уйти: ") == '1':
             self.x = new_x
             self.y = new_y
             print(f"Ах, это же ты, {self.name}! Постой, кажется ты не должен был меня видеть..")
             print("\x1B[3m ВЫ БЫЛИ ПОГЛОЩЕНЫ СВОЕЙ КОПИЕЙ \x1B[0m")
     elif game_map[new_y][new_x] == 'H!':
            if input("Вы подошли к хижине с подвалом. Выберите действие: 1 - войти в подвал, 2 - уйти: ") == '1':
                if quests == [True, True, True]:
                 self.x = 1
                 self.y = 1
                 game_map, map_type, enemies = change_location(game_map, player, enemies, 'basement')
                else:
                 print("Вы еще не взяли все задания!")
     elif game_map[new_y][new_x] == '[]':
            if input("Вы нашли выход. Выберите действие: 1 - выйти к озеру, 2 - вернуться: ") == '1':
                global q1_rat_count
                if q1_rat_count >= q1_rat_task:
                    quests_done[0] = True
                clear_player_from_map(player, game_map)
                game_map, map_type, enemies = change_location(game_map, player, enemies, 'lake')
                self.x = 2
                self.y = 5
     elif game_map[new_y][new_x] == 'R':
            self.x = new_x
            self.y = new_y
            if input("Вы подошли к крысе. Выберите действие: 1 - убить, 2 - пощадить: ") == '1':
                q1_rat_count += 1
                if random.randint(1,2) == 1:
                    print(f"Вы с лёгкостью давите крысу! Осталось по заданию: {q1_rat_task - q1_rat_count}.")
                else:
                    print(f"Вы еле убиваете крысу и она успевает вас поцарапать на 10 здоровья! Осталось по заданию: {q1_rat_task - q1_rat_count}.")
                    self.health -= 10
                    if self.health < 1:
                        print("Вы погибли от крысы! Какой позор!")
                        exit()
                if q1_rat_count >= q1_rat_task and quests_done[0] is False:
                    quests_done[0] = True
                    print("Первое задание успешно выполнено!")
            else:
                print(f"Крыса убегает с противным писком! Осталось по заданию: {q1_rat_task - q1_rat_count}.")
     elif game_map[new_y][new_x] == 'O':
            if input("Вы подошли к воде. Выберите действие: 1 - умыться, 2 - вернуться: ") == '1':
                w_health_restored = int(self.max_health * 0.25)
                w_stamina_restored = int(self.max_stamina * 0.25)
                print(f"{self.name} утолил жажду и восстановил {w_health_restored} здоровья и {w_stamina_restored} выносливости.")
                self.health = min(self.health + w_health_restored, self.max_health)
                self.stamina = min(self.stamina + w_stamina_restored, self.max_stamina)
     elif game_map[new_y][new_x] == 'F':
            if input("Вы нашли травы по заданию 2. Выберите действие: 1 - собрать, 2 - вернуться: ") == '1':
                self.x = new_x
                self.y = new_y
                global q2_herb_count
                q2_herb_count += 1
                fake_random = 3
                if random.randint(1,10) < fake_random:
                  enemies.append(Enemy(name='Фея', health=300, armor=2, damage=150))
                  combat_cycle(self, enemies[-1])
                else: fake_random += 1
     elif game_map[new_y][new_x] == '>':
            if input("Вы нашли проход в лес. Выберите действие: 1 - двигаться дальше, 2 - вернуться: ") == '1':
                if q2_herb_count >= q2_herb_task:
                    quests_done[1] = True
                clear_player_from_map(player, game_map)
                game_map, map_type, enemies = change_location(game_map, player, enemies, 'forest')
                forest.generate_trees(game_map)
                self.x = 1
                self.y = 6
     elif game_map[new_y][new_x] == '^':
            if input("Вы нашли выход из леса. Выберите действие: 1 - выйти и завершить игру, 2 - вернуться: ") == '1':
                global q3_kill_count
                if q3_kill_count >= q3_kill_task:
                    quests_done[2] = True
                if quests_done == [True, True, True]:
                    print("Хорошая работа! Вы выполнили все задания заработали много шекелей от жителей деревни!")
                    print(r"""
                                   /\\_/\\
                                   ( o.o )
                                    > ^ <
                                 __// _ \\__
                                / _  ___  _ \\
                               (_/_(/___\\)_\\)
                                               """)
                    endwait = input("Введите любой символ...")
                    quit()
                else:
                    print("Вы выжили, но не выполнили все задания! Плохая концовка!")
                    endwait = input("Введите любой символ...")
                    quit()

     else:
        print("Нельзя зайти на эту клетку.")

     return game_map, map_type, enemies
        

    def attack(self, enemy):
        stamina_used = int(self.damage * 0.1)
        damage_dealt = self.damage - enemy.get_damage_reduction(self.damage)
        if damage_dealt > 0 and self.stamina > stamina_used:
            enemy.take_damage(damage_dealt)
            self.stamina -= stamina_used
            print(f"{self.name} нанес {damage_dealt} урона {enemy.name} и использовал {stamina_used} выносливости.")
        else:
            print("Вы слишком слабы для нанесения удара врагу!")
        

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
        3: {'name': 'самурай', 'health': 150, 'stamina': 35, 'armor': 5, 'damage': 130},
        4: {'name': 'чит', 'health': 9999, 'stamina': 9999, 'armor': 0, 'damage': 9999},
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
        if map_type != 'basement':
            enemy_type = random.choice(['орк', 'гоблин', 'тролль'])
            if enemy_type == 'орк':
                enemies.append(Enemy(name='Орк', health=500, armor=4, damage=95))
            elif enemy_type == 'гоблин':
                enemies.append(Enemy(name='Гоблин', health=300, armor=2, damage=80))
            elif enemy_type == 'тролль':
                enemies.append(Enemy(name='Тролль', health=700, armor=6, damage=110))
    return enemies

def combat_cycle(player, enemy):
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
                    action = input(f"Введите действие (a - атаковать, d - защищаться): ").strip().lower()
                    if action == 'a':
                        player.attack(enemy)
                        if enemy.is_alive():
                            enemy.attack(player)
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
                        global q3_kill_count
                        q3_kill_count += 1
                        break

def quest_acquire(quests):
    for i in range(len(quests)):
        if not quests[i]:
            quests[i] = True
            print(f"Квест {i+1} выдан!")
            return quests
    print("У жителя больше нет заданий!")
    return quests

def change_location(game_map, player, enemies, map_type):
    if map_type == 'basement':
        game_map = basement.load_basement()
        map_type = 'basement'
        width = len(game_map[0]) - 2
        height = len(game_map) - 2
        enemies = generate_enemies(width, height, num_enemies=0)
        place_player_on_map(player, game_map)
        place_enemies_on_map(enemies, game_map)
        return game_map, map_type, enemies
    elif map_type == 'village':
        game_map = village.load_village()
        map_type = 'village'
        width = len(game_map[0]) - 2
        height = len(game_map) - 2
        enemies = generate_enemies(width, height, num_enemies=0)
        place_player_on_map(player, game_map)
        place_enemies_on_map(enemies, game_map)
        return game_map, map_type, enemies
    elif map_type == 'forest':
        game_map = forest.load_forest()
        map_type = 'forest'
        width = len(game_map[0]) - 2
        height = len(game_map) - 2
        enemies = generate_enemies(width, height, num_enemies=10)
        place_player_on_map(player, game_map)
        place_enemies_on_map(enemies, game_map)
        return game_map, map_type, enemies
    elif map_type == 'lake':
        game_map = lake.load_lake()
        map_type = 'lake'
        width = len(game_map[0]) - 2
        height = len(game_map) - 2
        enemies = generate_enemies(width, height, num_enemies=5)
        place_player_on_map(player, game_map)
        place_enemies_on_map(enemies, game_map)
        return game_map, map_type, enemies
#    elif map_type == 'wasteland':
#        game_map = wasteland.load_wasteland()
#        map_type = 'wasteland'
#        width = len(game_map[0]) - 2
#        height = len(game_map) - 2
#        enemies = generate_enemies(width, height, num_enemies=15)
#        place_player_on_map(player, game_map)
#        place_enemies_on_map(enemies, game_map)
#        return game_map, map_type, enemies

if __name__ == "__main__":
    game_map = village.load_village()
    map_type = 'village'
    width = len(game_map[0]) - 2  # Учитываем границы карты
    height = len(game_map) - 2  # Учитываем границы карты
    quests = [False, False, False]
    quests_done = [False, False, False]
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

    # Данные для квестов

    q1_rat_count = 0
    q1_rat_task = 7
    q2_herb_count = 0
    q2_herb_task = 4
    q3_kill_count = 0
    q3_kill_task = 10

    num_enemies = 0
    enemies = generate_enemies(width, height, num_enemies)
    # Размещение игрока и врагов на карте
    place_player_on_map(player, game_map)
    place_enemies_on_map(enemies, game_map)
    # Основной цикл игры
    while True:
        player_info = str(player)
        print_map(game_map, player_info)
        command = input("Введите команду (w/a/s/d для движения, i для информации о заданиях, q для выхода): ").strip().lower()
        if command == 'q':
            break
        elif command in ['w', 'a', 's', 'd']:
            clear_player_from_map(player, game_map)
            dx, dy = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}[command]
            game_map, map_type, enemies = player.move(dx, dy, game_map, map_type, player, enemies)
            place_player_on_map(player, game_map)
        elif command == 'i':
            count = 0
            for quest in quests:
                count += 1
                print(f"Задание {count}: {quest}.")
                if count == 1:
                    print(f"Осталось убить крыс: {q1_rat_task - q1_rat_count}.")
                elif count == 2:
                    print(f"Осталось собрать трав: {q2_herb_task - q2_herb_count}.")
                elif count == 3:
                    print(f"Осталось убить врагов: {q3_kill_task - q3_kill_count}.")
        else:
            print("Неизвестная команда")
        
        # Очистка экрана для обновления карты
#        print("\033[H\033[J", end="")