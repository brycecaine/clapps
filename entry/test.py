import unittest
from datetime import date, datetime

from entry.entry import (Transaction, exists_in_db, get_amount, get_dates,
                         get_entry_type, get_started_action, insert_tx_into_db,
                         is_todo, parse_txs)


class AmountTestCase(unittest.TestCase):
    def _test_get_amount(self, entry, expected_amount):
        amount = get_amount(entry)

        self.assertEqual(amount, expected_amount)

    # ----------
    def test_get_amount_at_beginning(self):
        entry = '3.45 toothpick'
        expected_amount = 3.45

        self._test_get_amount(entry, expected_amount)

    def test_get_amount_surrounded_by_text(self):
        entry = 'krogers 3.45 toothpick'
        expected_amount = 3.45

        self._test_get_amount(entry, expected_amount)

    def test_get_amount_surrounded_by_text_and_date(self):
        entry = '1/1/2000 3.45 toothpick'
        expected_amount = 3.45

        self._test_get_amount(entry, expected_amount)

    def test_get_amount_surrounded_by_text_and_date_conversational_format(self):
        entry = 'Jan 1 2000 3.45 toothpick'
        expected_amount = 3.45

        self._test_get_amount(entry, expected_amount)

    def test_get_amount_before_date(self):
        entry = '3.45 1/1/2000 toothpick'
        expected_amount = 3.45

        self._test_get_amount(entry, expected_amount)

    # ----------
    def test_get_zero_amount_at_beginning(self):
        entry = '0.00 toothpick'
        expected_amount = 0.00

        self._test_get_amount(entry, expected_amount)

    def test_get_zero_amount_surrounded_by_text(self):
        entry = 'krogers 0.00 toothpick'
        expected_amount = 0.00

        self._test_get_amount(entry, expected_amount)

    def test_get_zero_amount_surrounded_by_text_and_date(self):
        entry = '1/1/2000 0.00 toothpick'
        expected_amount = 0.00

        self._test_get_amount(entry, expected_amount)

    def test_get_zero_amount_surrounded_by_text_and_date_conversational_format(self):
        entry = 'Jan 1 2000 0.00 toothpick'
        expected_amount = 0.00

        self._test_get_amount(entry, expected_amount)

    def test_get_zero_before_date(self):
        entry = '0.00 1/1/2000 toothpick'
        expected_amount = 0.00

        self._test_get_amount(entry, expected_amount)

    # ----------
    def test_get_no_decimal_amount_at_beginning(self):
        entry = '98 toothpick'
        expected_amount = 98

        self._test_get_amount(entry, expected_amount)

    def test_get_no_decimal_amount_surrounded_by_text(self):
        entry = 'krogers 98 toothpick'
        expected_amount = 98

        self._test_get_amount(entry, expected_amount)

    def test_get_no_decimal_amount_surrounded_by_text_and_date(self):
        entry = '1/1/2000 98 toothpick'
        expected_amount = 98

        self._test_get_amount(entry, expected_amount)

    def test_get_no_decimal_amount_surrounded_by_text_and_date_conversational_format(self):
        entry = 'Jan 1 2000 98 toothpick'
        expected_amount = 98

        self._test_get_amount(entry, expected_amount)

    def test_get_no_decimal_before_date(self):
        entry = '98 1/1/2000 toothpick'
        expected_amount = 98

        self._test_get_amount(entry, expected_amount)


class DateTestCase(unittest.TestCase):
    def _test_get_date(self, entry, expected_dates):
        dates = get_dates(entry)

        self.assertEqual(dates, expected_dates)

    def test_get_date_yyyy_mm_dd_at_beginning(self):
        entry = '2000-01-01 3.45 toothpick'
        expected_date = [datetime(2000, 1, 1)]

        self._test_get_date(entry, expected_date)

    def test_get_date_mm_dd_yyyy_at_beginning(self):
        entry = '1/1/2000 3.45 toothpick'
        expected_date = [datetime(2000, 1, 1)]

        self._test_get_date(entry, expected_date)

    def test_get_date_mon_dd_yyyy_at_beginning(self):
        entry = 'Jan 1 2000 3.45 toothpick'
        expected_date = [datetime(2000, 1, 1)]

        self._test_get_date(entry, expected_date)

    def test_get_two_dates_yyyy_mm_dd(self):
        entry = '2000-01-01 3.45 toothpick 2/2/2002'
        expected_date = [datetime(2000, 1, 1), datetime(2002, 2, 2)]

        self._test_get_date(entry, expected_date)

    # ----------
    def test_get_no_year_conversational(self):
        entry = '46.00 Jun 30 Xfinity'
        expected_date = [datetime(2022, 6, 30)]

        self._test_get_date(entry, expected_date)


class EntryTestCase(unittest.TestCase):
    def test_tx_is_tx(self):
        entry = '1/1/2000 3.45 toothpick'
        entry_type = get_entry_type(entry)

        self.assertEqual(entry_type, 'transaction')

    def test_action_is_action(self):
        entry = 'Sleep 1/1/2000'
        entry_type = get_entry_type(entry)

        self.assertEqual(entry_type, 'action')

    def test_journal_is_journal(self):
        entry = '1/1/2000 I slept today'
        entry_type = get_entry_type(entry)

        self.assertEqual(entry_type, 'journal')


