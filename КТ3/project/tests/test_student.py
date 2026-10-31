"""Ваши проверки. Сначала рассчитайте ожидания по требованиям, затем пишите код."""

import unittest
from copy import deepcopy
from mediapolka import issue, new_state, return_loan


class StudentTests(unittest.TestCase):
    def test_initial_state(self):
        state = new_state()
        self.assertEqual(state["stock"], {"mic": 3, "tripod": 1, "light": 0})
        self.assertEqual(state["loans"], [])
        self.assertEqual(state["next_id"], 1)

    def test_issue_does_not_touch_other_items(self):
        state = new_state()
        issue(state, "mic", "2")
        self.assertEqual(state["stock"], {"mic": 1, "tripod": 1, "light": 0})

    def test_return_does_not_touch_other_items(self):
        state = new_state()
        loan_id = issue(state, "tripod", "1")["loan_id"]
        return_loan(state, loan_id)
        self.assertEqual(state["stock"], {"mic": 3, "tripod": 1, "light": 0})

    def test_states_do_not_interfere(self):
        state_a = new_state()
        state_b = new_state()
        issue(state_a, "mic", "1")
        self.assertEqual(state_a["stock"]["mic"], 2)
        self.assertEqual(state_b["stock"]["mic"], 3)
        self.assertEqual(state_b["loans"], [])
        self.assertEqual(state_b["next_id"], 1)
    
    def test_allowed_quantities(self):
        for quantity_text, expected in (("1", 2), ("2", 1), ("3", 0)):
            with self.subTest(quantity_text=quantity_text):
                state = new_state()
                result = issue(state, "mic", quantity_text)
                self.assertTrue(result["ok"])
                self.assertEqual(state["stock"]["mic"], expected)
                self.assertEqual(state["loans"][0]["quantity"], int(quantity_text))

    def test_whitespace_trimmed(self):
        state = new_state()
        result = issue(state, "mic", "  2  ")
        self.assertTrue(result["ok"])
        self.assertEqual(state["stock"]["mic"], 1)

    def test_invalid_quantities(self):
        for quantity_text in ("", "   ", "abc", "1.5", "-1", "0", "4", "10", "1 2"):
            with self.subTest(quantity_text=quantity_text):
                state = new_state()
                snapshot = deepcopy(state)
                result = issue(state, "mic", quantity_text)        
                self.assertFalse(result["ok"])
                self.assertEqual(result["message"], "Введите целое количество от 1 до 3")
                self.assertNotIn("loan_id", result)
                self.assertEqual(state["stock"], snapshot["stock"])
                self.assertEqual(state["loans"], snapshot["loans"])
                self.assertEqual(state["next_id"], snapshot["next_id"])

    def test_rejection_does_not_corrupt_id(self):
        state = new_state()
        issue(state, "mic", "0")          
        self.assertEqual(state["next_id"], 1)
        result = issue(state, "mic", "1") 
        self.assertEqual(result["loan_id"], 1)

    def test_r2_before_r3(self):
        state = new_state()
        result = issue(state, "light", "0")
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Введите целое количество от 1 до 3")

    def test_more_than_available(self):
        state = new_state()
        result = issue(state, "mic", "3")
        self.assertTrue(result["ok"])            
        self.assertEqual(state["stock"]["mic"], 0)
        result = issue(state, "mic", "1")      
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Недостаточно оборудования")
        self.assertEqual(state["stock"]["mic"], 0)
        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(state["next_id"], 2)
    
    def test_zero_stock(self):
        state = new_state()
        result = issue(state, "light", "1")
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Недостаточно оборудования")
        self.assertEqual(state["stock"]["light"], 0)
        self.assertEqual(state["loans"], [])
        self.assertEqual(state["next_id"], 1)

    def test_zero_tripod(self):
        state = new_state()
        self.assertTrue(issue(state, "tripod", "1")["ok"])
        result = issue(state, "tripod", "1")
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Недостаточно оборудования")
        self.assertEqual(state["next_id"], 2)

    def test_success_response(self):
        state = new_state()
        result = issue(state, "mic", "2")

        self.assertTrue(result["ok"])
        self.assertEqual(result["message"], "Выдано")
        self.assertEqual(result["loan_id"], 1)

        self.assertEqual(len(state["loans"]), 1)
        self.assertEqual(
            state["loans"][0],
            {"id": 1, "item": "mic", "quantity": 2, "status": "issued"},
        )
        self.assertEqual(state["stock"]["mic"], 1)
    
    def test_ids_increment(self):
        state = new_state()
        self.assertEqual(issue(state, "mic", "1")["loan_id"], 1)
        self.assertEqual(issue(state, "mic", "1")["loan_id"], 2)
        self.assertEqual(issue(state, "mic", "1")["loan_id"], 3)
        self.assertEqual(state["next_id"], 4)

    def test_failed_issue_does_not_corrupt_id(self):
        state = new_state()
        issue(state, "mic", "0")
        issue(state, "mic", "0")
        self.assertEqual(state["next_id"], 1)
        self.assertEqual(issue(state, "mic", "1")["loan_id"], 1)

    def test_return_restores_stock(self):
        state = new_state()
        loan_id = issue(state, "mic", "2")["loan_id"]
        result = return_loan(state, loan_id)
        self.assertTrue(result["ok"])
        self.assertEqual(result["message"], "Возвращено")
        self.assertEqual(state["stock"]["mic"], 3)
        self.assertEqual(state["loans"][0]["status"], "returned")
        self.assertEqual(len(state["loans"]), 1)
    
    def test_return_does_not_change_next_id(self):
        state = new_state()
        loan_id = issue(state, "mic", "1")["loan_id"]
        next_id_before = state["next_id"]
        return_loan(state, loan_id)
        self.assertEqual(state["next_id"], next_id_before)

    def test_issue_return_issue_again(self):
        state = new_state()
        first = issue(state, "mic", "2")["loan_id"]
        return_loan(state, first)
        second = issue(state, "mic", "2")
        self.assertEqual(second["loan_id"], 2)
        self.assertEqual(state["stock"]["mic"], 1)

    def test_double_return_rejected_unchanged(self):
        state = new_state()
        loan_id = issue(state, "mic", "2")["loan_id"]
        return_loan(state, loan_id)

        snapshot_stock = dict(state["stock"])
        snapshot_loans = [dict(loan) for loan in state["loans"]]
        snapshot_next = state["next_id"]

        result = return_loan(state, loan_id)
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Уже возвращено")
        self.assertEqual(state["stock"], snapshot_stock)
        self.assertEqual(state["loans"], snapshot_loans)
        self.assertEqual(state["next_id"], snapshot_next)

    def test_unknown_id_rejected_unchanged(self):
        state = new_state()
        issue(state, "mic", "1")

        snapshot_stock = dict(state["stock"])
        snapshot_loans = [dict(loan) for loan in state["loans"]]
        snapshot_next = state["next_id"]

        result = return_loan(state, 99)
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Выдача не найдена")
        self.assertEqual(state["stock"], snapshot_stock)
        self.assertEqual(state["loans"], snapshot_loans)
        self.assertEqual(state["next_id"], snapshot_next)

    def test_return_on_empty_state(self):
        state = new_state()
        result = return_loan(state, 1)
        self.assertFalse(result["ok"])
        self.assertEqual(result["message"], "Выдача не найдена")
        self.assertEqual(state["stock"], {"mic": 3, "tripod": 1, "light": 0})
        self.assertEqual(state["loans"], [])
        self.assertEqual(state["next_id"], 1)