using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace FraudDetection.DAL.Extensions;

public static class ProgramExtensions
{
    public static async Task<IServiceCollection> AddDALDependenciesAsync(this IServiceCollection services, IConfiguration configuration)
    {
        await services.ConfigurePersistenceDependencies(configuration);

        return services;
    }
}