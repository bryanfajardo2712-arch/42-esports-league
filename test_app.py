import tempfile
import unittest
from pathlib import Path

import app as app_module


class LeagueTest(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        app_module.DATABASE = Path(temp_dir.name) / "test.db"
        app_module.init_db()
        self.temp_dir = temp_dir
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_register_and_list_player(self):
        response = self.client.post(
            "/",
            data={"username": "bryanfajardo", "display_name": "Bryan"},
        )
        self.assertEqual(response.status_code, 302)

        page = self.client.get("/")
        self.assertIn(b"Bryan", page.data)
        self.assertIn(b"bryanfajardo", page.data)
        self.assertIn(b"cdn.intra.42.fr/users/bryanfajardo.jpg", page.data)

    def test_duplicate_username_is_rejected(self):
        data = {"username": "bryanfajardo", "display_name": "Bryan"}
        self.client.post("/", data=data)
        response = self.client.post(
            "/",
            data={"username": "bryanfajardo", "display_name": "Otro nombre"},
        )
        self.assertEqual(response.status_code, 302)

        page = self.client.get("/")
        self.assertIn(b"ya esta registrado", page.data)

    def test_invalid_username_is_rejected(self):
        response = self.client.post(
            "/",
            data={"username": "usuario!", "display_name": "Bryan"},
        )
        self.assertEqual(response.status_code, 302)
        page = self.client.get("/")
        self.assertIn(b"letras, numeros", page.data)

    def test_delete_player(self):
        self.client.post(
            "/",
            data={"username": "bryanfajardo", "display_name": "Bryan"},
        )
        with app_module.get_db() as connection:
            player_id = connection.execute(
                "SELECT id FROM players WHERE username = 'bryanfajardo'"
            ).fetchone()["id"]

        response = self.client.post(f"/players/{player_id}/delete")
        self.assertEqual(response.status_code, 302)
        page = self.client.get("/")
        self.assertIn(b"<span>0</span>", page.data)
        self.assertNotIn(b'class="player-card"', page.data)


if __name__ == "__main__":
    unittest.main()
