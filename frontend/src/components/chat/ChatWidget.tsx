/**
 * ChatWidget - Floating Assistant Component
 *
 * A professional AI assistant widget that appears at the bottom-right
 * of the screen. Click to open a compact chat interface.
 */

'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ChatProvider, useChatContext } from '@/contexts/ChatContext';

// Floating button styles
const floatingButtonStyles: React.CSSProperties = {
  position: 'fixed',
  bottom: '24px',
  right: '24px',
  width: '64px',
  height: '64px',
  borderRadius: '50%',
  background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
  boxShadow: '0 4px 20px rgba(59, 130, 246, 0.4)',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  border: 'none',
  zIndex: 9999,
  transition: 'transform 0.3s ease, box-shadow 0.3s ease',
};

// Chat popup styles
const chatPopupStyles: React.CSSProperties = {
  position: 'fixed',
  bottom: '100px',
  right: '24px',
  width: '380px',
  height: '520px',
  maxWidth: 'calc(100vw - 48px)',
  maxHeight: 'calc(100vh - 120px)',
  backgroundColor: '#ffffff',
  borderRadius: '16px',
  boxShadow: '0 8px 40px rgba(0, 0, 0, 0.15)',
  display: 'flex',
  flexDirection: 'column',
  overflow: 'hidden',
  zIndex: 9998,
  animation: 'slideUp 0.3s ease',
};

// Message bubble styles
const userMessageStyles: React.CSSProperties = {
  backgroundColor: '#3b82f6',
  color: '#ffffff',
  padding: '10px 14px',
  borderRadius: '16px',
  borderBottomRightRadius: '4px',
  maxWidth: '80%',
  alignSelf: 'flex-end',
  marginBottom: '8px',
};

const assistantMessageStyles: React.CSSProperties = {
  backgroundColor: '#f3f4f6',
  color: '#1f2937',
  padding: '10px 14px',
  borderRadius: '16px',
  borderBottomLeftRadius: '4px',
  maxWidth: '80%',
  alignSelf: 'flex-start',
  marginBottom: '8px',
};

// Input area styles
const inputAreaStyles: React.CSSProperties = {
  padding: '12px',
  borderTop: '1px solid #e5e7eb',
  display: 'flex',
  gap: '8px',
  backgroundColor: '#ffffff',
};

const inputStyles: React.CSSProperties = {
  flex: 1,
  padding: '10px 14px',
  borderRadius: '24px',
  border: '1px solid #e5e7eb',
  outline: 'none',
  fontSize: '14px',
  fontFamily: 'inherit',
  resize: 'none' as const,
  maxHeight: '80px',
  overflow: 'auto',
};

const sendButtonStyles: React.CSSProperties = {
  width: '40px',
  height: '40px',
  borderRadius: '50%',
  backgroundColor: '#3b82f6',
  color: '#ffffff',
  border: 'none',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: 'background-color 0.2s ease',
  flexShrink: 0,
};

// Chat messages container
function ChatMessages() {
  const { messages, isLoading } = useChatContext();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div style={{ flex: 1, overflow: 'auto', padding: '16px' }}>
      {messages.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '32px 16px', color: '#6b7280' }}>
          <div style={{ fontSize: '40px', marginBottom: '12px' }}>🤖</div>
          <p style={{ fontSize: '15px', fontWeight: 500, color: '#374151', marginBottom: '4px' }}>
            Hi! I'm your AI Task Assistant
          </p>
          <p style={{ fontSize: '13px' }}>
            I can help you create, list, update, and delete tasks. Just ask me!
          </p>
        </div>
      ) : (
        messages.map((msg, index) => (
          <div
            key={index}
            style={msg.role === 'user' ? userMessageStyles : assistantMessageStyles}
          >
            <div style={{ fontSize: '14px', lineHeight: '1.5', whiteSpace: 'pre-wrap' }}>
              {msg.content}
            </div>
          </div>
        ))
      )}
      {isLoading && (
        <div style={assistantMessageStyles}>
          <div style={{ display: 'flex', gap: '4px' }}>
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: '#9ca3af',
              animation: 'bounce 1s infinite'
            }} />
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: '#9ca3af',
              animation: 'bounce 1s infinite 0.15s'
            }} />
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: '#9ca3af',
              animation: 'bounce 1s infinite 0.3s'
            }} />
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}

// Input component
function ChatInput() {
  const [input, setInput] = useState('');
  const { sendMessage, isLoading } = useChatContext();

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      sendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={inputAreaStyles}>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask me to create a task..."
        style={inputStyles}
        disabled={isLoading}
        rows={1}
      />
      <button
        onClick={handleSend}
        disabled={!input.trim() || isLoading}
        style={{
          ...sendButtonStyles,
          backgroundColor: (!input.trim() || isLoading) ? '#9ca3af' : '#3b82f6',
          cursor: (!input.trim() || isLoading) ? 'not-allowed' : 'pointer',
        }}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" />
        </svg>
      </button>
    </div>
  );
}

// Header component
function ChatHeader() {
  const { clearMessages } = useChatContext();

  return (
    <div style={{
      padding: '14px 16px',
      background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
      color: '#ffffff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '50%',
          backgroundColor: 'rgba(255,255,255,0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '18px',
        }}>
          🤖
        </div>
        <div>
          <div style={{ fontSize: '15px', fontWeight: 600 }}>AI Assistant</div>
          <div style={{ fontSize: '12px', opacity: 0.9 }}>Online • Ready to help</div>
        </div>
      </div>
      <button
        onClick={clearMessages}
        style={{
          background: 'none',
          border: 'none',
          color: '#ffffff',
          cursor: 'pointer',
          padding: '4px',
          borderRadius: '4px',
          opacity: 0.8,
        }}
        title="Clear chat"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
        </svg>
      </button>
    </div>
  );
}

// Main chat popup content
function ChatPopupContent() {
  return (
    <>
      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-4px); }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        .chat-fab:hover {
          transform: scale(1.1);
        }
        .chat-fab.open {
          transform: rotate(90deg);
        }
      `}</style>
      <div style={chatPopupStyles}>
        <ChatHeader />
        <ChatMessages />
        <ChatInput />
      </div>
    </>
  );
}

// Main widget component
export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if chat is enabled
  const isChatEnabled = process.env.NEXT_PUBLIC_CHAT_ENABLED === 'true';

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    setIsAuthenticated(!!token);
  }, []);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    }
  }, [isOpen]);

  // Don't show widget if chat is disabled or user is not authenticated
  if (!isChatEnabled || !isAuthenticated) {
    return null;
  }

  return (
    <>
      <ChatProvider>
        {/* Chat Popup */}
        {isVisible && isOpen && (
          <ChatPopupContent />
        )}

        {/* Floating Button */}
        <button
          className={`chat-fab ${isOpen ? 'open' : ''}`}
          onClick={() => setIsOpen(!isOpen)}
          style={{
            ...floatingButtonStyles,
            animation: isOpen ? 'none' : 'pulse 2s infinite',
          }}
          title="Chat with AI Assistant"
        >
          {isOpen ? (
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          ) : (
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
            </svg>
          )}
        </button>
      </ChatProvider>
    </>
  );
}
