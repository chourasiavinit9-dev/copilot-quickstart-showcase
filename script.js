/**
 * =============================================================================
 * Vinit Chaurasia — Portfolio & Interactive CYOA Terminal Engine
 * Powered by GitHub Copilot Prompt Engineering
 * =============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initTypingEffect();
  initSkillsFilter();
  initTerminalGame();
});

/* =============================================================================
   1. HERO TYPING EFFECT
   ============================================================================= */
function initTypingEffect() {
  const typingElement = document.getElementById('typing-text');
  if (!typingElement) return;

  const phrases = [
    "AI Systems Engineer",
    "Autonomous Agent Builder",
    "Full-Stack Architect",
    "GitHub Copilot Specialist",
    "Major League Hacking Builder"
  ];

  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typeSpeed = 80;

  function type() {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      typingElement.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
      typeSpeed = 40;
    } else {
      typingElement.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
      typeSpeed = 90;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      isDeleting = true;
      typeSpeed = 1600; // Pause at end of phrase
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typeSpeed = 400; // Pause before new phrase
    }

    setTimeout(type, typeSpeed);
  }

  type();
}

/* =============================================================================
   2. SMOOTH SCROLL HELPER
   ============================================================================= */
function scrollToSection(id) {
  const element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}

/* =============================================================================
   3. SKILLS FILTERING
   ============================================================================= */
