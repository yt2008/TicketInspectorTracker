using TicketInspectorTracker.Api.Controllers;
using TicketInspectorTracker.Api.Models;

namespace TicketInspectorTracker.Api.Tests;

public class TicketsControllerTests
{
    [Fact]
    public void GetTickets_ReturnsSeededTickets()
    {
        var controller = new TicketsController();

        var tickets = controller.GetTickets();

        Assert.Equal(4, tickets.Count);
        Assert.Contains(tickets, ticket => ticket.ExternalId == "INC-1001" && ticket.Status == TicketStatus.Investigating);
    }

    [Fact]
    public void GetSummary_ReturnsCountsByStatus()
    {
        var controller = new TicketsController();

        var summary = controller.GetSummary();

        Assert.Equal(4, summary.Total);
        Assert.Equal(1, summary.New);
        Assert.Equal(1, summary.Investigating);
        Assert.Equal(1, summary.Monitoring);
        Assert.Equal(1, summary.Resolved);
    }
}
