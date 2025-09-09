import React, { useState, useEffect, useCallback } from 'react';
import { ChatStateProvider } from './ChatStateContext';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { SpecificationPanel } from './SpecificationPanel';
import { ProjectSelector } from './ProjectSelector';
import { useChatWebSocket } from '../hooks/useChatWebSocket';
import { useSpecificationSync } from '../hooks/useSpecificationSync';
import { ChatMessage, Project, Specification } from '../types';

interface ChatContainerProps {
  initialProject?: Project;
  onSpecificationUpdate?: (spec: Specification) => void;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({
  initialProject,
  onSpecificationUpdate
}) => {
  const [selectedProject, setSelectedProject] = useState<Project | null>(initialProject || null);
  const [isSpecPanelOpen, setIsSpecPanelOpen] = useState(true);

  const {
    messages,
    isConnected,
    sendMessage,
    clearChat,
    isTyping
  } = useChatWebSocket(selectedProject?.id);

  const {
    currentSpecification,
    updateSpecification,
    syncStatus
  } = useSpecificationSync(selectedProject?.id);

  const handleProjectChange = useCallback((project: Project) => {
    setSelectedProject(project);
    clearChat();
  }, [clearChat]);

  const handleMessageSend = useCallback((content: string, attachments?: File[]) => {
    if (!selectedProject) {
      throw new Error('No project selected');
    }
    
    sendMessage({
      content,
      attachments,
      projectId: selectedProject.id,
      timestamp: new Date()
    });
  }, [selectedProject, sendMessage]);

  useEffect(() => {
    if (currentSpecification && onSpecificationUpdate) {
      onSpecificationUpdate(currentSpecification);
    }
  }, [currentSpecification, onSpecificationUpdate]);

  if (!selectedProject) {
    return (
      <div className="chat-container chat-container--no-project">
        <ProjectSelector onProjectSelect={setSelectedProject} />
      </div>
    );
  }

  return (
    <ChatStateProvider
      projectId={selectedProject.id}
      initialMessages={messages}
      specification={currentSpecification}
    >
      <div className="chat-container">
        <header className="chat-header">
          <ProjectSelector
            selectedProject={selectedProject}
            onProjectSelect={handleProjectChange}
          />
          <div className="chat-controls">
            <button
              className="btn btn--secondary"
              onClick={() => setIsSpecPanelOpen(!isSpecPanelOpen)}
            >
              {isSpecPanelOpen ? 'Hide' : 'Show'} Specification
            </button>
            <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
              {isConnected ? '🟢' : '🔴'}
            </div>
          </div>
        </header>

        <div className="chat-body">
          <div className="chat-main">
            <MessageList
              messages={messages}
              isTyping={isTyping}
              projectId={selectedProject.id}
            />
            <MessageInput
              onSendMessage={handleMessageSend}
              disabled={!isConnected}
              placeholder="Describe your requirements..."
            />
          </div>

          {isSpecPanelOpen && (
            <SpecificationPanel
              specification={currentSpecification}
              syncStatus={syncStatus}
              onUpdate={updateSpecification}
              onClose={() => setIsSpecPanelOpen(false)}
            />
          )}
        </div>
      </div>
    </ChatStateProvider>
  );
};