
# --- Resources & Access ---
RESOURCE_ACCESS_CATEGORIES = {
    "hospitality": {
        "name": "Hospitality, Dining & Experiences",
        "items": [
            "Hotel", "Boutique hotel", "Guesthouse", "Members club",
            "Beach club", "Private dining venue", "Retreat center",
            "Airbnb / short-term rentals", "Villas or private residences for hosting",
            "Restaurant", "Bar", "Nightclub", "Café", "Specialty coffee shop",
            "Cannabis coffeeshop", "Tea shop", "Wine bar", "Wine shop",
            "Winery", "Craft brewery", "Distillery", "Catering company",
            "Travel agency", "Concierge service", "Car rental service",
            "Boat rental service"
        ]
    },
    "creative_spaces": {
        "name": "Creative & Cultural Spaces",
        "items": [
            "Art gallery", "Artist studio", "Project space", "Exhibition space",
            "Cultural center", "Music studio", "Dance studio", "Photography studio",
            "Podcast studio", "Creative production studio",
            "Rehearsal or performance space", "Event space", "Festival space",
            "Co-working space", "Office space", "Workshop space", "Maker space"
        ]
    },
    "media_platforms": {
        "name": "Media, Platforms & Promotion",
        "items": [
            "Media platform", "Podcast", "YouTube channel", "Blog",
            "Streaming channel", "Online marketplace", "E-commerce platform",
            "Booking platform", "Ticketing platform", "Production company",
            "Marketing platform", "Influencer network", "PR agency",
            "Creative agency", "Talent management agency",
            "Influential social media account"
        ]
    },
    "wellness_beauty": {
        "name": "Wellness, Beauty & Medical",
        "items": [
            "Wellness center", "Spa", "Yoga studio", "Pilates studio",
            "Meditation, breathwork & sound healing center", "Fitness studio",
            "Gym", "Beauty salon", "Aesthetic clinic", "Massage studio",
            "Medical clinic", "Dental clinic"
        ]
    },
    "brands_craft": {
        "name": "Brands & Craft Production",
        "items": [
            "Fashion brand", "Jewelry brand", "Watch brand", "Eyewear brand",
            "Perfume brand", "Beauty brand", "Design objects brand",
            "Furniture brand", "Home decor brand", "Food brand",
            "Beverage brand", "Specialty food brand", "Automotive brand",
            "Audio equipment brand", "Tech device brand", "Craft workshop",
            "Ceramics studio", "Rare craft production"
        ]
    },
    "investment_business": {
        "name": "Investment & Business Infrastructure",
        "items": [
            "Venture fund", "Angel investor network", "Startup accelerator",
            "Business network", "Investment club", "Manufacturing facility",
            "Manufacturing & sourcing network", "Distribution network",
            "Logistics service", "Licensing company"
        ]
    }
}

SKILL_CATEGORIES = {
    "A": {
        "name": "Business & Strategy",
        "items": [
            "Business consulting", "Startup mentorship", "Marketing and branding",
            "Sales and negotiations", "PR and communications", "Legal consultation",
            "Finance and taxation", "Investments and stock market", "Cryptocurrency and DeFi",
            "Project management", "Product management", "HR and recruitment",
            "Business process organization", "Packaging and offer development",
            "Freelance business strategy", "Operations management", "Growth and scaling strategies",
            "Partnership strategy", "Business development", "Fundraising / investment strategy",
            "Company / venture building", "Product strategy", "Deal structuring",
            "Go-to-market strategy", "Market expansion strategy",
            "Freelance / independent work strategy", "Offer / service development",
            "Client acquisition"
        ]
    },
    "B": {
        "name": "IT & Digital",
        "items": [
            "UX/UI design", "Web development", "Mobile development", "AR/VR, metaverse",
            "3D modeling", "Animation", "Programming (Python, JS, Go, etc.)",
            "Data Science and analytics", "AI and automation", "Cybersecurity",
            "DevOps and system architecture", "Technical support",
            "Working with neural networks / integrations",
            "Product design", "Graphic design", "Creative coding"
        ]
    },
    "C": {
        "name": "Creativity & Art",
        "items": [
            "Photography", "Videography", "Creative direction", "Editing", "Color grading",
            "Sound design", "Music production", "DJ", "Vocals", "Playing musical instruments",
            "Illustration", "Painting", "Sculpture", "Ceramics", "Digital art",
            "Fashion design", "Styling", "Curatorial practices", "Art mentorship",
            "Installation creation", "3D printing in art",
            "Film directing", "Performing arts", "Architecture", "Urbanism",
            "Art space creation & curation", "Craft & independent brands",
            "Interior design", "Tattoo art", "Sound engineering",
            "Performance art", "Creative production", "Generative / AI art"
        ]
    },
    "D": {
        "name": "Wellbeing",
        "items": [
            "Psychology", "Body-oriented therapy", "Breathing practices",
            "Meditation and mindfulness", "Yoga", "Somatics", "Emotional intelligence",
            "Life coaching", "Energy practices (Reiki, healing, etc.)", "Trauma work",
            "Neuropsychology", "Self-regulation practices",
            "Nutrition & dietary guidance", "Movement practices",
            "Performance & mental resilience"
        ]
    },
    "E": {
        "name": "Sports & Health",
        "items": [
            "Personal training", "Functional training", "Pilates", "Dance", "Stretching",
            "Home workouts", "Nutrition and dietetics", "Recovery after training",
            "Ice bathing, Wim Hof breathing", "Massage techniques", "Holistic wellness",
            "Singing bowls", "Esoterics", "Mobility & posture work"
        ]
    },
    "F": {
        "name": "Languages",
        "items": [
            "Language teaching", "Interview preparation", "Translation and localization",
            "Cross-cultural communication"
        ]
    },
    "G": {
        "name": "Media & PR",
        "items": [
            "Photo & video production", "Press relations", "Copywriting",
            "Media Publications", "Personal branding",
            "SMM and content strategy", "Creating Reels / TikTok",
            "Instagram growth strategies", "Media strategy", "Crisis communication",
            "Public speaking", "Business communication"
        ]
    },
    "H": {
        "name": "Lifestyle",
        "items": [
            "Private dining & culinary experiences", "Barista", "Mixology",
            "Event organization", "Travel and routes",
            "Personal style and image", "Immigration navigation",
            "Space organization", "Life management",
            "Home rituals and self-care practices",
            "Hospitality management", "Music & nightlife culture",
            "Wine & gastronomy", "Coffee culture & specialty coffee",
            "Tea culture", "Sailing / yachting", "Beauty & aesthetics",
            "Cars & automotive", "Cannabis culture", "Sommelier",
            "Private chef", "Gourmet food curator",
            "Private aviation & jet access"
        ]
    }
}

