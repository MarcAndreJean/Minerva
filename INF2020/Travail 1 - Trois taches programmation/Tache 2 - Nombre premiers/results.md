# Python
❯ python .\prime-numbers.py 10_000_000
Prime numbers up to 10000000:
[...]
Execution time = 1.084s

## moyenne sur 10 éxécutions
1.097s

# C#
❯ dotnet run -- 10000000
Prime numbers up to 10000000:
[...]
Execution time = 0.686s

## moyenne sur 10 éxécutions
0.649s

# Source
http://research.cs.wisc.edu/techreports/1990/TR909.pdf
Computer Sciences Technical Report #909, Department of Computer Sciences University of Wisconsin-Madison, January 2, 1990 (the use of optimization of starting from squares, and thus using only the numbers whose square is below the upper limit, is shown).