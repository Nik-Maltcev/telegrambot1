import tempfile
import unittest
from pathlib import Path

from bot.database import Database


class GetUsersByCityTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = Database(str(Path(self.temp_dir.name) / "test.db"))
        await self.db.init_db()

        await self.db.add_user(
            1, "single", "Single city", "Paris 🇫🇷", "Paris 🇫🇷", "-", "-"
        )
        await self.db.add_user(
            2,
            "multiple",
            "Multiple cities",
            "London 🇬🇧, Paris 🇫🇷",
            "London 🇬🇧, Paris 🇫🇷",
            "-",
            "-",
        )
        await self.db.add_user(
            3,
            "new_york",
            "New York only",
            "New York 🇺🇸",
            "New York 🇺🇸",
            "-",
            "-",
        )
        await self.db.add_user(
            4, "hidden", "Hidden user", "Paris 🇫🇷", "Paris 🇫🇷", "-", "-"
        )
        await self.db.set_user_hidden(4, True)

    async def asyncTearDown(self):
        self.temp_dir.cleanup()

    async def test_finds_single_and_multiple_city_users(self):
        users = await self.db.get_users_by_city("Paris 🇫🇷")

        self.assertEqual({user["user_id"] for user in users}, {1, 2})

    async def test_finds_user_by_each_selected_city(self):
        users = await self.db.get_users_by_city("London 🇬🇧")

        self.assertEqual([user["user_id"] for user in users], [2])

    async def test_does_not_match_part_of_another_city(self):
        users = await self.db.get_users_by_city("York 🇺🇸")

        self.assertEqual(users, [])

    async def test_excludes_hidden_users(self):
        users = await self.db.get_users_by_city("Paris 🇫🇷")

        self.assertNotIn(4, {user["user_id"] for user in users})


if __name__ == "__main__":
    unittest.main()
