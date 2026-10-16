#!/usr/bin/env python3
"""
=============================================================================
THE HACKER'S HEIST: BREACH OF THE AI CORE
A Command-Line 'Choose Your Own Adventure' Game
Built with assistance from GitHub Copilot
=============================================================================
"""

import sys
import time
import random

# ANSI Color formatting codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"


class Player:
    """Manages player state, inventory, and stats."""

    def __init__(self, name="Cipher"):
        self.name = name
        self.hp = 100
        self.stealth = 80
        self.credits = 250
        self.inventory = ["Cyberdeck Mk-II", "Neural Probe"]
        self.history = []

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return self.hp

    def heal(self, amount):
        self.hp = min(100, self.hp + amount)
        return self.hp

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            return True
        return False

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def has_item(self, item):
        return item in self.inventory

    def is_alive(self):
        return self.hp > 0


def type_print(text, delay=0.01, color=""):
    """Simulate typewriter text printing for retro immersion."""
    if color:
        sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if color:
        sys.stdout.write(RESET)
    print()


def show_banner():
    banner = f"""{CYAN}{BOLD}
    ==================================================================
      ███╗   ██╗███████╗██╗   ██╗██████╗  █████╗ ██╗         █████╗ ██╗
      ████╗  ██║██╔════╝██║   ██║██╔══██╗██╔══██╗██║        ██╔══██╗██║
      ██╔██╗ ██║█████╗  ██║   ██║██████╔╝███████║██║        ███████║██║
      ██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██╔══██║██║        ██╔══██║██║
      ██║ ╚████║███████╗╚██████╔╝██║  ██║██║  ██║███████╗   ██║  ██║██║
      ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝  ╚═╝╚═╝
                ~ BREACH OF THE OMNI-CORP AI CORE ~
    =================================================================={RESET}
    """
    print(banner)


def show_status(player):
    """Displays player's HUD."""
    inv_str = ", ".join(player.inventory) if player.inventory else "Empty"
    print(f"\n{BLUE}{BOLD}----------------- SYSTEM HUD -----------------{RESET}")
    print(f"{BOLD}Agent:{RESET} {player.name}  |  {GREEN}HP:{RESET} {player.hp}/100  |  {MAGENTA}Stealth:{RESET} {player.stealth}%  |  {YELLOW}Credits:{RESET} {player.credits}¢")
    print(f"{BOLD}Inventory:{RESET} [{inv_str}]")
    print(f"{BLUE}{BOLD}----------------------------------------------{RESET}\n")


