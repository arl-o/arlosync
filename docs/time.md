Time tracking
=============

### Feb 11 - 30m

Understanding problem, setting up dev env, checking and fixing provided tests.

### Feb 21 - 4h

Planning server/client relationship on sticky notes, reviewing grpc API. Read rsync wikipedia page, avoiding looking at more detailed code/example implementations.

Algorithm outlined (in my brain) for file moves/copies, updates, updates&moves simultaneously, but I haven't yet cleanly covered the case 'client creates two identical files between sync events (where we only want to send one copy of the file on the wire).

Read about file watcher libs. Want to minimize differences between 'live' behavior and startup behavior, which means not relying overmuch on individual events like 'file moved', so I'll just repeat syncs at regular intervals and minimize the cost of these events.

Chose hash implementations.

Read https://rsync.samba.org/~tridge/phd_thesis.pdf - Discarded run-length-encoding of rolling tokens as a non-worthwile investment. Stream compression also looks only marginally worse than 'enhanced compression', so we'll rely on our RPC compression implementation.

Added own implementation of adler32 for rolling properties.

Started thinking about the client-side file reads - poking around with simplest version to test file throughput.

### Feb 25 - 30m

Fixed some of the hashing.

### Feb 26 - 2h

Cleaned up and implemented the basic 1-file rsync behavior. Exchanges tokens and literal bytes to reconstruct the file.

### Mar 9 - 8h

All the file/directory behavior, GRPC integration. Design is pretty much final

### Mar 12 - 7h

Cleaning up, deduplicating, adding error handling and better logging.
