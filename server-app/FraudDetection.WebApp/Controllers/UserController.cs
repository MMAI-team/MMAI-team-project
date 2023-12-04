using FraudDetection.BLL.Abstractions;
using FraudDetection.DAL.Entities;
using FraudDetection.WebApp.Models.TransactionModels;
using FraudDetection.WebApp.Models.UserModels;
using Mapster;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FraudDetection.WebApp.Controllers;

[Route("api/[controller]")]
[ApiController]
public class UserController : ControllerBase
{
    private readonly IEntityManager<User> _userManager;
    private readonly IEntityManager<Transaction> _transactionManager;

    public UserController(IEntityManager<User> userManager, IEntityManager<Transaction> transactionManager)
    {
        _userManager = userManager;
        _transactionManager = transactionManager;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var userFraudIds = await _transactionManager.GetAll()
            .Where(x => x.is_fraud)
            .Select(x => x.cc_num)
            .Distinct()
            .Take(5)
            .ToArrayAsync();

        var users = await _userManager.GetAll()
            .Where(x => userFraudIds.Contains(x.cc_num))
            .Include(x => x.Transactions
                .OrderByDescending(y => y.is_fraud)
                .Take(30)
                .OrderBy(y => y.trans_date_trans_time))
            .ToListAsync();

        var res = users.Adapt<List<UserViewModel>>();

        res.ForEach(x => x.Name = x.Transactions.FirstOrDefault()?.merchant ?? "Unknown");

        return Ok(res);
    }
}