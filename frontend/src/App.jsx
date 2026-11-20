import { useState } from 'react'
import { useEffect } from 'react'
import './App.css'
import ProblemList from './components/ProblemList'

function App() {
  const[problems, setProblems]= useState([])
  const [loading, setLoading]= useState(true)
  const [error, setError]= useState(false)
  useEffect(()=>{
      fetch("/get-problems")
      .then(res=>res.json())
      .then(data=> {
        setProblems(data);
        setLoading(false);
      })
      

      .catch((err)=>{
        setError(true);
        setLoading(false);
      
      });
     

  },[])

  let content;
  if (loading){
    content= <p>Loading...</p>;
  }else if(error){
    content= <p>something went wrong</p>;
  }
  else{
    content= <ProblemList problems={problems} />
  }

  return (
    <>
      <section id="center">
        {content}
      </section>

      <section id="spacer"></section>
    </>
  )
}

export default App
