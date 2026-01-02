
SKILL_CATEGORIES = {
    "A": {
        "name": "Business & Strategy",
        "items": [
            "Business consulting", "Startup mentorship", "Marketing and branding",
            "Sales and negotiations", "PR and communications", "Legal consultation",
            "Finance and taxation", "Investments and stock market", "Cryptocurrency and DeFi",
            "Project management", "Product management", "HR and recruitment",
            "Business process organization", "Packaging and offer development",
            "Freelance business strategy", "Operations management", "Growth and scaling strategies"
        ]
    },
    "B": {
        "name": "IT & Digital",
        "items": [
            "UX/UI design", "Web development", "Mobile development", "AR/VR, metaverse",
            "3D modeling", "Animation", "Programming (Python, JS, Go, etc.)",
            "Data Science and analytics", "AI and automation", "Cybersecurity",
            "DevOps and system architecture", "Technical support",
            "Working with neural networks / integrations"
        ]
    },
    "C": {
        "name": "Creativity & Art",
        "items": [
            "Photography", "Videography", "Creative direction", "Editing", "Color grading",
            "Sound design", "Music production", "DJ", "Vocals", "Playing musical instruments",
            "Illustration", "Painting", "Sculpture", "Ceramics", "Digital art",
            "Fashion design", "Styling", "Curatorial practices", "Art mentorship",
            "Creative direction / artistic direction", "Installation creation",
            "3D printing in art"
        ]
    },
    "D": {
        "name": "Wellbeing",
        "items": [
            "Psychology", "Body-oriented therapy", "Breathing practices",
            "Meditation and mindfulness", "Yoga", "Somatics", "Emotional intelligence",
            "Life coaching", "Energy practices (Reiki, healing, etc.)", "Trauma work",
            "Neuropsychology", "Self-regulation practices"
        ]
    },
    "E": {
        "name": "Sports & Health",
        "items": [
            "Personal training", "Functional training", "Pilates", "Dance", "Stretching",
            "Home workouts", "Nutrition and dietetics", "Recovery after training",
            "Ice bathing, Wim Hof breathing", "Massage techniques", "Holistic wellness",
            "Singing bowls", "Esoterics"
        ]
    },
    "F": {
        "name": "Languages",
        "items": [
            "Language teaching", "Interview preparation", "Translation and localization"
        ]
    },
    "G": {
        "name": "Media & PR",
        "items": [
            "Production of shoots", "Press relations", "Copywriting",
            "Media Publications", "Personal branding",
            "SMM and content strategy", "Creating Reels / TikTok",
            "Instagram growth strategies", "Media planning", "Crisis communication"
        ]
    },
    "H": {
        "name": "Lifestyle",
        "items": [
            "Cooking", "Barista / mixology", "Event organization", "Travel and routes",
            "Personal style and image", "Freelance mentorship", "Immigration navigation",
            "Interior design", "Space organization", "Life management",
            "Home rituals and self-care practices"
        ]
    },
    "I": {
        "name": "Eco & Social",
        "items": [
            "Conscious consumption", "Eco-projects", "Social initiatives",
            "Volunteering", "Community building", "Mutual aid projects"
        ]
    }
}

OFFER_FORMATS = [
    "Professional consultations", "Access to courses / materials", "Educational practices",
    "Workshops", "Professional coaching", "Individual programs",
    "Project or task implementation"
]

INTERACTION_FORMATS = [
    "Online", "Offline", "Both"
]

RESULT_TYPES = [
    "Concrete outcome: design, plan, etc.",
    "Practical skill",
    "Learning / skill improvement",
    "Support and guidance",
    "1:1 consultation",
    "Other form of result"
]

# --- Cities list (used across multiple sections) ---
CITIES = [
    "Online",
    "New York 🇺🇸", "Los Angeles 🇺🇸", "San Francisco 🇺🇸", "Miami 🇺🇸",
    "London 🇬🇧", "Paris 🇫🇷", "Berlin 🇩🇪", "Hamburg 🇩🇪",
    "Amsterdam 🇳🇱", "Rotterdam 🇳🇱", "Milan 🇮🇹", "Rome 🇮🇹",
    "Barcelona 🇪🇸", "Copenhagen 🇩🇰", "Stockholm 🇸🇪", "Lisbon 🇵🇹",
    "Vienna 🇦🇹", "Zurich 🇨🇭", "Prague 🇨🇿", "Budapest 🇭🇺",
    "Warsaw 🇵🇱", "Moscow 🇷🇺",
    "Bangkok 🇹🇭", "Singapore 🇸🇬", "Hong Kong 🇭🇰", "Tokyo 🇯🇵", "Seoul 🇰🇷",
    "Shanghai 🇨🇳", "Beijing 🇨🇳", "Dubai 🇦🇪",
    "Sydney 🇦🇺", "Melbourne 🇦🇺",
    "Mexico City 🇲🇽", "São Paulo 🇧🇷", "Rio de Janeiro 🇧🇷", "Buenos Aires 🇦🇷",
    "Tel Aviv 🇮🇱", "Istanbul 🇹🇷", "Bali 🇮🇩"
]

