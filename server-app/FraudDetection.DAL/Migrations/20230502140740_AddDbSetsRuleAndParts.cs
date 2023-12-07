using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace FraudDetection.DAL.Migrations
{
    /// <inheritdoc />
    public partial class AddDbSetsRuleAndParts : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Rules",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Description = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    RuleType = table.Column<int>(type: "int", nullable: false),
                    FraudScore = table.Column<decimal>(type: "decimal(18,2)", nullable: true),
                    FraudScoreOperation = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Rules", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "RuleParts",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    DisplayName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Feature = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Operation = table.Column<int>(type: "int", nullable: false),
                    Value = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    RuleId = table.Column<Guid>(type: "uniqueidentifier", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_RuleParts", x => x.Id);
                    table.ForeignKey(
                        name: "FK_RuleParts_Rules_RuleId",
                        column: x => x.RuleId,
                        principalTable: "Rules",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_RuleParts_RuleId",
                table: "RuleParts",
                column: "RuleId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "RuleParts");

            migrationBuilder.DropTable(
                name: "Rules");
        }
    }
}