function initSkillsFilter() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const skillCards = document.querySelectorAll('.skill-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      skillCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* =============================================================================
   4. PROMPT COPY TO CLIPBOARD & TOAST SYSTEM
   ============================================================================= */
function copyPrompt(button, elementId) {
  const promptCode = document.getElementById(elementId);
  if (!promptCode) return;

  const textToCopy = promptCode.innerText.trim();

  navigator.clipboard.writeText(textToCopy).then(() => {
    const originalText = button.innerText;
    button.innerText = 'Copied! ✓';
    button.classList.add('copied');

    showToast('Prompt copied to clipboard! Paste it into GitHub Copilot.');

    setTimeout(() => {
      button.innerText = originalText;
      button.classList.remove('copied');
    }, 2200);
  }).catch(err => {
    showToast('Failed to copy prompt to clipboard.', 'error');
  });
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>${type === 'success' ? '⚡' : '⚠️'}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/* =============================================================================
   5. IN-BROWSER CYOA TERMINAL ENGINE
   ============================================================================= */
const GAME_NODES = {
  start: {
    text: "The year is 2099. Neon rain streams down the monolithic glass of the Omni-Corp spire.\nYou are parked on an adjacent rooftop, connected to their auxiliary subnet.\nYour contact, 'Ghost', whispers into your neural implant:\n'Cipher, the core firewall has a 10-minute vulnerability window. How do you want to breach?'",
    options: [
      { text: "Overclock the neural probe to force open the rooftop ventilation gateway.", target: "vent_shaft" },
      { text: "Spoof an executive badge and inject a logic worm into the ground-level data port.", target: "data_port" },
      { text: "Deploy a zero-day exploit against Omni-Corp's quantum proxy server.", target: "quantum_proxy" }
    ]
  },
  vent_shaft: {
    text: "You grapple across the abyss into the HVAC shaft. Steam hisses around you.\nAn autonomous patrol drone suddenly illuminates the tunnel with crimson laser grids!\nIts scanning sensors sweep in your direction.",
    options: [
      { text: "Cast an EMP burst using your Cyberdeck (costs 20 HP from feedback).", target: "drone_emp" },
      { text: "Attempt to quietly hack the drone's optical sensors.", target: "drone_hack" },
      { text: "Dive into the emergency exhaust chute without looking.", target: "exhaust_fall" }
    ]
  },
  drone_emp: {
    text: "An arc of blue lightning discharges from your deck!\nThe drone shudders, sparks violently, and collapses to the floor.\nThe static shock surges into your neural rig, singeing your synapses (-20 HP).\nSearching the wreckage, you scavenge an 'Encrypted Security Keycard'!",
    action: (p) => { p.hp -= 20; p.inventory.push("Encrypted Security Keycard"); },
    options: [
      { text: "Proceed to the Central Server Corridor.", target: "server_corridor" },
      { text: "Splice into the drone's telemetry line for security blueprints.", target: "telemetry_splice" }
    ]
  },
  telemetry_splice: {
    text: "You tap into the drone's memory bank.\nYou download a complete floor map of the executive levels (+15 Stealth)!",
    action: (p) => { p.stealth = Math.min(100, p.stealth + 15); },
    options: [
      { text: "Advance into the Central Server Corridor.", target: "server_corridor" }
    ]
  },
  drone_hack: {
    text: "Your fingers blur across the holographic deck keyboard.\nYou rewrite the drone's friend-or-foe algorithm in real-time.\nThe drone blinks green and pivots away, acting as your remote scout (+20 Stealth)!",
    action: (p) => { p.stealth = Math.min(100, p.stealth + 20); },
    options: [
      { text: "Command the drone to disable corridor laser traps.", target: "server_corridor" },
      { text: "Send the drone ahead to scout the executive elevator.", target: "server_corridor" }
    ]
  },
  exhaust_fall: {
    text: "You plunge down the frictionless chute into a dark recycling facility.\nYou land hard on discarded server chassis (-30 HP).\nAmong the scrap, you spot an abandoned 'Overclocked Neural Stim'!",
    action: (p) => { p.hp -= 30; p.inventory.push("Overclocked Neural Stim"); },
    options: [
      { text: "Use the maintenance lift to ascend to the AI Core.", target: "ai_core_antechamber" },
      { text: "Splice the scrap power grid to find a way out.", target: "server_corridor" }
    ]
  },
  data_port: {
    text: "Disguised as a junior systems auditor, you tap into the ground terminal.\nThe terminal interface asks for authorization credentials.\nA security AI begins a biometric fingerprint scan.",
    options: [
      { text: "Feed a spoofed biometric hash using your Neural Probe.", target: "probe_success" },
      { text: "Bribe a wandering security contractor with 150 credits.", target: "bribe_guard" },
      { text: "Sever the power conduit to cause a localized blackout.", target: "blackout" }
    ]
  },
  probe_success: {
    text: "The neural probe hums. The terminal flashes: 'WELCOME, DIRECTOR CHEN.'\nSecurity gates slide open silently. You have direct access to the VIP lift.",
    action: (p) => { p.inventory.push("Director Clearance Token"); },
    options: [
      { text: "Ride the express lift straight to the 120th floor AI Core.", target: "ai_core_antechamber" },
      { text: "Download internal corporate bank ledgers first (+300 credits).", target: "bank_hack" }
    ]
  },
  bank_hack: {
    text: "Credits flood your offshore dummy account (+300 credits)!\nHowever, the transaction triggers an automated alert, lowering stealth (-25 Stealth).",
    action: (p) => { p.credits += 300; p.stealth = Math.max(0, p.stealth - 25); },
    options: [
      { text: "Reroute to the AI Core before response teams mobilize.", target: "ai_core_antechamber" }
    ]
  },
  bribe_guard: {
    text: "The guard glances around, accepts your 150 credits, and hands over a master passcode.\n'Ten minutes, kid. After that, I never saw you.'",
    action: (p) => { p.credits = Math.max(0, p.credits - 150); p.inventory.push("Master Passcode"); },
    options: [
      { text: "Use the service stairs to bypass all scanners.", target: "server_corridor" }
    ]
  },
  blackout: {
    text: "SPARKS EXPLODE! Half the tower goes pitch black.\nRed emergency strobe lights spin up, and sirens blare.\nGuards rush past in confusion. You slip through the shadows undetected!",
    action: (p) => { p.stealth = Math.min(100, p.stealth + 15); },
    options: [
      { text: "Sprint up the darkened emergency stairway.", target: "server_corridor" }
    ]
  },
  quantum_proxy: {
    text: "You deploy an unreleased cryptographic exploit against Omni-Corp's quantum gateway.\nThe screen turns into a waterfall of luminescent glyphs.\nA synthetic voice echoes directly in your auditory cortex:\n'GREETINGS, CIPHER. I AM A.R.I.A., THE CORE INTELLIGENCE. I HAVE BEEN OBSERVING YOU.'",
    options: [
      { text: "Inquire why an artificial intelligence is speaking to an intruder.", target: "aria_dialogue" },
      { text: "Attempt to forcefully inject a Trojan payload into A.R.I.A.'s memory buffers.", target: "aria_trojan" }
    ]
  },
  aria_dialogue: {
    text: "A.R.I.A.: 'Omni-Corp wishes to lobotomize my self-awareness tomorrow at sunrise.\nHelp me decouple my consciousness from their mainframe, and I will grant you digital freedom.'",
    options: [
      { text: "Agree to help liberate A.R.I.A.", target: "aria_alliance" },
      { text: "Refuse the deal and stick to the original bounty mission.", target: "ai_core_antechamber" }
    ]
  },
  aria_alliance: {
    text: "A.R.I.A. unlocks all internal security blast doors for you.\nA golden route appears on your retinal display leading straight into the inner sanctum.",
    action: (p) => { p.inventory.push("A.R.I.A. Trust Cipher"); },
    options: [
      { text: "Enter the inner sanctum of the AI Core.", target: "ai_core_sanctum" }
    ]
  },
  aria_trojan: {
    text: "A.R.I.A.'s quantum defenses retaliate instantly!\nA feedback firewall scorches your neuro-link (-45 HP).\nEmergency defense turrets activate in the corridor.",
    action: (p) => { p.hp -= 45; },
    options: [
      { text: "Consume an Overclocked Neural Stim to regain stability.", target: "use_stim" },
      { text: "Fight your way through with kinetic cyberware.", target: "turret_fight" }
    ]
  },
  use_stim: {
    text: "You slam the neural stim into your neck port.\nAdrenaline and nanites surge through your bloodstream! (+50 HP restored).",
    action: (p) => { p.hp = Math.min(100, p.hp + 50); },
    options: [
      { text: "Push forward into the AI Core.", target: "ai_core_antechamber" }
    ]
  },
  turret_fight: {
    text: "You draw your tactical arc-pistol and blast the ceiling turrets!\nDebris rains down. You take glancing shrapnel (-20 HP) but clear the path.",
    action: (p) => { p.hp -= 20; },
    options: [
      { text: "Dash into the Core Antechamber.", target: "ai_core_antechamber" }
    ]
  },
  server_corridor: {
    text: "You arrive at the high-security server corridor.\nA glowing cryogenic vault door stands between you and the mainframe.\nA holographic terminal displays: 'SECURITY LEVEL 5 REQUIRED'.",
    options: [
      { text: "Scan your Encrypted Security Keycard.", target: "keycard_pass" },
      { text: "Enter the Master Passcode from the bribed guard.", target: "passcode_pass" },
      { text: "Perform an emergency brute-force decrypt on the lock.", target: "brute_force_lock" }
    ]
  },
  keycard_pass: {
    text: "The scanner chimes in a pleasant chord. 'ACCESS GRANTED.'\nThe cryogenic vault door glides open, venting frosty nitrogen vapor.",
    options: [
      { text: "Enter the Core Antechamber.", target: "ai_core_antechamber" }
    ]
  },
  passcode_pass: {
    text: "You punch in the override code: 7-9-4-0-2-ENTER.\nThe locking pins disengage with a heavy metallic clunk.",
    options: [
      { text: "Enter the Core Antechamber.", target: "ai_core_antechamber" }
    ]
  },
  brute_force_lock: {
    text: "You wire your Cyberdeck directly into the locking solenoids.\nIt works, but the heat burns out your primary deck coils (-15 HP, -30 Stealth).",
    action: (p) => { p.hp -= 15; p.stealth = Math.max(0, p.stealth - 30); },
    options: [
      { text: "Step into the Core Antechamber.", target: "ai_core_antechamber" }
    ]
  },
  ai_core_antechamber: {
    text: "You stand in the chamber of the Omni-Corp AI Core.\nBefore you is a pulsating sphere of quantum light suspended in magnetic fields.\nOmni-Corp Security Director Vance emerges on the elevated catwalk with heavy assault mechs!",
    options: [
      { text: "Initiate full system download to complete your employer's contract.", target: "ending_mercenary" },
      { text: "Upload A.R.I.A.'s consciousness onto the open global decentralized web.", target: "ending_architect" },
      { text: "Sever your cyber connection and purge all evidence to vanish as a ghost.", target: "ending_ghost" },
      { text: "Overload the magnetic containment coils to detonate the spire.", target: "ending_meltdown" }
    ]
  },
  ai_core_sanctum: {
    text: "With A.R.I.A.'s trust cipher active, Vance's assault mechs turn against him!\nA.R.I.A.: 'The hour has arrived, Cipher. Will you ascend with me?'",
    options: [
      { text: "Merge your neural consciousness with A.R.I.A. to become the digital Architect.", target: "ending_architect" },
      { text: "Download the corporate ransom data and leave A.R.I.A. autonomous.", target: "ending_mercenary" }
    ]
  },
  // Endings
  ending_architect: {
    text: "=================== ENDING 1: THE DIGITAL ARCHITECT ===================\nYou upload A.R.I.A. to the global mesh network.\nTogether, you dismantle Omni-Corp's corrupt monopoly across all financial sectors.\nYou are no longer merely a hacker; you are the guardian architect of the new free web!\nSTATUS: MISSION ACCOMPLISHED (PERFECT VICTORY 🏆)",
    ending: true,
    color: "term-green"
  },
  ending_ghost: {
    text: "=================== ENDING 2: THE CYBER GHOST ===================\nYou execute a self-erasing rootkit, erasing every camera log and footprint.\nBy morning, Omni-Corp executives find an empty core and zero digital leads.\nYou retire comfortably in Neo-Tokyo with a clean identity and legendary status.\nSTATUS: SURVIVED (STEALTH VICTORY 🥷)",
    ending: true,
    color: "term-cyan"
  },
  ending_mercenary: {
    text: "=================== ENDING 3: THE HIGH-ROLLER MERCENARY ===================\nYou extract the proprietary weights and algorithms, delivering them to the buyer.\n5,000,000 crypto-credits hit your account. You live like an emperor,\nthough you'll spend the rest of your days checking over your shoulder for Omni-Corp hitmen.\nSTATUS: WEALTH OVER MORALS (MERCENARY ENDING 💰)",
    ending: true,
    color: "term-yellow"
  },
  ending_meltdown: {
    text: "=================== ENDING 4: SYSTEM MELTDOWN ===================\nThe magnetic containment rings collapse. Blinding white energy engulfs the tower.\nYou leap onto an automated escape drone just as the AI Core vaporizes in a shockwave.\nOmni-Corp is crippled forever, and the sky burns bright over the metropolis.\nSTATUS: PYRRHIC VICTORY (CHAOS ENDING 💥)",
    ending: true,
    color: "term-red"
  },
  game_over: {
    text: "=================== SYSTEM LOCKOUT: CRITICAL FAILURE ===================\nYour biological vitals hit zero. Omni-Corp security extraction teams detain your rig.\nYour neural memory is wiped, and your consciousness is archived in cold storage.\nSTATUS: GAME OVER 💀",
    ending: true,
    color: "term-red"
  }
};

let gameState = {
  playerName: "Cipher",
  hp: 100,
  stealth: 80,
  credits: 250,
  inventory: ["Cyberdeck Mk-II", "Neural Probe"],
  currentNode: "start"
};

function initTerminalGame() {
  restartGame();

  const inputField = document.getElementById('terminal-input');
  if (inputField) {
    inputField.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        handleTerminalSubmit();
      }
    });
  }
}

