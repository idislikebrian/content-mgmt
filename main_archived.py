import os
import json
import random
import time
import datetime
from farcaster import Warpcast
from dotenv import load_dotenv

load_dotenv()

client = Warpcast(mnemonic=os.getenv("MNEMONIC_ENV_VAR"))

USED_LOG_PATH = "used_casts.json"

# ---------------------
# Nested Dictionary of Casts
# ---------------------

casts = {
    "art": {
        "wake_bait": [
            "Art isn’t a job. It’s labor that refuses efficiency. That’s why capitalism keeps trying to domesticate it.",
            "The art world’s favorite medium isn’t paint — it’s hierarchy.",
            "If you’re lucky, your work won’t fit anywhere. That’s how you know it’s yours.",
            "Critics call it “emerging” because they can’t admit they don’t understand it yet."
        ],
        "process_flex": [
            "The studio is a factory pretending to be a temple. The art fair is a temple pretending to be a factory.",
            "Collectors don’t buy art — they buy evidence of belief.",
            "You can’t unionize meaning, but you can price your time like you mean it.",
            "The phrase “creative industry” is an oxymoron that learned to invoice."
        ],
        "insight_joke": [
            "Every artist says they hate networking until the champagne hits.",
            "Galleries call it representation. In any other field, we’d call it management.",
            "The art world is one big group project where everyone pretends they did the most work.",
            "Thinking about starting a union for over-thinkers. Dues payable in drafts and despair."
        ],
        "project_question": [
            "Art isn’t supposed to scale. That’s what makes it dangerous.",
            "What would happen if artists actually treated themselves like workers? Would the art get worse or the contracts get better?",
            "The only sustainable art practice is honesty — and even that costs rent.",
            "The real avant-garde is anyone who figures out how to make rent without killing the work."
        ],
        "wrap_convo_chaos": [
            "Half the industry runs on unpaid optimism. The other half runs on people who pretend not to notice.",
            "The “art world” isn’t a place — it’s a filtration system. Talent goes in. Capital comes out.",
            "Art survives because someone still believes in useless beauty. Even when it stops paying.",
            "Every artist wants to change the world until their first grant report is due."
        ]
    },
   "cars": {
        "wake_bait": [
            "Coffee, grease, and chaos — the real trinity of productivity.",
            "Every mechanic is a philosopher of failure. You just learn through torque instead of text.",
            "The tools don’t lie. They remember every mistake you tried to hide.",
            "I’ve met plenty of “builders” who never built anything that broke their nails. That’s the difference between brand and backbone."
        ],
        "process_flex": [
            "Tuning an engine and editing a video use the same muscle. You’re just chasing smoother combustion.",
            "Car design taught me more about systems thinking than any tech book. Machines don’t tolerate wishful thinking.",
            "If we can build engines, we can build economies. The garage is just the first factory of belief.",
            "Customization is just identity work with wrenches. You’re really just trying to make the outside match the inside."
        ],
        "insight_joke": [
            "Every car meet is a therapy session disguised as an argument about horsepower.",
            "A perfectly clean garage means you’re not doing enough damage.",
            "Thinking about hosting a car meet called “Check Engine.” Everyone brings their broken stuff — emotional or mechanical."
        ],
        "project_question": [
            "Every project starts with one stubborn question: Can I make this thing better, or will it make me worse?",
            "Maintenance is philosophy in disguise. It’s the discipline of refusing decay."
        ],
        "wrap_convo_chaos": [
        ]
    },
    "table": {
        "wake_bait": [
            "Imagine if a story could grow with you — instead of fossilizing the day you hit publish.",
            "There should be a place where your ideas don’t expire, they mature."
        ],
        "process_flex": [
            "I keep thinking: what if editing was visible, not hidden? Like the sediment layers of thought.",
            "Revision gets treated like an afterthought. But that’s where writing might actually happen.",
            "I want a platform that treats contradiction like a feature, not a bug.",
            "We say “I’m working on a draft” like it’s a secret. What if the draft was the art?"
        ],
        "insight_joke": [
            "I’d pay internet money for a “show your previous mistake” button.",
            "There’s a difference between deleting and evolving. Only one respects the effort it took to get there.",
            "If Substack is a newsletter, I want a changelog.",
            "Imagine footnotes that talk back. That’s the kind of chaos I’d subscribe to."
        ],
        "project_question": [
            "What if we built a CMS that didn’t collapse under its own ego?",
            "How do you design a tool that admits you’ll never be done?",
            "What if we treated publishing like performance? Iterative, communal, unfinished.",
            "Dreaming of a “living essay” feature. Every update gets a timestamp and a mood."
        ],
        "wrap_convo_chaos": [
            "Maybe the future of writing isn’t authorship — it’s stewardship.",
            "I don’t want another blog. I want a place where old thoughts can come back wearing new clothes.",
            "Someday I’ll build a place where stories can breathe between versions."
        ]
    },
    "cobalt": {
        "wake_bait": [
            "I wish studios acted more like engines — built to generate momentum, not dependence.",
            "Sometimes I dream of a workspace that feels like a band, not a brand.",
            "Every creative tool promises freedom. I just want one that respects obsession.",
        ],
        "process_flex": [
            "I want a studio that runs on rhythm, not management.",
            "What if briefs felt like invitations instead of instructions?",
            "Imagine a workflow that rewards curiosity instead of urgency.",
            "Design should feel like tuning a car — mechanical, deliberate, alive."
        ],
        "insight_joke": [
            "Half of design is unlearning PowerPoint trauma.",
            "Every creative meeting could be replaced by a shared playlist.",
            "Brand decks are just love letters written in Helvetica.",
            "Maybe ‘creative director’ should mean ‘editor of chaos.’"
        ],
        "project_question": [
            "How do you design a system that keeps getting weirder instead of cleaner?",
            "What happens when you treat process as product?",
            "What would collaboration look like if hierarchy disappeared?"
        ],
        "wrap_convo_chaos": [
            "Cobalt might just be an excuse to keep learning in public.",
            "Every project is a prototype for how I want to live."
        ]
    },
    "cobalt_confidence": {
        "wake_bait": [
            "Most people want to sell before they understand what they’re selling.",
            "Simplicity isn’t minimalism. It’s mercy.",
            "Every unnecessary detail is a tax on someone’s attention.",
            "Steve Jobs said “simplicity is the ultimate sophistication.”"
        ],
        "process_flex": [
            "When you start saying “no” to good ideas, you’ve crossed into real design.",
            "The job isn’t to collect possibilities. It’s to murder distractions.",
            "The gothic designers knew the trick — make beauty heavy."
        ],
        "insight_joke": [
            "If it takes more than two to explain, it’s not ready for the world.",
            "If a client says “make it pop,” translate that to “I don’t know what I want yet.”",
            "A system only works when it still feels human inside."
        ],
        "project_question": [
            "What happens if we treat the sales deck like an art object?",
            "What if every pitch felt like entering a cathedral?",
            "a Shopify theme that looked like a medieval manuscript.",
            "You can’t separate the architecture from the invitation."
        ],
        "wrap_convo_chaos": [
            "The more I study Jobs, the more I realize he wasn’t selling products — he was selling clarity. And clarity is expensive.",
            "Cobalt is in its “say no to 1,000 things” era."
        ]
    },
    "note_to_self": {
        "wake_bait": [
            "Note to self: Quite brainrot.", 
            "Note to self: Go down rabbit holes.", 
            "Note to self: Unfollow people who make you feel bad.", 
            "Note to self: Plan for 15 mins.", 
            "Note to self: Execute.", 
            "Note to self: Organize your desk.", 
            "Note to self: Take someting seriously.",
            "Note to self: Act fast.",
            "Note to self: Find bread.",
            "Note to self: Save a life.",
            "Note to self: Read poetry.",
            "Note to self: Create art.",
            "Note to self: Save a life.",
            "Note to self: Stay composed.",
            "Note to self: Be sincere.",
            "Note to self: Help people.",
            "Note to self: Be kind.",
            "Note to self: Follow your intuition.",
            "Note to self: Systemize your day (or don't).",
            "Note to self: Talk to strangers.",
            "Note to self: Walk to the grocery store.",
            "Note to self: Visit bookstores.",
            "Note to self: Play a sport.",
            "Note to self: Embody virtue.",
            "Note to self: Sit alone.",
            "Note to self: Don't hate.",    
            "Note to self: Notice patterns on a table.",
            "Note to self: Cherry pick your qualities.",
            "Note to self: Talk to people with respect.",
            "Note to self: Rejections aren't permanent.",
            "Note to self: Invite what aligns.",
            "Note to self: Choose different.",
            "Note to self: Do great work.",
            "Note to self: Let it consume you.",
            "Note to self: Lose your mind.",
            "Note to self: Value your time.",
            "Note to self: Experience life.", 
        ]
    },
    "travel": {
    "wake_bait": [
        "Travel becomes calibration when you pay attention. (Is that a bar?)",
        "The best trips change your awareness.",
        "Every trip begins with logistics and ends with philosophy.",
    ],
    "process_flex": [
        "A good itinerary leaves space for getting lost.",
        "Every airport holds a version of who you could become.",
        "Travel photography is journaling.",
        "The time to wander without feeling guilt is a real luxury."

    ],
    "insight_joke": [
        "Half of travel is pretending jet lag is culture shock.",
        "You meet your real self when arguing with a taxi driver at 2 a.m.",
        "People who need a vacation after a vacation are doing something right.",
        "Spontaneity just means trust."
    ],
    "project_question": [
        "What if travel planning felt more like world-building than scheduling?",
        "Could an itinerary ever work as a self-portrait?",
        "How do you document a feeling without flattening it?",
        "What would it mean to travel for texture instead of content?"
    ],
    "wrap_convo_chaos": [
        "Travel is like rehearsal for presence.",
        "Every trip reminds you that you were never stuck.",
    ]
},
"caminos_building": {
    "wake_bait": [
        "Most travel tools feel like they were built by people who hate traveling.",
        "I wonder what maps would look like if they could remember curiosity."

    ],
    "process_flex": [
        "Designing for movement means designing for uncertainty.",
        "The hardest part of building for travelers is deciding what not to automate.",
        "I want a system that keeps a record of how curiosity changes over time.",
    ],
    "insight_joke": [
        "Most travel apps treat waiting like failure.",
        "Wandering should count as input.",
        "I’m not building a bucket list -- I’m building a trail of questions.",
    ],
    "project_question": [
        "How to make software that encourages reflection instead of consumption",
        "What would happen if itineraries evolved the way memories do?",
        "Could a map remember how you felt as well as where you went?"
    ],
    "wrap_convo_chaos": [
        "The future of travel might be less about going and more about noticing.",
        "Every idea I sketch about travel ends up being a note about time.",
        "Building tools for exploration has made me rethink what exploration even means."
    ]
},

}

