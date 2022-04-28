--- a/Lib/dumbdbm.py
+++ b/Lib/dumbdbm.py
@@ -21,6 +21,7 @@ is read when the database is opened, and
 
 """
 
+import ast as _ast
 import os as _os
 import __builtin__
 import UserDict
@@ -85,7 +86,7 @@ class _Database(UserDict.DictMixin):
             with f:
                 for line in f:
                     line = line.rstrip()
-                    key, pos_and_siz_pair = eval(line)
+                    key, pos_and_siz_pair = _ast.literal_eval(line)
                     self._index[key] = pos_and_siz_pair
 
     # Write the index dict to the directory file.  The original directory
--- a/Lib/test/test_dumbdbm.py
+++ b/Lib/test/test_dumbdbm.py
@@ -160,6 +160,14 @@ class DumbDBMTestCase(unittest.TestCase)
             self.assertEqual(expected, got)
             f.close()
 
+    def test_eval(self):
+        with open(_fname + '.dir', 'w') as stream:
+            stream.write("str(__import__('sys').stdout.write('Hacked!')), 0\n")
+        with test_support.captured_stdout() as stdout:
+            with self.assertRaises(ValueError):
+                dumbdbm.open(_fname).close()
+            self.assertEqual(stdout.getvalue(), '')
+
     def tearDown(self):
         _delete_files()
 
--- a/Misc/NEWS
+++ b/Misc/NEWS
@@ -18,6 +18,9 @@ Core and Builtins
 Library
 -------
 
+- Issue #22885: Fixed arbitrary code execution vulnerability in the dumbdbm
+  module.  Original patch by Claudiu Popa.
+
 - Issue #21849: Fixed xmlrpclib serialization of non-ASCII unicode strings in
   the multiprocessing module.
