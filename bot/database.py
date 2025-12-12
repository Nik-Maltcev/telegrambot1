import aiosqlite
from typing import Optional, List, Dict
from datetime import datetime


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init_db(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Users table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    name TEXT NOT NULL,
                    main_city TEXT NOT NULL,
                    current_city TEXT NOT NULL,
                    about TEXT,
                    instagram TEXT,
                    points INTEGER DEFAULT 0,
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Resources table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    city TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

            # Lots table (what users share or seek)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS lots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,  -- 'share' or 'seek'
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',  -- 'pending', 'approved', 'rejected'
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Add status column if not exists (migration for existing DBs)
            try:
                await db.execute("ALTER TABLE lots ADD COLUMN status TEXT DEFAULT 'approved'")
            except:
                pass  # Column already exists

            # Open resources table (maps, accesses, specialists)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS open_resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section TEXT NOT NULL,  -- 'maps', 'accesses', 'specialists'
                    title TEXT NOT NULL,
                    description TEXT,
                    link TEXT,
                    city TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Invite tokens table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS invite_tokens (
                    token TEXT PRIMARY KEY,
                    is_used BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Deals table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proposer_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    status TEXT NOT NULL, -- pending, accepted, completed, declined
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (proposer_id) REFERENCES users (user_id),
                    FOREIGN KEY (receiver_id) REFERENCES users (user_id)
                )
            """)

            # User Answers table (Questionnaire)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_slug TEXT NOT NULL,
                    answer_data TEXT NOT NULL, -- JSON or comma-separated string
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

            await db.commit()

    # User methods
    async def add_user(self, user_id: int, username: Optional[str], name: str,
                      main_city: str, current_city: str, about: str,
                      instagram: str, points: int = 0) -> bool:
        """Add new user to database"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO users (user_id, username, name, main_city, current_city, about, instagram, points)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, username, name, main_city, current_city, about, instagram, points))
                await db.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def update_user_points(self, user_id: int, points: int) -> bool:
        """Update user points"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("UPDATE users SET points = ? WHERE user_id = ?", (points, user_id))
                await db.commit()
            return True
        except Exception as e:
            print(f"Error updating points: {e}")
            return False

    async def add_user_answer(self, user_id: int, question_slug: str, answer_data: str) -> bool:
        """Add or update a user's answer to the questionnaire."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # specific logic to avoid duplicates for the same user/question
                await db.execute("DELETE FROM user_answers WHERE user_id = ? AND question_slug = ?", (user_id, question_slug))
                await db.execute("""
                    INSERT INTO user_answers (user_id, question_slug, answer_data)
                    VALUES (?, ?, ?)
                """, (user_id, question_slug, answer_data))
                await db.commit()
            return True
        except Exception as e:
            print(f"Error adding user answer: {e}")
            return False

    async def get_user_answers(self, user_id: int) -> List[Dict]:
        """Get all answers for a user."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM user_answers WHERE user_id = ?", (user_id,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_users_by_city(self, city: str) -> List[Dict]:
        """Get all users in a specific city"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE current_city = ? ORDER BY name",
                (city,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_all_cities(self) -> List[str]:
        """Get list of all cities where users are located"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT DISTINCT current_city FROM users ORDER BY current_city"
            ) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    # Resource methods
    async def add_resource(self, user_id: int, category: str, title: str,
                          description: str, city: str) -> bool:
        """Add new resource"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO resources (user_id, category, title, description, city)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, category, title, description, city))
                await db.commit()
            return True
        except Exception as e:
            print(f"Error adding resource: {e}")
            return False

    async def get_resources_by_city_and_category(self, city: str, category: str) -> List[Dict]:
        """Get resources filtered by city and category"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT r.*, u.name, u.instagram, u.points
                FROM resources r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.city = ? AND r.category = ?
                ORDER BY r.created_at DESC
            """, (city, category)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_resource_cities(self) -> List[str]:
        """Get list of cities with resources"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT DISTINCT city FROM resources ORDER BY city"
            ) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    # Lot methods
    async def add_lot(self, user_id: int, lot_type: str, title: str,
                     description: str, status: str = "pending") -> Optional[int]:
        """Add new lot (share or seek), returns lot ID"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    INSERT INTO lots (user_id, type, title, description, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, lot_type, title, description, status))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error adding lot: {e}")
            return None

    async def get_user_lots(self, user_id: int, lot_type: str) -> List[Dict]:
        """Get user lots by type (share or seek) - shows all statuses for owner"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM lots
                WHERE user_id = ? AND type = ?
                ORDER BY created_at DESC
            """, (user_id, lot_type)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_lot(self, lot_id: int) -> Optional[Dict]:
        """Get lot by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM lots WHERE id = ?", (lot_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def get_pending_lots(self) -> List[Dict]:
        """Get all pending lots for moderation"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT l.*, u.name as user_name, u.username
                FROM lots l
                JOIN users u ON l.user_id = u.user_id
                WHERE l.status = 'pending'
                ORDER BY l.created_at ASC
            """) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def update_lot_status(self, lot_id: int, status: str) -> bool:
        """Update lot status (approve/reject)"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE lots SET status = ? WHERE id = ?",
                    (status, lot_id)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Error updating lot status: {e}")
            return False

    async def delete_lot(self, lot_id: int, user_id: int) -> bool:
        """Delete lot if it belongs to user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "DELETE FROM lots WHERE id = ? AND user_id = ?",
                    (lot_id, user_id)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Error deleting lot: {e}")
            return False

    # Open resources methods
    async def add_open_resource(self, section: str, title: str,
                               description: str, link: str = "",
                               city: str = "") -> bool:
        """Add open resource"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT INTO open_resources (section, title, description, link, city)
                    VALUES (?, ?, ?, ?, ?)
                """, (section, title, description, link, city))
                await db.commit()
            return True
        except Exception as e:
            print(f"Error adding open resource: {e}")
            return False

    async def get_open_resources(self, section: str) -> List[Dict]:
        """Get open resources by section"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM open_resources
                WHERE section = ?
                ORDER BY city, title
            """, (section,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def get_all_users(self) -> List[Dict]:
        """Get all users (for admin)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users ORDER BY name") as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    # Invite token methods
    async def add_invite_token(self, token: str) -> bool:
        """Add a new invite token."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("INSERT INTO invite_tokens (token) VALUES (?)", (token,))
                await db.commit()
            return True
        except Exception as e:
            print(f"Error adding invite token: {e}")
            return False

    async def is_valid_token(self, token: str) -> bool:
        """Check if an invite token is valid and unused."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT * FROM invite_tokens WHERE token = ? AND is_used = FALSE",
                (token,)
            ) as cursor:
                return await cursor.fetchone() is not None

    async def use_invite_token(self, token: str) -> bool:
        """Mark an invite token as used."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE invite_tokens SET is_used = TRUE WHERE token = ?",
                    (token,)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Error using invite token: {e}")
            return False

    # Deal methods
    async def create_deal(self, proposer_id: int, receiver_id: int) -> Optional[int]:
        """Create a new deal."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("""
                    INSERT INTO deals (proposer_id, receiver_id, status)
                    VALUES (?, ?, 'pending')
                """, (proposer_id, receiver_id))
                await db.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating deal: {e}")
            return None

    async def get_deal(self, deal_id: int) -> Optional[Dict]:
        """Get deal by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM deals WHERE id = ?", (deal_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def update_deal_status(self, deal_id: int, status: str) -> bool:
        """Update deal status."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE deals SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, deal_id)
                )
                await db.commit()
            return True
        except Exception as e:
            print(f"Error updating deal status: {e}")
            return False

    async def get_user_deals(self, user_id: int) -> List[Dict]:
        """Get all deals for a user."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT d.*, p.name as proposer_name, r.name as receiver_name
                FROM deals d
                JOIN users p ON d.proposer_id = p.user_id
                JOIN users r ON d.receiver_id = r.user_id
                WHERE d.proposer_id = ? OR d.receiver_id = ?
                ORDER BY d.created_at DESC
            """, (user_id, user_id)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
