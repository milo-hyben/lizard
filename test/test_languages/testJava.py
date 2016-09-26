import unittest
from lizard import analyze_file


def get_java_fileinfo(source_code):
    return analyze_file.analyze_source_code("a.java", source_code)


def get_java_function_list(source_code):
    return get_java_fileinfo(source_code).function_list


class TestJava(unittest.TestCase):

    def test_function_with_throws(self):
        result = get_java_function_list("void fun() throws e1, e2{}")
        self.assertEqual(1, len(result))

    def test_function_with_decorator(self):
        result = get_java_function_list("@abc() void fun() throws e1, e2{}")
        self.assertEqual(1, len(result))

    def test_class_with_decorator(self):
        result = get_java_function_list("@abc() class funxx{ }")
        self.assertEqual(0, len(result))

    def test_class_with_decorator_that_has_namespace(self):
        result = get_java_function_list("@a.b() class funxx{ }")
        self.assertEqual(0, len(result))

    def test_functions_with_class_literal(self):
        result = get_java_function_list("""
            void funA(){
                Class[] p = new Class[]{ String.class,String.class };
            }
            void funB(){
            }
        """)
        self.assertEqual(2, len(result))
        self.assertEqual("funA", result[0].name)
        self.assertEqual("funB", result[1].name)
        self.assertEqual(2, result[0].start_line)
        self.assertEqual(4, result[0].end_line)
        self.assertEqual(5, result[1].start_line)
        self.assertEqual(6, result[1].end_line)

