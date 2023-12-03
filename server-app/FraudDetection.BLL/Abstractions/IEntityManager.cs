using FraudDetection.DAL.Entities;

namespace FraudDetection.BLL.Abstractions;

public interface IEntityManager<Entity> where Entity : BaseEntity
{
    IQueryable<Entity> GetAll();

    Task<Entity> GetByIdAsync(Guid Id);

    Task<Entity> CreateAsync(Entity model);

    Task CreateRangeAsync(IEnumerable<Entity> models);

    Task<Entity> UpdateAsync(Entity model);

    Task<bool> DeleteAsync(Guid id);

    Task<bool> DeleteAllDataAsync();
}