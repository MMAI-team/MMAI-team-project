using FraudDetection.DAL.Enums;

namespace FraudDetection.DAL.Entities;

public record Rule : BaseEntity
{
    public string Name { get; set; }
    public string Description { get; set; }
    public RuleType RuleType { get; set; }
    public decimal? FraudScore { get; set; }
    public FraudScoreOperation? FraudScoreOperation { get; set; }

    public ICollection<RulePart> Parts { get; set; } = new List<RulePart>();
}