arlosync
========

Toy rsync-like library for keeping two directories in sync.

Features:

-	Optimizes network usage by using local information for files whenever possible (such as when they are edited, moved, or duplicated).
-	Uses the sync algorithm for directory metadata, as well as file contents.
-	Optimizes for size of network transfer by choosing an appropriate hashing window. For a file of size N changed in one place, makes one round-trip with O(sqrt(N)) network usage.
-	Supports fuzzy lookaround for copied or duplicated files.
-	O(mB/s) throughput (on my laptop), not bad for pure python.
