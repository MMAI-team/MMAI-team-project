namespace FraudDetection.WebApp.Models.TransactionModels;

public record TransactionViewModel
{
    public string trans_date_trans_time { get; init; }
    public string cc_num { get; init; }
    public string merchant { get; init; }
    public string categoryamt { get; init; }
    public string first { get; init; }
    public string last { get; init; }
    public string gender { get; init; }
    public string street { get; init; }
    public string city { get; init; }
    public string state { get; init; }
    public string zip { get; init; }
    public string lat { get; init; }
    public string longs { get; init; }
    public string city_pop { get; init; }
    public string job { get; init; }
    public string dob { get; init; }
    public string trans_num { get; init; }
    public string unix_time { get; init; }
    public string merch_lat { get; init; }
    public string merch_long { get; init; }

    public DateTimeOffset CreatedAt { get; init; }
    public DateTimeOffset? VerifiedAt { get; init; }
}