/* Task 3: Web Scraping
Scrape text content from a webpage.
Usage : dotnet run <url>
*/
using System.Diagnostics;
using System.Globalization;
using HtmlAgilityPack;

class Program
{
    static async Task Main(string[] args)
    {
        if (args.Length < 1) {
            Console.WriteLine("Error: Missing URL argument.");
            return;
        }

        Console.WriteLine($"url: {args[0]}");
        // Start measuring time.
        var perfStopWatch = Stopwatch.StartNew();

        // Load data from URL.
        var textContent = string.Empty;
        try {
            using (var client = new HttpClient()) {
                client.DefaultRequestHeaders.Add("User-Agent", "scraping/1.0");
                textContent = await client.GetStringAsync(args[0]);
            }
        }
        catch (Exception e) {
            Console.WriteLine($"Error while fetching URL '{args[0]}': {e.Message}");
            return;
        }

        // Remove css, js and html content.
        var doc = new HtmlDocument();
        doc.LoadHtml(textContent);
        var nodes = doc.DocumentNode.SelectNodes("//script | //style | //noscript | //template") ?? Enumerable.Empty<HtmlNode>();
        foreach (var node in nodes)
        {
            node.Remove();
        }
        // Extract text content and count words.
        var textNodes = doc.DocumentNode.SelectNodes("//text()") ?? Enumerable.Empty<HtmlNode>();
        string text = string.Join(" ", textNodes
            .Select(node => HtmlEntity.DeEntitize(node.InnerText).Trim())
            .Where(nodeText => nodeText.Length > 0));
        var wordCount = text.Split((char[]?)null, StringSplitOptions.RemoveEmptyEntries).Length;
        
        Console.WriteLine($"Word count: {wordCount}");

        var perfTime = perfStopWatch.Elapsed.TotalMilliseconds;
        Console.WriteLine($"Execution time = {perfTime:F2} ms");
    }
}