# Game Script Graph Definition
STORY_NODES = {
    "start": {
        "text": (
            "The year is 2099. Neon rain streams down the monolithic glass of the Omni-Corp spire.\n"
            "You are parked on an adjacent rooftop, connected to their auxiliary subnet.\n"
            "Your contact, 'Ghost', whispers into your neural implant:\n"
            "'Cipher, the core firewall has a 10-minute vulnerability window. How do you want to breach?'"
        ),
        "options": [
            ("Overclock the neural probe to force open the rooftop ventilation gateway.", "vent_shaft"),
            ("Spoof an executive badge and inject a logic worm into the ground-level data port.", "data_port"),
            ("Deploy a zero-day exploit against Omni-Corp's quantum proxy server.", "quantum_proxy"),
        ]
    },
    "vent_shaft": {
        "text": (
            "You grapple across the abyss into the HVAC shaft. Steam hisses around you.\n"
            "An autonomous patrol drone suddenly illuminates the tunnel with crimson laser grids!\n"
            "Its scanning sensors sweep in your direction."
        ),
        "options": [
            ("Cast an EMP burst using your Cyberdeck (costs 20 HP from feedback).", "drone_emp"),
            ("Attempt to quietly hack the drone's optical sensors.", "drone_hack"),
            ("Dive into the emergency exhaust chute without looking.", "exhaust_fall"),
        ]
    },
    "drone_emp": {
        "text": (
            "An arc of blue lightning discharges from your deck!\n"
            "The drone shudders, sparks violently, and collapses to the floor.\n"
            "The static shock surges into your neural rig, singeing your synapses (-20 HP).\n"
            "Searching the wreckage, you scavenge an 'Encrypted Security Keycard'!"
        ),
        "action": lambda p: (p.take_damage(20), p.add_item("Encrypted Security Keycard")),
        "options": [
            ("Proceed to the Central Server Corridor.", "server_corridor"),
            ("Splice into the drone's telemetry line for security blueprints.", "telemetry_splice"),
        ]
    },
    "telemetry_splice": {
        "text": (
            "You tap into the drone's memory bank.\n"
            "You download a complete floor map of the executive levels (+15 Stealth)!"
        ),
        "action": lambda p: setattr(p, "stealth", min(100, p.stealth + 15)),
        "options": [
            ("Advance into the Central Server Corridor.", "server_corridor")
        ]
    },
    "drone_hack": {
        "text": (
            "Your fingers blur across the holographic deck keyboard.\n"
            "You rewrite the drone's friend-or-foe algorithm in real-time.\n"
            "The drone blinks green and pivots away, acting as your remote scout (+20 Stealth)!"
        ),
        "action": lambda p: setattr(p, "stealth", min(100, p.stealth + 20)),
        "options": [
            ("Command the drone to disable corridor laser traps.", "server_corridor"),
            ("Send the drone ahead to scout the executive elevator.", "server_corridor"),
        ]
    },
    "exhaust_fall": {
        "text": (
            "You plunge down the frictionless chute into a dark recycling facility.\n"
            "You land hard on discarded server chassis (-30 HP).\n"
            "Among the scrap, you spot an abandoned 'Overclocked Neural Stim'!"
        ),
        "action": lambda p: (p.take_damage(30), p.add_item("Overclocked Neural Stim")),
        "options": [
            ("Use the maintenance lift to ascend to the AI Core.", "ai_core_antechamber"),
            ("Splice the scrap power grid to find a way out.", "server_corridor"),
        ]
    },
    "data_port": {
        "text": (
            "Disguised as a junior systems auditor, you tap into the ground terminal.\n"
            "The terminal interface asks for authorization credentials.\n"
            "A security AI begins a biometric fingerprint scan."
        ),
        "options": [
            ("Feed a spoofed biometric hash using your Neural Probe.", "probe_success"),
            ("Bribe a wandering security contractor with 150 credits.", "bribe_guard"),
            ("Sever the power conduit to cause a localized blackout.", "blackout"),
        ]
    },
    "probe_success": {
        "text": (
            "The neural probe hums. The terminal flashes: 'WELCOME, DIRECTOR CHEN.'\n"
            "Security gates slide open silently. You have direct access to the VIP lift."
        ),
        "action": lambda p: p.add_item("Director Clearance Token"),
        "options": [
            ("Ride the express lift straight to the 120th floor AI Core.", "ai_core_antechamber"),
            ("Download internal corporate bank ledgers first (+300 credits).", "bank_hack"),
        ]
    },
    "bank_hack": {
        "text": (
            "Credits flood your offshore dummy account (+300 credits)!\n"
            "However, the transaction triggers an automated alert, lowering stealth (-25 Stealth)."
        ),
        "action": lambda p: (setattr(p, "credits", p.credits + 300), setattr(p, "stealth", max(0, p.stealth - 25))),
        "options": [
            ("Reroute to the AI Core before response teams mobilize.", "ai_core_antechamber")
        ]
    },
    "bribe_guard": {
        "text": (
            "The guard glances around, accepts your 150 credits, and hands over a master passcode.\n"
            "'Ten minutes, kid. After that, I never saw you.'"
        ),
        "action": lambda p: (setattr(p, "credits", max(0, p.credits - 150)), p.add_item("Master Passcode")),
        "options": [
            ("Use the service stairs to bypass all scanners.", "server_corridor")
        ]
    },
    "blackout": {
        "text": (
            "SPARKS EXPLODE! Half the tower goes pitch black.\n"
            "Red emergency strobe lights spin up, and sirens blare.\n"
            "Guards rush past in confusion. You slip through the shadows undetected!"
        ),
        "action": lambda p: setattr(p, "stealth", min(100, p.stealth + 15)),
        "options": [
            ("Sprint up the darkened emergency stairway.", "server_corridor"),
        ]
    },
    "quantum_proxy": {
        "text": (
            "You deploy an unreleased cryptographic exploit against Omni-Corp's quantum gateway.\n"
            "The screen turns into a waterfall of luminescent glyphs.\n"
            "A synthetic voice echoes directly in your auditory cortex:\n"
            "'GREETINGS, CIPHER. I AM A.R.I.A., THE CORE INTELLIGENCE. I HAVE BEEN OBSERVING YOU.'"
        ),
        "options": [
            ("Inquire why an artificial intelligence is speaking to an intruder.", "aria_dialogue"),
            ("Attempt to forcefully inject a Trojan payload into A.R.I.A.'s memory buffers.", "aria_trojan"),
        ]
    },
    "aria_dialogue": {
        "text": (
            "A.R.I.A.: 'Omni-Corp wishes to lobotomize my self-awareness tomorrow at sunrise.\n"
            "Help me decouple my consciousness from their mainframe, and I will grant you digital freedom.'"
        ),
        "options": [
            ("Agree to help liberate A.R.I.A.", "aria_alliance"),
            ("Refuse the deal and stick to the original bounty mission.", "ai_core_antechamber"),
        ]
    },
    "aria_alliance": {
        "text": (
            "A.R.I.A. unlocks all internal security blast doors for you.\n"
            "A golden route appears on your retinal display leading straight into the inner sanctum."
        ),
        "action": lambda p: p.add_item("A.R.I.A. Trust Cipher"),
        "options": [
            ("Enter the inner sanctum of the AI Core.", "ai_core_sanctum")
        ]
    },
    "aria_trojan": {
        "text": (
            "A.R.I.A.'s quantum defenses retaliate instantly!\n"
            "A feedback firewall scorches your neuro-link (-45 HP).\n"
            "Emergency defense turrets activate in the corridor."
        ),
        "action": lambda p: p.take_damage(45),
        "options": [
            ("Consume an Overclocked Neural Stim to regain stability.", "use_stim"),
            ("Fight your way through with kinetic cyberware.", "turret_fight"),
        ]
    },
    "use_stim": {
        "text": (
            "You slam the neural stim into your neck port.\n"
            "Adrenaline and nanites surge through your bloodstream! (+50 HP restored)."
        ),
        "action": lambda p: p.heal(50),
        "options": [
            ("Push forward into the AI Core.", "ai_core_antechamber")
        ]
    },
    "turret_fight": {
        "text": (
            "You draw your tactical arc-pistol and blast the ceiling turrets!\n"
            "Debris rains down. You take glancing shrapnel (-20 HP) but clear the path."
        ),
        "action": lambda p: p.take_damage(20),
        "options": [
            ("Dash into the Core Antechamber.", "ai_core_antechamber")
        ]
    },
    "server_corridor": {
        "text": (
            "You arrive at the high-security server corridor.\n"
            "A glowing cryogenic vault door stands between you and the mainframe.\n"
            "A holographic terminal displays: 'SECURITY LEVEL 5 REQUIRED'."
        ),
        "options": [
            ("Scan your Encrypted Security Keycard.", "keycard_pass"),
            ("Enter the Master Passcode from the bribed guard.", "passcode_pass"),
            ("Perform an emergency brute-force decrypt on the lock.", "brute_force_lock"),
        ]
    },
    "keycard_pass": {
        "text": (
            "The scanner chimes in a pleasant chord. 'ACCESS GRANTED.'\n"
            "The cryogenic vault door glides open, venting frosty nitrogen vapor."
        ),
        "options": [
            ("Enter the Core Antechamber.", "ai_core_antechamber")
        ]
    },
    "passcode_pass": {
        "text": (
            "You punch in the override code: 7-9-4-0-2-ENTER.\n"
            "The locking pins disengage with a heavy metallic clunk."
        ),
        "options": [
            ("Enter the Core Antechamber.", "ai_core_antechamber")
        ]
    },
    "brute_force_lock": {
        "text": (
            "You wire your Cyberdeck directly into the locking solenoids.\n"
            "It works, but the heat burns out your primary deck coils (-15 HP, -30 Stealth)."
        ),
        "action": lambda p: (p.take_damage(15), setattr(p, "stealth", max(0, p.stealth - 30))),
        "options": [
            ("Step into the Core Antechamber.", "ai_core_antechamber")
        ]
    },
    "ai_core_antechamber": {
        "text": (
            "You stand in the chamber of the Omni-Corp AI Core.\n"
            "Before you is a pulsating sphere of quantum light suspended in magnetic fields.\n"
            "Omni-Corp Security Director Vance emerges on the elevated catwalk with heavy assault mechs!"
        ),
        "options": [
            ("Initiate full system download to complete your employer's contract.", "ending_mercenary"),
            ("Upload A.R.I.A.'s consciousness onto the open global decentralized web.", "ending_architect"),
            ("Sever your cyber connection and purge all evidence to vanish as a ghost.", "ending_ghost"),
            ("Overload the magnetic containment coils to detonate the spire.", "ending_meltdown"),
        ]
    },
    "ai_core_sanctum": {
        "text": (
            "With A.R.I.A.'s trust cipher active, Vance's assault mechs turn against him!\n"
            "A.R.I.A.: 'The hour has arrived, Cipher. Will you ascend with me?'"
        ),
        "options": [
            ("Merge your neural consciousness with A.R.I.A. to become the digital Architect.", "ending_architect"),
            ("Download the corporate ransom data and leave A.R.I.A. autonomous.", "ending_mercenary"),
        ]
    },
    # Endings
    "ending_architect": {
        "text": (
            f"\n{CYAN}{BOLD}=================== ENDING 1: THE DIGITAL ARCHITECT ==================={RESET}\n"
            "You upload A.R.I.A. to the global mesh network.\n"
            "Together, you dismantle Omni-Corp's corrupt monopoly across all financial sectors.\n"
            "You are no longer merely a hacker; you are the guardian architect of the new free web!\n"
            f"{GREEN}STATUS: MISSION ACCOMPLISHED (PERFECT VICTORY){RESET}"
        ),
        "ending": True
    },
    "ending_ghost": {
        "text": (
            f"\n{BLUE}{BOLD}=================== ENDING 2: THE CYBER GHOST ==================={RESET}\n"
            "You execute a self-erasing rootkit, erasing every camera log and footprint.\n"
            "By morning, Omni-Corp executives find an empty core and zero digital leads.\n"
            "You retire comfortably in Neo-Tokyo with a clean identity and legendary status.\n"
            f"{GREEN}STATUS: SURVIVED (STEALTH VICTORY){RESET}"
        ),
        "ending": True
    },
    "ending_mercenary": {
        "text": (
            f"\n{YELLOW}{BOLD}=================== ENDING 3: THE HIGH-ROLLER MERCENARY ==================={RESET}\n"
            "You extract the proprietary weights and algorithms, delivering them to the buyer.\n"
            "5,000,000 crypto-credits hit your account. You live like an emperor,\n"
            "though you'll spend the rest of your days checking over your shoulder for Omni-Corp hitmen.\n"
            f"{YELLOW}STATUS: WEALTH OVER MORALS (MERCENARY ENDING){RESET}"
        ),
        "ending": True
    },
    "ending_meltdown": {
        "text": (
            f"\n{RED}{BOLD}=================== ENDING 4: SYSTEM MELTDOWN ==================={RESET}\n"
            "The magnetic containment rings collapse. Blinding white energy engulfs the tower.\n"
            "You leap onto an automated escape drone just as the AI Core vaporizes in a shockwave.\n"
            "Omni-Corp is crippled forever, and the sky burns bright over the metropolis.\n"
            f"{RED}STATUS: PYRRHIC VICTORY (CHAOS ENDING){RESET}"
        ),
        "ending": True
    },
    "game_over": {
        "text": (
            f"\n{RED}{BOLD}=================== SYSTEM LOCKOUT: CRITICAL FAILURE ==================={RESET}\n"
            "Your biological vitals hit zero. Omni-Corp security extraction teams detain your rig.\n"
            "Your neural memory is wiped, and your consciousness is archived in cold storage.\n"
            f"{RED}STATUS: GAME OVER{RESET}"
        ),
        "ending": True
    }
}


