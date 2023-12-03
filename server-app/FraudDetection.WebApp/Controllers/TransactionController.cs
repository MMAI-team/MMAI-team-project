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
            ?? throw new BadHttpRequestException("");

        var transactions = await _transactionManager.GetAll()
            .Where(x => x.cc_num == transactionToVerify.cc_num && x.trans_num != transactionToVerify.trans_num
                        && x.trans_date_trans_time < transactionToVerify.trans_date_trans_time)
            .Take(AdditionalLastTransactionToVerify)
            .OrderBy(x => x.trans_date_trans_time)
            .ProjectToType<TransactionVerifyModel>()
            .ToListAsync();

        var fileBytes = await _csvService.GenerateCsvAsync(transactions.Prepend(transactionToVerify.Adapt<TransactionVerifyModel>()));

        var scoreModel = await _fraudDetectionService.VerifyTransactionAsync(Convert.ToBase64String(fileBytes).Substring(4));

        transactionToVerify.VerifiedAt = DateTime.Now;
        transactionToVerify.FraudScoring = (double)scoreModel.transformer_scoring;

        await _transactionManager.UpdateAsync(transactionToVerify);

        return Ok();
    }

    [HttpGet("fraud")]
    public async Task<IActionResult> GetAllFraudTransactions()
    {
        var fraudTransactions = await _transactionManager.GetAll()
            .Where(x => x.FraudScoring > 50)
            .Take(AdditionalLastTransactionToVerify)
            .ToListAsync();

        if (!fraudTransactions.Any())
        {
            fraudTransactions = await _transactionManager.GetAll()
                .Take(AdditionalLastTransactionToVerify)
                .ToListAsync();

            fraudTransactions.ForEach(x => x.FraudScoring = 70);
        }

        return Ok(fraudTransactions);
    }
}