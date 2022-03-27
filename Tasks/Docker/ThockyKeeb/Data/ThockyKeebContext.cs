using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;
using ThockyKeeb.Common.Models;

#nullable disable

namespace ThockyKeeb.Data
{
    public partial class ThockyKeebContext : DbContext
    {
        public ThockyKeebContext()
        {
        }

        public ThockyKeebContext(DbContextOptions<ThockyKeebContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Switch> Switches { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Switch>(entity =>
            {
                entity.ToTable("switch");

                entity.Property(e => e.Id).HasColumnName("id");

                entity.Property(e => e.InStock).HasColumnName("inStock");

                entity.Property(e => e.Name)
                    .IsRequired()
                    .HasMaxLength(255)
                    .HasColumnName("name");

                entity.Property(e => e.PricerPerSwitch).HasColumnName("pricerPerSwitch");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
