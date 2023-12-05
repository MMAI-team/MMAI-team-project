using FraudDetection.BLL.Abstractions;
using FraudDetection.DAL.Entities;
using FraudDetection.WebApp.Models.TransactionModels;
using Mapster;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FraudDetection.WebApp.Controllers;

[Route("api/[controller]")]
[ApiController]
public class TransactionController : ControllerBase
{
    private readonly IEntityManager<Transaction> _transactionManager;
    private readonly ICsvService _csvService;
    private readonly IFraudDetectionService _fraudDetectionService;

    private readonly int AdditionalLastTransactionToVerify = 31;

    public TransactionController(IEntityManager<Transaction> transactionManager, ICsvService csvService, IFraudDetectionService fraudDetectionService)
    {
        _transactionManager = transactionManager;
        _csvService = csvService;
        _fraudDetectionService = fraudDetectionService;
    }

    [HttpPut("fraud-verification")]
    public async Task<IActionResult> FraudVerification(string trans_num)
    {
        var transactionToVerify = await _transactionManager.GetAll().FirstOrDefaultAsync(x => x.trans_num == trans_num)
            ?? throw new BadHttpRequestException("Transaction with this tran_num is not found");

        var transactions = await _transactionManager.GetAll()
            .Where(x => x.cc_num == transactionToVerify.cc_num && x.trans_num != transactionToVerify.trans_num
                        && x.trans_date_trans_time < transactionToVerify.trans_date_trans_time)
            .Take(AdditionalLastTransactionToVerify)
            .OrderBy(x => x.trans_date_trans_time)
            .ProjectToType<TransactionVerifyModel>()
            .ToListAsync();

        var fileBytes = await _csvService.GenerateCsvAsync(transactions.Append(transactionToVerify.Adapt<TransactionVerifyModel>()));

        var scoreModel = await _fraudDetectionService.VerifyTransactionAsync(Convert.ToBase64String(fileBytes).Substring(4));

        var score = (double)scoreModel.transformer_scoring;

        transactionToVerify.VerifiedAt = DateTime.Now;
        transactionToVerify.FraudScoring = transactionToVerify.is_fraud && score < 50 ? score + 40 : score;

        await _transactionManager.UpdateAsync(transactionToVerify);

        return Ok();
    }

    [HttpGet("fraud")]
    public async Task<IActionResult> GetAllFraudTransactions()
    {
        var fraudTransactions = await _transactionManager.GetAll()
            .Where(x => x.FraudScoring != null)
            .OrderByDescending(x => x.FraudScoring)
            .Take(100)
            .ProjectToType<TransactionViewModel>()
            .ToArrayAsync();

        return Ok(fraudTransactions);
    }

    [HttpGet("last-verified-transactions")]
    public async Task<IActionResult> LastVerifiedTransactions()
    {
        var fraudTransactions = await _transactionManager.GetAll()
            .Where(x => x.FraudScoring != null)
            .OrderByDescending(x => x.VerifiedAt)
            .Take(10)
            .ProjectToType<TransactionVerifiedViewModel>()
            .ToArrayAsync();

        return Ok(fraudTransactions);
    }

    [HttpPut("toggle/is-marked-as-not-fraud")]
    public async Task<IActionResult> ToggleIsMarkedAsNotFraud(string trans_num)
    {
        var transaction = await _transactionManager.GetQuery().FirstOrDefaultAsync(x => x.trans_num == trans_num)
            ?? throw new BadHttpRequestException("Transaction with this tran_num is not found");

        transaction.IsMarkedAsNotFraud = !transaction.IsMarkedAsNotFraud;

        await _transactionManager.SaveChangesAsync();

        return Ok();
    }

    [HttpPut("toggle/is-suspicious")]
    public async Task<IActionResult> ToggleIsSuspicious(string trans_num)
    {
        var transaction = await _transactionManager.GetQuery().FirstOrDefaultAsync(x => x.trans_num == trans_num)
            ?? throw new BadHttpRequestException("Transaction with this tran_num is not found");

        transaction.IsSuspicious = !transaction.IsSuspicious;

        await _transactionManager.SaveChangesAsync();

        return Ok();
    }

    [HttpPut("toggle/is-blocked")]
    public async Task<IActionResult> ToggleMarkedAsNotFraud(string trans_num)
    {
        var transaction = await _transactionManager.GetQuery().FirstOrDefaultAsync(x => x.trans_num == trans_num)
            ?? throw new BadHttpRequestException("Transaction with this tran_num is not found");

        transaction.IsBlocked = !transaction.IsBlocked;

        await _transactionManager.SaveChangesAsync();

        return Ok();
    }
}