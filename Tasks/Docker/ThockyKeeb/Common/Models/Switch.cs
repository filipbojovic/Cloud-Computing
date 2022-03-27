using System;
using System.Collections.Generic;

#nullable disable

namespace ThockyKeeb.Common.Models
{
    public partial class Switch
    {
        public long Id { get; set; }
        public string Name { get; set; }
        public int InStock { get; set; }
        public double PricerPerSwitch { get; set; }
    }
}
