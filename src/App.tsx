import logo from './logo.svg';
import './App.css';

import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ImportPage from './pages/ImportPage';
import ExportPage from './pages/ExportPage';
import OverviewPage from './pages/OverviewPage';
import MiscPage from './pages/MiscPage';

function App() {
  return (
          <BrowserRouter>
                <div style={{ minHeight: '100vh', backgroundColor: '#f0fdf4', color: '#065f46', fontFamily: 'sans-serif' }}>
                  <nav style={{ padding: '1rem', backgroundColor: '#34d399', color: 'white' }}>
                    <Link to="/" style={{ marginRight: '1rem', color: 'white' }}>Home</Link>
                    <Link to="/import" style={{ marginRight: '1rem', color: 'white' }}>Import</Link>
                    <Link to="/export" style={{ marginRight: '1rem', color: 'white' }}>Export</Link>
                    <Link to="/overview" style={{ marginRight: '1rem', color: 'white' }}>Overview</Link>
                    <Link to="/misc" style={{ color: 'white' }}>Settings</Link>
                  </nav>
                  <Routes>
                    <Route path="/" element={<LandingPage />} />
                    <Route path="/import" element={<ImportPage />} />
                    <Route path="/export" element={<ExportPage />} />
                    <Route path="/overview" element={<OverviewPage />} />
                    <Route path="/misc" element={<MiscPage />} />
                  </Routes>
                </div>
              </BrowserRouter>
  );
}

export default App;
