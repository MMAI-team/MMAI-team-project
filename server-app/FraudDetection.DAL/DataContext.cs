using FraudDetection.DAL.Configurations.Abstractions;
using FraudDetection.DAL.Entities;
using Microsoft.EntityFrameworkCore;
using System.Reflection;

namespace FraudDetection.DAL;

public partial class DataContext : DbContext
{
    public virtual DbSet<Transaction> Transactions { get; set; }
    public virtual DbSet<Rule> Rules { get; set; }
    public virtual DbSet<RulePart> RuleParts { get; set; }
    public virtual DbSet<User> Users { get; set; }

    public DataContext(DbContextOptions<DataContext> options) : base(options) { }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        //To check migrations errors
        optionsBuilder.EnableSensitiveDataLogging();
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        ConfigureEntities(modelBuilder);
    }

    private static void ConfigureEntities(ModelBuilder modelBuilder)
    {
        IEnumerable<Type> mappingClasses = Assembly.GetExecutingAssembly().GetTypes()
            .Where(x => !x.IsAbstract && !x.IsInterface && typeof(IEntityConfiguration).IsAssignableFrom(x));

        foreach (Type mappingClass in mappingClasses)
        {
            dynamic mappingInstance = Activator.CreateInstance(mappingClass);
            modelBuilder.ApplyConfiguration(mappingInstance);
        }
    }
}