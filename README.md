# TicketInspectorTracker

ASP.NET Core Web API solution for tracking ticket inspection work.

## Solution structure

- `TicketInspectorTracker.sln` - solution file
- `src/TicketInspectorTracker.Api` - API project
- `tests/TicketInspectorTracker.Api.Tests` - xUnit test project

## Endpoints

- `GET /api/tickets` - list tracked tickets
- `GET /api/tickets/summary` - return ticket counts by status

## Run locally

```bash
dotnet run --project /home/runner/work/TicketInspectorTracker/TicketInspectorTracker/src/TicketInspectorTracker.Api/TicketInspectorTracker.Api.csproj
```

## Build and test

```bash
dotnet build /home/runner/work/TicketInspectorTracker/TicketInspectorTracker/TicketInspectorTracker.sln
dotnet test /home/runner/work/TicketInspectorTracker/TicketInspectorTracker/TicketInspectorTracker.sln
```