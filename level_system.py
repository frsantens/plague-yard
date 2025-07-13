class LevelSystem:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        print(f"Level up! You are now level {self.level}.")

    def upgrade_stat(self, player, stat):
        if stat == "speed":
            player.speed += 1
        elif stat == "attack":
            player.attack += 2
        elif stat == "dodge":
            player.dodge += 0.05
        elif stat == "defense":
            player.defense += 1
        elif stat == "critical_chance":
            player.critical_chance += 0.05
        print(f"Upgraded {stat}!")
