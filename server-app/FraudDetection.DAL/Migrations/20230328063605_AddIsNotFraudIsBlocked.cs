using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace FraudDetection.DAL.Migrations
{
    /// <inheritdoc />
    public partial class AddIsNotFraudIsBlocked : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "IsBlocked",
                table: "Transactions",
                type: "bit",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<bool>(
                name: "IsMarkedAsNotFraud",
                table: "Transactions",
                type: "bit",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<bool>(
                name: "IsSuspicious",
                table: "Transactions",
                type: "bit",
                nullable: false,
                defaultValue: false);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "IsBlocked",
                table: "Transactions");

            migrationBuilder.DropColumn(
                name: "IsMarkedAsNotFraud",
                table: "Transactions");

            migrationBuilder.DropColumn(
                name: "IsSuspicious",
                table: "Transactions");
        }
    }
}
