import React, { useState, useRef, useEffect } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import axios from 'axios';
import io from 'socket.io-client';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3001';

// Draggable shape component
const DraggableShape = ({ type, children }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: 'shape',
    item: { type },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <div
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
        padding: '8px',
        margin: '4px',
        border: '1px solid #ccc',
        borderRadius: '4px',
        cursor: 'move',
        backgroundColor: '#f9f9f9'
      }}
    >
      {children}
    </div>
  );
};

// Canvas component
const Canvas = ({ shapes, onShapeAdd, onShapeMove }) => {
  const [, drop] = useDrop(() => ({
    accept: 'shape',
    drop: (item, monitor) => {
      const offset = monitor.getClientOffset();
      const canvasRect = canvasRef.current.getBoundingClientRect();
      const x = offset.x - canvasRect.left;
      const y = offset.y - canvasRect.top;
      
      onShapeAdd({
        id: Date.now(),
        type: item.type,
        x,
        y,
        width: 100,
        height: 60
      });
    },
  }));

  const canvasRef = useRef();

  return (
    <div
      ref={(node) => {
        canvasRef.current = node;
        drop(node);
      }}
      style={{
        width: '800px',
        height: '600px',
        border: '2px dashed #ccc',
        position: 'relative',
        backgroundColor: '#fff'
      }}
    >
      {shapes.map((shape) => (
        <div
          key={shape.id}
          style={{
            position: 'absolute',
            left: shape.x,
            top: shape.y,
            width: shape.width,
            height: shape.height,
            border: '1px solid #333',
            borderRadius: '4px',
            backgroundColor: shape.type === 'rectangle' ? '#e3f2fd' : '#f3e5f5',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer'
          }}
          onClick={() => onShapeMove(shape.id)}
        >
          {shape.type}
        </div>
      ))}
    </div>
  );
};

// Main diagram editor
const DiagramEditor = () => {
  const [shapes, setShapes] = useState([]);
  const [diagramId, setDiagramId] = useState(null);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    // Initialize socket connection
    const newSocket = io(API_BASE);
    setSocket(newSocket);

    // Load existing diagram or create new one
    loadDiagram();

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (socket && diagramId) {
      socket.emit('join-diagram', diagramId);
      
      socket.on('shape-added', (shape) => {
        setShapes(prev => [...prev, shape]);
      });

      socket.on('shapes-updated', (updatedShapes) => {
        setShapes(updatedShapes);
      });
    }
  }, [socket, diagramId]);

  const loadDiagram = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/diagrams/latest`);
      if (response.data) {
        setDiagramId(response.data.id);
        setShapes(response.data.shapes || []);
      } else {
        createNewDiagram();
      }
    } catch (error) {
      console.error('Failed to load diagram:', error);
      createNewDiagram();
    }
  };

  const createNewDiagram = async () => {
    try {
      const response = await axios.post(`${API_BASE}/api/diagrams`, {
        name: 'New Diagram',
        shapes: []
      });
      setDiagramId(response.data.id);
    } catch (error) {
      console.error('Failed to create diagram:', error);
    }
  };

  const handleShapeAdd = async (shape) => {
    try {
      await axios.post(`${API_BASE}/api/diagrams/${diagramId}/shapes`, shape);
      if (socket) {
        socket.emit('shape-added', { diagramId, shape });
      }
    } catch (error) {
      console.error('Failed to add shape:', error);
    }
  };

  const handleShapeMove = async (shapeId) => {
    // Simple implementation - in production, this would handle drag operations
    console.log('Shape clicked:', shapeId);
  };

  const saveDiagram = async () => {
    try {
      await axios.put(`${API_BASE}/api/diagrams/${diagramId}`, { shapes });
      alert('Diagram saved successfully!');
    } catch (error) {
      console.error('Failed to save diagram:', error);
      alert('Failed to save diagram');
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div style={{ display: 'flex', padding: '20px', gap: '20px' }}>
        <div style={{ width: '200px' }}>
          <h3>Shapes</h3>
          <DraggableShape type="rectangle">Rectangle</DraggableShape>
          <DraggableShape type="circle">Circle</DraggableShape>
          <DraggableShape type="triangle">Triangle</DraggableShape>
          
          <div style={{ marginTop: '20px' }}>
            <button onClick={saveDiagram} style={{ width: '100%', padding: '8px' }}>
              Save Diagram
            </button>
          </div>
        </div>
        
        <div>
          <h3>Canvas</h3>
          <Canvas 
            shapes={shapes} 
            onShapeAdd={handleShapeAdd}
            onShapeMove={handleShapeMove}
          />
        </div>
      </div>
    </DndProvider>
  );
};

export default DiagramEditor;