﻿// <auto-generated />
using System;
using FraudDetection.DAL;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

#nullable disable

namespace FraudDetection.DAL.Migrations
{
    [DbContext(typeof(DataContext))]
    [Migration("20230325143011_Init")]
    partial class Init
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "7.0.4")
                .HasAnnotation("Relational:MaxIdentifierLength", 128);

            SqlServerModelBuilderExtensions.UseIdentityColumns(modelBuilder);

            modelBuilder.Entity("FraudDetection.DAL.Entities.Transaction", b =>
                {
                    b.Property<Guid>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("uniqueidentifier");

                    b.Property<DateTimeOffset>("CreatedAt")
                        .HasColumnType("datetimeoffset");

                    b.Property<double?>("FraudScoring")
                        .HasColumnType("float");

                    b.Property<Guid>("UserId")
                        .HasColumnType("uniqueidentifier");

                    b.Property<DateTimeOffset?>("VerifiedAt")
                        .HasColumnType("datetimeoffset");

                    b.Property<string>("amt")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("category")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("cc_num")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("city")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("city_pop")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("dob")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("first")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("gender")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("job")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("last")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("lat")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("longs")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("merch_lat")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("merch_long")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("merchant")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<int>("number")
                        .HasColumnType("int");

                    b.Property<string>("state")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("street")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<DateTimeOffset>("trans_date_trans_time")
                        .HasColumnType("datetimeoffset");

                    b.Property<string>("trans_num")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("unix_time")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("zip")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.HasKey("Id");

                    b.HasIndex("UserId");

                    b.ToTable("Transactions");
                });

            modelBuilder.Entity("FraudDetection.DAL.Entities.User", b =>
                {
                    b.Property<Guid>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("uniqueidentifier");

                    b.Property<string>("cc_num")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.HasKey("Id");

                    b.ToTable("Users");
                });

            modelBuilder.Entity("FraudDetection.DAL.Entities.Transaction", b =>
                {
                    b.HasOne("FraudDetection.DAL.Entities.User", null)
                        .WithMany("Transactions")
                        .HasForeignKey("UserId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();
                });

            modelBuilder.Entity("FraudDetection.DAL.Entities.User", b =>
                {
                    b.Navigation("Transactions");
                });
#pragma warning restore 612, 618
        }
    }
}
