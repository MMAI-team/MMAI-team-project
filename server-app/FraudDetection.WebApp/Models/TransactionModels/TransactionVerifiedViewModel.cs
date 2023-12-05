namespace FraudDetection.WebApp.Models.TransactionModels;

public record TransactionVerifiedViewModel
{
    public double FraudScoring { get; set; }
    public string trans_num { get; set; }
    public DateTimeOffset? VerifiedAt { get; set; }
}