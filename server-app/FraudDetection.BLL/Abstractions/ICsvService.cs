namespace FraudDetection.BLL.Abstractions;

public interface ICsvService
{
    IEnumerable<T> ReadCsv<T>(Stream file, Type? classMapType = null);
    void WriteCsv<T>(IEnumerable<T> records);
}