namespace TicketInspectorTracker.Api.Models;

public sealed record TicketInspection(
    int Id,
    string ExternalId,
    string Title,
    TicketStatus Status,
    string Assignee,
    DateOnly LastInspectedOn);