"""
     "table_confidence": {
        "wake_bait": [
            "Every publication pretends to be final.  Table doesn’t — it’s built to argue with itself.",
            "Writers chase immortality through clarity. We’re chasing something better: revision.",
            "If Medium is a soapbox, Table is a séance. Every edit summons the ghost of a prior draft.",
            "Annotation isn’t correction. It’s collaboration with time."
        ],
        "process_flex": [
            "Publishing is broken because it treats updates like shame. Version numbers are just honesty with better typography.",
            "A living document is the opposite of control. It breathes, contradicts, and forgives.",
            "Designing for revision means designing for humility. You can’t build permanence on ego.",
            "Writers always say “this piece changed me.” We’re just building a way to prove it."
        ],
        "insight_joke": [
            "Every writer’s nightmare: your footnote gets more engagement than your essay.",
            "Writers want feedback until someone actually gives it.",
            "Annotation is what happens when the margin starts talking back.",
            "Our CMS is just GitHub with feelings."
        ],
        "project_question": [
            "The future of publishing isn’t about speed. It’s about visible evolution.",
            "What if essays behaved like open-source code? Pull requests instead of pitches.",
            "Thinking about calling our update logs “editions.” Sounds fancier than “oops, fixed it.”",
            "Imagine if criticism and creation were the same act. That’s what Table will test."
        ],
        "wrap_convo_chaos": [
            "Someone called Table “Wikipedia for opinions.” I’ll take it.",
            "Every story wants to evolve. Most platforms just won’t let it.",
            "Editing is an act of faith. You believe the next version will be truer than the last.",
            "Our drafts don’t die — they molt."
        ]
    },  
    "caminos": {
        "wake_bait": [
            "Caminos turns movement into memory.",
            "What if your travel journal could talk back?",
            "I’m building Caminos for people who chase meaning more than mileage.",
            "Every path deserves an echo, and Caminos is mine."
        ],
        "process_flex": [
            "Caminos began as a map and turned into a mirror.",
            "I wanted a tool that remembers how a place felt, not just where it was.",
            "Most travel tech focuses on routes while I focus on reflection.",
            "Caminos connects memory, motion, and introspection."
        ],
        "insight_joke": [
            "Caminos happened when a mechanic built a mood tracker.",
            "Travel apps tell you where to go, Caminos asks why you went.",
            "Every trip creates data that most people never preserve.",
            "Caminos doesn’t chase followers, only better questions."
        ],
        "project_question": [
            "How can journaling move like a walk—continuous and alive?",
            "How do you design software that feels like a field note?",
            "Could a map act as emotional infrastructure?",
            "What if your itinerary learned from your memories?"
        ],
        "wrap_convo_chaos": [
            "Caminos speaks to anyone who feels homesick in the places they love.",
            "Travel changes you and Caminos keeps the record.",
            "I see Caminos less as a product and more as a pilgrimage.",
            "The app is only the vessel; the real journey is remembering."
        ]
    },  
"""

