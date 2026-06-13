import unittest

from backend.cag import apply_context


class TestApplyContextNoContext(unittest.TestCase):
    def test_empty_context_returns_base_answer_unchanged(self):
        result = apply_context("user1", "What is ML?", "Machine learning is...", [])
        self.assertEqual(result, "Machine learning is...")

    def test_empty_context_does_not_alter_whitespace(self):
        base = "  answer with spaces  "
        result = apply_context("user1", "Q?", base, [])
        self.assertEqual(result, base)

    def test_empty_context_preserves_multiline_answer(self):
        base = "line one\nline two\nline three"
        result = apply_context("user1", "Q?", base, [])
        self.assertEqual(result, base)


class TestApplyContextWithSingleItem(unittest.TestCase):
    def test_result_contains_base_answer(self):
        base = "Neural networks are layers of nodes."
        context = [{"key": "level", "value": "principiante"}]
        result = apply_context("user1", "What is a neural network?", base, context)
        self.assertIn(base, result)

    def test_result_contains_context_value(self):
        base = "Neural networks are layers of nodes."
        context = [{"key": "level", "value": "principiante"}]
        result = apply_context("user1", "What is a neural network?", base, context)
        self.assertIn("principiante", result)

    def test_different_context_value_appears_in_result(self):
        base = "Supervised learning uses labeled data."
        context = [{"key": "style", "value": "con ejemplos practicos"}]
        result = apply_context("user2", "What is supervised learning?", base, context)
        self.assertIn("practicos", result)

    def test_result_is_string(self):
        base = "Some answer."
        context = [{"key": "lang", "value": "Spanish"}]
        result = apply_context("user1", "Q?", base, context)
        self.assertIsInstance(result, str)


class TestApplyContextWithMultipleItems(unittest.TestCase):
    def test_all_context_values_appear_in_result(self):
        base = "Deep learning is a subset of machine learning."
        context = [
            {"key": "level", "value": "principiante"},
            {"key": "lang", "value": "espanol"},
        ]
        result = apply_context("user1", "What is deep learning?", base, context)
        self.assertIn("principiante", result)
        self.assertIn("espanol", result)

    def test_base_answer_and_all_values_present_with_three_items(self):
        base = "Gradient descent minimizes a loss function."
        context = [
            {"key": "level", "value": "avanzado"},
            {"key": "format", "value": "bullet points"},
            {"key": "examples", "value": "con codigo Python"},
        ]
        result = apply_context("user3", "Explain gradient descent.", base, context)
        self.assertIn(base, result)
        self.assertIn("avanzado", result)
        self.assertIn("bullet points", result)
        self.assertIn("Python", result)

    def test_result_is_string_with_multiple_items(self):
        base = "An answer."
        context = [
            {"key": "a", "value": "alpha"},
            {"key": "b", "value": "beta"},
        ]
        result = apply_context("user1", "Q?", base, context)
        self.assertIsInstance(result, str)


class TestApplyContextReturnType(unittest.TestCase):
    def test_result_is_string_with_no_context(self):
        result = apply_context("user1", "Q?", "answer", [])
        self.assertIsInstance(result, str)

    def test_result_is_string_with_context(self):
        result = apply_context("user1", "Q?", "answer", [{"key": "k", "value": "v"}])
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