# --- Personal Introductions ---
INTRO_CATEGORIES = {
    "media_culture": {
        "name": "Media, Culture, Art",
        "items": [
            "Magazine Editorial Team",
            "International Film Festival Team",
            "Heads or teams of art residencies",
            "Owners or curators of private galleries",
            "Art dealers with collector networks",
            "Well-known artists and photographers.",
            "Curators of major museum projects",
            "Venue Program Directors",
            "Independent art fair organizers"
        ]
    },
    "stage_music": {
        "name": "Stage, Music, Events",
        "items": [
            "Teams of major music festivals",
            "Members of private music communities",
            "Organizers of Burning Man and Burning Man camps",
            "Production teams of large shows"
        ]
    },
    "fashion_luxury": {
        "name": "Fashion & Luxury Industry",
        "items": [
            "Luxury boutique buyers",
            "Fashion house heads",
            "Fashion week producers",
            "Fashion production directors",
            "Niche brand owners",
            "Watchmakers & owners",
            "Private workshop jewelers"
        ]
    },
    "business_influence": {
        "name": "Business & Influence",
        "items": [
            "Private club founders",
            "Boutique fund partners",
            "Startup founders",
            "Digital platform heads",
            "CEO dinner organizers",
            "Niche media owners",
            "Business forum organizers",
            "Board members"
        ]
    },
    "travel_access": {
        "name": "Travel, Mobility & Special Access",
        "items": [
            "Private travel organizers",
            "Retreat center founders",
            "Boat/yacht owners",
            "Private aviation reps",
            "Private traveler club heads",
            "VIP sports access organizers",
            "Cultural center directors"
        ]
    },
    "rare_professions": {
        "name": "Specific and Rare Professions / Access",
        "items": [
            "Architects of unique projects",
            "University research lab heads",
            "Charitable foundation heads",
            "Diplomatic representatives"
        ]
    }
}

INTRO_FORMATS = [
    "Warm introduction via message",
    "Personal introduction at an event",
    "Joint call",
    "Only for very relevant requests"
]

# --- Real Estate ---
PROPERTY_TYPES = [
    "Apartment",
    "House / Villa",
    "Townhouse",
    "Loft / Studio",
    "Apartment in a complex",
    "Room (shared living)"
]

PROPERTY_USAGE_FORMAT = [
    "Exclusive stay - participant stays alone.",
    "Private area in owner’s home"
]

PROPERTY_DURATION = [
    "2–3 days",
    "1 week",
    "Several weeks",
    "Several months",
    "Situational (by agreement)"
]

PROPERTY_CAPACITY = [
    "1",
    "1–2",
    "3–4",
    "4+"
]

# --- Cars ---
VEHICLE_TYPES = [
    "Car",
    "Motorcycle / Scooter",
    "Bicycle",
    "Electric scooter",
    "Van",
    "Truck",
    "SUV / 4x4"
]

CAR_USAGE_CONDITIONS = [
    "Exclusive use by participant",
    "Shared use with owner",
    "Use only with driver"
]

CAR_DURATION = [
    "Single trip",
    "2–3 days",
    "Up to a week",
    "Several months",
    "Situational (pre-discussed)"
]

CAR_CONDITIONS = [
    "Fuel & Minor Costs Covered",
    "Insurance & Damage Coverage",
    "Safe deposit"
]

CAR_PASSENGERS = [
    "1",
    "2",
    "3",
    "4+"
]

# --- Equipment ---
EQUIPMENT_TYPES = [
    "Photo and video cameras",
    "Lenses",
    "Stabilizers / tripods / audio recorders",
    "Lighting equipment",
    "Microphones (lapel, directional, studio)",
    "Drones",
    "Action cameras",
    "Projectors and screens",
    "Sound equipment / speakers",
    "DJ equipment",
    "Musical instruments",
    "Editing workstation / production station",
    "Software (type of license)",
    "3D printers",
    "Tools for installations / sculpture",
    "Event tools",
    "Power tools",
    "Other"
]

