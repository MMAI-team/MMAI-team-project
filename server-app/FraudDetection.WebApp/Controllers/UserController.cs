using FraudDetection.BLL.Abstractions;
using FraudDetection.DAL.Entities;
using FraudDetection.WebApp.Models.TransactionModels;
using FraudDetection.WebApp.Models.UserModels;
using Mapster;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Transactions;

namespace FraudDetection.WebApp.Controllers;

[Route("api/[controller]")]
[ApiController]
public class UserController : ControllerBase
{
    private readonly IEntityManager<User> _userManager;

    public UserController(IEntityManager<User> transactionManager)
        => _userManager = transactionManager;

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var users = await _userManager.GetAll()
            .Include(x => x.Transactions
                .Take(30)
                .OrderBy(x => x.trans_date_trans_time))
            .Take(10)
            .ToListAsync();

        users.Adapt<List<UserViewModel>>().ForEach(x => x.Name = x.Transactions.FirstOrDefault()?.merchant);

        return Ok(users);
    }
}