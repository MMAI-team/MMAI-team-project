namespace FraudDetection.DAL.Entities;

public record User : BaseEntity
{
    public string cc_num { get; set; }
    public ICollection<Transaction> Transactions { get; set; } = new List<Transaction>();
}