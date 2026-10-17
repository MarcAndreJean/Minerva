/* Task 2: Prime Numbers
Output list of prime numbers up to a given limit.
Implementation of the `Sieve of Eratosthenes` algorithm.
Usage : dotnet run <limit>
*/
using System.Diagnostics;
using System.Globalization;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 1) {
            Console.WriteLine("Error: Missing limit argument.");
            return;
        }

        if (!int.TryParse(args[0], out int n)) {
            Console.WriteLine("Error: Limit must be an integer greater than 1");
            return;
        }

        if (n < 2) {
            Console.WriteLine("Error: Limit must be an integer greater than 1.");
            return;
        }

        // Start measuring time (performance counter).
        var perfStopWatch = Stopwatch.StartNew();

        var isPrimeList = Enumerable.Repeat(true, n + 1).ToArray();
        isPrimeList[0] = isPrimeList[1] = false;

        var limit = (int)Math.Sqrt(n);
        for (var i = 2; i <= limit; i++) {
            if (isPrimeList[i]) {
                for (var j = i * i; j <= n; j += i) {
                    isPrimeList[j] = false;
                }
            }
        }

        // Print the list of prime numbers.
        var primes = isPrimeList
            .Select((value, index) => new { value, index })
            .Where(x => x.value)
            .Select(x => x.index)
            .ToList();
        Console.WriteLine($"Prime numbers up to {n}:");
        Console.WriteLine(string.Join(", ", primes));

        var perfTime = perfStopWatch.Elapsed.TotalSeconds;
        Console.WriteLine($"Execution time = {perfTime:F3}s");
    }
}