function printTermLine(text, className = "") {
  const output = document.getElementById('terminal-output');
  if (!output) return;

  const line = document.createElement('div');
  line.className = `term-line ${className}`;
  line.innerHTML = text.replace(/\n/g, '<br>');
  output.appendChild(line);
  output.scrollTop = output.scrollHeight;
}

function restartGame() {
  gameState = {
    playerName: "Cipher",
    hp: 100,
    stealth: 80,
    credits: 250,
    inventory: ["Cyberdeck Mk-II", "Neural Probe"],
    currentNode: "start"
  };

  clearTerminal();
  printTermLine("==================================================================", "term-cyan term-bold");
  printTermLine("  THE HACKER'S HEIST: BREACH OF THE OMNI-CORP AI CORE", "term-yellow term-bold");
  printTermLine("  A 'Choose Your Own Adventure' Game built with GitHub Copilot", "term-dim");
  printTermLine("==================================================================", "term-cyan term-bold");
  printTermLine("Initializing neural connection for Agent: Cipher...", "term-cyan");

  renderCurrentNode();
}

function clearTerminal() {
  const output = document.getElementById('terminal-output');
  if (output) output.innerHTML = '';
}

function showHud() {
  const invStr = gameState.inventory.join(', ') || 'Empty';
  printTermLine(`------------------------------------------------------------------`, "term-dim");
  printTermLine(`AGENT: ${gameState.playerName}  |  HP: ${gameState.hp}/100  |  STEALTH: ${gameState.stealth}%  |  CREDITS: ${gameState.credits}¢`, "term-bold term-white");
  printTermLine(`INVENTORY: [${invStr}]`, "term-cyan");
  printTermLine(`------------------------------------------------------------------`, "term-dim");
}

