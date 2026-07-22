using Microsoft.AspNetCore.Mvc;
using TicketInspectorTracker.Api.Models;

namespace TicketInspectorTracker.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public sealed class TicketsController : ControllerBase
{
    private static readonly TicketInspection[] Tickets =
    [
        new(1, "INC-1001", "Vendor API latency spike", TicketStatus.Investigating, "Avery", new DateOnly(2026, 7, 20)),
        new(2, "BUG-2048", "Duplicate tracker event detected", TicketStatus.Monitoring, "Jordan", new DateOnly(2026, 7, 21)),
        new(3, "TASK-3301", "Backfill historical inspection data", TicketStatus.New, "Morgan", new DateOnly(2026, 7, 22)),
        new(4, "INC-1000", "Webhook delivery retry tuning", TicketStatus.Resolved, "Riley", new DateOnly(2026, 7, 18))
    ];

    [HttpGet]
    public IReadOnlyList<TicketInspection> GetTickets() => Tickets;

    [HttpGet("summary")]
    public TicketSummary GetSummary() => new(
        Tickets.Length,
        Tickets.Count(ticket => ticket.Status == TicketStatus.New),
        Tickets.Count(ticket => ticket.Status == TicketStatus.Investigating),
        Tickets.Count(ticket => ticket.Status == TicketStatus.Monitoring),
        Tickets.Count(ticket => ticket.Status == TicketStatus.Resolved));
}
