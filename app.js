/**
 * Chronicles of Aetheria: Web Adventure Engine
 * Interactive Choose Your Own Adventure built with GitHub Copilot workflows.
 */

// Simple Web Audio Sound Generator for retro sounds
class SoundEffects {
  constructor() {
    this.ctx = null;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
  }

  playBeep(freq = 440, type = 'sine', duration = 0.08) {
    try {
      this.init();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {
      // Audio might be blocked until user interaction
    }
  }

  playVictory() {
    const notes = [261.63, 329.63, 392.00, 523.25];
    notes.forEach((freq, idx) => {
      setTimeout(() => this.playBeep(freq, 'triangle', 0.2), idx * 120);
    });
  }

  playCombat() {
    this.playBeep(150, 'sawtooth', 0.15);
  }
}

const sfx = new SoundEffects();

class AdventureGame {
  constructor() {
    this.player = {
      name: "Aric",
      class: "Warrior",
      hp: 100,
      maxHp: 100,
      mana: 40,
      maxMana: 40,
      gold: 25,
      strength: 14,
      agility: 10,
      intelligence: 8,
      inventory: ["Health Potion", "Torch"],
      flags: {}
    };

    this.activeEnemy = null;
    this.currentNodeId = "start";

    this.initStoryData();
    this.bindEvents();
    this.render();
  }