EQUIPMENT_ACCESS_FORMAT = [
    "Can take independently",
    "Only with owner's presence",
    "Only under owner's supervision",
    "Only after instruction",
    "Community projects only",
    "Commercial use possible"
]

EQUIPMENT_DURATION = [
    "Up to 1 day",
    "1–7 days",
    "Long-term (week or more)",
    "Individually discussed"
]

EQUIPMENT_RESPONSIBILITY = [
    "Deposit",
    "Passport copy",
    "Insurance",
    "Damage compensation agreement",
    "Other"
]

# --- Air Transport ---
AIRCRAFT_TYPES = [
    "Plane",
    "Helicopter",
    "Gyrocopter",
    "Hang glider",
    "Paraglider",
    "Hot-air balloon",
    "Glider / Sailplane",
    "Ultralight aircraft",
    "Drone / UAV",
    "Airship / Blimp",
    "Paramotor",
    "Wingsuit",
    "Microlight trike",
    "Quadcopter",
    "Autogyro"
]

AIRCRAFT_USAGE_FORMAT = [
    "Exclusive (fully provided)",
    "Shared with owner (accompanied flight)"
]

AIRCRAFT_SAFETY = [
    "Aircraft insurance",
    "Third-party liability insurance",
    "Passenger insurance"
]

AIRCRAFT_EXPENSES = [
    "Fuel coverage",
    "Maintenance, parking, airport fees",
    "Minor operational expenses",
    "Damage coverage agreement"
]

# --- Water Transport ---
VESSEL_TYPES = [
    "Sailing yacht",
    "Motor yacht",
    "Catamaran",
    "Speedboat",
    "RIB / rigid inflatable boat",
    "Motorboat",
    "Jet Ski"
]

VESSEL_USAGE_FORMAT = [
    "Exclusive (full control of vessel)",
    "Shared with owner"
]

VESSEL_SAFETY = [
    "Mandatory insurance",
    "Operating license"
]

VESSEL_FINANCIAL = [
    "Refundable deposit",
    "Minor expenses & damage coverage",
    "Fuel paid by user",
    "Mooring fee paid by user"
]

# --- Specialists ---
SPECIALIST_CATEGORIES = {
    "legal_finance": {
        "name": "Legalization & Finance",
        "items": [
            "Tax specialist",
            "US visas",
            "European residence permits",
            "Schengen visas",
            "Citizenship",
            "Business legalization abroad",
            "Legal services",
            "Real estate investments",
            "Investments for HNWIs",
            "Wealth management"
        ]
    },
    "health_body": {
        "name": "Health & Body",
        "items": [
            "Doctors and health specialists",
            "Body-performance specialists",
            "Psychologists, mental health coaches"
        ]
    },
    "art_creative": {
        "name": "Art & Creative Industry",
        "items": [
            "Art managers and curators",
            "Gallerists",
            "Art dealers",
            "Professional photographers / videographers",
            "Sound producers",
            "High-level designers (fashion / graphic / UX)"
        ]
    },
    "business_startups": {
        "name": "Business & Startups",
        "items": [
            "Marketing strategists",
            "Bloggers / digital personalities producers",
            "SMM managers",
            "SEO / Ads US–Europe",
            "Online course launch consultants",
            "Sales and funnel specialists",
            "Business coaches"
        ]
    },
    "personal_brand": {
        "name": "Personal Brand & PR",
        "items": [
            "PR agents (Europe / US / Asia)",
            "Media strategy specialists"
        ]
    },
    "lifestyle_travel": {
        "name": "Lifestyle & Travel",
        "items": [
            "Concierge services",
            "Luxury travel agents",
            "Relocation specialists"
        ]
    },
    "real_estate_spec": {
        "name": "Real Estate",
        "items": [
            "Agents for rent/purchase worldwide",
            "Real estate investment specialists (yield-analysis)",
            "Property management specialists"
        ]
    }
}

SPECIALIST_CONNECTION_TYPE = [
    "Direct",
    "Through resident"
]

# --- Artworks ---
ART_FORMS = [
    "Painting",
    "Graphic art",
    "Photography",
    "Sculpture",
    "Digital art",
    "Installation",
    "Print",
    "Ceramics",
    "Textile / objects",
    "Other"
]

ART_AUTHOR_TYPE = [
    "Me",
    "Other artist"
]
