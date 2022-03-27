using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ThockyKeeb.Common.Models;
using ThockyKeeb.Data;

namespace ThockyKeeb.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SwitchesController : ControllerBase
    {
        private readonly ThockyKeebContext _context;

        public SwitchesController(ThockyKeebContext context)
        {
            _context = context;
        }

        // GET: api/Switches
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Switch>>> GetSwitches()
        {
            return await _context.Switches.ToListAsync();
        }

        // GET: api/Switches/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Switch>> GetSwitch(long id)
        {
            var @switch = await _context.Switches.FindAsync(id);

            if (@switch == null)
            {
                return NotFound();
            }

            return @switch;
        }

        // PUT: api/Switches/5
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutSwitch(long id, Switch @switch)
        {
            if (id != @switch.Id)
            {
                return BadRequest();
            }

            _context.Entry(@switch).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!SwitchExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        [HttpPut]
        public async Task<IActionResult> AddInStockValue(long id, int value)
        {
            var @switch = await _context.Switches.FindAsync(id);
            if (@switch == null)
            {
                return NotFound();
            }

            @switch.InStock += value;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!SwitchExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Switches
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPost]
        public async Task<ActionResult<Switch>> PostSwitch(Switch @switch)
        {
            _context.Switches.Add(@switch);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetSwitch", new { id = @switch.Id }, @switch);
        }

        // DELETE: api/Switches/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<Switch>> DeleteSwitch(long id)
        {
            var @switch = await _context.Switches.FindAsync(id);
            if (@switch == null)
            {
                return NotFound();
            }

            _context.Switches.Remove(@switch);
            await _context.SaveChangesAsync();

            return @switch;
        }

        private bool SwitchExists(long id)
        {
            return _context.Switches.Any(e => e.Id == id);
        }
    }
}
