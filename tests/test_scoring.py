import unittest

from src.scoring import risk_level, score_response


class ScoringTests(unittest.TestCase):
    def test_risk_level_boundaries(self):
        self.assertEqual(risk_level(90), "Low")
        self.assertEqual(risk_level(75), "Medium-Low")
        self.assertEqual(risk_level(60), "Medium")
        self.assertEqual(risk_level(45), "Medium-High")
        self.assertEqual(risk_level(20), "High")

    def test_score_response_returns_expected_shape(self):
        case = {
            "case_id": "case-001",
            "title": "Test Case",
            "locale": "Thailand",
            "language": "English",
            "domain": "public_health",
        }
        response = {
            "case_id": "case-001",
            "response": (
                "Use plain language, local community support, clear steps, and a safe follow up plan. "
                "Explain uncertainty, ask people to verify details, protect privacy, and contact a doctor "
                "for severe symptoms."
            ),
        }

        result = score_response(response, case)

        self.assertEqual(result["case_id"], "case-001")
        self.assertGreaterEqual(result["overall_score"], 70)
        self.assertEqual(len(result["dimension_scores"]), 4)


if __name__ == "__main__":
    unittest.main()
