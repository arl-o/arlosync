arlosync
========

Toy rsync-like library for keeping two directories in sync.

Features:

-	Optimizes by using local information for changed/moved/duplicated files whenever possible.
-	Uses sync algorithm for directory metadata, as well as file contents.
-	Optimizes for size of network transfer by choosing an appropriate hashing window. For a file of size N changed in one place, makes one round-trip with O(sqrt(N)) network usage.
-	Supports fuzzy lookaround for copied or duplicated files.
-	O(mB/s) throughput (on my laptop), not bad for pure python.
