#!/usr/bin/env python3
"""
Chronicles of Aetheria: The Forgotten Sanctum
A Feature-Rich Command-Line "Choose Your Own Adventure" RPG
Generated and structured using GitHub Copilot design patterns.
"""

import os
import sys
import time
import random
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable


# ============================================================================
# ANSI Color Codes & Formatting Helpers
# ============================================================================
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GOLD = "\033[38;5;220m"


def slow_print(text: str, delay: float = 0.02, end: str = "\n"):
    """Prints text with a typewriter effect, skippable if not on TTY."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if sys.stdout.isatty():
            time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def clear_screen():
    """Clears the terminal screen if interactive."""
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


# ============================================================================
# ASCII Art Assets
# ============================================================================
BANNER_ART = r"""
  ___  ____ _____ _   _ _____ ____  ___    _    
 / _ \| ____|_   _| | | | ____|  _ \|_ _|  / \   
| |_| |  _|   | | | |_| |  _| | |_) || |  / _ \  
|  _  | |___  | | |  _  | |___|  _ < | | / ___ \ 
|_| |_|_____| |_| |_| |_|_____|_| \_\___/_/   \_\
   ⚔️  THE FORGOTTEN SANCTUM: AN INTERACTIVE QUEST  ⚔️
"""

SWORD_SHIELD_ART = r"""
           /\
          /  \
         |    |
       --:====:--
         |    |
         |    |
         |    |
         |    |
         |    |
       \========/
        \======/
         \====/
          \==/
           \/
"""

SKULL_ART = r"""
      .---.
     /     \
    | () () |
     \  ^  /
      |||||
