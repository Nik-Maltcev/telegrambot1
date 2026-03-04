
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
            "Photo & video production", "Press relations", "Copywriting",
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

ALL_SKILLS = []
for cat in SKILL_CATEGORIES.values():
    ALL_SKILLS.extend(cat['items'])

OFFER_FORMATS = [
    "Professional consultations", "Access to courses / materials", "Educational practices",
    "Workshops", "Professional coaching", "Individual programs",
    "Project or task implementation"
]



# --- Cities list (used across multiple sections) ---
CITIES = [
    "Online",
    "New York 🇺🇸", "Los Angeles 🇺🇸", "San Francisco 🇺🇸", "Miami 🇺🇸",
    "London 🇬🇧", "Paris 🇫🇷", "Berlin 🇩🇪", "Hamburg 🇩🇪",
    "Amsterdam 🇳🇱", "Rotterdam 🇳🇱", "Milan 🇮🇹", "Rome 🇮🇹", "Venice 🇮🇹",
    "Barcelona 🇪🇸", "Copenhagen 🇩🇰", "Stockholm 🇸🇪", "Lisbon 🇵🇹",
    "Vienna 🇦🇹", "Zurich 🇨🇭", "Prague 🇨🇿", "Budapest 🇭🇺",
    "Warsaw 🇵🇱", "Moscow 🇷🇺", "Belgrade 🇷🇸",
    "Athens 🇬🇷", "Marseille 🇫🇷", "Cannes 🇫🇷", "Nice 🇫🇷",
    "Helsinki 🇫🇮", "Tallinn 🇪🇪",
    "Bangkok 🇹🇭", "Phuket 🇹🇭", "Singapore 🇸🇬", "Hong Kong 🇭🇰", "Tokyo 🇯🇵", "Seoul 🇰🇷",
    "Shanghai 🇨🇳", "Dubai 🇦🇪",
    "Melbourne 🇦🇺",
    "Tulum 🇲🇽", "Rio de Janeiro 🇧🇷", "Buenos Aires 🇦🇷",
    "Cape Town 🇿🇦",
    "Tel Aviv 🇮🇱", "Istanbul 🇹🇷", "Bali 🇮🇩",
    "Baku 🇦🇿", "Tbilisi 🇬🇪"
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



# --- Real Estate ---
PROPERTY_TYPES = [
    "Apartment",
    "House / Villa",
    "Townhouse",
    "Loft / Studio",
    "Apartment in a complex",
    "Room in a shared home",
    "Commercial property",
    "Land"
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

VESSEL_LOCATIONS = [
    "Barcelona 🇪🇸", "Ibiza 🇪🇸", "Mallorca 🇪🇸",
    "French Riviera 🇫🇷", "Monaco 🇲🇨", "Cannes 🇫🇷", "Nice 🇫🇷",
    "Amalfi Coast 🇮🇹", "Capri 🇮🇹", "Sardinia 🇮🇹",
    "Athens 🇬🇷", "Mykonos 🇬🇷", "Cyclades 🇬🇷",
    "Split 🇭🇷", "Hvar 🇭🇷",
    "Istanbul 🇹🇷", "Lisbon 🇵🇹",
    "Amsterdam 🇳🇱", "Rotterdam 🇳🇱",
    "Copenhagen 🇩🇰", "Stockholm 🇸🇪",
    "Miami 🇺🇸", "Los Angeles 🇺🇸", "New York 🇺🇸",
    "Dubai 🇦🇪",
    "Phuket 🇹🇭", "Koh Samui 🇹🇭",
    "Bali 🇮🇩", "Singapore 🇸🇬", "Hong Kong 🇭🇰",
    "Sydney 🇦🇺", "Melbourne 🇦🇺",
    "Rio de Janeiro 🇧🇷", "Tel Aviv 🇮🇱"
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
            "Psychologists, mental health coaches",
            "Functional medicine experts",
            "Longevity & preventive health",
            "Osteopaths / chiropractors",
            "Sports recovery therapists",
            "Clinical nutritionists",
            "Mobility & posture specialists",
            "Medical diagnostics experts"
        ]
    },
    "wellbeing": {
        "name": "Wellbeing",
        "items": [
            "Wellness specialists",
            "Somatic therapists",
            "Nutrition coaches",
            "Senior psychologists",
            "Somatic therapy experts",
            "Sleep optimization pros",
            "Nervous system experts",
            "Recovery & regeneration",
            "Stress resilience experts"
        ]
    },
    "human_potential": {
        "name": "Human potential",
        "items": [
            "Performance coaches",
            "Focus & time coaches",
            "Burnout specialists",
            "Habit designers",
            "Burnout recovery specialists",
            "Life transition coaches",
            "Purpose & direction mentors",
            "Decision-making advisors",
            "Personal strategy consultants",
            "Resilience coaches",
            "Flow state facilitators",
            "Founder psychology advisors",
            "Identity shift mentors"
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
            "High-level designers (fashion / graphic / UX)",
            "Art fair insiders",
            "Collectors",
            "Collection advisors",
            "Cultural institution leaders",
            "Residency program directors",
            "Art investment consultants",
            "Music supervisors",
            "Independent label founders",
            "Festival programmers",
            "Talent bookers",
            "Cultural network connectors"
        ]
    },
    "business_startups": {
        "name": "Business & Startups",
        "items": [
            "Marketing strategists",
            "Bloggers / digital personalities producers",
            "SMM managers",
            "SEO / Ads US\u2013Europe",
            "Online course launch consultants",
            "Sales and funnel specialists",
            "Business coaches",
            "Venture capital connectors",
            "Market entry strategists",
            "Cross-border expansion experts",
            "Investor relations advisors",
            "Capital raise strategists",
            "Startup ecosystem navigators",
            "Government relations advisors",
            "Licensing & compliance advisors",
            "Business model architects",
            "B2B growth strategists",
            "Distribution channel builders"
        ]
    },
    "personal_brand": {
        "name": "Personal Brand & PR",
        "items": [
            "PR agents (Europe / US / Asia)",
            "Media strategy specialists",
            "Brand strategists",
            "Content creators",
            "Community builders",
            "Executive presence coaches",
            "Media placement consultants",
            "Influence partnership advisors",
            "Podcast booking strategists",
            "Editorial strategy advisors",
            "Digital reputation architects",
            "High-profile networking advisors",
            "Awards & recognition strategists"
        ]
    },
    "lifestyle_travel": {
        "name": "Lifestyle & Travel",
        "items": [
            "Concierge services",
            "Luxury travel agents",
            "Relocation specialists",
            "Travel designers",
            "Retreat & event hosts",
            "Residency & visa strategists",
            "Property search consultants",
            "Second-home setup advisors",
            "Family relocation planners",
            "Experiential travel curators",
            "On-ground fixers (local experts)"
        ]
    },
    "real_estate_spec": {
        "name": "Real Estate",
        "items": [
            "Agents for rent/purchase worldwide",
            "Real estate investment specialists (yield-analysis)",
            "Property management specialists",
            "Property managers",
            "Off-market property brokers",
            "Real estate legal advisors",
            "Private market deal sourcers"
        ]
    },
    "complex_problem_solvers": {
        "name": "Complex Problem Solvers",
        "items": [
            "Special situations advisors",
            "Negotiation specialists",
            "Crisis navigation experts",
            "Behind-the-scenes fixers",
            "Cross-border problem solvers",
            "Access & escalation connectors"
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

