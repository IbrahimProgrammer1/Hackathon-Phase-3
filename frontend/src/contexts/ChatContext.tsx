/**
 * Chat Context
 *
 * Provides global state management for the AI chat interface.
 * Manages conversation history, loading states, and confirmation flows.
 *
 * T031-T034: Chat context with message and confirmation state management
 */

'use client';

import React, { createContext, useContext, useState, useCallback } from 'react';
import { sendChatMessage, ConversationMessage, ChatResponse } from '@/lib/chatApi';
import { emitTaskEvent } from '@/hooks/useTaskRefresh';

// T031: Define ChatContext state interface
interface ChatContextState {
  messages: ConversationMessage[];
  isLoading: boolean;
  error: string | null;
  pendingConfirmation: {
    action: string;
    taskId?: number;
    taskTitle?: string;
  } | null;
}

interface ChatContextValue extends ChatContextState {
  sendMessage: (message: string) => Promise<void>;
  setPendingConfirmation: (confirmation: ChatContextState['pendingConfirmation']) => void;
  clearPendingConfirmation: () => void;
  clearError: () => void;
  clearMessages: () => void;
}

const ChatContext = createContext<ChatContextValue | undefined>(undefined);

/**
 * ChatProvider component
 *
 * Wraps the application to provide chat functionality.
 */
export function ChatProvider({ children }: { children: React.ReactNode }) {
  // T031: Initialize state
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingConfirmation, setPendingConfirmationState] = useState<
    ChatContextState['pendingConfirmation']
  >(null);

  /**
   * T032: Send message to AI and update conversation
   *
   * Calls backend /api/chat with JWT and conversation history.
   * Automatically manages message state and error handling.
   */
  const sendMessage = useCallback(async (message: string) => {
    if (!message.trim()) {
      setError('Message cannot be empty');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      // T033: Add user message to conversation
      const userMessage: ConversationMessage = {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => {
        const updated = [...prev, userMessage];
        // T033: Trim to last 10 messages
        return updated.slice(-10);
      });

      // Call chat API with conversation history
      const response: ChatResponse = await sendChatMessage(
        message,
        messages // Send current messages as history
      );

      // T033: Add assistant response to conversation
      const assistantMessage: ConversationMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => {
        const updated = [...prev, assistantMessage];
        // T033: Trim to last 10 messages
        return updated.slice(-10);
      });

      // T035: Detect task creation and trigger refresh
      // Check if the AI successfully called a task creation tool
      if (response.tool_calls && response.tool_calls.length > 0) {
        const taskCreated = response.tool_calls.some(
          (tc: any) => tc.name === 'create_task' && response.message.toLowerCase().includes('created')
        );
        if (taskCreated) {
          // Emit task creation event to refresh task lists
          emitTaskEvent('task_created');
        }
      }

      // T034: Handle confirmation requirements
      if (response.requires_confirmation && response.confirmation_details) {
        setPendingConfirmationState({
          action: response.confirmation_details.action,
          taskId: response.confirmation_details.task_id,
          taskTitle: response.confirmation_details.task_title,
        });
      } else {
        // Clear any pending confirmation if not required
        setPendingConfirmationState(null);
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to send message. Please try again.';
      setError(errorMessage);

      // Add error message to conversation for user visibility
      const errorAssistantMessage: ConversationMessage = {
        role: 'assistant',
        content: errorMessage,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => {
        const updated = [...prev, errorAssistantMessage];
        return updated.slice(-10);
      });
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  /**
   * T034: Set pending confirmation state
   */
  const setPendingConfirmation = useCallback(
    (confirmation: ChatContextState['pendingConfirmation']) => {
      setPendingConfirmationState(confirmation);
    },
    []
  );

  /**
   * T034: Clear pending confirmation state
   */
  const clearPendingConfirmation = useCallback(() => {
    setPendingConfirmationState(null);
  }, []);

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  /**
   * Clear all messages (useful for starting fresh conversation)
   */
  const clearMessages = useCallback(() => {
    setMessages([]);
    setPendingConfirmationState(null);
    setError(null);
  }, []);

  const value: ChatContextValue = {
    messages,
    isLoading,
    error,
    pendingConfirmation,
    sendMessage,
    setPendingConfirmation,
    clearPendingConfirmation,
    clearError,
    clearMessages,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
}

/**
 * Hook to use chat context
 *
 * @throws Error if used outside ChatProvider
 */
export function useChatContext() {
  const context = useContext(ChatContext);

  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }

  return context;
}
