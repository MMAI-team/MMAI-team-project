using FraudDetection.DAL.Enums;

namespace FraudDetection.DAL.Entities;

public record RulePart : BaseEntity
{
    public string DisplayName { get; set; }
    public string Feature { get; set; }
    public RulePartOperation Operation { get; set; }
    public string Value { get; set; }
    public Guid RuleId { get; set; }
}