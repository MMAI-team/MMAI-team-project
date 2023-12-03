namespace FraudDetection.BLL.Abstractions;

public interface ICsvService
{
    IEnumerable<T> ReadCsv<T>(Stream file, Type? classMapType = null);
    Task<byte[]> GenerateCsvAsync<T>(IEnumerable<T> entities);
}