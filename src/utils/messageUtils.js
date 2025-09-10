export const createUserMessage = (message, userName, avatar) => ({
  type: 'user',
  message: message.trim(),
  userName,
  avatar,
  timestamp: new Date()
});

export const createSystemResponse = (message, options = {}) => ({
  type: 'system',
  message,
  status: 'completed',
  systemName: 'Assistant',
  showTypingEffect: false,
  timestamp: new Date(),
  ...options
});

export const createSpecPreview = (spec, options = {}) => ({
  type: 'spec-preview',
  spec,
  title: 'Specification Preview',
  language: 'json',
  collapsible: true,
  timestamp: new Date(),
  ...options
});

export const createInteractiveCustomizer = (spec, customizableFields, onSpecChange, options = {}) => ({
  type: 'interactive',
  spec,
  customizableFields,
  onSpecChange,
  title: 'Customize Specification',
  timestamp: new Date(),
  ...options
});

export const validateMessage = (message) => {
  if (!message || typeof message !== 'object') {
    return { valid: false, error: 'Message must be an object' };
  }
  
  if (!message.type) {
    return { valid: false, error: 'Message type is required' };
  }
  
  const validTypes = ['user', 'system', 'spec-preview', 'interactive'];
  if (!validTypes.includes(message.type)) {
    return { valid: false, error: `Invalid message type: ${message.type}` };
  }
  
  return { valid: true };
};