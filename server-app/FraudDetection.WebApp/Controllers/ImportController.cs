using FraudDetection.BLL.Abstractions;
using FraudDetection.BLL.Configuration.CSVHelper;
using FraudDetection.DAL.Entities;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FraudDetection.WebApp.Controllers;

[Route("api/[controller]")]
[ApiController]
public class ImportController : ControllerBase
{
    private readonly ICsvService _csvService;
    private readonly IEntityManager<User> _userManager;
    private readonly IEntityManager<Transaction> _transactionManager;

    public ImportController(ICsvService csvService, IEntityManager<User> userManager, IEntityManager<Transaction> transactionManager)
    {
        _csvService = csvService;
        _userManager = userManager;
        _transactionManager = transactionManager;
    }

    [HttpPost("user-transaction-csv")]
    public async Task<IActionResult> ImportTransactions([FromForm] IFormFileCollection file)
    {
        var transactions = _csvService.ReadCsv<Transaction>(file[0].OpenReadStream(), typeof(TransactionMap)).ToList();

        transactions.ForEach(x => x.CreatedAt = DateTime.Now);

        var transactionGroupedByUser = transactions.GroupBy(x => x.cc_num);

        var users = transactionGroupedByUser.Select(group => new User()
        {
            cc_num = group.Key,
            Transactions = group.ToList(),
        });

        foreach (var user in users)
            await _userManager.CreateAsync(user);

        return Ok();
    }

    [HttpDelete("clear-verifications")]
    public async Task<IActionResult> ClearVerifications()
    {
        var verifiedTransaction = await _transactionManager.GetQuery()
            .Where(x => x.VerifiedAt != null)
            .ToListAsync();

        verifiedTransaction.ForEach(x =>
        {
            x.VerifiedAt = null;
            x.FraudScoring = null;
        });

        await _transactionManager.SaveChangesAsync();

        return Ok();
    }

    //[HttpDelete("remove-users-transactions-data")]
    //public async Task<IActionResult> RemoveUsersTransactionsData()
    //{
    //    await _userManager.DeleteAllDataAsync();
    //    await _ruleManager.DeleteAllDataAsync();

    //    return Ok();
    //}
}