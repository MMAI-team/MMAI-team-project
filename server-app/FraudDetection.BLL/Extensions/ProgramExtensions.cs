using FraudDetection.BLL.Abstractions;
using FraudDetection.BLL.Managers;
using Microsoft.Extensions.DependencyInjection;

namespace FraudDetection.BLL.Extensions;

public static class ProgramExtensions
{
    public static IServiceCollection AddBLLDependencies(this IServiceCollection services)
    {
        services.AddServices();

        return services;
    }

    private static void AddServices(this IServiceCollection services)
    {
        services.AddScoped(typeof(IEntityManager<>), typeof(EntityManager<>));
        services.AddScoped<ICsvService, CsvService>();
    }
}