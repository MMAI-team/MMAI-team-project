namespace FraudDetection.DAL.Entities;

[Serializable]
public record Transaction : BaseEntity
{
    #region CSV Properties

    public int number { get; set; }
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
    public bool is_fraud { get; set; }

    #endregion CSV Properties

    #region General Properties

    public Guid UserId { get; set; }
    public DateTimeOffset CreatedAt { get; set; }

    #endregion General Properties

    #region Fraud Detection Properites

    public double? FraudScoring { get; set; }
    public DateTimeOffset? VerifiedAt { get; set; }

    #endregion Fraud Detection Properites
}