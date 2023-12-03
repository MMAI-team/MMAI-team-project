using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace FraudDetection.DAL.Extensions;

internal static class ServiceCollectionExtensions
{
    public static async Task<IServiceCollection> ConfigurePersistenceDependencies(this IServiceCollection services, IConfiguration configuration)
    {
        await services.ConfigureDatabase(configuration);

        return services;
    }

    public static async Task<IServiceCollection> ConfigureDatabase(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<DataContext>(opts =>
          opts.UseSqlServer(configuration["ConnectionStrings:FraudDetectionDatabaseConnection"]));

        await services.MigrateDatabaseAsync();

        return services;
    }

    public static async Task MigrateDatabaseAsync(this IServiceCollection services)
    {
        var serviceProvider = services.BuildServiceProvider();
        var context = serviceProvider.GetRequiredService<DataContext>();

        await context.Database.MigrateAsync();
    }
}