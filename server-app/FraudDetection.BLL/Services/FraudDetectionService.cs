using FraudDetection.BLL.Abstractions;
using FraudDetection.BLL.Models;
using Microsoft.AspNetCore.Http;
using RestSharp;
using System.Security.Claims;
using System.Text.Json;

namespace FraudDetection.BLL.Services;

public class FraudDetectionService : IFraudDetectionService
{
    public readonly string FraudDetectionSystemUrlProtocol = "http://";
    public readonly string FraudDetectionSystemBaseUrl = "fraud-detection-demo.centralus.azurecontainer.io:5571/api/v1";
    public readonly string TransactionVerificationUrl = "model/submit";

    public async Task<FraudScoringModel> VerifyTransactionAsync(string data)
    {
        var client = new RestClient(FraudDetectionSystemUrlProtocol + FraudDetectionSystemBaseUrl);
        var request = new RestRequest(TransactionVerificationUrl);
        request.AddBody(data);

        var response = await client.ExecutePostAsync(request);

        var res = JsonSerializer.Deserialize<FraudScoringModel>(response.Content);

        var test = 0.77M;

        return new()
        {
            transformer_scoring = PreprocessFraudScoring(test),
        };
    }

    private static decimal PreprocessFraudScoring(decimal score) => Math.Round(score * 100, 2);
}
