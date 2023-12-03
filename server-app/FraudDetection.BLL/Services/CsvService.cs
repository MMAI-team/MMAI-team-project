using CsvHelper;
using CsvHelper.Configuration;
using FraudDetection.BLL.Abstractions;
using System.Globalization;
using System.Text;

namespace FraudDetection.BLL.Services;

public class CsvService : ICsvService
{
    private readonly CsvConfiguration Configuration = new CsvConfiguration(CultureInfo.InvariantCulture)
    {
            Delimiter = ",",
            TrimOptions = TrimOptions.Trim,
            HasHeaderRecord = true,
    };

    public IEnumerable<T> ReadCsv<T>(Stream file, Type? classMapType = null)
    {
        var reader = new StreamReader(file);
        var csv = new CsvReader(reader, CultureInfo.InvariantCulture);

        if (classMapType is not null)
            csv.Context.RegisterClassMap(classMapType);

        var records = csv.GetRecords<T>();
        return records;
    }

    public async Task<byte[]> GenerateCsvAsync<T>(IEnumerable<T> entities)
    {
        var memoryStream = new MemoryStream();
        using (var streamWriter = new StreamWriter(memoryStream, Encoding.UTF8))
        using (var csv = new CsvWriter(streamWriter, Configuration))
        {
            csv.WriteRecords(entities);
            await streamWriter.FlushAsync();
        }

        byte[] res = memoryStream.ToArray();

        return res;
    }
}