class ParseTestCase(unittest.TestCase):
    def _test_parse_txs(self, entry, expected_txs):
        txs = parse_txs(entry)

        self.assertEqual(txs, expected_txs)

    def test_parse_txs_1(self):
        entry = '23.43 DI'

        expected_txs = [
            {'account_id': 1,
             'amount': -23.43,
             'category': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': 'DI',
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_2(self):
        entry = '14.57 Mo Bettahs'

        expected_txs = [
            {'account_id': 1,
             'amount': -14.57,
             'category': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': 'Mo Bettahs',
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_3(self):
        entry = '34.98 Costco Groceries 6/21/2022'

        expected_txs = [
            {'account_id': 1,
             'amount': -34.98,
             'category': 'Groceries',
             'dt': date(2022, 6, 21),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': 'Costco',
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_4(self):
        entry = '46.00 Jun 30 Xfinity'

        expected_txs = [
            {'account_id': 1,
             'amount': -46.00,
             'category': None,
             'dt': date(2022, 6, 30),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': 'Xfinity',
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_5(self):
        entry = '18.23 reimbursable'

        expected_txs = [
            {'account_id': 1,
             'amount': -18.23,
             'category': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': 'reimbursable',
             'vendor': None,
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_6(self):
        entry = '13'

        expected_txs = [
            {'account_id': 1,
             'amount': -13,
             'category': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': None,
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_7(self):
        entry = '32.76 yesterday'

        expected_txs = [
            {'account_id': 1,
             'amount': -32.76,
             'category': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day-1),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': None,
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_8(self):
        entry = '53.19 Jul 20'

        expected_txs = [
            {'account_id': 1,
             'amount': -53.19,
             'category': None,
             'dt': date(2022, 7, 20),
             'entry': entry,
             'file_path': '/wef/wef/wef',
             'seq_no': 1,
             'tags': '',
             'vendor': None,
            }
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_txs_9(self):
        entry = '42 split Groceries 20 Clothes 22'

        expected_txs = [
            {'amount': -20.0,
             'vendor': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day),
             'category': 'Groceries',
             'tags': '',
             'account_id': 1,
             'seq_no': 1,
             'entry': '42 split Groceries 20 Clothes 22',
             'file_path': '/wef/wef/wef',
            },
            {'amount': -22.0,
             'vendor': None,
             'dt': date(datetime.now().year, datetime.now().month, datetime.now().day),
             'category': 'Clothes',
             'tags': '',
             'account_id': 1,
             'seq_no': 2,
             'entry': '42 split Groceries 20 Clothes 22',
             'file_path': '/wef/wef/wef',
            },
        ]

        self._test_parse_txs(entry, expected_txs)

    def test_parse_todo_1(self):
        entry = 'had dinner'
        entry_is_todo = is_todo(entry)
        self.assertFalse(entry_is_todo)

    def test_parse_todo_2(self):
        entry = 'go grocery shopping'
        entry_is_todo = is_todo(entry)
        self.assertTrue(entry_is_todo)

    def test_parse_todo_3(self):
        entry = 'fix door'
        entry_is_todo = is_todo(entry)
        self.assertTrue(entry_is_todo)

    def test_parse_todo_4(self):
        entry = 'Emmett said cool'
        entry_is_todo = is_todo(entry)
        self.assertFalse(entry_is_todo)

    def test_parse_todo_5(self):
        entry = 'read book'
        entry_is_todo = is_todo(entry)
        self.assertTrue(entry_is_todo)

    def test_parse_todo_6(self):
        entry = 'buy food'
        entry_is_todo = is_todo(entry)
        self.assertTrue(entry_is_todo)

    def test_parse_todo_7(self):
        entry = 'bought food'
        entry_is_todo = is_todo(entry)
        self.assertFalse(entry_is_todo)

    def test_parse_todo_8(self):
        entry = 'sleep'
        entry_is_todo = is_todo(entry)
        self.assertTrue(entry_is_todo)

    def test_parse_todo_9(self):
        entry = 'sleep tomorrow'
        entry_is_todo = is_todo(entry)
        self.assertTrue(entry_is_todo)

    def test_parse_todo_10(self):
        entry = 'sleep yesterday'
        entry_is_todo = is_todo(entry)
        self.assertFalse(entry_is_todo)


class DBTestCase(unittest.TestCase):
    def test_tx_exists_in_db(self):
        tx = {'id': 13}
        self.assertTrue(exists_in_db('tx', tx))

    def test_tx_does_not_exist_in_db(self):
        tx = {'id': -1}
        self.assertFalse(exists_in_db('tx', tx))

    def test_insert_tx_into_db(self):
        insert_tx_into_db('5 socks')

    def test_insert_tx_obj_into_db(self):
        transaction = Transaction('500 apple')
        transaction.insert_into_db()

    def test_get_started_action(self):
        started_action = get_started_action('Sleep')
        self.assertFalse(started_action)


class TransactionClassCase(unittest.TestCase):
    def test_transaction_class(self):
        entry = '3.45 toothpick'
        transaction = Transaction(entry)
        self.assertEqual(transaction.amount, -3.45)


if __name__ == '__main__':
    unittest.main()

