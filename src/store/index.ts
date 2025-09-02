import create from 'zustand';
import { persist } from 'zustand/middleware';

const useStore = create(persist((set, get) => ({
  // Editor State
  editorState: {
    selectedElement: null,
    isDirty: false,
  },
  setEditorState: (editorState) => set({ editorState }),

  // Diagram Content
  diagramContent: '',
  setDiagramContent: (content) => set({ diagramContent: content }),

  // Validation Results
  validationResults: [],
  setValidationResults: (results) => set({ validationResults: results }),

  // Error Messages
  errorMessages: [],
  setErrorMessages: (messages) => set({ errorMessages: messages }),

  // User Preferences
  userPreferences: {
    theme: 'light',
    language: 'en',
  },
  setUserPreferences: (preferences) => set({ userPreferences: preferences }),
}), {
  name: 'editor-store',
  getStorage: () => sessionStorage, // Use sessionStorage for persistence
}));

export default useStore;