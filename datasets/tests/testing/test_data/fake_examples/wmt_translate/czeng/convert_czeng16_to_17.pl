# This is a fake perl script to mimic the one written to filter CzEng 1.6 to
# create CzEng 1.7. Our code just parses it to find the blocks that need to be
# filtered out.

use strict;

my %bad = map { ($_, 1) } qw{
2 3 5
9 10 16
};


print STDERR "Done.\n";

