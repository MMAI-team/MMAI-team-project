//using Microsoft.EntityFrameworkCore;
//using Microsoft.EntityFrameworkCore.Metadata.Builders;

//namespace BusinessGame.Infrastructure.Persistence.Configurations;

//internal class BrandConfiguration : IEntityTypeConfiguration<Brand>, IEntityConfiguration
//{
//    public void Configure(EntityTypeBuilder<Brand> builder)
//    {
//        builder.HasKey(x => x.Id);

//        builder.HasIndex(x => new { x.ProductId, x.TagId }).IsUnique();

//        builder.HasOne<Model>(s => s.Model)
//        .WithMany(g => g.Products)
//        .HasForeignKey(s => s.ModelId);

//        builder.HasIndex(x => x.DealerProductCode)
//            .IsUnique();

//        builder.HasOne<Tag>(x => x.Tag)
//        .WithMany(x => x.ProductTags)
//        .HasForeignKey(x => x.TagId)
//        .OnDelete(DeleteBehavior.Cascade);

//        builder.HasOne<Product>(x => x.Product)
//        .WithMany(x => x.ProductTags)
//        .HasForeignKey(x => x.ProductId)
//        .OnDelete(DeleteBehavior.Cascade);
//    }
//}