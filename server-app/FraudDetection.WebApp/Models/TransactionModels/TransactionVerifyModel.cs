namespace FraudDetection.WebApp.Models.TransactionModels;

public record TransactionVerifyModel
{
    public DateTimeOffset trans_date_trans_time { get; set; }
    public string cc_num { get; set; }
    public string merchant { get; set; }
    public string category { get; set; }
    public string amt { get; set; }
    public string first { get; set; }
    public string last { get; set; }
    public string gender { get; set; }
    public string street { get; set; }
    public string city { get; set; }
    public string state { get; set; }
    public string zip { get; set; }
    public string lat { get; set; }
    public string longs { get; set; }
    public string city_pop { get; set; }
    public string job { get; set; }
    public string dob { get; set; }
    public string trans_num { get; set; }
    public string unix_time { get; set; }
    public string merch_lat { get; set; }
    public string merch_long { get; set; }
}