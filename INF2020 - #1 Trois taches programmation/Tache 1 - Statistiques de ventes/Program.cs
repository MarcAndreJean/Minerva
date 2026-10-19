/* Task 1: Sales Statistics
Output statistics (mean, median, min, max) from a CSV file.
Csv file must have a header with at least the columns "price" and "quantity".
Usage : dotnet run <sales.csv>
*/
using System.Diagnostics;
using System.Globalization;

class Program
{
    const string PriceColumn = "price";
    const string QuantityColumn = "quantity";

    static void Main(string[] args)
    {
        if (args.Length < 1) {
            Console.WriteLine("Error: Missing CSV file path argument.");
            return;
        }

        // Start measuring time.
        var perfStopWatch = Stopwatch.StartNew();

        // Load data from CSV file.
        var priceList = Array.Empty<decimal>();
        var quantityList = Array.Empty<decimal>();
        try {
            var lines = File.ReadLines(args[0]).ToArray();
            var header = lines[0].Split(',').Select(h => h.Trim()).ToList();
            var priceIndex = header.IndexOf(PriceColumn);
            var quantityIndex = header.IndexOf(QuantityColumn);
            if (priceIndex < 0 || quantityIndex < 0) {
                throw new FormatException(
                    $"Missing column \"{PriceColumn}\" or \"{QuantityColumn}\" in header.");
            }

            var csvData = lines.Skip(1).Select(l => l.Split(',')).ToArray();
            priceList = csvData
                .Select(c => decimal.Parse(c[priceIndex], CultureInfo.InvariantCulture))
                .ToArray();
            quantityList = csvData
                .Select(c => decimal.Parse(c[quantityIndex], CultureInfo.InvariantCulture))
                .ToArray();
        }
        catch (Exception e) {
            Console.WriteLine($"Error while parsing file '{args[0]}': {e.Message}");
            return;
        }

        // Print statistics for price and quantity.
        Console.WriteLine("Price statistics:");
        Program.Output(priceList);

        Console.WriteLine("Quantity statistics:");
        Program.Output(quantityList);

        var perfTime = perfStopWatch.Elapsed.TotalMilliseconds;
        Console.WriteLine($"Execution time = {perfTime:F2} ms");
    }

    static void Output(decimal[] array)
    {
        var sorted = array.OrderBy(x => x).ToArray();
        var n = sorted.Length;

        var medianIndex = (int)(n / 2m);
        var median = (n % 2 != 0)
            ? sorted[medianIndex]
            : (sorted[medianIndex] + sorted[medianIndex - 1]) / 2m;

        Console.WriteLine($"\tMean:\t{array.Average():F2}");
        Console.WriteLine($"\tMedian:\t{median:F2}");
        Console.WriteLine($"\tMin:\t{array.Min():F2}");
        Console.WriteLine($"\tMax:\t{array.Max():F2}");
    }
}
