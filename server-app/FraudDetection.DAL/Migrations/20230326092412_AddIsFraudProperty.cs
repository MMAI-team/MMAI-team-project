using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace FraudDetection.DAL.Migrations
{
    /// <inheritdoc />
    public partial class AddIsFraudProperty : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "is_fraud",
                table: "Transactions",
                type: "bit",
                nullable: false,
                defaultValue: false);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "is_fraud",
                table: "Transactions");
        }
    }
}
