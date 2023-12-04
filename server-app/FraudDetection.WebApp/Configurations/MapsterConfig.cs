using FraudDetection.DAL.Entities;
using FraudDetection.WebApp.Models.TransactionModels;
using Mapster;

namespace BusinessGame.WebApi.Configurations;

public static class MapsterConfig
{
    public static void RegisterMapsterConfig()
    {
        TypeAdapterConfig<Transaction, TransactionViewModel>.NewConfig()
            .Map(dest => dest.merchant,
                src => src.merchant.Replace("fraud_", "").Replace("_", " "))
            .Map(dest => dest.category,
                src => src.category.Replace("_"," "));
    }
}