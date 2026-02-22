"""
AI Agent Core for Task Management Assistant

This module implements the main AI agent that processes user messages,
calls the LLM with tool definitions, executes tools via ToolExecutor,
and returns conversational responses.

Constitutional Requirements:
- Stateless processing (no conversation state stored)
- JWT propagated to all tool executions
- System prompt always takes precedence
- Confirmation required for deletions
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import cohere
from .tools import ToolRegistry
from .tool_executor import ToolExecutor


class AIAgent:
    """
    Main AI agent for conversational task management.

    Handles:
    - LLM initialization (Cohere or OpenAI based on env)
    - System prompt loading
    - Message processing with conversation history
    - Tool calling and execution
    - Response formatting
    """

    def __init__(self):
        """Initialize the AI agent with LLM client and system prompt."""
        # T019: Initialize LLM client based on provider
        self.provider = os.getenv("AI_PROVIDER", "cohere").lower()
        self.model = os.getenv("AI_MODEL", "command-r-plus")

        if self.provider == "cohere":
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY environment variable not set")
            self.client = cohere.Client(api_key)
        elif self.provider == "openai":
            # OpenAI support can be added here
            raise NotImplementedError("OpenAI provider not yet implemented")
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

        # T020: Load system prompt from file
        self.system_prompt = self._load_system_prompt()

        # Get tool schemas for LLM
        self.tools = ToolRegistry.get_tool_schemas_for_llm(provider=self.provider)

    def _load_system_prompt(self) -> str:
        """
        Load system prompt from prompts/system.txt.

        Returns:
            System prompt text

        Raises:
            FileNotFoundError: If system prompt file doesn't exist
        """
        prompt_path = os.getenv(
            "AI_SYSTEM_PROMPT_PATH",
            "prompts/system.txt"
        )

        # Handle both absolute and relative paths
        if not os.path.isabs(prompt_path):
            # Relative to backend directory
            backend_dir = Path(__file__).parent.parent.parent
            prompt_path = backend_dir / prompt_path

        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"System prompt not found at: {prompt_path}")

        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    def process(
        self,
        message: str,
        conversation_history: List[Dict[str, Any]],
        jwt: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response.

        T021: Main processing method that accepts message, history, jwt, user_id

        Args:
            message: User's current message
            conversation_history: List of previous messages (last 10)
            jwt: JWT token for authentication
            user_id: User ID from JWT claims

        Returns:
            Dict containing:
            - message: AI's response text
            - tool_calls: List of tool calls made (optional)
            - requires_confirmation: Whether confirmation is needed (optional)
        """
        try:
            # Initialize tool executor with JWT
            tool_executor = ToolExecutor(jwt=jwt, user_id=user_id)

            # T022: Implement LLM function calling
            response = self._call_llm_with_tools(
                message=message,
                conversation_history=conversation_history
            )

            # T023: Execute tool calls and get final response
            final_response = self._handle_tool_calls(
                response=response,
                tool_executor=tool_executor,
                message=message,
                conversation_history=conversation_history
            )

            tool_executor.close()
            return final_response

        except Exception as e:
            error_message = str(e)
            # Provide more specific error messages based on exception type
            if "timeout" in error_message.lower():
                user_message = "The request took too long. Please try again."
            elif "connection" in error_message.lower():
                user_message = "I'm having trouble connecting to the server. Please check your connection."
            elif "api" in error_message.lower() or "cohere" in error_message.lower():
                user_message = "There's an issue with the AI service. Please try again in a moment."
            else:
                user_message = "I'm having trouble processing your request right now. Please try again in a moment."

            return {
                "message": user_message,
                "error": error_message
            }

    def _call_llm_with_tools(
        self,
        message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> Any:
        """
        Call LLM with message, history, and tool definitions.

        T022: Send message + history + tools to LLM, receive tool calls

        Args:
            message: Current user message
            conversation_history: Previous conversation messages

        Returns:
            LLM response object
        """
        if self.provider == "cohere":
            return self._call_cohere(message, conversation_history)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

    def _call_cohere(
        self,
        message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> Any:
        """
        Call Cohere API with tool support.

        Args:
            message: Current user message
            conversation_history: Previous messages

        Returns:
            Cohere response object

        Raises:
            Exception: If Cohere API call fails
        """
        # Convert conversation history to Cohere format
        chat_history = []
        for msg in conversation_history:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "user":
                chat_history.append({
                    "role": "USER",
                    "message": content
                })
            elif role == "assistant":
                chat_history.append({
                    "role": "CHATBOT",
                    "message": content
                })

        # Call Cohere with tools
        try:
            response = self.client.chat(
                model=self.model,
                message=message,
                chat_history=chat_history,
                preamble=self.system_prompt,
                tools=self.tools,
                temperature=0.3  # Lower temperature for more consistent behavior
            )
            return response
        except Exception as e:
            # Re-raise with more context
            error_msg = str(e)
            if "model" in error_msg.lower() and "not found" in error_msg.lower():
                raise Exception(f"AI model '{self.model}' not available. Please contact support.")
            raise Exception(f"Cohere API error: {error_msg}")

    def _handle_tool_calls(
        self,
        response: Any,
        tool_executor: ToolExecutor,
        message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Handle tool calls from LLM response.

        T023: Execute tool calls, return results to LLM for formatting

        Args:
            response: LLM response object
            tool_executor: ToolExecutor instance
            message: Original user message
            conversation_history: Conversation history

        Returns:
            Final response dict with message and metadata
        """
        if self.provider == "cohere":
            return self._handle_cohere_tool_calls(
                response, tool_executor, message, conversation_history
            )
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")

    def _handle_cohere_tool_calls(
        self,
        response: Any,
        tool_executor: ToolExecutor,
        message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Handle Cohere-specific tool calls.

        Args:
            response: Cohere response object
            tool_executor: ToolExecutor instance
            message: Original user message
            conversation_history: Conversation history

        Returns:
            Final response dict
        """
        # Check if Cohere wants to use tools
        if not hasattr(response, 'tool_calls') or not response.tool_calls:
            # No tool calls - return direct response
            return {
                "message": response.text,
                "tool_calls": []
            }

        # Execute tool calls
        tool_results = []
        for tool_call in response.tool_calls:
            tool_name = tool_call.name
            parameters = tool_call.parameters

            # Execute the tool
            result = tool_executor.execute_tool(tool_name, parameters)

            # Format result for Cohere - must include id field
            # Cohere expects: {"call": {"id": "string", "name": "string"}, "outputs": [{"id": "string", ...}]}
            tool_call_id = tool_call.id if hasattr(tool_call, 'id') else f"call_{tool_name}"

            if result["success"]:
                # Remove the 'id' field from result to avoid conflict with Cohere's required string id
                result_data = {k: v for k, v in result["result"].items() if k != 'id'}
                # Create output with string id first, then add result fields (excluding id)
                tool_result_output = {"id": f"output_{tool_call_id}"}
                tool_result_output.update(result_data)
                tool_results.append({
                    "call": {"id": tool_call_id, "name": tool_name},
                    "outputs": [tool_result_output]
                })
            else:
                # Tool execution failed - return error to LLM
                tool_results.append({
                    "call": {"id": tool_call_id, "name": tool_name},
                    "outputs": [{
                        "id": f"error_{tool_call_id}",
                        "error": result["error"],
                        "error_type": result["error_type"]
                    }]
                })

        # Send tool results back to Cohere for final response
        # Use force_single_step=True and DON'T include tools in second call
        # to prevent the model from calling tools again
        final_response = self.client.chat(
            model=self.model,
            message=message,
            chat_history=self._build_chat_history_with_tools(
                conversation_history,
                message,
                response,
                tool_results
            ),
            preamble=self.system_prompt,
            # Don't include tools in second call - we've already executed them
            tool_results=tool_results,
            temperature=0.3,
            force_single_step=True  # Enable multi-hop tool calling
        )

        # Check if delete_task was called (requires confirmation tracking)
        requires_confirmation = False
        confirmation_details = None

        for tool_call in response.tool_calls:
            if tool_call.name == "delete_task":
                # Check if this was a confirmation request or actual deletion
                # This is a simplified check - full implementation would track state
                if "Are you sure" in final_response.text:
                    requires_confirmation = True
                    confirmation_details = {
                        "action": "delete",
                        "task_id": tool_call.parameters.get("task_id")
                    }

        return {
            "message": final_response.text,
            "tool_calls": [
                {
                    "name": tc.name,
                    "parameters": tc.parameters
                }
                for tc in response.tool_calls
            ],
            "requires_confirmation": requires_confirmation,
            "confirmation_details": confirmation_details
        }

    def _build_chat_history_with_tools(
        self,
        conversation_history: List[Dict[str, Any]],
        current_message: str,
        tool_response: Any,
        tool_results: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Build chat history including tool calls for Cohere.

        Args:
            conversation_history: Previous messages
            current_message: Current user message
            tool_response: Response with tool calls
            tool_results: Results from tool execution

        Returns:
            Chat history in Cohere format
        """
        chat_history = []

        # Add previous conversation
        for msg in conversation_history:
            role = msg.get("role")
            content = msg.get("content", "")

            if role == "user":
                chat_history.append({"role": "USER", "message": content})
            elif role == "assistant":
                chat_history.append({"role": "CHATBOT", "message": content})

        # Add current user message
        chat_history.append({"role": "USER", "message": current_message})

        # Add tool response
        if hasattr(tool_response, 'text') and tool_response.text:
            chat_history.append({"role": "CHATBOT", "message": tool_response.text})

        return chat_history
