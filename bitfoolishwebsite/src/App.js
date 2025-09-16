import logo from './logo.svg';
import './App.css';
 
import MyButton from './components/button';
import Registry from './components/registry';
import Counter from './components/tester';
import {HashRouter as Router, Routes, Route} from 'react-router-dom';

import { Home } from './pages/home';
import { Layout } from './Layout';

import AllProjects from './components/AllProjects';

function App() {
  return (
  
    <>
    <Router>
      <Routes>
        <Route element={<Layout/>}>
          <Route path="/" element={<Home/>}/>
          <Route path="/projects" element={<AllProjects/>}/>
        </Route>
      </Routes>
    </Router>
    </>
  );
}



export default App;
