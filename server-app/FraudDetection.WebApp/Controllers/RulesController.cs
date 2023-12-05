using FraudDetection.BLL.Abstractions;
using FraudDetection.DAL.Entities;
using FraudDetection.DAL.Enums;
using FraudDetection.WebApp.Models.TransactionModels;
using Mapster;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FraudDetection.WebApp.Controllers;

[Route("api/[controller]")]
[ApiController]
public class RuleController : ControllerBase
{
    private readonly IEntityManager<Rule> _ruleManager;

    public RuleController(IEntityManager<Rule> ruleManager)
    {
        _ruleManager = ruleManager;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(Guid id)
    {
        var model = await _ruleManager.GetByIdAsync(id);
        return model is null ? NotFound() : Ok(model);
    }

    [HttpGet]
    public async Task<IActionResult> Get(RuleType ruleType)
        => Ok(await _ruleManager.GetAll()
            .Where(x => x.RuleType == ruleType)
            .OrderBy(x => x.Name)
            .ToListAsync());

    [HttpPost]
    public async Task<IActionResult> Create(Rule rule)
        => Ok(await _ruleManager.CreateAsync(rule));

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(Guid id, Rule rule)
    {
        var model = await _ruleManager.GetByIdAsync(id);
        if (model is null)
            return NotFound();

        await _ruleManager.UpdateAsync(rule);

        return Ok(rule);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Delete(Guid id)
        => Ok(await _ruleManager.DeleteAsync(id));
}