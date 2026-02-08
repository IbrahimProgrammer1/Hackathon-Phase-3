# Data Model: AI-Powered Task Assistant

## Entities

### ChatMessage
Represents a single message in the conversation.
- `role`: "user" | "assistant" | "system" | "tool"
- `content`: string
- `tool_call_id`: Optional[string] (for tool responses)

### AIIntent
Represents the parsed intent from the LLM.
- `tool_name`: string
- `arguments`: JSON object
- `confidence`: float (optional)

### ToolCall
Represents a request from the AI to execute a backend function.
- `id`: string
- `type`: "function"
- `function`: object { name, arguments }

## State Transitions
- **User Message** -> **AI Reasoning** -> **Tool Call (Optional)** -> **Tool Execution** -> **AI Response**
- **Destructive Action** -> **Ask Confirmation** -> **User Confirmation** -> **Execution**
