using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using ThockyKeeb.Data;

namespace ThockyKeeb
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            // enable CORS
            services.AddCors(c =>
            {
                c.AddPolicy("AllowOrigin", options => options.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
            });

            // keep json serializer as default
            // services.AddControllersWithViews().AddNewtonsoftJson()

            services.AddControllers();
            //ConfigureSwagger(services);
            services.AddSwaggerGen();

            if (Environment.GetEnvironmentVariable("CONN_STRING") == null)
                Environment.SetEnvironmentVariable("CONN_STRING", "Data Source=db;Initial Catalog=thockykeeb;User Id=root;password=;port=3306");
            // DATABASE 
            services.AddDbContext<Data.ThockyKeebContext>(options => options.UseMySQL(Environment.GetEnvironmentVariable("CONN_STRING")));
            // UseMySQL(Configuration.GetConnectionString("ThockyKeebDB")));
        }

        private static void ConfigureSwagger(IServiceCollection services)
        {
            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new OpenApiInfo { Title = "ThockyKeebAPI", Version = "v1" });
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env, ThockyKeebContext context)
        {
            // enable CORS
            app.UseCors(options => options.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());

            while(true)
            {
                try
                {
                    if (context.Database.EnsureCreated())
                    {
                        context.Database.ExecuteSqlRaw("INSERT INTO `switch` (`id`, `name`, `inStock`, `pricerPerSwitch`) VALUES" +
                            "(1, 'Cherry MX Brown RGB', 9999, 0.49)," +
                            "(2, 'Gateron Black Ink', 3310, 0.75)," +
                            "(3, 'Zealios V2', 3441, 0.95)," +
                            "(4, 'Zilent v2', 1110, 1.2); ");
                    }

                    break;
                }
                catch (Exception e)
                {
                    Console.WriteLine("The DataBase is not ready yet.");
                    Thread.Sleep(6000);
                }
            }

            app.UseDeveloperExceptionPage();

            // app.UseHttpsRedirection();

            // ---------------- SWAGGER -------------

            app.UseSwagger();
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("/swagger/v1/swagger.json", "ThockyKeeb API V1");
                c.RoutePrefix = string.Empty;
            });

            // --------------------------------------

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
