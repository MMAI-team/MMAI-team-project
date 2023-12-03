using CsvHelper.Configuration;
using FraudDetection.DAL.Entities;
using System.Globalization;

namespace FraudDetection.BLL.Abstractions;

public sealed class TransactionMap : ClassMap<Transaction>
{
    public TransactionMap()
    {
        AutoMap(CultureInfo.InvariantCulture);

        Map(m => m.Id).Ignore();
        Map(m => m.UserId).Ignore();
        Map(m => m.CreatedAt).Ignore();

        Map(m => m.FraudScoring).Ignore();
        Map(m => m.VerifiedAt).Ignore();
    }
}