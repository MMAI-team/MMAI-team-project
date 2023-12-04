namespace FraudDetection.BLL.Models;

public class FraudScoringModel
{
    public decimal FNN { get; set; }
    public decimal transformer_scoring { get; set; }
    public decimal xgoost_regressor { get; set; }
    public decimal random_forest_regressor { get; set; }
}