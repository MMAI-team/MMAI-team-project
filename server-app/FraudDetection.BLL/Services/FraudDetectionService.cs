using FraudDetection.BLL.Abstractions;
using FraudDetection.BLL.Models;
using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using RestSharp;
using System.Security.Claims;
using System.Text.Json;

namespace FraudDetection.BLL.Services;

public class FraudDetectionService : IFraudDetectionService
{
    public readonly string FraudDetectionSystemUrlProtocol = "http://";
    public readonly string FraudDetectionSystemBaseUrl = "localhost:5571/api/v1";
    public readonly string TransactionVerificationUrl = "model/submit";

    public async Task<FraudScoringModel> VerifyTransactionAsync(string data)
    {
        var client = new RestClient(FraudDetectionSystemUrlProtocol + FraudDetectionSystemBaseUrl);
        var request = new RestRequest(TransactionVerificationUrl);
        request.AddBody(data);

        var response = await client.ExecutePostAsync(request);

        if (!response.IsSuccessful)
        {
            Random rnd = new Random();
            int num = rnd.Next(100);

            return new()
            {
                transformer_scoring = num,
            };
        }

        var fraudScoreModel = JsonConvert.DeserializeObject<FraudScoringModel>(response.Content!)
            ?? throw new ArgumentNullException("Fraud Detection System: returned bad response");

        return new()
        {
            transformer_scoring = PreprocessFraudScoring(fraudScoreModel.FNN > fraudScoreModel.xgoost_regressor ? fraudScoreModel.FNN : fraudScoreModel.xgoost_regressor),
        };
    }

    private static decimal PreprocessFraudScoring(decimal score) 
    {
        var res = Math.Round(score * 100, 2);

        return res > 100 ? 100 : res;
    }
}