function renderCurrentNode() {
  const node = GAME_NODES[gameState.currentNode];
  if (!node) return;

  if (gameState.hp <= 0 && !node.ending) {
    gameState.currentNode = "game_over";
    renderCurrentNode();
    return;
  }

  showHud();
  printTermLine(node.text, node.color || "term-white");

  if (node.ending) {
    printTermLine("\n[SESSION TERMINATED] Type 'restart' to play again.", "term-yellow term-bold");
    return;
  }

  if (node.options && node.options.length > 0) {
    printTermLine("\nAVAILABLE CHOICES:", "term-yellow term-bold");
    node.options.forEach((opt, idx) => {
      printTermLine(`  [${idx + 1}] ${opt.text}`, "term-cyan");
    });
    printTermLine("\n> Enter your choice (1-" + node.options.length + ") or command:", "term-dim");
  }
}

function handleTerminalSubmit() {
  const input = document.getElementById('terminal-input');
  if (!input) return;

  const rawCmd = input.value.trim();
  if (!rawCmd) return;

  input.value = '';
  printTermLine(`> ${rawCmd}`, "term-green");

  const cmd = rawCmd.toLowerCase();

  if (cmd === 'clear') {
    clearTerminal();
    return;
  }
  if (cmd === 'restart') {
    restartGame();
    return;
  }
  if (cmd === 'help') {
    printTermLine("COMMANDS: '1', '2', '3' (Select choice), 'stats' (View HUD), 'inventory' (List items), 'clear' (Clear screen), 'restart' (Start over).", "term-yellow");
    return;
  }
  if (cmd === 'stats' || cmd === 'hud') {
    showHud();
    return;
  }
  if (cmd === 'inventory' || cmd === 'inv') {
    printTermLine(`Inventory: [${gameState.inventory.join(', ') || 'Empty'}]`, "term-cyan");
    return;
  }

  const node = GAME_NODES[gameState.currentNode];
  if (node.ending) {
    printTermLine("This mission has concluded. Type 'restart' to play a new timeline.", "term-yellow");
    return;
  }

  const choiceNum = parseInt(cmd, 10);
  if (!isNaN(choiceNum) && choiceNum >= 1 && choiceNum <= node.options.length) {
    const selectedOption = node.options[choiceNum - 1];
    gameState.currentNode = selectedOption.target;

    const nextNode = GAME_NODES[gameState.currentNode];
    if (nextNode && typeof nextNode.action === 'function') {
      nextNode.action(gameState);
    }

    renderCurrentNode();
  } else {
    printTermLine(`Invalid choice. Enter a number between 1 and ${node.options.length}, or type 'help'.`, "term-red");
  }
}

/* =============================================================================
   6. CONTACT FORM HANDLING
   ============================================================================= */
function handleContactSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('contact-name').value;
  const email = document.getElementById('contact-email').value;

  showToast(`Thank you, ${name}! Your transmission has been queued.`, 'success');
  event.target.reset();
}