  initStoryData() {
    this.storyNodes = {
      start: {
        title: "The Crossroads of Whispering Vale",
        art: "⚔️  THE FORGOTTEN SANCTUM: AN INTERACTIVE QUEST  ⚔️",
        text: "You stand before the weathered boundary stone of the Whispering Vale. A chilling fog coils about your knees. To the north rises the obsidian parapets of the Sunken Sanctum. To the east lies a yawning crypt entrance, and to the west flickers the lantern of Barnaby's traveling caravan.",
        choices: [
          { text: "March north toward the Sanctum Gate", target: "sanctum_gate" },
          { text: "Explore the dark Sunken Crypt to the east", target: "crypt" },
          { text: "Visit Barnaby's Caravan to the west", target: "caravan" },
          { text: "Inspect ancient runic markings on the boundary stone", target: "inspect_runes", check: "intelligence", dc: 10 }
        ]
      },

      inspect_runes: {
        title: "Celestial Glyphs",
        art: "   .---.\n  /     \\\n | () () |\n  \\  ^  /\n   |||||",
        text: "You trace the faint blue sigils carved deep into the obelisk. As your fingers align the planetary symbols, a hidden granite panel clicks open! Inside rests a glowing Runic Stone.",
        onEnter: (p) => {
          p.inventory.push("Glowing Runic Stone");
          p.flags.found_rune = true;
          return "Obtained: Glowing Runic Stone!";
        },
        choices: [
          { text: "Return to the crossroads", target: "start" }
        ]
      },

      caravan: {
        title: "Barnaby's Curious Caravan",
        art: "  [=== BARNABY'S APOTHECARY ===]",
        text: "'Welcome, brave soul!' Barnaby greets you with a gap-toothed grin. 'Few dare to challenge the Sunken Sanctum. I have elixirs and rare artifacts that might keep your heartbeat steady.'",
        choices: [
          { text: "Buy Health Potion (15 Gold)", target: "buy_potion" },
          { text: "Buy Silvered Sanctum Key (25 Gold)", target: "buy_key" },
          { text: "Ask Barnaby about the Sanctum's beast", target: "barnaby_counsel" },
          { text: "Return to the crossroads", target: "start" }
        ]
      },

      buy_potion: {
        title: "Elixir Purchased",
        art: "      ( )\n     .-'-.\n    /     \\\n   |  HP+  |\n    '-----'",
        text: "You hand over the coins. Barnaby slides a glass vial of ruby-colored nectar across the counter.",
        onEnter: (p) => {
          if (p.gold >= 15) {
            p.gold -= 15;
            p.inventory.push("Health Potion");
            return "Bought Health Potion! (-15 Gold, +1 Health Potion)";
          }
          return "You do not possess enough gold!";
        },
        choices: [
          { text: "Back to caravan counter", target: "caravan" }
        ]
      },

      buy_key: {
        title: "The Raven's Key",
        art: "  0==={========>",
        text: "Barnaby unlocks a velvet box. Inside is a delicate silver key engraved with raven wings.",
        onEnter: (p) => {
          if (p.gold >= 25) {
            p.gold -= 25;
            p.inventory.push("Silvered Sanctum Key");
            p.flags.has_key = true;
            return "Purchased Silvered Sanctum Key! (-25 Gold)";
          }
          return "Barnaby shakes his head: '25 gold is the price, adventurer.'";
        },
        choices: [
          { text: "Back to caravan counter", target: "caravan" }
        ]
      },

      barnaby_counsel: {
        title: "The Alchemist's Counsel",
        art: "  ( ? )",
        text: "'The guardian inside is the Obsidian Wyrmling,' Barnaby warns. 'Its scales deflect mundane weapons unless struck at close quarters with high agility or broken by celestial lightning.'",
        choices: [
          { text: "Thank him and return", target: "caravan" }
        ]
      },

      crypt: {
        title: "The Sunken Crypt",
        art: "   |====|\n   |RIP |\n   |====|",
        text: "The crypt air is rancid and thick. Broken statues of forgotten kings gaze down at a cracked sarcophagus. You hear the rattling of armor deeper in the darkness.",
        choices: [
          { text: "Search the cracked sarcophagus for loot", target: "loot_sarcophagus", check: "agility", dc: 11 },
          { text: "Advance deeper and confront the rattling presence", target: "crypt_fight" },
          { text: "Back out toward the crossroads", target: "start" }
        ]
      },

      loot_sarcophagus: {
        title: "The Entombed Blade",
        art: "  /| ________________\nO|===|* >________________>\n  \\|",
        text: "Avoiding a rusty pressure needle, you reach into the crypt vault and pull out a gleaming Sun-Blade!",
        onEnter: (p) => {
          p.inventory.push("Sun-Blade");
          p.strength += 4;
          return "Obtained Sun-Blade! (+4 Strength)";
        },
        choices: [
          { text: "Face the guardian deeper inside", target: "crypt_fight" },
          { text: "Return to the crossroads", target: "start" }
        ]
      },

      crypt_fight: {
        title: "Skeletal Warden Awoken",
        art: "      .---.\n     /     \\\n    | () () |\n     \\  ^  /\n      |||||",
        text: "An armored skeleton rises from a heap of bones, brandishing an ancient battle halberd!",
        enemy: {
          name: "Skeletal Warden",
          hp: 45,
          maxHp: 45,
          attack: 10,
          gold: 20,
          loot: "Shield of Dawn"
        },
        choices: []
      },

      sanctum_gate: {
        title: "The Great Iron Gates",
        art: "   |  [===]  |\n   |  |   |  |\n   |__|___|__|",
        text: "Massive iron gates bar entry to the sanctum hall. A double raven emblem surrounds an intricate silver keyhole. Up above, a shattered stained-glass window provides an alternate entry.",
        choices: [
          { text: "Unlock the gate with the Silvered Sanctum Key", target: "inner_sanctum", reqItem: "Silvered Sanctum Key" },
          { text: "Climb the ivy wall to the high balcony window", target: "inner_sanctum", check: "agility", dc: 12 },
          { text: "Smash through the iron latch with raw force", target: "inner_sanctum", check: "strength", dc: 15 },
          { text: "Return to the crossroads to prepare", target: "start" }
        ]
      },

      inner_sanctum: {
        title: "The Chamber of the Heart",
        art: "    < ★ >\n   /  |  \\\n  =========",
        text: "You step into the vaulted sanctuary. Above an illuminated dais floats the Heart of Aetheria. Suddenly, the chamber tremors as the Obsidian Wyrmling unfurls from the shadows!",
        enemy: {
          name: "Obsidian Wyrmling",
          hp: 75,
          maxHp: 75,
          attack: 15,
          gold: 80,
          loot: "Heart of Aetheria"
        },
        choices: []
      },

      victory: {
        title: "VICTORY: Savior of Aetheria",
        art: "       ___________\n      '._==_==_=_.'\n      .-\\:      /-.\n     | (|:.     |) |\n      '-|:.     |-'",
        text: "With the Obsidian Wyrmling vanquished, you claim the Heart of Aetheria! Radiant gold light floods the valley, lifting the ancient curse. Your saga will echo throughout eternity!",
        choices: [
          { text: "Play Again from the Beginning", target: "start", restart: true }
        ]
      },

      game_over: {
        title: "DEFEAT: Journey's End",
        art: "      .---.\n     /     \\\n    | () () |\n     \\  ^  /\n      |||||",
        text: "Your strength fails as darkness overtakes you. The secrets of the Forgotten Sanctum remain dormant beneath the mists...",
        choices: [
          { text: "Awaken at the Crossroads (Retry)", target: "start", restart: true }
        ]
      }
    };
  }

