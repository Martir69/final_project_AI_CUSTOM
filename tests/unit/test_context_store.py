import json
import os
import tempfile
import unittest

from backend.context_store import ContextStore


class TestContextStoreSave(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.store = ContextStore(path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_save_returns_truthy(self):
        result = self.store.save("user1", "topic", "machine learning")
        self.assertTrue(result)


class TestContextStoreListForUser(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        self.store = ContextStore(path=self.tmp.name)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_list_for_user_returns_saved_entries(self):
        self.store.save("user1", "topic", "machine learning")
        self.store.save("user1", "level", "advanced")

        entries = self.store.list_for_user("user1")

        self.assertIn({"key": "topic", "value": "machine learning"}, entries)
        self.assertIn({"key": "level", "value": "advanced"}, entries)

    def test_list_for_user_without_context_returns_empty_list(self):
        entries = self.store.list_for_user("ghost_user")

        self.assertEqual(entries, [])

    def test_users_context_does_not_bleed_into_another(self):
        self.store.save("alice", "lang", "Python")
        self.store.save("bob", "lang", "Java")

        alice_entries = self.store.list_for_user("alice")
        bob_entries = self.store.list_for_user("bob")

        self.assertEqual(len(alice_entries), 1)
        self.assertEqual(alice_entries[0], {"key": "lang", "value": "Python"})

        self.assertEqual(len(bob_entries), 1)
        self.assertEqual(bob_entries[0], {"key": "lang", "value": "Java"})


class TestContextStorePersistence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_second_instance_reads_data_saved_by_first(self):
        first = ContextStore(path=self.tmp.name)
        first.save("user1", "course", "AI")
        first.save("user1", "semester", "ninth")

        second = ContextStore(path=self.tmp.name)
        entries = second.list_for_user("user1")

        self.assertIn({"key": "course", "value": "AI"}, entries)
        self.assertIn({"key": "semester", "value": "ninth"}, entries)


class TestContextStoreCrossInstanceSync(unittest.TestCase):
    """Reproduce el bug: dos instancias sobre el mismo archivo no comparten estado en memoria."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_instance_b_sees_save_made_by_instance_a_after_b_was_created(self):
        # Simula server.py y assistant.py arrancando a la vez (ambas instancias
        # cargan el archivo vacío en __init__).
        instance_a = ContextStore(path=self.tmp.name)
        instance_b = ContextStore(path=self.tmp.name)

        # A escribe después de que B ya cargó su snapshot vacío.
        instance_a.save("user1", "k", "v")

        # B debería leer del disco, no de su caché en memoria.
        entries = instance_b.list_for_user("user1")
        self.assertIn({"key": "k", "value": "v"}, entries)


if __name__ == "__main__":
    unittest.main()
