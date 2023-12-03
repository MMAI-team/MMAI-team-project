using FraudDetection.WebApp.Models.TransactionModels;

namespace FraudDetection.WebApp.Models.UserModels;

public record UserViewModel
{
    public string Name { get; set; }
    public string cc_num { get; set; }
    public ICollection<TransactionViewModel> Transactions { get; set; } = new List<TransactionViewModel>();
}