  bindEvents() {
    document.getElementById("btn-save").addEventListener("click", () => this.saveGame());
    document.getElementById("btn-load").addEventListener("click", () => this.loadGame());
    document.getElementById("btn-restart").addEventListener("click", () => this.restartGame());
  }

  saveGame() {
    const data = {
      player: this.player,
      currentNodeId: this.currentNodeId
    };
    localStorage.setItem("aetheria_savegame", JSON.stringify(data));
    this.showNotification("Game progress saved to local storage! 💾");
  }

  loadGame() {
    const raw = localStorage.getItem("aetheria_savegame");
    if (!raw) {
      this.showNotification("No saved game found!");
      return;
    }
    try {
      const data = JSON.parse(raw);
      this.player = data.player;
      this.currentNodeId = data.currentNodeId;
      this.showNotification("Save file loaded successfully! 📂");
      this.render();
    } catch (e) {
      this.showNotification("Failed to load save file.");
    }
  }

  restartGame() {
    this.player = {
      name: "Aric",
      class: "Warrior",
      hp: 100,
      maxHp: 100,
      mana: 40,
      maxMana: 40,
      gold: 25,
      strength: 14,
      agility: 10,
      intelligence: 8,
      inventory: ["Health Potion", "Torch"],
      flags: {}
    };
    this.currentNodeId = "start";
    this.activeEnemy = null;
    this.showNotification("Game restarted!");
    this.render();
  }

  showNotification(msg) {
    const box = document.getElementById("notification-box");
    box.textContent = msg;
    box.classList.remove("hidden");
    setTimeout(() => {
      box.classList.add("hidden");
    }, 3500);
  }

  combatAction(action) {
    if (!this.activeEnemy) return;
    sfx.playCombat();

    const enemy = this.activeEnemy;
    let turnLog = "";

    if (action === "attack") {
      const dmg = Math.floor(this.player.strength * 1.2) + Math.floor(Math.random() * 5);
      enemy.hp = Math.max(0, enemy.hp - dmg);
      turnLog = `You struck ${enemy.name} for ${dmg} damage!`;
    } else if (action === "spell") {
      if (this.player.mana >= 15) {
        this.player.mana -= 15;
        const dmg = Math.floor(this.player.intelligence * 2.5);
        enemy.hp = Math.max(0, enemy.hp - dmg);
        turnLog = `Arcane Lightning dealt ${dmg} magic damage!`;
      } else {
        turnLog = "Not enough mana to cast spell!";
        this.showNotification(turnLog);
        return;
      }
    } else if (action === "potion") {
      const idx = this.player.inventory.indexOf("Health Potion");
      if (idx !== -1) {
        this.player.inventory.splice(idx, 1);
        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 40);
        turnLog = "You drank a Health Potion and healed 40 HP!";
      } else {
        turnLog = "No Health Potions remaining!";
        this.showNotification(turnLog);
        return;
      }
    } else if (action === "flee") {
      if (Math.random() > 0.4) {
        this.activeEnemy = null;
        this.showNotification("Escaped safely back to the crossroads!");
        this.currentNodeId = "start";
        this.render();
        return;
      } else {
        turnLog = "Failed to flee! The enemy blocks your escape.";
      }
    }

    // Check Enemy Defeated
    if (enemy.hp <= 0) {
      this.player.gold += enemy.gold;
      if (enemy.loot && !this.player.inventory.includes(enemy.loot)) {
        this.player.inventory.push(enemy.loot);
      }
      this.showNotification(`Victory! Defeated ${enemy.name}! (+${enemy.gold}g)`);

      if (this.currentNodeId === "inner_sanctum") {
        sfx.playVictory();
        this.activeEnemy = null;
        this.currentNodeId = "victory";
      } else {
        this.activeEnemy = null;
        this.currentNodeId = "start";
      }
      this.render();
      return;
    }

    // Enemy Retaliation
    const enemyDmg = Math.max(1, enemy.attack + Math.floor(Math.random() * 4) - 2);
    this.player.hp = Math.max(0, this.player.hp - enemyDmg);
    turnLog += ` ${enemy.name} counter-attacked for ${enemyDmg} damage.`;

