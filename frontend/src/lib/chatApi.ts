/**
 * Chat API Client
 *
 * Provides methods to interact with the AI chat endpoint.
 * Handles JWT authentication and conversation history management.
 *
 * T035-T036: Chat API with JWT attachment
 */

import { apiClient } from './api';

export interface ConversationMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_history: ConversationMessage[];
}

export interface ChatResponse {
  message: string;
  requires_confirmation: boolean;
  confirmation_details?: {
    action: string;
    task_id?: number;
    task_title?: string;
  };
  tool_calls?: Array<{
    name: string;
    parameters: Record<string, any>;
  }>;
}

/**
 * Send a message to the AI chat endpoint.
 *
 * T035: POST /api/chat with Authorization header and conversation history
 * T036: JWT automatically attached via apiClient
 *
 * @param message - User's current message
 * @param conversationHistory - Previous messages (last 10)
 * @returns AI response with message and metadata
 */
export async function sendChatMessage(
  message: string,
  conversationHistory: ConversationMessage[] = []
): Promise<ChatResponse> {
  try {
    // Ensure conversation history is limited to last 10 messages
    const trimmedHistory = conversationHistory.slice(-10);

    const response = await apiClient.post<ChatResponse>('/chat', {
      message,
      conversation_history: trimmedHistory,
    });

    return response;
  } catch (error: any) {
    // Handle API errors
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    } else if (error.message) {
      throw new Error(error.message);
    } else {
      throw new Error('Failed to send message. Please try again.');
    }
  }
}

/**
 * Check health status of the AI chat service.
 *
 * @returns Health status information
 */
export async function checkChatHealth(): Promise<{
  status: string;
  provider?: string;
  model?: string;
  tools_available?: number;
}> {
  try {
    const response = await apiClient.get<{
      status: string;
      provider?: string;
      model?: string;
      tools_available?: number;
    }>('/chat/health');

    return response;
  } catch (error) {
    return {
      status: 'unhealthy',
    };
  }
}
