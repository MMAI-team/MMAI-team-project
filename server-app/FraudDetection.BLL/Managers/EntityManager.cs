using FraudDetection.BLL.Abstractions;
using FraudDetection.DAL;
using FraudDetection.DAL.Entities;
using Microsoft.EntityFrameworkCore;

namespace FraudDetection.BLL.Managers;

public class EntityManager<Entity> : IEntityManager<Entity> where Entity : BaseEntity
{
    protected DataContext _dataContext { get; init; }

    public EntityManager(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    public virtual IQueryable<Entity> GetAll()
    {
        return _dataContext.Set<Entity>().AsNoTracking();
    }

    public virtual async Task<Entity?> GetByIdAsync(Guid Id)
    {
        return await _dataContext.Set<Entity>()
            .AsNoTracking()
            .FirstOrDefaultAsync((Entity x) => x.Id == Id);
    }

    public virtual async Task<Entity> CreateAsync(Entity model)
    {
        await _dataContext.Set<Entity>().AddAsync(model);
        await _dataContext.SaveChangesAsync();
        return model;
    }

    public virtual async Task CreateRangeAsync(IEnumerable<Entity> models)
    {
        await _dataContext.Set<Entity>().AddRangeAsync(models);
        await _dataContext.SaveChangesAsync();
    }

    public virtual async Task<Entity> UpdateAsync(Entity model)
    {
        _dataContext.Set<Entity>().Update(model);
        await _dataContext.SaveChangesAsync();
        return model;
    }

    public virtual async Task<bool> DeleteAsync(Guid id)
    {
        Entity val = await _dataContext.Set<Entity>().FirstOrDefaultAsync((Entity c) => c.Id == id)
            ?? throw new ArgumentNullException("The entity with such id does not exist.");

        _dataContext.Entry(val).State = EntityState.Deleted;
        await _dataContext.SaveChangesAsync();
        return true;
    }

    public virtual async Task<bool> DeleteAllDataAsync()
    {
        _dataContext.Set<Entity>().RemoveRange(_dataContext.Set<Entity>());
        await _dataContext.SaveChangesAsync();
        return true;
    }
}