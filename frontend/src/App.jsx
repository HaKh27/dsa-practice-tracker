import { useState } from 'react'
import { useEffect } from 'react'
import './App.css'
import ProblemList from './components/ProblemList'

function App() {
  const[problems, setProblems]= useState([])
  useEffect(()=>{
      fetch("/get-problems")
      .then(res=>res.json())
      .then(data=>setProblems(data))

  },[])


  return (
    <>
      <section id="center">
        <ProblemList problems={problems} />
        
      </section>

      

      
      <section id="spacer"></section>
    </>
  )
}

export default App
