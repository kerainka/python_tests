import unittest
import unittest.mock
import documents as doc_module
from documents import *
import copy

documents_test = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories_test = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


# Следует протестировать основные функции по
# получению информации о документах, добавлении и удалении элементов из словаря.
class TestDocuments(unittest.TestCase):

    def setUp(self):
        doc_module.documents = copy.deepcopy(documents_test)
        doc_module.directories = copy.deepcopy(directories_test)

    def tearDown(self):
        pass

    def test_check_document_existance(self):
        self.assertTrue(check_document_existance("2207 876234"))
        self.assertFalse(check_document_existance("1302 444444"))

    def test_get_doc_owner_name(self):
        with unittest.mock.patch("builtins.input", return_value="2207 876234"):
            self.assertEqual("Василий Гупкин", get_doc_owner_name())
        with unittest.mock.patch("builtins.input", return_value="1302 444444"):
            self.assertIsNone(get_doc_owner_name())

    def test_get_all_doc_owners_names(self):
        names = set(["Василий Гупкин", "Геннадий Покемонов", "Аристарх Павлов"])
        self.assertSetEqual(names, get_all_doc_owners_names())

    def test_remove_doc_from_shelf(self):
        doc_number = "2207 876234"
        remove_doc_from_shelf(doc_number)
        self.assertNotIn(doc_number, doc_module.directories["1"])

    def test_add_new_shelf(self):
        with unittest.mock.patch("builtins.input", return_value="2"):
            self.assertEqual(("2", False), add_new_shelf())
        with unittest.mock.patch("builtins.input", return_value="4"):
            self.assertEqual(("4", True), add_new_shelf())

    def test_append_doc_to_shelf(self):
        append_doc_to_shelf("10006", "3")
        self.assertIn("10006", doc_module.directories["3"])

    def test_delete_doc(self):
        with unittest.mock.patch("builtins.input", return_value="2207 876234"):
            self.assertEqual(("2207 876234", True), delete_doc())
            self.assertNotIn({"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
                             doc_module.documents)
            self.assertNotIn("2207 876234", doc_module.directories["1"])

    def test_get_doc_shelf(self):
        with unittest.mock.patch("builtins.input", return_value="2207 876234"):
            self.assertEqual("1", get_doc_shelf())

    def test_move_doc_to_shelf(self):
        self.assertEqual('Документ номер "2207 876234" был перемещен на полку номер "3"',
                         move_doc_to_shelf("2207 876234", "3"))
        self.assertNotIn("2207 876234", doc_module.directories["1"])
        self.assertIn("2207 876234", doc_module.directories["3"])

    def test_show_document_info(self):
        self.assertEqual('passport "2207 876234" "Василий Гупкин"', show_document_info(doc_module.documents[0]))

    def test_show_all_docs_info(self):
        self.assertEqual(['passport "2207 876234" "Василий Гупкин"', 'invoice "11-2" "Геннадий Покемонов"',
                          'insurance "10006" "Аристарх Павлов"'], show_all_docs_info())

    def test_add_new_doc(self):
        self.assertEqual("2", add_new_doc("doc number", "doc type", "owner name", "2"))
        self.assertIn({"type": "doc type", "number": "doc number", "name": "owner name"}, doc_module.documents)
        self.assertIn("doc number", doc_module.directories["2"])


if __name__ == "__main__":
    unittest.main()
