using FraudDetection.BLL.Models;

namespace FraudDetection.BLL.Abstractions;

public interface IFraudDetectionService
{
    Task<FraudScoringModel> VerifyTransactionAsync(string data);
}