    if (this.player.hp <= 0) {
      this.activeEnemy = null;
      this.currentNodeId = "game_over";
      this.render();
      return;
    }

    this.showNotification(turnLog);
    this.updateHUD();
    this.updateCombatView();
  }

  updateCombatView() {
    const combatBox = document.getElementById("combat-container");
    if (!this.activeEnemy) {
      combatBox.classList.add("hidden");
      return;
    }
    combatBox.classList.remove("hidden");
    document.getElementById("combat-enemy-name").textContent = this.activeEnemy.name;
    const pct = Math.max(0, Math.round((this.activeEnemy.hp / this.activeEnemy.maxHp) * 100));
    document.getElementById("enemy-hp-bar").style.width = `${pct}%`;
    document.getElementById("enemy-hp-text").textContent = `${this.activeEnemy.hp} / ${this.activeEnemy.maxHp} HP`;
  }

  updateHUD() {
    document.getElementById("hud-name").textContent = this.player.name;
    document.getElementById("hud-class").textContent = this.player.class;

    const hpPct = Math.max(0, (this.player.hp / this.player.maxHp) * 100);
    document.getElementById("hp-bar").style.width = `${hpPct}%`;
    document.getElementById("hp-text").textContent = `${this.player.hp}/${this.player.maxHp}`;

    const manaPct = Math.max(0, (this.player.mana / this.player.maxMana) * 100);
    document.getElementById("mana-bar").style.width = `${manaPct}%`;
    document.getElementById("mana-text").textContent = `${this.player.mana}/${this.player.maxMana}`;

    document.getElementById("gold-text").textContent = `${this.player.gold} Gold`;
    document.getElementById("inventory-count").textContent = `${this.player.inventory.length} Items`;

    const invContainer = document.getElementById("inventory-list");
    invContainer.innerHTML = "";
    this.player.inventory.forEach(item => {
      const tag = document.createElement("span");
      tag.className = "inv-tag";
      tag.textContent = item;
      invContainer.appendChild(tag);
    });
  }

  selectChoice(choice) {
    sfx.playBeep(520, 'sine', 0.05);

    if (choice.restart) {
      this.restartGame();
      return;
    }

    if (choice.check) {
      const statBonus = Math.floor(this.player[choice.check] / 3);
      const roll = Math.floor(Math.random() * 20) + 1;
      const total = roll + statBonus;
      if (total >= choice.dc) {
        this.showNotification(`Dice Roll: ${roll} + ${statBonus} = ${total} (Passed DC ${choice.dc})!`);
        this.currentNodeId = choice.target;
      } else {
        this.showNotification(`Dice Roll: ${roll} + ${statBonus} = ${total} (Failed DC ${choice.dc})! You stumble back.`);
        this.player.hp = Math.max(1, this.player.hp - 10);
      }
    } else {
      this.currentNodeId = choice.target;
    }

    this.render();
  }

  render() {
    this.updateHUD();
    const node = this.storyNodes[this.currentNodeId] || this.storyNodes.start;

    document.getElementById("ascii-art").textContent = node.art || "";
    document.getElementById("node-title").textContent = node.title;
    document.getElementById("story-text").textContent = node.text;

    // Trigger onEnter effects
    if (node.onEnter) {
      const res = node.onEnter(this.player);
      if (res) this.showNotification(res);
      this.updateHUD();
    }

    // Handle Combat node
    if (node.enemy) {
      this.activeEnemy = { ...node.enemy };
      this.updateCombatView();
    } else {
      this.activeEnemy = null;
      this.updateCombatView();
    }

    // Render Choice Buttons
    const choicesBox = document.getElementById("choices-container");
    choicesBox.innerHTML = "";

    if (!node.enemy) {
      node.choices.forEach(c => {
        // Condition checks
        if (c.reqItem && !this.player.inventory.includes(c.reqItem)) {
          return;
        }

        const btn = document.createElement("button");
        btn.className = "choice-btn";
        btn.innerHTML = `
          <span>${c.text}</span>
          ${c.check ? `<span class="choice-badge">${c.check.toUpperCase()} (DC ${c.dc})</span>` : ""}
        `;
        btn.onclick = () => this.selectChoice(c);
        choicesBox.appendChild(btn);
      });
    }
  }
}

// Instantiate game on DOM ready
let game;
window.addEventListener("DOMContentLoaded", () => {
  game = new AdventureGame();
});