ALL_SKILLS = []
for cat in SKILL_CATEGORIES.values():
    ALL_SKILLS.extend(cat['items'])

OFFER_FORMATS = [
    "Professional consultations", "Access to courses / materials", "Private Sessions & Appointments",
    "Workshops", "Professional coaching", "Individual programs",
    "Project or task implementation"
]

RESULT_TYPES = [
    "Strategic clarity",
    "Problem solving",
    "Feedback / expert review",
    "Optimization",
    "Guidance and Support",
    "Creative development",
    "Service delivery"
]

# --- Cities list (used across multiple sections) ---
CITIES = [
    "Online",
    "New York 🇺🇸", "Los Angeles 🇺🇸", "San Francisco 🇺🇸", "Miami 🇺🇸",
    "London 🇬🇧", "Paris 🇫🇷", "Berlin 🇩🇪", "Hamburg 🇩🇪",
    "Amsterdam 🇳🇱", "Rotterdam 🇳🇱", "Milan 🇮🇹", "Rome 🇮🇹", "Venice 🇮🇹",
    "Barcelona 🇪🇸", "Madrid 🇪🇸", "Copenhagen 🇩🇰", "Stockholm 🇸🇪", "Lisbon 🇵🇹",
    "Vienna 🇦🇹", "Zurich 🇨🇭", "Prague 🇨🇿", "Budapest 🇭🇺",
    "Warsaw 🇵🇱", "Moscow 🇷🇺", "Belgrade 🇷🇸",
    "Athens 🇬🇷", "Marseille 🇫🇷", "Cannes/Nice 🇫🇷",
    "Helsinki 🇫🇮", "Tallinn 🇪🇪",
    "Bangkok 🇹🇭", "Phuket 🇹🇭", "Singapore 🇸🇬", "Hong Kong 🇭🇰", "Tokyo 🇯🇵", "Seoul 🇰🇷",
    "Shanghai 🇨🇳", "Dubai 🇦🇪",
    "Melbourne 🇦🇺",
    "Tulum 🇲🇽", "Rio de Janeiro 🇧🇷", "Buenos Aires 🇦🇷",
    "Cape Town 🇿🇦",
    "Tel Aviv 🇮🇱", "Istanbul 🇹🇷", "Bali 🇮🇩", "Ubud 🇮🇩",
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
            "Well-known artists and photographers",
            "Curators of major museum projects",
            "Venue Program Directors",
            "Independent art fair organizers",
            "Art critics and writers",
            "Documentary filmmakers",
            "Cultural foundation directors",
            "Public art commissioners",
            "Private art collectors",
            "Art advisors to collectors",
            "Directors of art biennales",
            "Independent exhibition curators",
            "Museum board members",
            "Cultural institution directors",
            "Art fair directors",
            "Public art producers"
        ]
    },
    "stage_music": {
        "name": "Stage, Music, Events",
        "items": [
            "Teams of major music festivals",
            "Members of private music communities",
            "Organizers of Burning Man and Burning Man camps",
            "Production teams of large shows",
            "Talent booking agents",
            "Music label founders",
            "Artist managers",
            "Club founders and owners",
            "Touring production managers",
            "Concert promoters",
            "Event creative directors",
            "Immersive show creators",
            "Cultural event curators",
            "Stage designers",
            "Music influencers",
            "Booking agents",
            "Radio & podcast hosts",
            "Nightlife owners",
            "Event sponsors",
            "Festival curators",
            "Event marketing & PR teams",
            "Event promoters",
            "Burning Man & AB organizers"
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
            "Private workshop jewelers",
            "Luxury brand founders",
            "Creative directors of fashion houses",
            "Fashion investors",
            "Rare fashion collectors",
            "Fashion archive owners",
            "Luxury stylist networks",
            "Fashion show casting directors",
            "Fashion media editors",
            "Luxury concept store founders",
            "Couture atelier owners",
            "Jewelry designers",
            "Watch collectors",
            "Private jewelers"
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
            "Board members",
            "Angel investors",
            "Serial entrepreneurs",
            "Family office principals",
            "Venture capital partners",
            "Private equity partners",
            "Tech company founders",
            "Scale-up founders",
            "Venture scouts",
            "Innovation hub founders",
            "Startup accelerator directors",
            "Dealmakers & connectors",
            "Global community founders",
            "Policy advisors",
            "Brand founders",
            "Luxury brand executives",
            "High-end event hosts",
            "Industry association heads",
            "Strategic advisors",
            "Growth hackers",
            "Global conference organizers",
            "Capital owners",
            "Fund managers"
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
            "Cultural center directors",
            "Luxury travel concierges",
            "Expedition leaders",
            "Safari lodge owners",
            "Private island owners",
            "Remote resort founders",
            "Cultural expedition organizers",
            "Members of exploration clubs",
            "Private guide networks",
            "Luxury concierge founders",
            "Adventure travel curators",
            "Overland expedition organizers",
            "Yacht charter brokers",
            "Private aviation brokers",
            "Global relocation specialists"
        ]
    },
    "rare_professions": {
        "name": "Specific & Rare Professions / Access",
        "items": [
            "Architects of unique projects",
            "University research lab heads",
            "Charitable foundation heads",
            "Diplomatic representatives",
            "Rare book collectors",
            "Private archive keepers",
            "Space industry engineers",
            "Cultural heritage restorers",
            "Experimental research scientists",
            "Think tank founders and directors",
            "Antique artifact specialists"
        ]
    },
    "collectors_patrons": {
        "name": "Collectors & Patrons",
        "items": [
            "Art collectors",
            "Rare watch collectors",
            "Vintage car collectors",
            "Cultural patrons",
            "Private museum founders"
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
    "SUV / 4x4",
    "ATV / Quad bike",
    "Camper van"
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
    "Photo studio equipment",
    "Portable studio kits",
    "Podcast recording equipment",
    "Audio interfaces",
    "Synthesizers",
    "Drum machines",
    "MIDI controllers",
    "Music production gear",
    "Stage equipment",
    "Projection mapping equipment",
    "LED walls / video walls",
    "VR / AR equipment",
    "Motion capture equipment",
    "Streaming equipment",
    "Party lighting",
    "Laser lights",
    "DJ controllers",
    "Turntables",
    "VJ equipment",
    "Smoke machines",
    "Bubble machines",
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
    "Barcelona 🇪🇸", "Ibiza 🇪🇸", "Mallorca 🇪🇸", "Formentera 🇪🇸", "Marbella 🇪🇸", "Menorca 🇪🇸",
    "French Riviera 🇫🇷", "Saint-Tropez 🇫🇷", "Monaco 🇲🇨", "Cannes 🇫🇷", "Nice 🇫🇷", "Saint-Barth 🇫🇷",
    "Amalfi Coast 🇮🇹", "Capri 🇮🇹", "Sardinia 🇮🇹", "Portofino 🇮🇹", "Lake Como 🇮🇹",
    "Athens 🇬🇷", "Mykonos 🇬🇷", "Cyclades 🇬🇷", "Santorini 🇬🇷",
    "Split 🇭🇷", "Hvar 🇭🇷",
    "Istanbul 🇹🇷", "Bodrum 🇹🇷", "Göcek 🇹🇷", "Lisbon 🇵🇹",
    "Amsterdam 🇳🇱", "Rotterdam 🇳🇱",
    "Copenhagen 🇩🇰", "Stockholm 🇸🇪",
    "Miami 🇺🇸", "Los Angeles 🇺🇸", "New York 🇺🇸", "Bahamas 🇧🇸", "British Virgin Islands 🇻🇬",
    "Dubai 🇦🇪",
    "Phuket 🇹🇭", "Koh Samui 🇹🇭", "Langkawi 🇲🇾",
    "Bali 🇮🇩", "Komodo 🇮🇩", "Singapore 🇸🇬", "Hong Kong 🇭🇰",
    "Whitsundays 🇦🇺", "Melbourne 🇦🇺",
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
