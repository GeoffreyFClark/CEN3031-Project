import { useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
// Import your components

import ResourceList from './ResourceList';
import AddResource from './AddResource';
import MyResources from './MyResources';
import Navigation from './Navigation';
import Register from './Register';
import Login from './Login';

function App() {

  return (
    <div>
      <nav>
        <Navigation />
      </nav>
      <Routes>
        <Route path="/" element={<ResourceList />} />
        <Route path="/my-resources" element={<MyResources />} />
        <Route path="/add-resource" element={<AddResource />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}

export default App
