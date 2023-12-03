using CsvHelper;
using FraudDetection.BLL.Abstractions;
using System.Globalization;

namespace FraudDetection.BLL.Managers;

public class CsvService : ICsvService
{
    public IEnumerable<T> ReadCsv<T>(Stream file, Type? classMapType = null)
    {
        var reader = new StreamReader(file);
        var csv = new CsvReader(reader, CultureInfo.InvariantCulture);

        if (classMapType is not null)
            csv.Context.RegisterClassMap(classMapType);

        var records = csv.GetRecords<T>();
        return records;
    }

    public void WriteCsv<T>(IEnumerable<T> records)
    {
        using (var writer = new StreamWriter("D:\\file.csv"))
        using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
        {
            csv.WriteRecords(records);
        }
    }
}