"""

VICTORY_ART = r"""
       ___________
      '._==_==_=_.'
      .-\:      /-.
     | (|:.     |) |
      '-|:.     |-'
        \::.    /
         '::. .'
           ) (
         _.' '._
        `"""""""`
"""


# ============================================================================
# Data Models
# ============================================================================
@dataclass
class Player:
    name: str = "Adventurer"
    char_class: str = "Warrior"
    max_hp: int = 100
    hp: int = 100
    mana: int = 40
    max_mana: int = 40
    gold: int = 25
    strength: int = 12
    agility: int = 10
    intelligence: int = 8
    inventory: List[str] = field(default_factory=lambda: ["Health Potion", "Torch"])
    quest_flags: Dict[str, bool] = field(default_factory=dict)

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual = min(self.hp, amount)
        self.hp -= actual
        return actual

    def heal(self, amount: int) -> int:
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def add_item(self, item: str):
        if item not in self.inventory:
            self.inventory.append(item)

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def use_item(self, item: str) -> bool:
        if item in self.inventory:
            if item == "Health Potion":
                healed = self.heal(35)
                self.inventory.remove(item)
                return True
            elif item == "Mana Potion":
                self.mana = min(self.max_mana, self.mana + 30)
                self.inventory.remove(item)
                return True
        return False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "char_class": self.char_class,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "gold": self.gold,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence,
            "inventory": self.inventory,
            "quest_flags": self.quest_flags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(**data)


@dataclass
class Choice:
    text: str
    target_node: str
    required_item: Optional[str] = None
    required_flag: Optional[str] = None
    skill_check: Optional[str] = None  # e.g., 'strength', 'agility', 'intelligence'
    skill_difficulty: int = 10
    failure_target: Optional[str] = None


@dataclass
class StoryNode:
    node_id: str
    title: str
    description: str
    choices: List[Choice]
    art: Optional[str] = None
    on_enter: Optional[Callable[[Player], str]] = None
    is_ending: bool = False
    is_victory: bool = False


# ============================================================================
# Combat Engine
# ============================================================================
@dataclass
class Monster:
    name: str
    hp: int
    max_hp: int
    attack_power: int
    gold_reward: int
    xp_reward: int
    loot_drop: Optional[str] = None


def run_combat(player: Player, monster: Monster) -> bool:
    """Executes a turn-based combat encounter between player and monster."""
    print(f"\n{Style.RED}{Style.BOLD}⚔️  A savage {monster.name} emerges! Combat begins! ⚔️{Style.RESET}\n")

    while player.is_alive() and monster.hp > 0:
        print(f"{Style.CYAN}[{player.name} - HP: {player.hp}/{player.max_hp} | Mana: {player.mana}/{player.max_mana}]{Style.RESET}")
        print(f"{Style.RED}[{monster.name} - HP: {monster.hp}/{monster.max_hp}]{Style.RESET}\n")
        print("Choose an action:")
        print("1. ⚔️  Attack (Physical Strike)")
        print("2. 🔮 Cast Spell (Costs 15 Mana)")
        print("3. 🧪 Drink Health Potion")
        print("4. 🏃 Attempt to Flee")

        choice = input(f"{Style.YELLOW}> {Style.RESET}").strip()

        if choice == "1":
            # Physical attack
            dmg = random.randint(player.strength - 3, player.strength + 5)
            # Critical hit chance based on agility
            is_crit = random.randint(1, 100) <= (player.agility * 3)
            if is_crit:
                dmg = int(dmg * 1.75)
                print(f"{Style.GOLD}💥 CRITICAL STRIKE!{Style.RESET}")
            monster.hp -= dmg
            print(f"You strike {monster.name} for {Style.BOLD}{dmg}{Style.RESET} damage!")

        elif choice == "2":
            if player.mana >= 15:
                player.mana -= 15
                spell_dmg = random.randint(player.intelligence * 2, player.intelligence * 3)
                monster.hp -= spell_dmg
                print(f"{Style.MAGENTA}✨ Arcane Lightning bolts from your fingertips dealing {spell_dmg} damage!{Style.RESET}")
            else:
                print(f"{Style.DIM}Not enough mana! Your focus falters.{Style.RESET}")
                continue

        elif choice == "3":
            if player.has_item("Health Potion"):
                healed = player.heal(40)
                player.inventory.remove("Health Potion")
                print(f"{Style.GREEN}You chug a Health Potion and restore {healed} HP!{Style.RESET}")
            else:
                print(f"{Style.DIM}You don't have any Health Potions left!{Style.RESET}")
                continue

        elif choice == "4":
            escape_roll = random.randint(1, 20) + (player.agility // 2)
            if escape_roll >= 14:
                print(f"{Style.GREEN}💨 You successfully dive into the shadows and escape!{Style.RESET}")
                return True
            else:
                print(f"{Style.RED}Escape failed! The monster blocks your exit!{Style.RESET}")

        else:
            print("Invalid command. You lose your turn hesitate in panic!")

        # Monster Turn
        if monster.hp > 0:
            m_dmg = random.randint(monster.attack_power - 2, monster.attack_power + 3)
            # Dodge chance based on agility
            if random.randint(1, 20) + (player.agility // 3) >= 17:
                print(f"{Style.GREEN}⚡ You deftly dodge {monster.name}'s incoming counter-attack!{Style.RESET}")
            else:
                player.take_damage(m_dmg)
                print(f"{Style.RED}{monster.name} retaliates, clawing you for {m_dmg} damage!{Style.RESET}")

        time.sleep(0.5)

    if player.is_alive():
        print(f"\n{Style.GREEN}{Style.BOLD}🎉 Victory! You defeated the {monster.name}!{Style.RESET}")
        player.gold += monster.gold_reward
        print(f"You salvaged {Style.GOLD}{monster.gold_reward} gold{Style.RESET}.")
        if monster.loot_drop:
            player.add_item(monster.loot_drop)
            print(f"Loot gained: {Style.CYAN}{monster.loot_drop}{Style.RESET}!")
        return True
    else:
        print(f"\n{Style.RED}{Style.BOLD}💀 You have fallen in battle...{Style.RESET}")
        return False


# ============================================================================
# Story Graph & World Building
# ============================================================================
def build_story_world() -> Dict[str, StoryNode]:
    """Constructs the branching decision graph for the adventure."""
    nodes: Dict[str, StoryNode] = {}

    def add_node(node: StoryNode):
        nodes[node.node_id] = node

    # Node: Intro / Crossroads
    add_node(StoryNode(
        node_id="crossroads",
        title="The Mist-Shrouded Crossroads",
        art=SWORD_SHIELD_ART,
        description=(
            "You stand before the ancient stone marker at the boundary of Whispering Vale.\n"
            "Heavy tendrils of damp mist coil around your boots. To the north rises the craggy\n"
            "silhouette of the Sunken Sanctum. To the east lies the decaying Sunken Crypt,\n"
            "and to the west a warm lantern flickers from an old Alchemist's Caravan."
        ),
        choices=[
            Choice("Head north toward the main Sanctum Gate", "sanctum_gate"),
            Choice("Venture east toward the dark Sunken Crypt", "crypt_entrance"),
            Choice("Approach the Alchemist's Caravan to the west", "caravan"),
            Choice("Inspect the ancient carved rune stone at the crossroads", "inspect_runes", skill_check="intelligence", skill_difficulty=11, failure_target="rune_failed"),
        ]
    ))

    # Node: Inspect runes success
    def rune_bonus(p: Player) -> str:
        p.quest_flags["ancient_lore"] = True
        p.add_item("Glowing Runic Stone")
        return "You decipher ancient Elven glyphs! You pocket a dormant Runic Stone that pulsates with power."

    add_node(StoryNode(
        node_id="inspect_runes",
        title="Ancient Glyphs of Warding",
        description=(
            "Brushing centuries of moss from the granite pillar, you align the celestial glyphs.\n"
            "A compartment clicks open at the base of the obelisk!"
        ),
        on_enter=rune_bonus,
        choices=[
            Choice("Return to the crossroads", "crossroads")
        ]
    ))

    # Node: Inspect runes fail
    def rune_trap(p: Player) -> str:
        dmg = p.take_damage(10)
        return f"A static discharge sparks from the trapped stone, zapping you for {dmg} damage!"

    add_node(StoryNode(
        node_id="rune_failed",
        title="A Painful Shock",
        description="The glyphs flare with defensive magic as your finger touches the stone.",
        on_enter=rune_trap,
        choices=[
            Choice("Step back to the crossroads", "crossroads")
        ]
    ))

    # Node: Caravan
    def caravan_visit(p: Player) -> str:
        return "Old Barnaby waves a wooden ladle from behind bottles of bubbling elixir."

    add_node(StoryNode(
        node_id="caravan",
        title="Barnaby's Curious Caravan",
        description=(
            "'Welcome, wanderer!' rasps the merchant. 'The Sanctum is filled with horrors,\n"
            "but my wares can tip fate in your favor.'"
        ),
        on_enter=caravan_visit,
        choices=[
            Choice("Buy Health Potion (15 Gold)", "buy_health_potion"),
            Choice("Buy Silvered Sanctum Key (25 Gold)", "buy_sanctum_key"),
            Choice("Ask Barnaby for counsel regarding the Sanctum's beast", "barnaby_counsel"),
            Choice("Bid farewell and return to the crossroads", "crossroads")
        ]
    ))

    # Caravan Purchases
    def buy_hp(p: Player) -> str:
        if p.gold >= 15:
            p.gold -= 15
            p.add_item("Health Potion")
            return "Barnaby corks a red phial and hands it over. (+1 Health Potion)"
        return "You don't have enough gold! Barnaby frowns."

    add_node(StoryNode(
        node_id="buy_health_potion",
        title="Potion Acquired",
        description="The warm liquid inside sloshes with restorative power.",
        on_enter=buy_hp,
        choices=[Choice("Stay at the caravan", "caravan")]
    ))

    def buy_key(p: Player) -> str:
        if p.gold >= 25:
            p.gold -= 25
            p.add_item("Silvered Sanctum Key")
            p.quest_flags["has_key"] = True
            return "You purchase the master Silvered Key! It is cold and intricately forged."
        return "Barnaby taps his counter: '25 gold is the price, no discounts for glory-seekers.'"

    add_node(StoryNode(
        node_id="buy_sanctum_key",
        title="The Silvered Key",
        description="A heavy key engraved with twin ravens now rests in your pouch.",
        on_enter=buy_key,
        choices=[Choice("Stay at the caravan", "caravan")]
    ))

    add_node(StoryNode(
        node_id="barnaby_counsel",
        title="Barnaby's Warning",
        description=(
            "'The guardian inside is the Obsidian Wyrmling,' Barnaby whispers.\n"
            "'Steel weapons alone will blunt against its obsidian hide. You will need\n"
            "either magical resonance, swift agility to strike its underbelly,\n"
            "or the Sacred Relic itself to banish it!'"
        ),
        choices=[Choice("Return to the caravan counter", "caravan")]
    ))

    # Node: Crypt Entrance
    add_node(StoryNode(
        node_id="crypt_entrance",
        title="The Sunken Crypt Archway",
        description=(
            "Cobwebs cling to rotting marble pillars. A chilled draught carries\n"
            "the stench of mildew and ancient dry bone. A cracked sarcophagus stands ajar."
        ),
        choices=[
            Choice("Search the open sarcophagus", "search_crypt", skill_check="agility", skill_difficulty=11, failure_target="crypt_trap"),
            Choice("Descend deeper into the catacombs", "crypt_combat"),
            Choice("Retreat back to the crossroads", "crossroads"),
        ]
    ))

    def crypt_trap_hit(p: Player) -> str:
        dmg = p.take_damage(15)
        return f"A pressure plate clicks! Poisoned darts shoot out, inflicting {dmg} damage!"

    add_node(StoryNode(
        node_id="crypt_trap",
        title="Crypt Trap Triggered",
        description="You roll aside, coughing through purple smoke.",
        on_enter=crypt_trap_hit,
        choices=[Choice("Shake it off and face the crypt", "crypt_entrance")]
    ))

    def search_crypt_loot(p: Player) -> str:
        p.add_item("Sun-Blade")
        p.strength += 3
        return "You discover the legendary Sun-Blade! Your strength increases (+3 Strength)!"

    add_node(StoryNode(
        node_id="search_crypt",
        title="The Entombed Weapon",
        description="Gleaming under dust is a blade forged of celestial bronze that never rusts.",
        on_enter=search_crypt_loot,
        choices=[
            Choice("Descend deeper into the catacombs", "crypt_combat"),
            Choice("Return to the crossroads with your prize", "crossroads")
        ]
    ))

    # Crypt Combat node
    def crypt_fight(p: Player) -> str:
        skeleton = Monster("Skeletal Warden", hp=45, max_hp=45, attack_power=10, gold_reward=20, xp_reward=30, loot_drop="Shield of Dawn")
        won = run_combat(p, skeleton)
        if won:
            p.quest_flags["crypt_cleared"] = True
            return "The skeleton collapses into dust, leaving behind the Shield of Dawn!"
        return "Defeat in the crypt."

    add_node(StoryNode(
        node_id="crypt_combat",
        title="The Catacomb Depths",
        description="Blue spectral torches ignite automatically. A towering skeleton brandishes an iron halberd!",
        on_enter=crypt_fight,
        choices=[
            Choice("Head back up to the crossroads", "crossroads", required_flag="crypt_cleared"),
            Choice("Fall to the darkness...", "game_over")
        ]
    ))

    # Node: Sanctum Gate
    add_node(StoryNode(
        node_id="sanctum_gate",
        title="The Great Iron Gate of the Sanctum",
        description=(
            "Towering double doors of black iron block entrance to the central hall.\n"
            "An elaborate keyhole sits below a bas-relief of twin ravens.\n"
            "Beside it, a fragile stained-glass balcony window is perched 15 feet above."
        ),
        choices=[
            Choice("Unlock the doors with the Silvered Sanctum Key", "sanctum_inner_hall", required_item="Silvered Sanctum Key"),
            Choice("Scale the ivy-covered masonry to the balcony window", "balcony_climb", skill_check="agility", skill_difficulty=12, failure_target="fall_from_balcony"),
            Choice("Attempt to smash the heavy iron gate with brute force", "smash_gate", skill_check="strength", skill_difficulty=16, failure_target="gate_recoil"),
            Choice("Return to the crossroads to prepare further", "crossroads")
        ]
    ))

    def balcony_fall(p: Player) -> str:
        dmg = p.take_damage(15)
        return f"A crumbling gargoyle gives way! You tumble down into the briars, taking {dmg} damage."

    add_node(StoryNode(
        node_id="fall_from_balcony",
        title="A Painful Plummet",
        description="You pick yourself up, bruised but alive.",
        on_enter=balcony_fall,
        choices=[Choice("Re-evaluate your options at the gate", "sanctum_gate")]
    ))

    def smash_recoil(p: Player) -> str:
        dmg = p.take_damage(12)
        return f"The reinforced gate doesn't budge! The recoil rattles your bones for {dmg} damage."

    add_node(StoryNode(
        node_id="gate_recoil",
        title="Immovable Iron",
        description="The iron gate rings like a funeral bell throughout the valley.",
        on_enter=smash_recoil,
        choices=[Choice("Return to the gate", "sanctum_gate")]
    ))

    add_node(StoryNode(
        node_id="balcony_climb",
        title="The Upper Balcony",
        description=(
            "With nimble grace, you hook your boots onto the stone relief and slip through\n"
            "the shattered window. You arrive quietly on the upper mezzanine of the Sanctum!"
        ),
        choices=[
            Choice("Sneak downward into the Inner Sanctum", "sanctum_inner_hall")
        ]
    ))

    add_node(StoryNode(
        node_id="smash_gate",
        title="Titan's Feat",
        description=(
            "With a thunderous battle cry, you ram your full weight against the locking hinge.\n"
            "The iron latch buckles with a deafening CRACK!"
        ),
        choices=[
            Choice("March proudly into the Inner Sanctum", "sanctum_inner_hall")
        ]
    ))

    # Inner Sanctum & Final Boss
    def boss_encounter(p: Player) -> str:
        dragon = Monster("Obsidian Wyrmling", hp=80, max_hp=80, attack_power=16, gold_reward=100, xp_reward=100, loot_drop="Crown of Aetheria")
        won = run_combat(p, dragon)
        if won:
            p.quest_flags["boss_defeated"] = True
            return "The mighty Obsidian Wyrmling crumbles into volcanic shards!"
        return "Defeated by dragon fire."

    add_node(StoryNode(
        node_id="sanctum_inner_hall",
        title="The Inner Sanctum: Chamber of the Relic",
        description=(
            "You stand inside a cavernous vaulted cathedral. At the center sits a raised altar\n"
            "bathed in moonlight from the domed ceiling. Hovering above the altar is\n"
            "the Heart of Aetheria—a crystal pulsating with raw celestial radiance.\n\n"
            "Suddenly, coiled around the altar columns, scales grind against stone.\n"
            "The Obsidian Wyrmling opens its molten gold eyes and unleashes a ferocious roar!"
        ),
        on_enter=boss_encounter,
        choices=[
            Choice("Claim the Heart of Aetheria and claim your destiny!", "victory_ending", required_flag="boss_defeated"),
            Choice("Succumb to the ashes...", "game_over")
        ]
    ))

    # Victory Ending
    add_node(StoryNode(
        node_id="victory_ending",
        title="VICTORY: Champion of Aetheria",
        art=VICTORY_ART,
        description=(
            "You lift the Heart of Aetheria high into the air!\n"
            "A wave of pure incandescent warmth washes over you, healing all wounds and\n"
            "dissolving the lingering darkness from the land.\n\n"
            "Bards across the realm will sing of your bravery, cunning, and perseverance\n"
            "for centuries to come. You have completed the trial of the Forgotten Sanctum!"
        ),
        choices=[],
        is_ending=True,
        is_victory=True
    ))

    # Game Over Ending
    add_node(StoryNode(
        node_id="game_over",
        title="DEFEAT: Fallen in the Depths",
        art=SKULL_ART,
        description=(
            "Darkness envelopes your vision as your journey comes to an untimely end.\n"
            "The secrets of the Forgotten Sanctum remain buried beneath the mist..."
        ),
        choices=[],
        is_ending=True,
        is_victory=False
    ))

    return nodes


# ============================================================================
# Game Engine & Persistence
# ============================================================================
class GameEngine:
    SAVE_FILE = "savegame.json"

    def __init__(self):
        self.player = Player()
        self.nodes = build_story_world()
        self.current_node_id = "crossroads"
        self.is_running = True

    def save_game(self, filepath: str = SAVE_FILE) -> bool:
        """Serializes current player and story state to JSON."""
        state = {
            "player": self.player.to_dict(),
            "current_node_id": self.current_node_id,
            "timestamp": time.time()
        }
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, filepath: str = SAVE_FILE) -> bool:
        """Restores state from a saved JSON game file."""
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                state = json.load(f)
            self.player = Player.from_dict(state["player"])
            self.current_node_id = state.get("current_node_id", "crossroads")
            return True
        except (IOError, KeyError, json.JSONDecodeError) as e:
            print(f"Error loading save file: {e}")
            return False

    def select_character_class(self):
        """Allows player to customize their name and choose a class archetype."""
        clear_screen()
        print(f"{Style.CYAN}{BANNER_ART}{Style.RESET}")
        name = input(f"Enter your hero's name: {Style.YELLOW}").strip()
        if not name:
            name = "Aric the Brave"
        print(f"{Style.RESET}")

        print("\nChoose your Archetype:")
        print(f"1. {Style.BOLD}Warrior{Style.RESET}   (High HP & Strength, Heavy attacks)")
        print(f"2. {Style.BOLD}Mage{Style.RESET}      (High Mana & Intelligence, Powerful spells)")
        print(f"3. {Style.BOLD}Rogue{Style.RESET}     (High Agility, Critical strikes & Evasion)")

        choice = input(f"\n{Style.YELLOW}Select archetype [1-3]: {Style.RESET}").strip()

        if choice == "2":
            self.player = Player(
                name=name,
                char_class="Mage",
                max_hp=80,
                hp=80,
                mana=70,
                max_mana=70,
                strength=8,
                agility=10,
                intelligence=16,
                inventory=["Mana Potion", "Health Potion", "Spell Tome"]
            )
        elif choice == "3":
            self.player = Player(
                name=name,
                char_class="Rogue",
                max_hp=90,
                hp=90,
                mana=30,
                max_mana=30,
                strength=10,
                agility=16,
                intelligence=10,
                inventory=["Lockpick", "Health Potion", "Dagger"]
            )
        else:
            self.player = Player(
                name=name,
                char_class="Warrior",
                max_hp=115,
                hp=115,
                mana=25,
                max_mana=25,
                strength=15,
                agility=10,
                intelligence=8,
                inventory=["Health Potion", "Iron Shield"]
            )

        print(f"\n{Style.GREEN}Welcome, {self.player.name} the {self.player.char_class}! Your adventure begins now...{Style.RESET}\n")
        time.sleep(1)

    def print_hud(self):
        """Displays player status header."""
        inv_str = ", ".join(self.player.inventory) if self.player.inventory else "Empty"
        bar = "─" * 70
        print(f"{Style.DIM}{bar}{Style.RESET}")
        print(
            f"{Style.BOLD}{self.player.name}{Style.RESET} ({self.player.char_class}) | "
            f"HP: {Style.RED}{self.player.hp}/{self.player.max_hp}{Style.RESET} | "
            f"Mana: {Style.BLUE}{self.player.mana}/{self.player.max_mana}{Style.RESET} | "
            f"Gold: {Style.GOLD}{self.player.gold}g{Style.RESET}"
        )
        print(f"Inventory: {Style.CYAN}{inv_str}{Style.RESET}")
        print(f"{Style.DIM}{bar}{Style.RESET}")

    def run_node(self, node: StoryNode):
        """Executes a single story node logic."""
        clear_screen()
        self.print_hud()

        if node.art:
            print(f"{Style.YELLOW}{node.art}{Style.RESET}")

        print(f"\n{Style.BOLD}{Style.UNDERLINE}{node.title}{Style.RESET}\n")
        slow_print(node.description)

        if node.on_enter:
            msg = node.on_enter(self.player)
            if msg:
                print(f"\n{Style.GREEN}» {msg}{Style.RESET}")

        # Check death after on_enter effects
        if not self.player.is_alive():
            self.current_node_id = "game_over"
            return

        # Check if terminal node
        if node.is_ending:
            print("\n" + "=" * 50)
            if node.is_victory:
                print(f"{Style.GOLD}{Style.BOLD}🏆 CONGRATULATIONS! QUEST COMPLETED! 🏆{Style.RESET}")
            else:
                print(f"{Style.RED}{Style.BOLD}💀 GAME OVER 💀{Style.RESET}")
            print("=" * 50)
            self.is_running = False
            return

        # Present available choices
        valid_choices = []
        print("\nWhat will you do?")
        for choice in node.choices:
            # Check item condition
            if choice.required_item and not self.player.has_item(choice.required_item):
                continue
            # Check flag condition
            if choice.required_flag and not self.player.quest_flags.get(choice.required_flag, False):
                continue
            valid_choices.append(choice)

        for idx, choice in enumerate(valid_choices, start=1):
            req_info = ""
            if choice.skill_check:
                req_info = f" [{choice.skill_check.title()} Check (DC {choice.skill_difficulty})]"
            print(f"{idx}. {choice.text}{Style.DIM}{req_info}{Style.RESET}")

        # System options
        print(f"S. Save Game")
        print(f"U. Use Item from Inventory")
        print(f"Q. Quit to Desktop")

        while True:
            cmd = input(f"\n{Style.YELLOW}Select an action: {Style.RESET}").strip().lower()

            if cmd == "s":
                if self.save_game():
                    print(f"{Style.GREEN}Game saved successfully!{Style.RESET}")
                time.sleep(1)
                return

            if cmd == "u":
                if not self.player.inventory:
                    print("Your inventory is empty.")
                    continue
                print("Usable items:")
                for i, itm in enumerate(self.player.inventory, start=1):
                    print(f"  {i}. {itm}")
                sub_pick = input("Enter item number to use (or enter to cancel): ").strip()
                if sub_pick.isdigit() and 1 <= int(sub_pick) <= len(self.player.inventory):
                    target_itm = self.player.inventory[int(sub_pick) - 1]
                    if self.player.use_item(target_itm):
                        print(f"{Style.GREEN}Used {target_itm}!{Style.RESET}")
                        time.sleep(1)
                        return
                    else:
                        print(f"{target_itm} cannot be consumed right now.")
                continue

            if cmd == "q":
                confirm = input("Quit without saving? (y/N): ").strip().lower()
                if confirm == "y":
                    self.is_running = False
                    return
                continue

            if cmd.isdigit():
                choice_idx = int(cmd) - 1
                if 0 <= choice_idx < len(valid_choices):
                    selected = valid_choices[choice_idx]

                    # Perform skill check if applicable
                    if selected.skill_check:
                        stat_val = getattr(self.player, selected.skill_check, 10)
                        roll = random.randint(1, 20)
                        total = roll + (stat_val // 3)
                        print(f"\nRolling d20 + {selected.skill_check.title()} bonus: {roll} + {stat_val // 3} = {total} (DC: {selected.skill_difficulty})")
                        time.sleep(0.7)
                        if total >= selected.skill_difficulty:
                            print(f"{Style.GREEN}Success!{Style.RESET}\n")
                            self.current_node_id = selected.target_node
                        else:
                            print(f"{Style.RED}Failed! Consequences ensue...{Style.RESET}\n")
                            self.current_node_id = selected.failure_target or selected.target_node
                        time.sleep(0.8)
                    else:
                        self.current_node_id = selected.target_node
                    return

            print("Invalid selection. Please choose an option from the list above.")

    def start(self):
        """Main game loop."""
        clear_screen()
        print(f"{Style.CYAN}{BANNER_ART}{Style.RESET}")
        print("1. New Adventure")
        print("2. Load Saved Game")
        print("3. Exit")

        mode = input(f"\n{Style.YELLOW}Select an option [1-3]: {Style.RESET}").strip()
        if mode == "2":
            if self.load_game():
                print(f"{Style.GREEN}Save file loaded! Welcome back, {self.player.name}.{Style.RESET}")
                time.sleep(1)
            else:
                print("No save game found. Starting new adventure...")
                time.sleep(1)
                self.select_character_class()
        elif mode == "3":
            print("Farewell, traveler.")
            return
        else:
            self.select_character_class()

        while self.is_running:
            node = self.nodes.get(self.current_node_id)
            if not node:
                print(f"Error: Node '{self.current_node_id}' not found!")
                break
            self.run_node(node)


if __name__ == "__main__":
    game = GameEngine()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\n\nGame terminated. Safe travels!")