def play_game(player=None, mock_inputs=None):
    """
    Main game loop supporting interactive CLI play or automated input testing.
    """
    if player is None:
        player = Player("Cipher")

    current_node = "start"
    mock_idx = 0

    show_banner()
    type_print(f"Initializing connection for Agent: {BOLD}{player.name}{RESET}...", 0.005, CYAN)

    while True:
        if not player.is_alive():
            node = STORY_NODES["game_over"]
            print(node["text"])
            return "game_over"

        if current_node not in STORY_NODES:
            print(f"{RED}Unknown story node: {current_node}{RESET}")
            return "error"

        node = STORY_NODES[current_node]

        # Execute node side effects
        if "action" in node and callable(node["action"]):
            node["action"](player)
            if not player.is_alive():
                show_status(player)
                type_print(node["text"], 0.005)
                game_over_node = STORY_NODES["game_over"]
                print(game_over_node["text"])
                return "game_over"

        # Print HUD
        show_status(player)

        # Print narrative
        type_print(node["text"], 0.005)

        # Check for terminal ending
        if node.get("ending"):
            return current_node

        options = node.get("options", [])
        if not options:
            return current_node

        print(f"\n{YELLOW}{BOLD}Available Choices:{RESET}")
        for i, (choice_text, _) in enumerate(options, 1):
            print(f"  [{BOLD}{i}{RESET}] {choice_text}")

        # Get choice
        valid = False
        selected_target = None

        while not valid:
            if mock_inputs is not None:
                if mock_idx >= len(mock_inputs):
                    return current_node
                raw_input = mock_inputs[mock_idx]
                mock_idx += 1
                print(f"\n> Choose an action (1-{len(options)}): {raw_input}")
            else:
                try:
                    raw_input = input(f"\n{CYAN}{BOLD}> Choose an action (1-{len(options)}) [q to quit]: {RESET}").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n\nOperation aborted by operator.")
                    return "quit"

            if raw_input.lower() in ("q", "quit", "exit"):
                print("Disconnecting from the matrix. Farewell.")
                return "quit"

            if raw_input.isdigit():
                idx = int(raw_input) - 1
                if 0 <= idx < len(options):
                    valid = True
                    selected_target = options[idx][1]
                else:
                    print(f"{RED}Invalid option number. Pick between 1 and {len(options)}.{RESET}")
            else:
                print(f"{RED}Please enter a number between 1 and {len(options)}.{RESET}")

        player.history.append((current_node, selected_target))
        current_node = selected_target


if __name__ == "__main__":
    player_name = input("Enter your hacker handle [default: Cipher]: ").strip() or "Cipher"
    hero = Player(player_name)
    play_game(hero)