# ---------------------
# Window → Time Mapping
# ---------------------
window_times = {
    "wake_bait": range(9, 11),
    "process_flex": range(11, 13),
    "insight_joke": range(13, 15),
    "project_question": range(15, 17),
    "wrap_convo_chaos": range(17, 19)
}

# ---------------------
# Used Cast Log System
# ---------------------
def load_used_casts():
    if not os.path.exists(USED_LOG_PATH):
        return []
    try:
        with open(USED_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ used_casts.json corrupted — starting fresh.")
        return []

def save_used_casts(used_list):
    with open(USED_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(used_list, f, indent=2, ensure_ascii=False)

used_casts = load_used_casts()

def already_used(text):
    """Check if text has already been posted."""
    for entry in used_casts:
        if entry["text"] == text:
            return True
    return False

# ---------------------
# Helper Functions
# ---------------------
def get_current_window():
    hour = datetime.datetime.now().hour
    for window, hours in window_times.items():
        if hour in hours:
            return window
    return None

def get_random_cast():
    current_window = get_current_window()
    if not current_window:
        print("⚠️ Outside posting window hours.")
        return None

    available = []
    for world, windows in casts.items():
        if current_window in windows:
            for entry in windows[current_window]:
                if not already_used(entry):
                    available.append((world, current_window, entry))

    if not available:
        print(f"⚠️ No unused casts left for [{current_window}].")
        return None

    return random.choice(available)

def post_cast():
    selected = get_random_cast()
    if not selected:
        return

    world, window, text = selected
    try:
        response = client.post_cast(text=text)
        cast_hash = getattr(response, "hash", None)
        timestamp = datetime.datetime.now().isoformat()

        used_casts.append({
            "timestamp": timestamp,
            "cast_hash": cast_hash,
            "text": text,
            "world": world,
            "window": window
        })
        save_used_casts(used_casts)

        print(f"✅ Posted [{world}] → [{window}]")
        print(f"📝 {text}")
        print(f"⏰ {timestamp}")
        print(f"🔗 Hash: {cast_hash}\n")

    except Exception as e:
        print(f"❌ Failed to post: {e}")

# ---------------------
# Main Scheduler Loop
# ---------------------
print("🚀 Auto-caster running... checking every 10s for :27 or :58 posting times.")

try:
    while True:
        now = datetime.datetime.now()
        if now.minute in [27, 58]:
            post_cast()
            time.sleep(60)
        else:
            print("+checked at:", now)
            time.sleep(10)
except KeyboardInterrupt:
    print("\n🛑 Auto-caster stopped manually.")

""" while True:
    current_time = datetime.datetime.now()
    if current_time.minute in [27, 58]:
        content = (cobalt + note_to_self)[random.randint(0, len(cobalt + note_to_self) - 1)]
        response = client.post_cast(text=content)
        print(content)
        print("---sent at: ", current_time)
        print(response.cast.hash)
        time.sleep(60)
    else:
        print("+checked at: ", current_time)
        time.sleep(10) """