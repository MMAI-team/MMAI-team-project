namespace FraudDetection.DAL.Entities;

public abstract record BaseEntity
{
    public Guid Id { get; set; }
}