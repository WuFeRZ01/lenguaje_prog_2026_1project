# Tool Lending CLI

Sistema CLI para gestionar préstamos de herramientas.

## Arquitectura

```mermaid
flowchart LR
CLI --> Services
Services --> Storage
Storage --> JSON