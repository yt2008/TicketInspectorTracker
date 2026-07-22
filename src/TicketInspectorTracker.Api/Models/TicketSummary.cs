namespace TicketInspectorTracker.Api.Models;

public sealed record TicketSummary(
    int Total,
    int New,
    int Investigating,
    int Monitoring,
    int Resolved);
